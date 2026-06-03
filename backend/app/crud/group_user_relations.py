"""
用户组成员关系 CRUD 操作
"""
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.groups import GroupUserRelation, GroupRole, Group
from typing import Optional, List


async def add_member(
    db: AsyncSession,
    group_id: int,
    user_id: int,
    role: GroupRole = GroupRole.MEMBER,
) -> GroupUserRelation:
    """添加成员到组"""
    # 检查是否已存在
    existing = await db.execute(
        select(GroupUserRelation)
        .where(GroupUserRelation.group_id == group_id)
        .where(GroupUserRelation.user_id == user_id)
    )
    if existing.scalar_one_or_none():
        raise ValueError("User is already a member of this group")

    relation = GroupUserRelation(
        group_id=group_id,
        user_id=user_id,
        role=role,
    )
    db.add(relation)
    await db.commit()
    await db.refresh(relation)
    return relation


async def remove_member(db: AsyncSession, group_id: int, user_id: int) -> bool:
    """从组移除成员"""
    result = await db.execute(
        select(GroupUserRelation)
        .where(GroupUserRelation.group_id == group_id)
        .where(GroupUserRelation.user_id == user_id)
    )
    relation = result.scalar_one_or_none()
    if not relation:
        return False
    await db.delete(relation)
    await db.commit()
    return True


async def update_member_role(
    db: AsyncSession,
    group_id: int,
    user_id: int,
    role: GroupRole,
) -> Optional[GroupUserRelation]:
    """更新成员角色"""
    result = await db.execute(
        select(GroupUserRelation)
        .where(GroupUserRelation.group_id == group_id)
        .where(GroupUserRelation.user_id == user_id)
    )
    relation = result.scalar_one_or_none()
    if not relation:
        return None
    relation.role = role
    await db.commit()
    await db.refresh(relation)
    return relation


async def get_group_members(
    db: AsyncSession,
    group_id: int,
    page: int = 1,
    page_size: int = 20,
) -> List[dict]:
    """获取组成员列表（分页，含用户基本信息）"""
    from app.models.users import User
    result = await db.execute(
        select(GroupUserRelation, User)
        .join(User, GroupUserRelation.user_id == User.id)
        .where(GroupUserRelation.group_id == group_id)
        .order_by(GroupUserRelation.created_at)
        .offset((page - 1) * page_size)
        .limit(page_size)
    )
    rows = result.all()
    return [
        {
            "relation_id": rel.id,
            "user_id": user.id,
            "username": user.username,
            "email": user.email,
            "job_number": user.job_number,
            "role": rel.role.value,
            "created_at": rel.created_at,
        }
        for rel, user in rows
    ]


async def get_user_group_ids(db: AsyncSession, user_id: int) -> List[int]:
    """快速查询用户所属的组 ID 列表"""
    result = await db.execute(
        select(GroupUserRelation.group_id)
        .where(GroupUserRelation.user_id == user_id)
    )
    return list(result.scalars().all())


async def is_user_in_group(db: AsyncSession, user_id: int, group_id: int) -> bool:
    """判断用户是否在某组中"""
    result = await db.execute(
        select(GroupUserRelation)
        .where(GroupUserRelation.group_id == group_id)
        .where(GroupUserRelation.user_id == user_id)
    )
    return result.scalar_one_or_none() is not None


async def is_user_admin(db: AsyncSession, user_id: int) -> bool:
    """判断用户是否为管理员（在 admin 组中）"""
    group_result = await db.execute(
        select(Group).where(Group.name == "admin").where(Group.group_type == "system")
    )
    admin_group = group_result.scalar_one_or_none()
    if not admin_group:
        return False
    return await is_user_in_group(db, user_id, admin_group.id)


async def is_user_banned(db: AsyncSession, user_id: int) -> bool:
    """判断用户是否被封禁（在 ban 组中）"""
    group_result = await db.execute(
        select(Group).where(Group.name == "ban").where(Group.group_type == "system")
    )
    ban_group = group_result.scalar_one_or_none()
    if not ban_group:
        return False
    return await is_user_in_group(db, user_id, ban_group.id)
