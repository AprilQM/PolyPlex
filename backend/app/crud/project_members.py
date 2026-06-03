"""
项目成员 CRUD 操作
"""
from sqlalchemy import select, desc, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.members import ProjectMember, RoleType
from app.models.projects import Project
from typing import Optional, List


# ========== ProjectMember CRUD ==========

async def get_project_member(
    db: AsyncSession,
    project_id: int,
    user_id: int
) -> Optional[ProjectMember]:
    """获取项目成员关系"""
    result = await db.execute(
        select(ProjectMember)
        .where(ProjectMember.project_id == project_id)
        .where(ProjectMember.user_id == user_id)
    )
    return result.scalar_one_or_none()


async def add_project_member(
    db: AsyncSession,
    project_id: int,
    user_id: int,
    role: RoleType = RoleType.VIEWER,
) -> ProjectMember:
    """添加项目成员"""
    relation = ProjectMember(
        project_id=project_id,
        user_id=user_id,
        role=role,
    )
    db.add(relation)
    await db.commit()
    await db.refresh(relation)
    return relation


async def update_member_role(
    db: AsyncSession,
    project_id: int,
    user_id: int,
    role: RoleType,
) -> Optional[ProjectMember]:
    """更新成员角色"""
    relation = await get_project_member(db, project_id, user_id)
    if not relation:
        return None

    relation.role = role
    await db.commit()
    await db.refresh(relation)
    return relation


async def remove_project_member(
    db: AsyncSession,
    project_id: int,
    user_id: int,
) -> bool:
    """移除项目成员"""
    relation = await get_project_member(db, project_id, user_id)
    if not relation:
        return False

    await db.delete(relation)
    await db.commit()
    return True


async def get_project_members(
    db: AsyncSession,
    project_id: int,
    role: Optional[RoleType] = None,
) -> List[ProjectMember]:
    """获取项目的所有成员"""
    query = select(ProjectMember).where(ProjectMember.project_id == project_id)

    if role is not None:
        query = query.where(ProjectMember.role == role)

    query = query.order_by(ProjectMember.created_at)
    result = await db.execute(query)
    return list(result.scalars().all())


async def get_user_projects(
    db: AsyncSession,
    user_id: int,
    role: Optional[RoleType] = None,
) -> List[Project]:
    """获取用户参与的所有项目"""
    query = (
        select(Project)
        .join(ProjectMember)
        .where(ProjectMember.user_id == user_id)
    )

    if role is not None:
        query = query.where(ProjectMember.role == role)

    result = await db.execute(query)
    return list(result.scalars().all())


async def get_member_count(
    db: AsyncSession,
    project_id: int,
    role: Optional[RoleType] = None,
) -> int:
    """统计项目成员数量"""
    query = select(func.count(ProjectMember.id)).where(
        ProjectMember.project_id == project_id
    )

    if role is not None:
        query = query.where(ProjectMember.role == role)

    result = await db.execute(query)
    return result.scalar()


async def has_member_permission(
    db: AsyncSession,
    project_id: int,
    user_id: int,
    min_role: RoleType,
) -> bool:
    """检查用户是否有指定级别以上的权限"""
    relation = await get_project_member(db, project_id, user_id)
    if not relation:
        return False

    role_hierarchy = {
        RoleType.VIEWER: 0,
        RoleType.CONTRIBUTOR: 1,
        RoleType.ADMIN: 2,
        RoleType.OWNER: 3,
    }

    return role_hierarchy.get(relation.role, 0) >= role_hierarchy.get(min_role, 0)


async def is_project_owner(
    db: AsyncSession,
    project_id: int,
    user_id: int,
) -> bool:
    """检查用户是否是项目所有者"""
    relation = await get_project_member(db, project_id, user_id)
    return relation is not None and relation.role == RoleType.OWNER


async def is_project_admin(
    db: AsyncSession,
    project_id: int,
    user_id: int,
) -> bool:
    """检查用户是否是项目管理员（包括所有者）"""
    return await has_member_permission(db, project_id, user_id, RoleType.ADMIN)


async def is_project_contributor(
    db: AsyncSession,
    project_id: int,
    user_id: int,
) -> bool:
    """检查用户是否是项目贡献者（包括管理员和所有者）"""
    return await has_member_permission(db, project_id, user_id, RoleType.CONTRIBUTOR)


async def is_project_editor(
    db: AsyncSession,
    project_id: int,
    user_id: int,
) -> bool:
    """（兼容旧版）检查用户是否有编辑权限，等同于 is_project_contributor"""
    return await is_project_contributor(db, project_id, user_id)


async def is_project_member(
    db: AsyncSession,
    project_id: int,
    user_id: int,
) -> bool:
    """检查用户是否是项目成员"""
    relation = await get_project_member(db, project_id, user_id)
    return relation is not None


async def is_project_viewer(
    db: AsyncSession,
    project_id: int,
    user_id: int,
) -> bool:
    """检查用户是否有查看权限（最低级别）"""
    return await has_member_permission(db, project_id, user_id, RoleType.VIEWER)


async def batch_add_project_members(
    db: AsyncSession,
    project_id: int,
    members: List[dict],
) -> List[ProjectMember]:
    """批量添加项目成员"""
    relations = []
    for member in members:
        existing = await get_project_member(db, project_id, member["user_id"])
        if existing:
            existing.role = member.get("role", RoleType.VIEWER)
        else:
            relation = ProjectMember(
                project_id=project_id,
                user_id=member["user_id"],
                role=member.get("role", RoleType.VIEWER),
            )
            db.add(relation)
            relations.append(relation)

    await db.commit()
    for relation in relations:
        await db.refresh(relation)

    return relations
