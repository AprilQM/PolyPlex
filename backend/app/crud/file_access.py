"""
文件/项目访问权限 CRUD 操作
"""
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.groups import ProjectGroup, FileGroup
from typing import List


# ========== 项目权限 ==========

async def grant_project_access(
    db: AsyncSession,
    project_id: int,
    group_id: int,
) -> ProjectGroup:
    """赋予组对项目的访问权限"""
    existing = await db.execute(
        select(ProjectGroup)
        .where(ProjectGroup.project_id == project_id)
        .where(ProjectGroup.group_id == group_id)
    )
    if existing.scalar_one_or_none():
        raise ValueError("Group already has access to this project")

    pg = ProjectGroup(project_id=project_id, group_id=group_id)
    db.add(pg)
    await db.commit()
    await db.refresh(pg)
    return pg


async def revoke_project_access(db: AsyncSession, project_id: int, group_id: int) -> bool:
    """撤销组对项目的访问权限"""
    result = await db.execute(
        select(ProjectGroup)
        .where(ProjectGroup.project_id == project_id)
        .where(ProjectGroup.group_id == group_id)
    )
    pg = result.scalar_one_or_none()
    if not pg:
        return False
    await db.delete(pg)
    await db.commit()
    return True


async def get_project_groups(db: AsyncSession, project_id: int) -> List[ProjectGroup]:
    """获取有权访问项目的所有组"""
    result = await db.execute(
        select(ProjectGroup).where(ProjectGroup.project_id == project_id)
    )
    return list(result.scalars().all())


# ========== 文件权限 ==========

async def grant_file_access(
    db: AsyncSession,
    file_id: int,
    group_id: int,
) -> FileGroup:
    """赋予组对文件的访问权限"""
    existing = await db.execute(
        select(FileGroup)
        .where(FileGroup.file_id == file_id)
        .where(FileGroup.group_id == group_id)
    )
    if existing.scalar_one_or_none():
        raise ValueError("Group already has access to this file")

    fg = FileGroup(file_id=file_id, group_id=group_id)
    db.add(fg)
    await db.commit()
    await db.refresh(fg)
    return fg


async def revoke_file_access(db: AsyncSession, file_id: int, group_id: int) -> bool:
    """撤销组对文件的访问权限"""
    result = await db.execute(
        select(FileGroup)
        .where(FileGroup.file_id == file_id)
        .where(FileGroup.group_id == group_id)
    )
    fg = result.scalar_one_or_none()
    if not fg:
        return False
    await db.delete(fg)
    await db.commit()
    return True


async def get_file_groups(db: AsyncSession, file_id: int) -> List[FileGroup]:
    """获取有权访问文件的所有组"""
    result = await db.execute(
        select(FileGroup).where(FileGroup.file_id == file_id)
    )
    return list(result.scalars().all())
