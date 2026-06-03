"""
项目相关 CRUD 操作
"""
from sqlalchemy import select, desc, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.projects import Project, ProjectTag, ProjectTagRelation, ProjectType
from typing import Optional, List


# ========== Project CRUD ==========

async def get_project(db: AsyncSession, project_id: int) -> Optional[Project]:
    """根据 ID 获取项目"""
    result = await db.execute(select(Project).where(Project.id == project_id))
    return result.scalar_one_or_none()


async def get_project_by_name(db: AsyncSession, name: str) -> Optional[Project]:
    """根据名称获取项目"""
    result = await db.execute(select(Project).where(Project.name == name))
    return result.scalar_one_or_none()


async def create_project(
    db: AsyncSession,
    name: str,
    owner_id: int,
    description: Optional[str] = None,
    project_type: ProjectType = ProjectType.OTHER,
    is_private: bool = False,
    cover_image_uuid: Optional[str] = None,
) -> Project:
    """创建新项目"""
    project = Project(
        name=name,
        description=description,
        owner_id=owner_id,
        project_type=project_type,
        is_private=is_private,
        cover_image=cover_image_uuid,
    )
    db.add(project)
    await db.commit()
    await db.refresh(project)
    return project


async def update_project(
    db: AsyncSession,
    project_id: int,
    name: Optional[str] = None,
    description: Optional[str] = None,
    project_type: Optional[ProjectType] = None,
    is_private: Optional[bool] = None,
    is_started: Optional[bool] = None,
    cover_image_uuid: Optional[str] = None,
) -> Optional[Project]:
    """更新项目信息"""
    project = await get_project(db, project_id)
    if not project:
        return None

    if name is not None:
        project.name = name
    if description is not None:
        project.description = description
    if project_type is not None:
        project.project_type = project_type
    if is_private is not None:
        project.is_private = is_private
    if is_started is not None:
        project.is_started = is_started
    if cover_image_uuid is not None:
        project.cover_image = cover_image_uuid

    await db.commit()
    await db.refresh(project)
    return project


async def delete_project(db: AsyncSession, project_id: int) -> bool:
    """删除项目"""
    project = await get_project(db, project_id)
    if not project:
        return False

    await db.delete(project)
    await db.commit()
    return True


async def start_project(db: AsyncSession, project_id: int) -> Optional[Project]:
    """启动项目"""
    return await update_project(db, project_id, is_started=True)


async def close_project(db: AsyncSession, project_id: int) -> Optional[Project]:
    """关闭项目"""
    return await update_project(db, project_id, is_started=False)


async def get_project_list(
    db: AsyncSession,
    page: int = 1,
    page_size: int = 20,
    owner_id: Optional[int] = None,
    project_type: Optional[ProjectType] = None,
    is_private: Optional[bool] = None,
    is_started: Optional[bool] = None,
) -> List[Project]:
    """获取项目列表（分页）"""
    query = select(Project)

    if owner_id is not None:
        query = query.where(Project.owner_id == owner_id)
    if project_type is not None:
        query = query.where(Project.project_type == project_type)
    if is_private is not None:
        query = query.where(Project.is_private == is_private)
    if is_started is not None:
        query = query.where(Project.is_started == is_started)

    query = query.order_by(desc(Project.created_at))
    query = query.offset((page - 1) * page_size).limit(page_size)

    result = await db.execute(query)
    return list(result.scalars().all())


async def count_projects(
    db: AsyncSession,
    owner_id: Optional[int] = None,
    project_type: Optional[ProjectType] = None,
    is_private: Optional[bool] = None,
    is_started: Optional[bool] = None,
) -> int:
    """统计项目数量"""
    query = select(func.count(Project.id))

    if owner_id is not None:
        query = query.where(Project.owner_id == owner_id)
    if project_type is not None:
        query = query.where(Project.project_type == project_type)
    if is_private is not None:
        query = query.where(Project.is_private == is_private)
    if is_started is not None:
        query = query.where(Project.is_started == is_started)

    result = await db.execute(query)
    return result.scalar()


# ========== ProjectTag CRUD ==========

async def get_project_tag(db: AsyncSession, tag_id: int) -> Optional[ProjectTag]:
    """根据 ID 获取项目标签"""
    result = await db.execute(select(ProjectTag).where(ProjectTag.id == tag_id))
    return result.scalar_one_or_none()


