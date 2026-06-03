"""
文件 CRUD 操作
"""
from sqlalchemy import select, desc, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.files import File
from typing import Optional, List


# ========== File CRUD ==========

async def get_file(db: AsyncSession, file_id: int) -> Optional[File]:
    """根据 ID 获取文件"""
    result = await db.execute(select(File).where(File.id == file_id))
    return result.scalar_one_or_none()


async def get_file_by_uuid(db: AsyncSession, uuid: str) -> Optional[File]:
    """根据 UUID 获取文件"""
    result = await db.execute(select(File).where(File.uuid == uuid))
    return result.scalar_one_or_none()


async def get_file_by_hash(db: AsyncSession, file_hash: str) -> Optional[File]:
    """根据哈希值获取文件（用于去重）"""
    result = await db.execute(select(File).where(File.file_hash == file_hash))
    return result.scalar_one_or_none()


async def create_file(
    db: AsyncSession,
    filename: str,
    file_size: int,
    file_type: str,
    file_ext: str,
    folder_name: str,
    uploader_id: int,
    file_hash: Optional[str] = None,
    target_type: Optional[str] = None,
    target_id: Optional[int] = None,
    git_path: Optional[str] = None,
) -> File:
    """创建文件记录"""
    file = File(
        filename=filename,
        file_size=file_size,
        file_type=file_type,
        file_ext=file_ext,
        file_hash=file_hash,
        folder_name=folder_name,
        uploader_id=uploader_id,
        target_type=target_type,
        target_id=target_id,
        git_path=git_path,
    )
    db.add(file)
    await db.commit()
    await db.refresh(file)
    return file


async def delete_file(db: AsyncSession, file_id: int) -> bool:
    """删除文件（软删除）"""
    import time
    file = await get_file(db, file_id)
    if not file:
        return False

    file.is_deleted = True
    file.deleted_at = int(time.time())

    await db.commit()
    return True


async def hard_delete_file(db: AsyncSession, file_id: int) -> bool:
    """彻底删除文件记录"""
    file = await get_file(db, file_id)
    if not file:
        return False

    await db.delete(file)
    await db.commit()
    return True


async def restore_file(db: AsyncSession, file_id: int) -> bool:
    """恢复已删除的文件"""
    file = await get_file(db, file_id)
    if not file:
        return False

    file.is_deleted = False
    file.deleted_at = None

    await db.commit()
    return True


async def get_user_files(
    db: AsyncSession,
    uploader_id: int,
    page: int = 1,
    page_size: int = 20,
    include_deleted: bool = False,
) -> List[File]:
    """获取用户的文件列表"""
    query = select(File).where(File.uploader_id == uploader_id)

    if not include_deleted:
        query = query.where(File.is_deleted == False)

    query = query.order_by(desc(File.created_at))
    query = query.offset((page - 1) * page_size).limit(page_size)

    result = await db.execute(query)
    return list(result.scalars().all())


async def count_user_files(
    db: AsyncSession,
    uploader_id: int,
    include_deleted: bool = False,
) -> int:
    """统计用户的文件数量"""
    query = select(func.count(File.id)).where(File.uploader_id == uploader_id)

    if not include_deleted:
        query = query.where(File.is_deleted == False)

    result = await db.execute(query)
    return result.scalar()


async def get_user_storage_size(
    db: AsyncSession,
    uploader_id: int,
) -> int:
    """获取用户存储空间使用量（字节）"""
    result = await db.execute(
        select(func.sum(File.file_size))
        .where(File.uploader_id == uploader_id)
        .where(File.is_deleted == False)
    )
    total = result.scalar()
    return total or 0


async def get_duplicate_file(
    db: AsyncSession,
    file_hash: str,
) -> Optional[File]:
    """查找已存在的相同文件（用于秒传）"""
    result = await db.execute(
        select(File)
        .where(File.file_hash == file_hash)
        .where(File.is_deleted == False)
    )
    return result.scalar_one_or_none()


async def get_files_by_type(
    db: AsyncSession,
    file_type: str,
    page: int = 1,
    page_size: int = 20,
) -> List[File]:
    """根据文件类型获取文件"""
    query = (
        select(File)
        .where(File.file_type == file_type)
        .where(File.is_deleted == False)
        .order_by(desc(File.created_at))
        .offset((page - 1) * page_size)
        .limit(page_size)
    )

    result = await db.execute(query)
    return list(result.scalars().all())


async def batch_delete_files(
    db: AsyncSession,
    file_ids: List[int],
    uploader_id: Optional[int] = None,
) -> int:
    """批量删除文件

    Args:
        file_ids: 文件 ID 列表
        uploader_id: 可选，限制只能删除指定上传者的文件

    Returns:
        成功删除的文件数量
    """
    import time
    query = (
        update(File)
        .where(File.id.in_(file_ids))
        .values(is_deleted=True, deleted_at=int(time.time()))
    )

    if uploader_id is not None:
        query = query.where(File.uploader_id == uploader_id)

    result = await db.execute(query)
    await db.commit()

    return result.rowcount
