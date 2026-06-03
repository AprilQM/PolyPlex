"""
分支版本 CRUD 操作 - 类似 Git 的分支版本管理

核心功能:
- create_version: 创建当前分支的新版本（类似 git commit）
- compare_versions: 对比两个版本的差异（类似 git diff）
- get_version_history: 查看版本历史（类似 git log）
- get_version_details: 获取版本详情
"""
from typing import Optional, List, Dict, Any
from sqlalchemy import select, desc, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.versions import BranchVersion, BranchVersionChange
from app.models.projects import ProjectPage
from app.models.components import Component
from app.models.files import FilePackageRelation, File
from app.models.branches import Branch


# ========== BranchVersion CRUD ==========

async def get_branch_version(
    db: AsyncSession,
    version_id: int,
) -> Optional[BranchVersion]:
    """根据 ID 获取分支版本"""
    return await db.get(BranchVersion, version_id)


async def create_branch_version(
    db: AsyncSession,
    branch_id: int,
    project_id: int,
    message: str,
    created_by: int,
    version_name: Optional[str] = None,
    page_changes: Optional[List[Dict[str, Any]]] = None,
) -> BranchVersion:
    """
    创建分支的新版本（类似 git commit）

    Args:
        db: 数据库会话
        branch_id: 分支 ID
        project_id: 项目 ID
        message: 提交信息
        created_by: 创建人 ID
        version_name: 版本名称（可选，如 "v1.0"）
        page_changes: 页面变更列表

    Returns:
        创建的 BranchVersion 对象
    """
    # 获取最新的版本作为父版本
    latest_result = await db.execute(
        select(BranchVersion)
        .where(BranchVersion.branch_id == branch_id)
        .order_by(desc(BranchVersion.created_at))
        .limit(1)
    )
    latest_version = latest_result.scalar_one_or_none()

    # 创建版本
    version = BranchVersion(
        branch_id=branch_id,
        project_id=project_id,
        parent_version_id=latest_version.id if latest_version else None,
        version_name=version_name,
        message=message,
        created_by=created_by,
    )

    db.add(version)
    await db.flush()  # 获取 version.id

    # 记录页面变更
    if page_changes:
        for change_data in page_changes:
            change = BranchVersionChange(
                version_id=version.id,
                page_id=change_data["page_id"],
                change_type=change_data["change_type"],
                changed_components=change_data.get("changed_components"),
                file_uuids_changed=change_data.get("file_uuids_changed"),
                summary=change_data.get("summary"),
            )
            db.add(change)

    # 更新版本摘要
    await _update_version_summary(db, version.id)

    await db.commit()
    await db.refresh(version)

    return version


async def create_branch_version_by_name(
    db: AsyncSession,
    project_id: int,
    branch_name: str,
    message: str,
    created_by: int,
    version_name: Optional[str] = None,
    page_changes: Optional[List[Dict[str, Any]]] = None,
) -> BranchVersion:
    """
    根据分支名创建版本（自动解析分支名 -> 分支 ID）

    这是一个便捷方法，直接传入分支名即可创建版本，
    无需先手动查询分支 ID 再调用 create_branch_version。

    Args:
        db: 数据库会话
        project_id: 项目 ID
        branch_name: 分支名称（如 "main", "feature-new-design"）
        message: 提交信息
        created_by: 创建人 ID
        version_name: 版本名称（可选，如 "v1.0"）
        page_changes: 页面变更列表

    Returns:
        创建的 BranchVersion 对象

    Raises:
        ValueError: 当指定名称的分支不存在时抛出
    """
    # 查询分支
    result = await db.execute(
        select(Branch)
        .where(Branch.project_id == project_id)
        .where(Branch.name == branch_name)
    )
    branch = result.scalar_one_or_none()

    if not branch:
        raise ValueError(f"分支 '{branch_name}' 不存在")

    # 委托给 create_branch_version
    return await create_branch_version(
        db=db,
        branch_id=branch.id,
        project_id=project_id,
        message=message,
        created_by=created_by,
        version_name=version_name,
        page_changes=page_changes,
    )


async def compare_branch_versions(
    db: AsyncSession,
    version1_id: int,
    version2_id: int,
) -> Dict[str, List[Dict[str, Any]]]:
    """
    对比两个分支版本的差异（类似 git diff）
    """
    v1 = await db.get(BranchVersion, version1_id)
    v2 = await db.get(BranchVersion, version2_id)

    if not v1 or not v2:
        raise ValueError("版本不存在")

    if v1.branch_id != v2.branch_id:
        raise ValueError("只能对比同一分支的版本")

    # 获取两个版本的变更记录
    changes1_result = await db.execute(
        select(BranchVersionChange)
        .where(BranchVersionChange.version_id == version1_id)
    )
    changes1 = {c.page_id: c for c in changes1_result.scalars().all()}

    changes2_result = await db.execute(
        select(BranchVersionChange)
        .where(BranchVersionChange.version_id == version2_id)
    )
    changes2 = {c.page_id: c for c in changes2_result.scalars().all()}

    result = {
        "added_pages": [],
        "modified_pages": [],
        "deleted_pages": [],
        "file_changes": [],
    }

    all_page_ids = set(changes1.keys()) | set(changes2.keys())

    for page_id in all_page_ids:
        c1 = changes1.get(page_id)
        c2 = changes2.get(page_id)

        page_info = {"page_id": page_id}

        if c1 is None and c2 is not None:
            page_info["change"] = c2
            result["added_pages"].append(page_info)
        elif c1 is not None and c2 is None:
            page_info["change"] = c1
            result["deleted_pages"].append(page_info)
        elif c1 != c2:
            page_info["old_change"] = c1
            page_info["new_change"] = c2
            result["modified_pages"].append(page_info)

        if c2 and c2.file_uuids_changed:
            result["file_changes"].append({
                "page_id": page_id,
                "changes": c2.file_uuids_changed,
            })

    return result


