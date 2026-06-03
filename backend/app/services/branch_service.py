"""
分支版本管理服务层 — 提供一键式操作方法
类似 Git 的语义化操作：commit, merge, branch

使用方法：
    from app.services.branch_service import commit, create_branch_clone, execute_merge

    # 一键提交
    await commit(db, branch_id=1, project_id=1, message="feat: 添加新功能", created_by=1)

    # 从源分支创建分支并克隆页面
    await create_branch_clone(db, project_id=1, name="feature-nav",
                              source_branch_id=1, created_by=1)

    # 执行合并（增量更新）
    await execute_merge(db, mr_id=1, merged_by=1)
"""
import time
from typing import Optional, List, Dict, Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import (
    create_branch,
    get_branch,
    create_branch_version,
    get_merge_request,
    create_branch_version_by_name,
)
from app.crud.components import get_page_components, batch_add_components_to_page
from app.models import (
    Branch,
    BranchVersion,
    BranchStatus,
    MergeRequest,
    MergeRequestStatus,
    ProjectPage,
    Component,
    PageComponentRelation,
)


async def commit(
    db: AsyncSession,
    branch_id: int,
    project_id: int,
    message: str,
    created_by: int,
    version_name: Optional[str] = None,
    page_changes: Optional[List[Dict[str, Any]]] = None,
) -> BranchVersion:
    """一键提交版本（类似 git commit）

    传入必要参数即可完成版本创建，无需手动处理父版本查找、变更记录插入等逻辑。

    Args:
        db: 数据库会话
        branch_id: 分支 ID
        project_id: 项目 ID
        message: 提交信息
        created_by: 创建人 ID
        version_name: 版本名称（可选，如 "v1.0"）
        page_changes: 页面变更列表，格式：
            [{
                "page_id": 123,
                "change_type": "create"|"update"|"delete",
                "changed_components": [1, 2, 3],  # 可选
                "file_uuids_changed": {"added": [], "removed": []},  # 可选
                "summary": "添加了设计稿页面",  # 可选
            }]

    Returns:
        创建的 BranchVersion 对象
    """
    return await create_branch_version(
        db=db,
        branch_id=branch_id,
        project_id=project_id,
        message=message,
        created_by=created_by,
        version_name=version_name,
        page_changes=page_changes,
    )


async def commit_by_name(
    db: AsyncSession,
    project_id: int,
    branch_name: str,
    message: str,
    created_by: int,
    version_name: Optional[str] = None,
    page_changes: Optional[List[Dict[str, Any]]] = None,
) -> BranchVersion:
    """按分支名一键提交（类似 git commit，自动解析分支名）

    无需先查询分支 ID，传入分支名即可完成提交。

    Args:
        db: 数据库会话
        project_id: 项目 ID
        branch_name: 分支名称（如 "main", "feature-nav"）
        message: 提交信息
        created_by: 创建人 ID
        version_name: 版本名称（可选，如 "v1.0"）
        page_changes: 页面变更列表

    Returns:
        创建的 BranchVersion 对象

    Raises:
        ValueError: 当指定名称的分支不存在时抛出
    """
    return await create_branch_version_by_name(
        db=db,
        project_id=project_id,
        branch_name=branch_name,
        message=message,
        created_by=created_by,
        version_name=version_name,
        page_changes=page_changes,
    )


async def create_branch_clone(
    db: AsyncSession,
    project_id: int,
    name: str,
    source_branch_id: int,
    created_by: int,
    description: Optional[str] = None,
) -> Branch:
    """从源分支创建新分支并克隆所有页面（类似 git branch + 自动初始化）

    传入参数即可：创建分支 → 克隆源分支的所有页面和组件，一气呵成。

    Args:
        db: 数据库会话
        project_id: 项目 ID
        name: 新分支名称
        source_branch_id: 源分支 ID（从此分支复制页面和组件）
        created_by: 创建人 ID
        description: 分支描述（可选）

    Returns:
        创建的新 Branch 对象（已包含所有克隆的页面和组件）
    """
    from app.crud.branches import clone_branch_pages

    # 1. 创建分支（仅元数据）
    branch = await create_branch(
        db=db,
        project_id=project_id,
        name=name,
        created_by=created_by,
        description=description,
    )

    # 2. 克隆源分支的所有页面和组件
    await clone_branch_pages(
        db=db,
        source_branch_id=source_branch_id,
        target_branch_id=branch.id,
        created_by=created_by,
    )

    return branch


