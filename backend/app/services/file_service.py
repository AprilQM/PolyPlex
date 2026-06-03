import os
import hashlib
import uuid as uuid_lib
from pathlib import Path
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from fastapi import UploadFile, HTTPException

from app.crud.files import create_file, get_file_by_uuid
from app.models.files import File
from app.services.git_service import GitService
from app.core.git_config import get_worktree_path


class FileService:
    """文件统一管理服务"""

    UPLOAD_DIR = os.getenv("FILE_PATH", "./uploads")
    MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE", "50")) * 1024 * 1024
    FOLDER_FILE_LIMIT = int(os.getenv("FOLDER_FILE_LIMIT", "1000"))

    ALLOWED_EXTENSIONS = {
        '.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg', '.bmp', '.ico',
        '.pdf', '.doc', '.docx', '.txt', '.md',
        '.mp3', '.wav', '.flac', '.mp4', '.avi', '.mov',
        '.zip', '.rar', '.7z', '.tar', '.gz',
        '.py', '.js', '.ts', '.json', '.xml', '.html', '.css',
    }

    def __init__(self, db: AsyncSession):
        self.db = db
        self._ensure_upload_dir()

    def _ensure_upload_dir(self):
        Path(self.UPLOAD_DIR).mkdir(parents=True, exist_ok=True)

    async def _get_writable_folder(self) -> str:
        """获取可写入的文件夹 UUID（未达上限的最早文件夹），若无则新建"""
        result = await self.db.execute(
            select(File.folder_name, func.count(File.id))
            .where(File.is_deleted == False)
            .group_by(File.folder_name)
            .order_by(func.min(File.created_at))
        )
        rows = result.all()
        for folder_name, count in rows:
            if count < self.FOLDER_FILE_LIMIT:
                return folder_name

        # 所有文件夹都满了或没有文件夹，新建一个
        new_folder = str(uuid_lib.uuid4())
        Path(self.UPLOAD_DIR, new_folder).mkdir(parents=True, exist_ok=True)
        return new_folder

    async def _compute_hash(self, content: bytes) -> str:
        return hashlib.sha256(content).hexdigest()

    async def upload_file(
        self,
        file: UploadFile,
        uploader_id: int,
        target_type: Optional[str] = None,
        target_id: Optional[int] = None,
        file_hash: Optional[str] = None,
        allow_duplicate: bool = False,
        project_id: Optional[int] = None,
        repo_id: Optional[int] = None,
        git_path: Optional[str] = None,
    ) -> File:
        content = await file.read()
        file_size = len(content)

        if file_size > self.MAX_FILE_SIZE:
            raise HTTPException(413, f"File too large (max {self.MAX_FILE_SIZE // 1024 // 1024}MB)")

        filename = file.filename or "unnamed"
        ext = os.path.splitext(filename)[1].lower()
        if ext not in self.ALLOWED_EXTENSIONS:
            raise HTTPException(415, f"Unsupported file type: {ext}")

        # 哈希：前端传入或后端计算
        if not file_hash:
            file_hash = await self._compute_hash(content)

        # 去重
        if not allow_duplicate:
            from app.crud.files import get_file_by_hash
            existing = await get_file_by_hash(self.db, file_hash)
            if existing:
                return existing

        if repo_id is not None and git_path is not None:
            # Git 模式：写入 worktree 并 commit
            folder_name = f"git:{repo_id}"
            file_record = await create_file(
                db=self.db,
                filename=filename,
                file_size=file_size,
                file_type=file.content_type or "application/octet-stream",
                file_ext=ext,
                folder_name=folder_name,
                uploader_id=uploader_id,
                file_hash=file_hash,
                target_type=target_type or "component",
                target_id=target_id or repo_id,
                git_path=git_path,
            )
            # 写入 worktree 并 commit
            await GitService.commit_file(
                repo_id=repo_id,
                relative_path=git_path,
                content=content,
                message=f"Upload {filename} via PolyPlex",
            )
        else:
            # 传统模式：UUID 文件夹存储
            folder_name = await self._get_writable_folder()

            file_record = await create_file(
                db=self.db,
                filename=filename,
                file_size=file_size,
                file_type=file.content_type or "application/octet-stream",
                file_ext=ext,
                folder_name=folder_name,
                uploader_id=uploader_id,
                file_hash=file_hash,
                target_type=target_type,
                target_id=target_id,
            )

            # 写入磁盘：{UPLOAD_DIR}/{folder_name}/{uuid}
            disk_path = Path(self.UPLOAD_DIR, folder_name, str(file_record.uuid))
            with open(disk_path, "wb") as f:
                f.write(content)

        return file_record

    async def get_file_by_uuid(self, uuid: str) -> Optional[File]:
        return await get_file_by_uuid(self.db, uuid)

    async def get_file_content(self, file_record: File) -> Optional[bytes]:
        # Git 模式：从 worktree 读取
        if file_record.git_path and file_record.folder_name.startswith("git:"):
            try:
                repo_id = int(file_record.folder_name.split(":", 1)[1])
                worktree_path = get_worktree_path(repo_id)
                file_path = worktree_path / file_record.git_path
                if file_path.exists():
                    return file_path.read_bytes()
            except (ValueError, IndexError, OSError):
                pass
            return None

        # 传统模式：从 UUID 文件夹读取
        disk_path = Path(self.UPLOAD_DIR, file_record.folder_name, str(file_record.uuid))
        if not disk_path.exists():
            return None
        with open(disk_path, "rb") as f:
            return f.read()

    async def delete_file(self, file_id: int) -> bool:
        from app.crud.files import delete_file as crud_delete, get_file
        file_record = await get_file(self.db, file_id)
        if not file_record:
            return False

        # 如果是 Git 管理的文件，也从 Git 仓库删除
        if file_record.git_path and file_record.folder_name.startswith("git:"):
            try:
                repo_id = int(file_record.folder_name.split(":", 1)[1])
                await GitService.commit_delete(
                    repo_id=repo_id,
                    relative_path=file_record.git_path,
                    message=f"Delete {file_record.filename} via PolyPlex",
                )
            except (ValueError, IndexError):
                pass

        return await crud_delete(self.db, file_id)

    async def batch_upload(
        self,
        files: List[UploadFile],
        uploader_id: int,
        target_type: Optional[str] = None,
        target_id: Optional[int] = None,
    ) -> List[File]:
        results = []
        for f in files:
            record = await self.upload_file(
                file=f,
                uploader_id=uploader_id,
                target_type=target_type,
                target_id=target_id,
            )
            results.append(record)
        return results
