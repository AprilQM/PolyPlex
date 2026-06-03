"""
文件包 CRUD 操作
"""
import os
import zipfile
import tempfile
import shutil
from pathlib import Path
from sqlalchemy import select, desc, func, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from app.models.files import FilePackage, FilePackageRelation
from app.models.files import File
from app.crud.files import create_file, get_file_by_uuid
from typing import Optional, List
import time


# ========== FilePackage CRUD ==========

async def get_file_package(db: AsyncSession, package_id: int) -> Optional[FilePackage]:
    """根据 ID 获取文件包"""
    result = await db.execute(select(FilePackage).where(FilePackage.id == package_id))
    return result.scalar_one_or_none()


async def create_file_package(
    db: AsyncSession,
    name: str,
    created_by: int,
    project_id: Optional[int] = None,
    page_id: Optional[int] = None,
    description: Optional[str] = None,
) -> FilePackage:
    """创建文件包"""
    package = FilePackage(
        name=name,
        description=description,
        project_id=project_id,
        page_id=page_id,
        created_by=created_by,
        file_count=0,
        total_size=0,
    )
    db.add(package)
    await db.commit()
    await db.refresh(package)
    return package


async def update_file_package(
    db: AsyncSession,
    package_id: int,
    name: Optional[str] = None,
    description: Optional[str] = None,
) -> Optional[FilePackage]:
    """更新文件包"""
    package = await get_file_package(db, package_id)
    if not package:
        return None

    if name is not None:
        package.name = name
    if description is not None:
        package.description = description

    await db.commit()
    await db.refresh(package)
    return package


async def delete_file_package(db: AsyncSession, package_id: int) -> bool:
    """删除文件包（不删除文件本身）"""
    package = await get_file_package(db, package_id)
    if not package:
        return False

    await db.delete(package)
    await db.commit()
    return True


async def get_project_packages(
    db: AsyncSession,
    project_id: int,
    page: int = 1,
    page_size: int = 20,
) -> List[FilePackage]:
    """获取项目的所有文件包"""
    query = (
        select(FilePackage)
        .where(FilePackage.project_id == project_id)
        .order_by(desc(FilePackage.created_at))
        .offset((page - 1) * page_size)
        .limit(page_size)
    )
    result = await db.execute(query)
    return list(result.scalars().all())


async def get_page_packages(
    db: AsyncSession,
    page_id: int,
) -> List[FilePackage]:
    """获取页面的所有文件包"""
    result = await db.execute(
        select(FilePackage)
        .where(FilePackage.page_id == page_id)
        .order_by(FilePackage.created_at)
    )
    return list(result.scalars().all())


# ========== FilePackageRelation CRUD ==========

async def add_file_to_package(
    db: AsyncSession,
    package_id: int,
    file_id: int,
    file_path: Optional[str] = None,
    display_name: Optional[str] = None,
    order_index: int = 0,
) -> FilePackageRelation:
    """添加文件到文件包"""
    relation = FilePackageRelation(
        package_id=package_id,
        file_id=file_id,
        file_path=file_path,
        display_name=display_name,
        order_index=order_index,
    )
    db.add(relation)

    # 更新文件包统计
    await _update_package_stats(db, package_id)

    await db.commit()
    await db.refresh(relation)
    return relation


async def remove_file_from_package(
    db: AsyncSession,
    package_id: int,
    file_id: int,
) -> bool:
    """从文件包移除文件（不删除文件本身）"""
    result = await db.execute(
        select(FilePackageRelation)
        .where(FilePackageRelation.package_id == package_id)
        .where(FilePackageRelation.file_id == file_id)
    )
    relation = result.scalar_one_or_none()

    if not relation:
        return False

    await db.delete(relation)

    # 更新文件包统计
    await _update_package_stats(db, package_id)

    await db.commit()
    return True


async def get_package_files(
    db: AsyncSession,
    package_id: int,
) -> List[dict]:
    """获取文件包的所有文件"""
    result = await db.execute(
        select(FilePackageRelation, File)
        .join(File, FilePackageRelation.file_id == File.id)
        .where(FilePackageRelation.package_id == package_id)
        .order_by(FilePackageRelation.order_index)
    )

    relations = result.all()
    return [
        {
            "relation_id": rel.id,
            "file_id": file.id,
            "uuid": file.uuid,
            "filename": file.filename,
            "file_type": file.file_type,
            "file_size": file.file_size,
            "file_path": rel.file_path,
            "display_name": rel.display_name or file.filename,
            "order_index": rel.order_index,
        }
        for rel, file in relations
    ]


async def batch_add_files_to_package(
    db: AsyncSession,
    package_id: int,
    file_ids: List[int],
    created_by: int,
) -> List[FilePackageRelation]:
    """批量添加文件到文件包"""
    relations = []

    # 获取当前最大 order_index
    max_order_result = await db.execute(
        select(func.max(FilePackageRelation.order_index))
        .where(FilePackageRelation.package_id == package_id)
    )
    max_order = max_order_result.scalar() or -1

    for idx, file_id in enumerate(file_ids):
        relation = FilePackageRelation(
            package_id=package_id,
            file_id=file_id,
            order_index=max_order + idx + 1,
        )
        db.add(relation)
        relations.append(relation)

    # 更新文件包统计
    await _update_package_stats(db, package_id)

    await db.commit()
    for relation in relations:
        await db.refresh(relation)

    return relations


