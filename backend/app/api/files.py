"""文件 API 路由"""
import uuid
from typing import Optional
from fastapi import APIRouter, Depends, UploadFile, File as FileForm, Form, HTTPException, Query, Body, Header
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import Response

from app.core.database import get_db
from app.api.deps import get_current_user_id
from app.services.file_service import FileService
from app.services.file_access_service import check_file_access
from app.crud.files import get_file_by_uuid, get_user_files, count_user_files

router = APIRouter(prefix="/api/files", tags=["files"])


@router.post("/upload")
async def upload_file(
    file: UploadFile = FileForm(...),
    target_type: Optional[str] = Form(None),
    target_id: Optional[int] = Form(None),
    project_id: Optional[int] = Form(None),
    repo_id: Optional[int] = Form(None),
    git_path: Optional[str] = Form(None),
    x_file_hash: Optional[str] = Header(None),
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    svc = FileService(db)
    record = await svc.upload_file(
        file=file,
        uploader_id=user_id,
        target_type=target_type,
        target_id=target_id,
        file_hash=x_file_hash,
        project_id=project_id,
        repo_id=repo_id,
        git_path=git_path,
    )
    return {
        "uuid": record.uuid,
        "filename": record.filename,
        "file_size": record.file_size,
        "file_type": record.file_type,
        "file_ext": record.file_ext,
    }


@router.get("/{file_uuid}")
async def get_file_meta(
    file_uuid: str,
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    record = await get_file_by_uuid(db, file_uuid)
    if not record or record.is_deleted:
        raise HTTPException(404, "File not found")
    if not await check_file_access(db, record, user_id):
        raise HTTPException(403, "Access denied")
    return {
        "uuid": record.uuid,
        "filename": record.filename,
        "file_size": record.file_size,
        "file_type": record.file_type,
        "file_ext": record.file_ext,
        "uploader_id": record.uploader_id,
        "target_type": record.target_type,
        "target_id": record.target_id,
        "created_at": record.created_at,
    }


@router.get("/{file_uuid}/download")
async def download_file(
    file_uuid: str,
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    svc = FileService(db)
    record = await svc.get_file_by_uuid(file_uuid)
    if not record or record.is_deleted:
        raise HTTPException(404, "File not found")
    if not await check_file_access(db, record, user_id):
        raise HTTPException(403, "Access denied")

    content = await svc.get_file_content(record)
    if content is None:
        raise HTTPException(404, "File content not found on disk")

    return Response(
        content=content,
        media_type=record.file_type,
        headers={
            "Content-Disposition": f'attachment; filename="{record.filename}"'
        },
    )


@router.get("")
async def list_files(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    file_type: Optional[str] = Query(None),
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    if file_type:
        from app.crud.files import get_files_by_type
        files = await get_files_by_type(db, file_type, page, page_size)
        total = len(files)
    else:
        files = await get_user_files(db, user_id, page, page_size)
        total = await count_user_files(db, user_id)

    return {
        "items": [
            {
                "uuid": f.uuid,
                "filename": f.filename,
                "file_size": f.file_size,
                "file_type": f.file_type,
                "file_ext": f.file_ext,
                "target_type": f.target_type,
                "target_id": f.target_id,
                "folder_name": f.folder_name,
                "created_at": f.created_at,
            }
            for f in files
        ],
        "total": total,
        "page": page,
        "page_size": page_size,
    }


@router.delete("/{file_uuid}")
async def delete_file_route(
    file_uuid: str,
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    svc = FileService(db)
    record = await svc.get_file_by_uuid(file_uuid)
    if not record or record.is_deleted:
        raise HTTPException(404, "File not found")
    if record.uploader_id != user_id:
        raise HTTPException(403, "Only the uploader can delete this file")
    await svc.delete_file(record.id)
    return {"message": "File deleted"}


@router.put("/{file_uuid}/restore")
async def restore_file_route(
    file_uuid: str,
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    record = await get_file_by_uuid(db, file_uuid)
    if not record:
        raise HTTPException(404, "File not found")
    if record.uploader_id != user_id:
        raise HTTPException(403, "Only the uploader can restore this file")
    from app.crud.files import restore_file as crud_restore
    await crud_restore(db, record.id)
    return {"message": "File restored"}


@router.put("/{file_uuid}")
async def update_file_meta(
    file_uuid: str,
    target_type: Optional[str] = Body(None),
    target_id: Optional[int] = Body(None),
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    record = await get_file_by_uuid(db, file_uuid)
    if not record or record.is_deleted:
        raise HTTPException(404, "File not found")
    if record.uploader_id != user_id:
        raise HTTPException(403, "Only the uploader can update this file")
    if target_type is not None:
        record.target_type = target_type
    if target_id is not None:
        record.target_id = target_id
    await db.commit()
    return {"message": "File updated"}


@router.post("/batch-delete")
async def batch_delete_files(
    uuids: list[str],
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    from app.crud.files import batch_delete_files as crud_batch_delete
    from sqlalchemy import select
    from app.models.files import File
    result = await db.execute(
        select(File.id).where(File.uuid.in_(uuids)).where(File.uploader_id == user_id)
    )
    file_ids = list(result.scalars().all())
    if not file_ids:
        raise HTTPException(404, "No files found")
    count = await crud_batch_delete(db, file_ids, uploader_id=user_id)
    return {"deleted_count": count}
