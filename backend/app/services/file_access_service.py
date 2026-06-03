"""
文件访问权限服务 — 5 步访问判断
"""
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.files import File
from app.models.groups import FileGroup, ProjectGroup


async def check_file_access(
    db: AsyncSession,
    file: File,
    user_id: int,
) -> bool:
    """检查用户是否有权访问文件（5 步判断）"""
    # 1. 上传者直接通过
    if file.uploader_id == user_id:
        return True

    # 2. admin 组直接通过
    from app.crud.group_user_relations import is_user_admin
    if await is_user_admin(db, user_id):
        return True

    # 3. 查 FileGroup：用户的组被直接授权
    from app.crud.group_user_relations import get_user_group_ids
    user_group_ids = await get_user_group_ids(db, user_id)
    if user_group_ids:
        fg_result = await db.execute(
            select(FileGroup)
            .where(FileGroup.file_id == file.id)
            .where(FileGroup.group_id.in_(user_group_ids))
        )
        if fg_result.scalar_one_or_none():
            return True

    # 4. 通过 file.target 查 ProjectGroup
    if file.target_type == "project" and file.target_id and user_group_ids:
        pg_result = await db.execute(
            select(ProjectGroup)
            .where(ProjectGroup.project_id == file.target_id)
            .where(ProjectGroup.group_id.in_(user_group_ids))
        )
        if pg_result.scalar_one_or_none():
            return True

    # 5. 拒绝
    return False
