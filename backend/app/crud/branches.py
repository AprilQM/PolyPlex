"""
项目分支 CRUD 操作
"""
from sqlalchemy import select, desc, func, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.branches import Branch, BranchStatus
from app.models.projects import ProjectPage
from app.models.components import PageComponentRelation, Component
from app.crud.components import batch_add_components_to_page
from app.project_templates import get_page_type_info
from typing import Optional, List


# ========== Branch CRUD ==========

async def get_branch(db: AsyncSession, branch_id: int) -> Optional[Branch]:
    """根据 ID 获取分支"""
    result = await db.execute(select(Branch).where(Branch.id == branch_id))
    return result.scalar_one_or_none()


async def get_branch_by_name(
    db: AsyncSession,
    project_id: int,
    name: str
) -> Optional[Branch]:
    """根据项目名称获取分支"""
    result = await db.execute(
        select(Branch)
        .where(Branch.project_id == project_id)
        .where(Branch.name == name)
    )
    return result.scalar_one_or_none()


async def create_branch(
    db: AsyncSession,
    project_id: int,
    name: str,
    created_by: int,
    description: Optional[str] = None,
    base_version: int = 1,
) -> Branch:
    """创建新分支"""
    branch = Branch(
        project_id=project_id,
        name=name,
        description=description,
        created_by=created_by,
        base_version=base_version,
    )
    db.add(branch)
    await db.commit()
    await db.refresh(branch)
    return branch


async def update_branch(
    db: AsyncSession,
    branch_id: int,
    name: Optional[str] = None,
    description: Optional[str] = None,
    status: Optional[BranchStatus] = None,
    base_version: Optional[int] = None,
) -> Optional[Branch]:
    """更新分支信息"""
    branch = await get_branch(db, branch_id)
    if not branch:
        return None

    if name is not None:
        branch.name = name
    if description is not None:
        branch.description = description
    if status is not None:
        branch.status = status
    if base_version is not None:
        branch.base_version = base_version

    await db.commit()
    await db.refresh(branch)
    return branch


async def delete_branch(db: AsyncSession, branch_id: int) -> bool:
    """删除分支"""
    branch = await get_branch(db, branch_id)
    if not branch:
        return False

    await db.delete(branch)
    await db.commit()
    return True


async def update_branch_status(
    db: AsyncSession,
    branch_id: int,
    status: BranchStatus,
) -> Optional[Branch]:
    """更新分支状态"""
    return await update_branch(db, branch_id, status=status)


async def get_project_branches(
    db: AsyncSession,
    project_id: int,
    status: Optional[BranchStatus] = None,
) -> List[Branch]:
    """获取项目的所有分支"""
    query = select(Branch).where(Branch.project_id == project_id)

    if status is not None:
        query = query.where(Branch.status == status)

    query = query.order_by(Branch.created_at)
    result = await db.execute(query)
    return list(result.scalars().all())


async def get_branch_page(
    db: AsyncSession,
    branch_id: int,
    page_type: str,
) -> Optional[ProjectPage]:
    """获取分支下特定类型的页面"""
    result = await db.execute(
        select(ProjectPage)
        .where(ProjectPage.branch_id == branch_id)
        .where(ProjectPage.page_type == page_type)
        .where(ProjectPage.is_hidden == False)
    )
    return result.scalar_one_or_none()


