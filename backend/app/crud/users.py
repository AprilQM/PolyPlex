"""
用户 CRUD 操作
"""
from sqlalchemy import select, desc, update, func, cast, Integer
from sqlalchemy.engine import result
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.users import User, UserTag, UserTagRelation
from typing import Optional, List


# ========== User CRUD ==========

async def get_user(db: AsyncSession, user_id: int) -> Optional[User]:
    """根据 ID 获取用户"""
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()


async def get_user_by_username(db: AsyncSession, username: str) -> Optional[User]:
    """根据用户名获取用户"""
    result = await db.execute(select(User).where(User.username == username))
    return result.scalar_one_or_none()


async def get_user_by_email(db: AsyncSession, email: str) -> Optional[User]:
    """根据邮箱获取用户"""
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()


async def get_user_by_job_number(db: AsyncSession, job_number: str) -> Optional[User]:
    """根据工号获取用户"""
    result = await db.execute(select(User).where(User.job_number == job_number))
    return result.scalar_one_or_none()


async def get_system_user(db: AsyncSession) -> Optional[User]:
    """获取系统用户"""
    result = await db.execute(select(User).where(User.is_system == True))
    return result.scalar_one_or_none()

async def create_user(
    db: AsyncSession,
    username: str,
    password_hash: str,
) -> User:
    """创建新用户，自动从 10000 递增分配工号"""
    from sqlalchemy import func, cast, Integer
    max_job = await db.execute(
        select(func.max(cast(User.job_number, Integer)))
    )
    next_num = (max_job.scalar() or 9999) + 1
    user = User(
        username=username,
        password_hash=password_hash,
        job_number=str(next_num),
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)

    # 自动加入 default 组
    from app.crud.groups import get_group_by_name
    from app.crud.group_user_relations import add_member
    from app.models.groups import GroupRole
    default_group = await get_group_by_name(db, "default")
    if default_group:
        await add_member(db, default_group.id, user.id, GroupRole.MEMBER)

    return user


async def update_user(
    db: AsyncSession,
    user_id: int,
    username: Optional[str] = None,
    email: Optional[str] = None,
    password_hash: Optional[str] = None,
    job_number: Optional[str] = None,
) -> Optional[User]:
    """更新用户信息"""
    user = await get_user(db, user_id)
    if not user:
        return None

    if username is not None:
        user.username = username
    if email is not None:
        user.email = email
    if password_hash is not None:
        user.password_hash = password_hash
    if job_number is not None:
        user.job_number = job_number

    await db.commit()
    await db.refresh(user)
    return user


async def delete_user(db: AsyncSession, user_id: int) -> bool:
    """删除用户"""
    user = await get_user(db, user_id)
    if not user:
        return False

    await db.delete(user)
    await db.commit()
    return True


async def update_user_login_time(db: AsyncSession, user_id: int) -> Optional[User]:
    """更新用户登录时间"""
    import time
    user = await get_user(db, user_id)
    if not user:
        return None

    user.login_at = int(time.time())
    await db.commit()
    await db.refresh(user)
    return user


async def get_user_by_git_token(db: AsyncSession, token_hash: str) -> Optional[User]:
    """根据 git_token_hash 查找用户"""
    result = await db.execute(
        select(User).where(User.git_token_hash == token_hash)
    )
    return result.scalar_one_or_none()


async def update_git_token_hash(
    db: AsyncSession,
    user_id: int,
    token_hash: Optional[str],
) -> Optional[User]:
    """更新用户的 git_token_hash（设为 None 可清除 token）"""
    user = await get_user(db, user_id)
    if not user:
        return None
    user.git_token_hash = token_hash
    await db.commit()
    await db.refresh(user)
    return user


async def get_user_list(
    db: AsyncSession,
    page: int = 1,
    page_size: int = 20,
) -> List[User]:
    """获取用户列表（分页）"""
    query = select(User)

    query = query.order_by(desc(User.created_at))
    query = query.offset((page - 1) * page_size).limit(page_size)

    result = await db.execute(query)
    return list(result.scalars().all())


