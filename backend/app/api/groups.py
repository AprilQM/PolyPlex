"""用户组 API 路由"""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.api.deps import get_current_user, require_active_user
from app.crud.groups import (
    get_group, get_group_by_name, create_group, update_group, delete_group,
    get_user_groups, get_all_groups,
)
from app.crud.group_user_relations import (
    add_member, remove_member, update_member_role, get_group_members,
    is_user_in_group,
)
from app.crud.file_access import (
    grant_project_access, revoke_project_access,
    grant_file_access, revoke_file_access,
)
from app.models.groups import GroupType, GroupRole
from app.models.files import File
from sqlalchemy import select

router = APIRouter(prefix="/api/groups", tags=["groups"])


@router.post("")
async def create_group_route(
    name: str,
    description: Optional[str] = None,
    current_user: dict = Depends(require_active_user),
    db: AsyncSession = Depends(get_db),
):
    user_id = current_user["id"]
    existing = await get_group_by_name(db, name)
    if existing:
        raise HTTPException(409, "Group name already exists")
    group = await create_group(db, name=name, description=description)
    return {"id": group.id, "name": group.name, "group_type": group.group_type.value}


@router.get("")
async def list_groups(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    user_id = current_user["id"]
    groups = await get_user_groups(db, user_id)
    return {
        "items": [
            {"id": g.id, "name": g.name, "group_type": g.group_type.value}
            for g in groups
        ],
        "total": len(groups),
    }


@router.get("/{group_id}")
async def get_group_route(
    group_id: int,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    group = await get_group(db, group_id)
    if not group:
        raise HTTPException(404, "Group not found")
    members = await get_group_members(db, group_id, page=1, page_size=100)
    return {
        "id": group.id,
        "name": group.name,
        "description": group.description,
        "group_type": group.group_type.value,
        "members": members,
        "created_at": group.created_at,
    }


@router.put("/{group_id}")
async def update_group_route(
    group_id: int,
    name: Optional[str] = None,
    description: Optional[str] = None,
    current_user: dict = Depends(require_active_user),
    db: AsyncSession = Depends(get_db),
):
    group = await update_group(db, group_id, name=name, description=description)
    if not group:
        raise HTTPException(404, "Group not found or is a system group")
    return {"id": group.id, "name": group.name}


@router.delete("/{group_id}")
async def delete_group_route(
    group_id: int,
    current_user: dict = Depends(require_active_user),
    db: AsyncSession = Depends(get_db),
):
    success = await delete_group(db, group_id)
    if not success:
        raise HTTPException(404, "Group not found or is a system group")
    return {"message": "Group deleted"}


@router.post("/{group_id}/members")
async def add_member_route(
    group_id: int,
    member_user_id: int,
    role: str = "member",
    current_user: dict = Depends(require_active_user),
    db: AsyncSession = Depends(get_db),
):
    group = await get_group(db, group_id)
    if not group:
        raise HTTPException(404, "Group not found")
    try:
        relation = await add_member(db, group_id, member_user_id, GroupRole(role))
        return {"relation_id": relation.id, "user_id": member_user_id, "role": role}
    except ValueError as e:
        raise HTTPException(409, str(e))


@router.delete("/{group_id}/members/{member_user_id}")
async def remove_member_route(
    group_id: int,
    member_user_id: int,
    current_user: dict = Depends(require_active_user),
    db: AsyncSession = Depends(get_db),
):
    success = await remove_member(db, group_id, member_user_id)
    if not success:
        raise HTTPException(404, "Member not found in group")
    return {"message": "Member removed"}


@router.put("/{group_id}/members/{member_user_id}")
async def update_member_role_route(
    group_id: int,
    member_user_id: int,
    role: str,
    current_user: dict = Depends(require_active_user),
    db: AsyncSession = Depends(get_db),
):
    relation = await update_member_role(db, group_id, member_user_id, GroupRole(role))
    if not relation:
        raise HTTPException(404, "Member not found in group")
    return {"relation_id": relation.id, "role": role}


@router.post("/{group_id}/projects/{project_id}")
async def grant_project_route(
    group_id: int,
    project_id: int,
    current_user: dict = Depends(require_active_user),
    db: AsyncSession = Depends(get_db),
):
    try:
        pg = await grant_project_access(db, project_id, group_id)
        return {"id": pg.id}
    except ValueError as e:
        raise HTTPException(409, str(e))


@router.delete("/{group_id}/projects/{project_id}")
async def revoke_project_route(
    group_id: int,
    project_id: int,
    current_user: dict = Depends(require_active_user),
    db: AsyncSession = Depends(get_db),
):
    success = await revoke_project_access(db, project_id, group_id)
    if not success:
        raise HTTPException(404, "Access rule not found")
    return {"message": "Access revoked"}


@router.post("/{group_id}/files/{file_uuid}")
async def grant_file_route(
    group_id: int,
    file_uuid: str,
    current_user: dict = Depends(require_active_user),
    db: AsyncSession = Depends(get_db),
):
    file_result = await db.execute(select(File).where(File.uuid == file_uuid))
    file = file_result.scalar_one_or_none()
    if not file:
        raise HTTPException(404, "File not found")
    try:
        fg = await grant_file_access(db, file.id, group_id)
        return {"id": fg.id}
    except ValueError as e:
        raise HTTPException(409, str(e))


@router.delete("/{group_id}/files/{file_uuid}")
async def revoke_file_route(
    group_id: int,
    file_uuid: str,
    current_user: dict = Depends(require_active_user),
    db: AsyncSession = Depends(get_db),
):
    file_result = await db.execute(select(File).where(File.uuid == file_uuid))
    file = file_result.scalar_one_or_none()
    if not file:
        raise HTTPException(404, "File not found")
    success = await revoke_file_access(db, file.id, group_id)
    if not success:
        raise HTTPException(404, "Access rule not found")
    return {"message": "Access revoked"}