async def execute_merge(
    db: AsyncSession,
    mr_id: int,
    merged_by: int,
) -> Dict[str, Any]:
    """执行分支合并（类似 git merge，增量更新）

    完整的合并流程：
    1. 验证合并请求已批准
    2. 对比源分支和目标分支的页面差异
    3. 增量更新：仅将源分支新增/修改的页面同步到目标分支
    4. 在目标分支上创建合并版本
    5. 更新源分支状态为已合并
    6. 更新合并请求状态

    所谓「增量更新」是指：
    - 源分支中新增的页面 → 克隆到目标分支
    - 源分支中已有的页面 → 更新目标分支对应页面的组件和数据
    - 目标分支独有的页面 → 保持不变（不会删除）

    Args:
        db: 数据库会话
        mr_id: 合并请求 ID
        merged_by: 执行合并的用户 ID

    Returns:
        合并结果统计字典：
        {
            "merge_request_id": int,
            "source_branch": str,
            "target_branch": str,
            "pages_added": int,
            "pages_updated": int,
            "total_pages_changed": int,
            "merge_version_id": int,
        }

    Raises:
        ValueError: 合并请求不存在、未批准、或分支不存在时抛出
    """
    # ===== 1. 获取并验证合并请求 =====
    mr = await get_merge_request(db, mr_id)
    if not mr:
        raise ValueError("合并请求不存在")
    if mr.status != MergeRequestStatus.APPROVED:
        raise ValueError("只有已批准的合并请求才能执行合并")

    source_branch = await get_branch(db, mr.source_branch_id)
    target_branch = await get_branch(db, mr.target_branch_id)
    if not source_branch or not target_branch:
        raise ValueError("源分支或目标分支不存在")

    # ===== 2. 获取源分支和目标分支的页面（ORM 对象） =====
    source_pages_result = await db.execute(
        select(ProjectPage)
        .where(ProjectPage.branch_id == source_branch.id)
        .where(ProjectPage.is_hidden == False)
    )
    source_pages: List[ProjectPage] = list(source_pages_result.scalars().all())

    target_pages_result = await db.execute(
        select(ProjectPage)
        .where(ProjectPage.branch_id == target_branch.id)
        .where(ProjectPage.is_hidden == False)
    )
    target_pages: List[ProjectPage] = list(target_pages_result.scalars().all())

    # 构建目标分支页面索引 {page_type: page}
    target_page_map: Dict[str, ProjectPage] = {}
    for p in target_pages:
        if p.page_type not in target_page_map:
            target_page_map[p.page_type] = p

    # ===== 3. 增量合并页面 =====
    pages_added = 0
    pages_updated = 0
    page_changes: List[Dict[str, Any]] = []

    for source_page in source_pages:
        # 跳过文件夹
        if source_page.is_folder:
            continue

        match_page = target_page_map.get(source_page.page_type)

        if not match_page:
            # --- 3a. 新增页面：克隆到目标分支 ---
            new_page = ProjectPage(
                project_id=source_page.project_id,
                branch_id=target_branch.id,
                title=source_page.title,
                page_type=source_page.page_type,
                icon=source_page.icon,
                control_power=source_page.control_power,
                edit_power=source_page.edit_power,
                view_power=source_page.view_power,
                order_index=source_page.order_index,
                is_hidden=source_page.is_hidden,
                parent_id=source_page.parent_id,
                is_folder=source_page.is_folder,
                created_by=merged_by,
                updated_by=merged_by,
            )
            db.add(new_page)
            await db.flush()

            # 复制组件
            source_comps = await get_page_components(db, source_page.id)
            comp_data_list = [
                {
                    "component_type": comp["component_type"],
                    "component_key": comp["component_key"],
                    "title": comp.get("title"),
                    "description": comp.get("description"),
                    "data": comp.get("data", {}),
                    "schema": comp.get("schema"),
                    "visible": comp.get("visible", True),
                    "order_index": comp.get("order_index", 0),
                }
                for comp in source_comps
            ]

            if comp_data_list:
                await batch_add_components_to_page(
                    db=db,
                    page_id=new_page.id,
                    components=comp_data_list,
                    created_by=merged_by,
                )

            pages_added += 1
            page_changes.append({
                "page_id": new_page.id,
                "change_type": "create",
                "summary": f"从分支 '{source_branch.name}' 合并新增",
            })
        else:
            # --- 3b. 更新页面：替换目标页面的组件和数据 ---
            source_comps = await get_page_components(db, source_page.id)
            comp_data_list = [
                {
                    "component_type": comp["component_type"],
                    "component_key": comp["component_key"],
                    "title": comp.get("title"),
                    "description": comp.get("description"),
                    "data": comp.get("data", {}),
                    "schema": comp.get("schema"),
                    "visible": comp.get("visible", True),
                    "order_index": comp.get("order_index", 0),
                }
                for comp in source_comps
            ]

            # 删除目标页面旧的组件关系
            await db.execute(
                PageComponentRelation.__table__.delete()
                .where(PageComponentRelation.page_id == match_page.id)
            )

            # 添加源页面的组件
            if comp_data_list:
                await batch_add_components_to_page(
                    db=db,
                    page_id=match_page.id,
                    components=comp_data_list,
                    created_by=merged_by,
                )

            # 更新目标页面的元数据
            match_page.title = source_page.title
            match_page.icon = source_page.icon
            match_page.updated_by = merged_by

            pages_updated += 1
            page_changes.append({
                "page_id": match_page.id,
                "change_type": "update",
                "summary": f"从分支 '{source_branch.name}' 合并更新",
            })

    # ===== 4. 在目标分支上创建合并版本 =====
    merge_version = await create_branch_version(
        db=db,
        branch_id=target_branch.id,
        project_id=mr.project_id,
        message=f"合并分支 '{source_branch.name}' 到 '{target_branch.name}'",
        created_by=merged_by,
        version_name=None,
        page_changes=page_changes,
    )

    # ===== 5. 更新源分支和 MR 状态 =====
    # create_branch_version 内部 commit 会过期所有对象，需要重新获取
    source_branch = await db.get(Branch, source_branch.id)
    source_branch.status = BranchStatus.MERGED

    mr = await db.get(MergeRequest, mr.id)
    mr.status = MergeRequestStatus.MERGED
    mr.merged_at = int(time.time())

    await db.commit()

    return {
        "merge_request_id": mr.id,
        "source_branch": source_branch.name,
        "target_branch": target_branch.name,
        "pages_added": pages_added,
        "pages_updated": pages_updated,
        "total_pages_changed": len(page_changes),
        "merge_version_id": merge_version.id,
    }
