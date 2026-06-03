"""
组件 CRUD 操作
"""
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.components import Component, PageComponentRelation
from typing import Any, Optional, List


# ========== Component CRUD ==========

async def get_component(db: AsyncSession, component_id: int) -> Optional[Component]:
    """根据 ID 获取组件"""
    result = await db.execute(select(Component).where(Component.id == component_id))
    return result.scalar_one_or_none()


async def get_component_by_key(db: AsyncSession, component_key: str) -> Optional[Component]:
    """根据 component_key 获取组件"""
    result = await db.execute(select(Component).where(Component.component_key == component_key))
    return result.scalar_one_or_none()


async def create_component(
    db: AsyncSession,
    component_type: str,
    component_key: str,
    data: dict,
    created_by: int,
    title: Optional[str] = None,
    description: Optional[str] = None,
    schema: Optional[dict] = None,
    visible: bool = True,
) -> Component:
    """创建新组件"""
    component = Component(
        component_type=component_type,
        component_key=component_key,
        title=title,
        description=description,
        data=data,
        schema=schema,
        visible=visible,
        created_by=created_by,
    )
    db.add(component)
    await db.commit()
    await db.refresh(component)
    return component


async def update_component(
    db: AsyncSession,
    component_id: int,
    data: Optional[dict] = None,
    title: Optional[str] = None,
    description: Optional[str] = None,
    schema: Optional[dict] = None,
    visible: Optional[bool] = None,
) -> Optional[Component]:
    """更新组件"""
    component = await get_component(db, component_id)
    if not component:
        return None

    if data is not None:
        component.data = data
    if title is not None:
        component.title = title
    if description is not None:
        component.description = description
    if schema is not None:
        component.schema = schema
    if visible is not None:
        component.visible = visible

    await db.commit()
    await db.refresh(component)
    return component


async def delete_component(db: AsyncSession, component_id: int) -> bool:
    """删除组件"""
    component = await get_component(db, component_id)
    if not component:
        return False

    await db.delete(component)
    await db.commit()
    return True


# ========== PageComponentRelation CRUD ==========

async def get_page_component_relation(
    db: AsyncSession,
    page_id: int,
    component_id: int
) -> Optional[PageComponentRelation]:
    """获取页面和组件的关系"""
    result = await db.execute(
        select(PageComponentRelation)
        .where(PageComponentRelation.page_id == page_id)
        .where(PageComponentRelation.component_id == component_id)
    )
    return result.scalar_one_or_none()


async def add_component_to_page(
    db: AsyncSession,
    page_id: int,
    component_id: int,
    order_index: int,
    created_by: int,
) -> PageComponentRelation:
    """将组件添加到页面"""
    relation = PageComponentRelation(
        page_id=page_id,
        component_id=component_id,
        order_index=order_index,
        created_by=created_by,
    )
    db.add(relation)
    await db.commit()
    await db.refresh(relation)
    return relation


async def update_component_order(
    db: AsyncSession,
    page_id: int,
    component_id: int,
    new_order: int,
) -> Optional[PageComponentRelation]:
    """更新组件在页面中的顺序"""
    relation = await get_page_component_relation(db, page_id, component_id)
    if not relation:
        return None

    relation.order_index = new_order
    await db.commit()
    await db.refresh(relation)
    return relation


async def remove_component_from_page(
    db: AsyncSession,
    page_id: int,
    component_id: int,
) -> bool:
    """从页面移除组件（不删除组件本身）"""
    relation = await get_page_component_relation(db, page_id, component_id)
    if not relation:
        return False

    await db.delete(relation)
    await db.commit()
    return True


async def get_page_components(db: AsyncSession, page_id: int) -> list[dict[str, Any]]:
    """获取页面的所有组件（按顺序）"""
    result = await db.execute(
        select(PageComponentRelation, Component)
        .join(Component, PageComponentRelation.component_id == Component.id)
        .where(PageComponentRelation.page_id == page_id)
        .order_by(PageComponentRelation.order_index)
    )

    relations = result.all()
    return [
        {
            "id": comp.id,
            "component_type": comp.component_type,
            "component_key": comp.component_key,
            "title": comp.title,
            "description": comp.description,
            "data": comp.data,
            "schema": comp.schema,
            "visible": comp.visible,
            "order_index": rel.order_index,
        }
        for rel, comp in relations
    ]


async def batch_add_components_to_page(
    db: AsyncSession,
    page_id: int,
    components: list[dict[str, Any]],
    created_by: int,
) -> list[PageComponentRelation]:
    """批量添加组件到页面"""
    relations = []

    for comp_data in components:
        component = Component(
            component_type=comp_data["component_type"],
            component_key=comp_data["component_key"],
            title=comp_data.get("title"),
            description=comp_data.get("description"),
            data=comp_data.get("data", {}),
            schema=comp_data.get("schema"),
            visible=comp_data.get("visible", True),
            created_by=created_by,
        )
        db.add(component)
        await db.flush()

        relation = PageComponentRelation(
            page_id=page_id,
            component_id=component.id,
            order_index=comp_data.get("order_index", 0),
            created_by=created_by,
        )
        db.add(relation)
        relations.append(relation)

    await db.commit()

    for relation in relations:
        await db.refresh(relation)

    return relations


async def sync_page_components(
    db: AsyncSession,
    page_id: int,
    components: list[dict[str, Any]],
    updated_by: int,
) -> list[dict[str, Any]]:
    """同步页面组件（先删除现有关系，再批量添加）"""
    # 1. 删除现有关系（不删除组件本身）
    await db.execute(
        PageComponentRelation.__table__.delete()
        .where(PageComponentRelation.page_id == page_id)
    )

    # 2. 批量添加新组件
    relations = await batch_add_components_to_page(
        db=db,
        page_id=page_id,
        components=components,
        created_by=updated_by,
    )

    # 3. 返回完整组件列表
    return await get_page_components(db, page_id)


# ========== 扩展辅助函数 ==========

async def get_components_by_type(
    db: AsyncSession,
    component_type: str,
    page_id: Optional[int] = None,
    limit: int = 50,
) -> list[dict[str, Any]]:
    """按组件类型过滤组件列表"""
    query = (
        select(Component)
        .where(Component.component_type == component_type)
        .order_by(desc(Component.created_at))
        .limit(limit)
    )
    result = await db.execute(query)
    return [
        {
            "id": c.id,
            "component_type": c.component_type,
            "component_key": c.component_key,
            "title": c.title,
            "description": c.description,
            "data": c.data,
            "visible": c.visible,
            "created_at": c.created_at,
        }
        for c in result.scalars().all()
    ]


async def get_component_type_stats(
    db: AsyncSession,
    page_id: int,
) -> dict[str, int]:
    """统计页面上各类型组件的分布"""
    result = await db.execute(
        select(Component.component_type, func.count(Component.id))
        .join(PageComponentRelation, PageComponentRelation.component_id == Component.id)
        .where(PageComponentRelation.page_id == page_id)
        .group_by(Component.component_type)
    )
    return {row[0]: row[1] for row in result.all()}