async def count_users(db: AsyncSession) -> int:
    """统计用户数量"""
    from sqlalchemy import func
    query = select(func.count(User.id))
    result = await db.execute(query)
    return result.scalar()


# ========== UserTag CRUD ==========

async def get_user_tag(db: AsyncSession, tag_id: int) -> Optional[UserTag]:
    """根据 ID 获取用户标签"""
    result = await db.execute(select(UserTag).where(UserTag.id == tag_id))
    return result.scalar_one_or_none()


async def get_user_tag_by_name(db: AsyncSession, name: str) -> Optional[UserTag]:
    """根据名称获取用户标签"""
    result = await db.execute(select(UserTag).where(UserTag.name == name))
    return result.scalar_one_or_none()


async def create_user_tag(
    db: AsyncSession,
    name: str,
    color: str,
) -> UserTag:
    """创建用户标签"""
    tag = UserTag(name=name, color=color)
    db.add(tag)
    await db.commit()
    await db.refresh(tag)
    return tag


async def update_user_tag(
    db: AsyncSession,
    tag_id: int,
    name: Optional[str] = None,
    color: Optional[str] = None,
) -> Optional[UserTag]:
    """更新用户标签"""
    tag = await get_user_tag(db, tag_id)
    if not tag:
        return None

    if name is not None:
        tag.name = name
    if color is not None:
        tag.color = color

    await db.commit()
    await db.refresh(tag)
    return tag


async def delete_user_tag(db: AsyncSession, tag_id: int) -> bool:
    """删除用户标签"""
    tag = await get_user_tag(db, tag_id)
    if not tag:
        return False

    await db.delete(tag)
    await db.commit()
    return True


async def get_all_user_tags(db: AsyncSession) -> List[UserTag]:
    """获取所有用户标签"""
    result = await db.execute(select(UserTag).order_by(UserTag.created_at))
    return list(result.scalars().all())


# ========== UserTagRelation CRUD ==========

async def get_user_tag_relation(
    db: AsyncSession,
    user_id: int,
    tag_id: int
) -> Optional[UserTagRelation]:
    """获取用户标签关系"""
    result = await db.execute(
        select(UserTagRelation)
        .where(UserTagRelation.user_id == user_id)
        .where(UserTagRelation.tag_id == tag_id)
    )
    return result.scalar_one_or_none()


async def add_user_tag(
    db: AsyncSession,
    user_id: int,
    tag_id: int,
) -> UserTagRelation:
    """给用户添加标签"""
    relation = UserTagRelation(user_id=user_id, tag_id=tag_id)
    db.add(relation)
    await db.commit()
    await db.refresh(relation)
    return relation


async def remove_user_tag(
    db: AsyncSession,
    user_id: int,
    tag_id: int,
) -> bool:
    """移除用户标签"""
    relation = await get_user_tag_relation(db, user_id, tag_id)
    if not relation:
        return False

    await db.delete(relation)
    await db.commit()
    return True


async def get_user_tags(db: AsyncSession, user_id: int) -> List[UserTag]:
    """获取用户的所有标签"""
    result = await db.execute(
        select(UserTag)
        .join(UserTagRelation)
        .where(UserTagRelation.user_id == user_id)
    )
    return list(result.scalars().all())


async def get_tag_users(db: AsyncSession, tag_id: int) -> List[User]:
    """获取标签下的所有用户"""
    result = await db.execute(
        select(User)
        .join(UserTagRelation)
        .where(UserTagRelation.tag_id == tag_id)
    )
    return list(result.scalars().all())


async def batch_add_user_tags(
    db: AsyncSession,
    user_id: int,
    tag_ids: List[int],
) -> List[UserTagRelation]:
    """批量给用户添加标签"""
    relations = []
    for tag_id in tag_ids:
        # 检查是否已存在
        existing = await get_user_tag_relation(db, user_id, tag_id)
        if not existing:
            relation = UserTagRelation(user_id=user_id, tag_id=tag_id)
            db.add(relation)
            relations.append(relation)

    if relations:
        await db.commit()
        for relation in relations:
            await db.refresh(relation)

    return relations