async def clone_branch_pages(
    db: AsyncSession,
    source_branch_id: int,
    target_branch_id: int,
    created_by: int,
) -> int:
    """克隆分支的页面和组件到新分支

    Args:
        source_branch_id: 源分支 ID
        target_branch_id: 目标分支 ID
        created_by: 创建人 ID

    Returns:
        克隆的页面数量
    """
    # 获取源分支的所有页面
    source_pages_result = await db.execute(
        select(ProjectPage)
        .where(ProjectPage.branch_id == source_branch_id)
        .where(ProjectPage.is_hidden == False)
    )
    source_pages = source_pages_result.scalars().all()

    cloned_count = 0

    for source_page in source_pages:
        # 克隆页面（不复制 ID）
        new_page = ProjectPage(
            project_id=source_page.project_id,
            branch_id=target_branch_id,
            title=source_page.title,
            page_type=source_page.page_type,
            icon=source_page.icon,
            control_power=source_page.control_power,
            edit_power=source_page.edit_power,
            view_power=source_page.view_power,
            order_index=source_page.order_index,
            is_hidden=source_page.is_hidden,
            created_by=created_by,
            updated_by=created_by,
        )
        db.add(new_page)
        await db.flush()  # 获取 new_page.id

        # 获取源页面的组件关系
        source_components_result = await db.execute(
            select(PageComponentRelation)
            .where(PageComponentRelation.page_id == source_page.id)
            .order_by(PageComponentRelation.order_index)
        )
        source_relations = source_components_result.scalars().all()

        # 克隆组件和关系
        for source_rel in source_relations:
            # 获取源组件
            source_component = await db.get(Component, source_rel.component_id)
            if source_component:
                # 创建组件副本
                new_component = Component(
                    component_type=source_component.component_type,
                    component_key=source_component.component_key,
                    title=source_component.title,
                    description=source_component.description,
                    data=source_component.data.copy(),
                    schema=source_component.schema.copy() if source_component.schema else None,
                    visible=source_component.visible,
                    created_by=created_by,
                )
                db.add(new_component)
                await db.flush()  # 获取 new_component.id

                # 创建关系
                new_relation = PageComponentRelation(
                    page_id=new_page.id,
                    component_id=new_component.id,
                    order_index=source_rel.order_index,
                    created_by=created_by,
                )
                db.add(new_relation)

        cloned_count += 1

    await db.commit()
    return cloned_count


async def get_main_branch(
    db: AsyncSession,
    project_id: int,
) -> Optional[Branch]:
    """获取项目的主分支（branch_id=0 或名为 main 的分支）"""
    # 先尝试获取 branch_id=0 的情况（如果 project_pages 的 branch_id=0 代表主分支）
    # 这里返回名为 "main" 的分支
    return await get_branch_by_name(db, project_id, "main")


async def create_branch_from_template(
    db: AsyncSession,
    project_id: int,
    name: str,
    created_by: int,
    category: str = "general",
    description: Optional[str] = None,
) -> Branch:
    """从模板创建分支（自动初始化页面）

    Args:
        project_id: 项目 ID
        name: 分支名称
        created_by: 创建人 ID
        category: 页面分类（general, code, writing 等）
        description: 分支描述
    """
    from app.project_templates import PAGE_TYPES_BY_CATEGORY

    # 1. 创建分支
    branch = await create_branch(
        db=db,
        project_id=project_id,
        name=name,
        created_by=created_by,
        description=description,
    )

    # 2. 获取该分类的页面模板
    page_templates = PAGE_TYPES_BY_CATEGORY.get(category, {})

    # 3. 创建默认页面
    for index, (page_type, template) in enumerate(page_templates.items()):
        page = ProjectPage(
            project_id=project_id,
            branch_id=branch.id,
            title=template["display_name"],
            page_type=page_type,
            icon=template["icon"],
            order_index=index,
            is_hidden=False,
            created_by=created_by,
            updated_by=created_by,
        )
        db.add(page)
        await db.flush()

        # 批量添加组件
        template_components = template["default_schema"]["components"]
        components_data = []

        for comp in template_components:
            components_data.append({
                "component_type": comp["type"],
                "component_key": comp["id"],
                "title": comp.get("title"),
                "description": comp.get("description"),
                "data": comp.get("data", {}),
                "schema": comp.get("schema"),
                "visible": comp.get("visible", True),
                "order_index": comp.get("order", 0),
            })

        await batch_add_components_to_page(
            db=db,
            page_id=page.id,
            components=components_data,
            created_by=created_by,
        )

    await db.commit()
    return branch