async def _update_package_stats(db: AsyncSession, package_id: int):
    """更新文件包的文件数量和总大小"""
    result = await db.execute(
        select(func.count(FilePackageRelation.file_id), func.sum(File.file_size))
        .join(File, FilePackageRelation.file_id == File.id)
        .where(FilePackageRelation.package_id == package_id)
    )
    row = result.first()
    file_count = row[0] or 0
    total_size = row[1] or 0

    await db.execute(
        update(FilePackage)
        .where(FilePackage.id == package_id)
        .values(file_count=file_count, total_size=total_size)
    )


# ========== 压缩包处理 ==========

def extract_zip_package(
    zip_path: str,
    uploader_id: int,
    sync_db_session: Session,
) -> List[int]:
    """
    解压 ZIP 文件并创建文件记录

    Args:
        zip_path: ZIP 文件路径
        uploader_id: 上传者 ID
        sync_db_session: 同步数据库会话

    Returns:
        创建的文件 ID 列表
    """
    file_ids = []
    temp_dir = tempfile.mkdtemp()

    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)

        # 遍历解压后的文件
        for root, dirs, files in os.walk(temp_dir):
            for filename in files:
                file_path = os.path.join(root, filename)

                # 跳过隐藏文件
                if filename.startswith('.'):
                    continue

                # 计算文件相对路径
                rel_path = os.path.relpath(file_path, temp_dir)

                # 创建文件记录
                file_record = create_file_record_from_path(
                    file_path=file_path,
                    uploader_id=uploader_id,
                    sync_db_session=sync_db_session,
                )
                if file_record:
                    file_ids.append(file_record.id)

    finally:
        # 清理临时目录
        shutil.rmtree(temp_dir)

    return file_ids


def create_file_record_from_path(
    file_path: str,
    uploader_id: int,
    sync_db_session: Session,
) -> Optional[File]:
    """从文件路径创建文件记录"""
    import hashlib
    from datetime import datetime

    try:
        # 读取文件内容
        with open(file_path, 'rb') as f:
            content = f.read()

        # 计算文件哈希
        file_hash = hashlib.sha256(content).hexdigest()

        # 获取文件信息
        file_size = len(content)
        filename = os.path.basename(file_path)
        file_ext = os.path.splitext(filename)[1].lower()

        # 猜测 MIME 类型
        mime_types = {
            '.pdf': 'application/pdf',
            '.doc': 'application/msword',
            '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            '.xls': 'application/vnd.ms-excel',
            '.xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            '.ppt': 'application/vnd.ms-powerpoint',
            '.pptx': 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
            '.txt': 'text/plain',
            '.md': 'text/markdown',
            '.py': 'text/x-python',
            '.js': 'application/javascript',
            '.ts': 'application/typescript',
            '.java': 'text/x-java',
            '.c': 'text/x-c',
            '.cpp': 'text/x-c++',
            '.go': 'text/x-go',
            '.rs': 'text/x-rust',
            '.rb': 'text/x-ruby',
            '.php': 'application/x-php',
            '.html': 'text/html',
            '.css': 'text/css',
            '.json': 'application/json',
            '.xml': 'application/xml',
            '.yaml': 'application/x-yaml',
            '.yml': 'application/x-yaml',
            '.png': 'image/png',
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.gif': 'image/gif',
            '.svg': 'image/svg+xml',
            '.webp': 'image/webp',
            '.mp3': 'audio/mpeg',
            '.wav': 'audio/wav',
            '.mp4': 'video/mp4',
            '.avi': 'video/x-msvideo',
            '.zip': 'application/zip',
            '.rar': 'application/vnd.rar',
            '.7z': 'application/x-7z-compressed',
            '.tar': 'application/x-tar',
            '.gz': 'application/gzip',
        }
        file_type = mime_types.get(file_ext, 'application/octet-stream')

        # 生成存储路径（按日期分目录）
        now = datetime.now()
        storage_dir = f"files/{now.year}/{now.month:02d}/{now.day:02d}"
        os.makedirs(storage_dir, exist_ok=True)

        # 使用 UUID 作为文件名
        import uuid
        file_uuid = str(uuid.uuid4())
        storage_path = os.path.join(storage_dir, f"{file_uuid}{file_ext}")

        # 保存文件到磁盘
        with open(storage_path, 'wb') as f:
            f.write(content)

        # 创建数据库记录
        file_record = File(
            filename=filename,
            file_size=file_size,
            file_type=file_type,
            file_ext=file_ext,
            file_hash=file_hash,
            storage_path=storage_path,
            uploader_id=uploader_id,
            uuid=file_uuid,
        )
        sync_db_session.add(file_record)
        sync_db_session.commit()
        sync_db_session.refresh(file_record)

        return file_record

    except Exception as e:
        print(f"创建文件记录失败：{e}")
        return None


def create_zip_from_package(
    package_id: int,
    output_path: str,
    sync_db_session: Session,
) -> int:
    """
    从文件包创建 ZIP 压缩包

    Args:
        package_id: 文件包 ID
        output_path: 输出 ZIP 路径
        sync_db_session: 同步数据库会话

    Returns:
        打包的文件数量
    """
    # 获取文件包的所有文件
    result = sync_db_session.execute(
        select(FilePackageRelation, File)
        .join(File, FilePackageRelation.file_id == File.id)
        .where(FilePackageRelation.package_id == package_id)
        .where(File.is_deleted == False)
        .order_by(FilePackageRelation.order_index)
    )
    relations = result.all()

    if not relations:
        return 0

    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for rel, file in relations:
            try:
                # 读取文件内容
                with open(file.storage_path, 'rb') as f:
                    content = f.read()

                # 确定 ZIP 内的文件名
                arcname = rel.file_path or rel.display_name or file.filename

                # 写入 ZIP
                zipf.writestr(arcname, content)

            except Exception as e:
                print(f"打包文件失败 {file.uuid}: {e}")
                continue

    return len(relations)
