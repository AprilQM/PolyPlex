"""
用户组 CRUD 操作
"""
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.groups import Group, GroupType
from typing import Optional, List
import os


async def get_group(db: AsyncSession, group_id: int) -> Optional[Group]:
    """根据 ID 获取组"""
    result = await db.execute(select(Group).where(Group.id == group_id))
    return result.scalar_one_or_none()


async def get_group_by_name(db: AsyncSession, name: str) -> Optional[Group]:
    """根据名称获取组"""
    result = await db.execute(select(Group).where(Group.name == name))
    return result.scalar_one_or_none()


async def create_group(
    db: AsyncSession,
    name: str,
    description: Optional[str] = None,
    group_type: GroupType = GroupType.USER,
) -> Group:
    """创建组"""
    group = Group(
        name=name,
        description=description,
        group_type=group_type,
    )
    db.add(group)
    await db.commit()
    await db.refresh(group)
    return group


async def update_group(
    db: AsyncSession,
    group_id: int,
    name: Optional[str] = None,
    description: Optional[str] = None,
) -> Optional[Group]:
    """更新组（system 组禁止修改 name）"""
    group = await get_group(db, group_id)
    if not group:
        return None
    if group.group_type == GroupType.SYSTEM:
        return None  # system 组不可修改
    if name is not None:
        group.name = name
    if description is not None:
        group.description = description
    await db.commit()
    await db.refresh(group)
    return group


async def delete_group(db: AsyncSession, group_id: int) -> bool:
    """删除组（system 组禁止删除）"""
    group = await get_group(db, group_id)
    if not group or group.group_type == GroupType.SYSTEM:
        return False
    await db.delete(group)
    await db.commit()
    return True


async def get_user_groups(db: AsyncSession, user_id: int) -> List[Group]:
    """获取用户所属的所有组"""
    from app.models.groups import GroupUserRelation
    result = await db.execute(
        select(Group)
        .join(GroupUserRelation, GroupUserRelation.group_id == Group.id)
        .where(GroupUserRelation.user_id == user_id)
    )
    return list(result.scalars().all())


async def get_all_groups(
    db: AsyncSession,
    page: int = 1,
    page_size: int = 20,
) -> List[Group]:
    """获取所有组（分页）"""
    result = await db.execute(
        select(Group)
        .order_by(desc(Group.created_at))
        .offset((page - 1) * page_size)
        .limit(page_size)
    )
    return list(result.scalars().all())


async def ensure_default_groups(db: AsyncSession) -> dict[str, Group]:
    """确保默认系统组存在，返回 {name: group} 字典"""
    default_names = ["admin", "default", "ban", "pending_approval", "rejected"]
    groups = {}
    for name in default_names:
        group = await get_group_by_name(db, name)
        if not group:
            group = await create_group(
                db=db,
                name=name,
                description=f"System {name} group",
                group_type=GroupType.SYSTEM,
            )
        groups[name] = group
    return groups
