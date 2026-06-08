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


# ── 短别名 ──────────────────────────────────────────────────────────────

async def is_admin(db: AsyncSession, user_id: int) -> bool:
    """is_user_admin 的短别名"""
    return await is_user_admin(db, user_id)


async def is_ban(db: AsyncSession, user_id: int) -> bool:
    """is_user_banned 的短别名"""
    return await is_user_banned(db, user_id)


# ── 注册审核 ──────────────────────────────────────────────────────────────


async def _get_system_group(db: AsyncSession, name: str) -> Optional[Group]:
    """按名称查找系统组"""
    result = await db.execute(
        select(Group).where(Group.name == name).where(Group.group_type == "system")
    )
    return result.scalar_one_or_none()


async def add_user_to_pending(db: AsyncSession, user_id: int) -> bool:
    """将用户加入 pending_approval 组"""
    group = await _get_system_group(db, "pending_approval")
    if not group:
        return False
    try:
        await add_member(db, group.id, user_id, GroupRole.MEMBER)
        return True
    except ValueError:
        return False  # 已在组中


async def approve_user(db: AsyncSession, user_id: int) -> bool:
    """审核通过：从 pending_approval 移到 default 组"""
    pending = await _get_system_group(db, "pending_approval")
    if pending:
        await remove_member(db, pending.id, user_id)

    default = await _get_system_group(db, "default")
    if not default:
        return False
    try:
        await add_member(db, default.id, user_id, GroupRole.MEMBER)
        return True
    except ValueError:
        # 已在 default 组，也算成功
        return True


async def reject_user(db: AsyncSession, user_id: int, reason: str = "") -> bool:
    """审核拒绝：从 pending_approval 移到 rejected 组，释放工号"""
    from app.models.users import User

    pending = await _get_system_group(db, "pending_approval")
    if pending:
        await remove_member(db, pending.id, user_id)

    # 移出 default 组（防并发异常）
    default = await _get_system_group(db, "default")
    if default:
        await remove_member(db, default.id, user_id)

    rejected = await _get_system_group(db, "rejected")
    if not rejected:
        return False
    try:
        await add_member(db, rejected.id, user_id, GroupRole.MEMBER)
    except ValueError:
        pass

    # 释放工号并记录拒绝理由
    from sqlalchemy import update
    stmt = (
        update(User)
        .where(User.id == user_id)
        .values(job_number=None, reject_reason=reason)
    )
    await db.execute(stmt)
    await db.commit()
    return True


async def is_user_pending(db: AsyncSession, user_id: int) -> bool:
    """判断用户是否在 pending_approval 组（待审核）"""
    group = await _get_system_group(db, "pending_approval")
    if not group:
        return False
    return await is_user_in_group(db, user_id, group.id)


async def is_user_rejected(db: AsyncSession, user_id: int) -> bool:
    """判断用户是否被拒绝（在 rejected 组）"""
    group = await _get_system_group(db, "rejected")
    if not group:
        return False
    return await is_user_in_group(db, user_id, group.id)


async def reappeal_user(db: AsyncSession, user_id: int, bio: str) -> bool:
    """用户申诉：从 rejected 移回 pending_approval，更新介绍，清空拒绝理由"""
    from app.models.users import User
    from sqlalchemy import update

    rejected = await _get_system_group(db, "rejected")
    if rejected:
        await remove_member(db, rejected.id, user_id)

    pending = await _get_system_group(db, "pending_approval")
    if not pending:
        return False
    try:
        await add_member(db, pending.id, user_id, GroupRole.MEMBER)
    except ValueError:
        pass

    stmt = update(User).where(User.id == user_id).values(bio=bio, reject_reason=None)
    await db.execute(stmt)
    await db.commit()
    return True


async def get_pending_users(
    db: AsyncSession,
    page: int = 1,
    page_size: int = 20,
) -> list[dict]:
    """获取待审核用户列表（分页，含用户信息）"""
    from app.models.users import User

    group = await _get_system_group(db, "pending_approval")
    if not group:
        return []

    result = await db.execute(
        select(GroupUserRelation, User)
        .join(User, GroupUserRelation.user_id == User.id)
        .where(GroupUserRelation.group_id == group.id)
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
            "email": user.email or "",
            "job_number": user.job_number,
            "bio": user.bio or "",
            "created_at": rel.created_at,
        }
        for rel, user in rows
    ]
