"""项目成员 API 路由"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.api.deps import get_current_user, require_active_user
from app.schemas.members import (
    AddMemberRequest,
    BatchAddMembersRequest,
    UpdateMemberRoleRequest,
    MemberResponse,
    MemberListResponse,
)
from app.crud.project_members import (
    get_project_member,
    add_project_member,
    update_member_role,
    remove_project_member,
    get_project_members,
    get_member_count,
    is_project_owner,
    is_project_admin,
    batch_add_project_members,
)
from app.crud.projects import get_project
from app.crud.users import get_user, get_users_by_ids
from app.models.members import RoleType

router = APIRouter(prefix="/api/projects/{project_id}/members", tags=["members"])


# ── 辅助函数 ─────────────────────────────────────────────────────────

async def _get_project_or_404(db: AsyncSession, project_id: int):
    project = await get_project(db, project_id)
    if not project:
        raise HTTPException(404, "项目不存在")
    return project


async def _require_owner(
    db: AsyncSession, project_id: int, user_id: int,
):
    """要求当前用户是项目所有者"""
    if not await is_project_owner(db, project_id, user_id):
        raise HTTPException(403, "只有项目所有者才能执行此操作")


async def _build_member_response(db: AsyncSession, project_id: int) -> list[MemberResponse]:
    """构建成员列表响应"""
    members = await get_project_members(db, project_id)
    user_ids = [m.user_id for m in members]
    users = {u.id: u for u in await get_users_by_ids(db, user_ids)}

    return [
        MemberResponse(
            id=m.id,
            user_id=m.user_id,
            username=users[m.user_id].username if m.user_id in users else "unknown",
            email=users[m.user_id].email if m.user_id in users else None,
            role=m.role,
            created_at=m.created_at,
        )
        for m in members
    ]


# ── 成员 CRUD ────────────────────────────────────────────────────────

@router.get("", response_model=MemberListResponse)
async def list_members(
    project_id: int,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """获取项目成员列表"""
    await _get_project_or_404(db, project_id)
    items = await _build_member_response(db, project_id)
    return MemberListResponse(items=items, total=len(items))


@router.post("", response_model=MemberResponse, status_code=201)
async def add_member(
    project_id: int,
    req: AddMemberRequest,
    current_user: dict = Depends(require_active_user),
    db: AsyncSession = Depends(get_db),
):
    """添加项目成员"""
    await _get_project_or_404(db, project_id)
    await _require_owner(db, project_id, current_user["id"])

    # 检查用户存在
    user = await get_user(db, req.user_id)
    if not user:
        raise HTTPException(404, "用户不存在")

    # 检查是否已是成员
    existing = await get_project_member(db, project_id, req.user_id)
    if existing:
        raise HTTPException(409, "该用户已是项目成员")

    member = await add_project_member(db, project_id, req.user_id, req.role)
    return MemberResponse(
        id=member.id,
        user_id=member.user_id,
        username=user.username,
        email=user.email,
        role=member.role,
        created_at=member.created_at,
    )


@router.post("/batch", status_code=201)
async def batch_add_members(
    project_id: int,
    req: BatchAddMembersRequest,
    current_user: dict = Depends(require_active_user),
    db: AsyncSession = Depends(get_db),
):
    """批量添加成员"""
    await _get_project_or_404(db, project_id)
    await _require_owner(db, project_id, current_user["id"])

    members_data = [{"user_id": m.user_id, "role": m.role} for m in req.members]
    relations = await batch_add_project_members(db, project_id, members_data)

    return {
        "message": f"已添加 {len(relations)} 名成员",
        "added_count": len(relations),
    }


@router.put("/{user_id}", response_model=MemberResponse)
async def update_member(
    project_id: int,
    user_id: int,
    req: UpdateMemberRoleRequest,
    current_user: dict = Depends(require_active_user),
    db: AsyncSession = Depends(get_db),
):
    """更新成员角色"""
    await _get_project_or_404(db, project_id)
    await _require_owner(db, project_id, current_user["id"])

    # 不允许修改所有者角色
    if await is_project_owner(db, project_id, user_id):
        raise HTTPException(400, "不能修改项目所有者的角色")

    member = await update_member_role(db, project_id, user_id, req.role)
    if not member:
        raise HTTPException(404, "该用户不是项目成员")

    user = await get_user(db, user_id)
    return MemberResponse(
        id=member.id,
        user_id=member.user_id,
        username=user.username if user else "unknown",
        email=user.email if user else None,
        role=member.role,
        created_at=member.created_at,
    )


@router.delete("/{user_id}")
async def remove_member(
    project_id: int,
    user_id: int,
    current_user: dict = Depends(require_active_user),
    db: AsyncSession = Depends(get_db),
):
    """移除项目成员"""
    await _get_project_or_404(db, project_id)
    await _require_owner(db, project_id, current_user["id"])

    # 不允许移除所有者
    if await is_project_owner(db, project_id, user_id):
        raise HTTPException(400, "不能移除项目所有者")

    # 不能移除自己（防止误操作）
    if user_id == current_user["id"]:
        raise HTTPException(400, "不能将自己移出项目，如需转让所有权请先变更所有者")

    ok = await remove_project_member(db, project_id, user_id)
    if not ok:
        raise HTTPException(404, "该用户不是项目成员")
    return {"message": "成员已移除"}