async def get_project_tag_by_name(db: AsyncSession, name: str) -> Optional[ProjectTag]:
    """根据名称获取项目标签"""
    result = await db.execute(select(ProjectTag).where(ProjectTag.name == name))
    return result.scalar_one_or_none()


async def create_project_tag(
    db: AsyncSession,
    name: str,
    background_color: str = "#808080",
    text_color: str = "#ffffff",
) -> ProjectTag:
    """创建项目标签"""
    tag = ProjectTag(
        name=name,
        background_color=background_color,
        text_color=text_color,
    )
    db.add(tag)
    await db.commit()
    await db.refresh(tag)
    return tag


async def update_project_tag(
    db: AsyncSession,
    tag_id: int,
    name: Optional[str] = None,
    background_color: Optional[str] = None,
    text_color: Optional[str] = None,
) -> Optional[ProjectTag]:
    """更新项目标签"""
    tag = await get_project_tag(db, tag_id)
    if not tag:
        return None

    if name is not None:
        tag.name = name
    if background_color is not None:
        tag.background_color = background_color
    if text_color is not None:
        tag.text_color = text_color

    await db.commit()
    await db.refresh(tag)
    return tag


async def delete_project_tag(db: AsyncSession, tag_id: int) -> bool:
    """删除项目标签"""
    tag = await get_project_tag(db, tag_id)
    if not tag:
        return False

    await db.delete(tag)
    await db.commit()
    return True


async def get_all_project_tags(db: AsyncSession) -> List[ProjectTag]:
    """获取所有项目标签"""
    result = await db.execute(select(ProjectTag).order_by(ProjectTag.created_at))
    return list(result.scalars().all())


# ========== ProjectTagRelation CRUD ==========

async def get_project_tag_relation(
    db: AsyncSession,
    project_id: int,
    tag_id: int
) -> Optional[ProjectTagRelation]:
    """获取项目标签关系"""
    result = await db.execute(
        select(ProjectTagRelation)
        .where(ProjectTagRelation.project_id == project_id)
        .where(ProjectTagRelation.tag_id == tag_id)
    )
    return result.scalar_one_or_none()


async def add_project_tag(
    db: AsyncSession,
    project_id: int,
    tag_id: int,
) -> ProjectTagRelation:
    """给项目添加标签"""
    relation = ProjectTagRelation(project_id=project_id, tag_id=tag_id)
    db.add(relation)
    await db.commit()
    await db.refresh(relation)
    return relation


async def remove_project_tag(
    db: AsyncSession,
    project_id: int,
    tag_id: int,
) -> bool:
    """移除项目标签"""
    relation = await get_project_tag_relation(db, project_id, tag_id)
    if not relation:
        return False

    await db.delete(relation)
    await db.commit()
    return True


async def get_project_tags(db: AsyncSession, project_id: int) -> List[ProjectTag]:
    """获取项目的所有标签"""
    result = await db.execute(
        select(ProjectTag)
        .join(ProjectTagRelation)
        .where(ProjectTagRelation.project_id == project_id)
    )
    return list(result.scalars().all())


async def get_tag_projects(db: AsyncSession, tag_id: int) -> List[Project]:
    """获取标签下的所有项目"""
    result = await db.execute(
        select(Project)
        .join(ProjectTagRelation)
        .where(ProjectTagRelation.tag_id == tag_id)
    )
    return list(result.scalars().all())


async def batch_add_project_tags(
    db: AsyncSession,
    project_id: int,
    tag_ids: List[int],
) -> List[ProjectTagRelation]:
    """批量给项目添加标签"""
    relations = []
    for tag_id in tag_ids:
        existing = await get_project_tag_relation(db, project_id, tag_id)
        if not existing:
            relation = ProjectTagRelation(project_id=project_id, tag_id=tag_id)
            db.add(relation)
            relations.append(relation)

    if relations:
        await db.commit()
        for relation in relations:
            await db.refresh(relation)

    return relations


async def sync_project_tags(
    db: AsyncSession,
    project_id: int,
    tag_ids: List[int],
) -> List[ProjectTag]:
    """同步项目标签（替换所有标签）"""
    await db.execute(
        ProjectTagRelation.__table__.delete()
        .where(ProjectTagRelation.project_id == project_id)
    )

    for tag_id in tag_ids:
        relation = ProjectTagRelation(project_id=project_id, tag_id=tag_id)
        db.add(relation)

    await db.commit()

    return await get_project_tags(db, project_id)