async def get_branch_version_history(
    db: AsyncSession,
    branch_id: int,
    limit: int = 50,
) -> List[Dict[str, Any]]:
    """获取分支的版本历史（类似 git log）"""
    result = await db.execute(
        select(BranchVersion)
        .where(BranchVersion.branch_id == branch_id)
        .order_by(desc(BranchVersion.created_at))
        .limit(limit)
    )

    versions = result.scalars().all()

    return [
        {
            "version_id": v.id,
            "version_name": v.version_name,
            "message": v.message,
            "summary": v.summary,
            "parent_version_id": v.parent_version_id,
            "created_by": v.created_by,
            "created_at": v.created_at,
        }
        for v in versions
    ]


async def get_version_details(
    db: AsyncSession,
    version_id: int,
) -> Optional[Dict[str, Any]]:
    """获取版本详细信息"""
    version = await db.get(BranchVersion, version_id)
    if not version:
        return None

    changes_result = await db.execute(
        select(BranchVersionChange)
        .where(BranchVersionChange.version_id == version_id)
    )
    changes = changes_result.scalars().all()

    return {
        "version_id": version.id,
        "branch_id": version.branch_id,
        "project_id": version.project_id,
        "version_name": version.version_name,
        "message": version.message,
        "summary": version.summary,
        "parent_version_id": version.parent_version_id,
        "created_by": version.created_by,
        "created_at": version.created_at,
        "changes": [
            {
                "page_id": c.page_id,
                "change_type": c.change_type,
                "changed_components": c.changed_components,
                "file_uuids_changed": c.file_uuids_changed,
                "summary": c.summary,
            }
            for c in changes
        ],
        "stats": {
            "pages_changed": len(changes),
            "files_changed": sum(
                len(c.file_uuids_changed.get("added", []) + c.file_uuids_changed.get("removed", []))
                for c in changes if c.file_uuids_changed
            ),
        },
    }


async def get_version_changes(
    db: AsyncSession,
    version_id: int,
) -> List[BranchVersionChange]:
    """获取版本的所有变更记录"""
    result = await db.execute(
        select(BranchVersionChange)
        .where(BranchVersionChange.version_id == version_id)
    )
    return list(result.scalars().all())


async def get_current_version(
    db: AsyncSession,
    branch_id: int,
) -> Optional[BranchVersion]:
    """获取分支的当前最新版本"""
    result = await db.execute(
        select(BranchVersion)
        .where(BranchVersion.branch_id == branch_id)
        .order_by(desc(BranchVersion.created_at))
        .limit(1)
    )
    return result.scalar_one_or_none()


async def _update_version_summary(db: AsyncSession, version_id: int):
    """更新版本的变更摘要"""
    result = await db.execute(
        select(BranchVersionChange)
        .where(BranchVersionChange.version_id == version_id)
    )
    changes = result.scalars().all()

    summary = {
        "pages_added": sum(1 for c in changes if c.change_type == "create"),
        "pages_modified": sum(1 for c in changes if c.change_type == "update"),
        "pages_deleted": sum(1 for c in changes if c.change_type == "delete"),
        "files_changed": sum(
            len(c.file_uuids_changed.get("added", []) + c.file_uuids_changed.get("removed", []))
            for c in changes if c.file_uuids_changed
        ),
    }

    version = await db.get(BranchVersion, version_id)
    if version:
        version.summary = summary
        await db.commit()


# ========== 文件变化检测 ==========

async def detect_file_changes(
    db: AsyncSession,
    page_id: int,
    old_component_ids: List[str],
    new_component_ids: List[str],
) -> Dict[str, List[str]]:
    """
    检测页面中文件列表组件的文件 UUID 变化
    """
    old_uuids = set()
    if old_component_ids:
        old_result = await db.execute(
            select(FilePackageRelation.file_id)
            .join(File)
            .where(
                FilePackageRelation.package_id.in_(old_component_ids),
                File.id == FilePackageRelation.file_id,
            )
        )
        old_uuids = {str(row[0]) for row in old_result.all()}

    new_uuids = set()
    if new_component_ids:
        new_result = await db.execute(
            select(FilePackageRelation.file_id)
            .join(File)
            .where(
                FilePackageRelation.package_id.in_(new_component_ids),
                File.id == FilePackageRelation.file_id,
            )
        )
        new_uuids = {str(row[0]) for row in new_result.all()}

    return {
        "added": list(new_uuids - old_uuids),
        "removed": list(old_uuids - new_uuids),
    }
