"""
项目页面 CRUD 操作（含文件夹树）
"""
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.projects import ProjectPage
from typing import Any, Optional


async def get_page(db: AsyncSession, page_id: int) -> Optional[ProjectPage]:
    """根据 ID 获取页面"""
    result = await db.execute(select(ProjectPage).where(ProjectPage.id == page_id))
    return result.scalar_one_or_none()


async def create_page(
    db: AsyncSession,
    project_id: int,
    title: str,
    branch_id: int = 0,
    page_type: str = "announcement",
    icon: Optional[str] = None,
    parent_id: Optional[int] = None,
    is_folder: bool = False,
    order_index: int = 0,
    created_by: int = 0,
) -> ProjectPage:
    """创建页面或文件夹"""
    page = ProjectPage(
        project_id=project_id,
        branch_id=branch_id,
        title=title,
        page_type=page_type,
        icon=icon,
        parent_id=parent_id,
        is_folder=is_folder,
        order_index=order_index,
        created_by=created_by,
        updated_by=created_by,
    )
    db.add(page)
    await db.commit()
    await db.refresh(page)
    return page


async def update_page(
    db: AsyncSession,
    page_id: int,
    title: Optional[str] = None,
    icon: Optional[str] = None,
    parent_id: Optional[int] = None,
    order_index: Optional[int] = None,
    is_hidden: Optional[bool] = None,
    updated_by: Optional[int] = None,
) -> Optional[ProjectPage]:
    """更新页面信息"""
    page = await get_page(db, page_id)
    if not page:
        return None

    if title is not None:
        page.title = title
    if icon is not None:
        page.icon = icon
    if parent_id is not None:
        page.parent_id = parent_id
    if order_index is not None:
        page.order_index = order_index
    if is_hidden is not None:
        page.is_hidden = is_hidden
    if updated_by is not None:
        page.updated_by = updated_by

    await db.commit()
    await db.refresh(page)
    return page


async def delete_page(db: AsyncSession, page_id: int) -> bool:
    """删除页面（非文件夹页面会级联删除关联数据）"""
    page = await get_page(db, page_id)
    if not page:
        return False

    await db.delete(page)
    await db.commit()
    return True


async def get_project_pages(
    db: AsyncSession,
    project_id: int,
    branch_id: int = 0,
    parent_id: Optional[int] = None,
) -> list[dict[str, Any]]:
    """获取项目在指定分支下的页面列表（扁平化）"""
    query = (
        select(ProjectPage)
        .where(ProjectPage.project_id == project_id)
        .where(ProjectPage.branch_id == branch_id)
        .order_by(ProjectPage.parent_id.asc().nullsfirst(), ProjectPage.order_index.asc())
    )
    if parent_id is not None:
        query = query.where(ProjectPage.parent_id == parent_id)

    result = await db.execute(query)
    return [
        {
            "id": p.id,
            "title": p.title,
            "page_type": p.page_type,
            "icon": p.icon,
            "parent_id": p.parent_id,
            "is_folder": p.is_folder,
            "is_hidden": p.is_hidden,
            "order_index": p.order_index,
            "created_at": p.created_at,
        }
        for p in result.scalars().all()
    ]


async def get_page_folder_tree(
    db: AsyncSession,
    project_id: int,
    branch_id: int = 0,
) -> list[dict[str, Any]]:
    """
    获取项目的页面文件夹树（嵌套字典/列表结构）。
    返回按 parent_id 组织的树状结构，用于前端渲染文件夹导航。
    """
    result = await db.execute(
        select(ProjectPage)
        .where(ProjectPage.project_id == project_id)
        .where(ProjectPage.branch_id == branch_id)
        .where(ProjectPage.is_hidden == False)
        .order_by(ProjectPage.order_index.asc())
    )
    pages = result.scalars().all()

    # 构建节点映射
    node_map: dict[int, dict] = {}
    for p in pages:
        node_map[p.id] = {
            "id": p.id,
            "title": p.title,
            "page_type": p.page_type,
            "icon": p.icon,
            "parent_id": p.parent_id,
            "is_folder": p.is_folder,
            "order_index": p.order_index,
            "children": [],
        }

    # 构建树
    root_nodes: list[dict] = []
    for node in node_map.values():
        parent_id = node["parent_id"]
        if parent_id is None or parent_id not in node_map:
            root_nodes.append(node)
        else:
            node_map[parent_id]["children"].append(node)

    return root_nodes


async def move_page(
    db: AsyncSession,
    page_id: int,
    new_parent_id: Optional[int],
    new_order_index: int = 0,
    updated_by: Optional[int] = None,
) -> Optional[ProjectPage]:
    """移动页面到新的父文件夹位置"""
    return await update_page(
        db=db,
        page_id=page_id,
        parent_id=new_parent_id,
        order_index=new_order_index,
        updated_by=updated_by,
    )
