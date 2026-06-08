"""管理员 API 路由 — 用户审核等"""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.api.deps import require_admin
from app.crud.group_user_relations import (
    get_pending_users, approve_user, reject_user, is_user_pending,
    is_user_admin, is_user_banned, is_user_rejected,
)
from app.crud.users import get_user, get_user_list, count_users
from app.core.email import send_approval_email, send_rejection_email


class RejectRequest(BaseModel):
    reason: str

router = APIRouter(prefix="/api/admin", tags=["admin"])


@router.get("/stats")
async def admin_stats(
    admin: dict = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    """管理后台仪表盘统计数据"""
    total = await count_users(db)
    pending = await get_pending_users(db, page=1, page_size=9999)
    return {
        "total_users": total,
        "pending_users": len(pending),
    }


@router.get("/pending-users")
async def list_pending_users(
    page: int = 1,
    page_size: int = 20,
    admin: dict = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    """获取待审核用户列表（分页）"""
    items = await get_pending_users(db, page=page, page_size=page_size)
    return {"items": items, "total": len(items), "page": page, "page_size": page_size}


@router.post("/approve-user/{user_id}")
async def approve_user_route(
    user_id: int,
    admin: dict = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    """审核通过用户，并发送邮件通知"""
    if not await is_user_pending(db, user_id):
        raise HTTPException(400, "该用户不在待审核状态")

    user = await get_user(db, user_id)
    if not user:
        raise HTTPException(404, "用户不存在")

    ok = await approve_user(db, user_id)
    if not ok:
        raise HTTPException(500, "审核通过操作失败")

    # 发送审核通过邮件
    if user.email:
        await send_approval_email(user.email, user.username)

    return {"message": f"用户 {user.username} 已审核通过"}


@router.post("/reject-user/{user_id}")
async def reject_user_route(
    user_id: int,
    req: RejectRequest,
    admin: dict = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    """拒绝用户（移至 ban 组），并通过邮件告知理由"""
    if not req.reason.strip():
        raise HTTPException(400, "请填写拒绝理由")

    if not await is_user_pending(db, user_id):
        raise HTTPException(400, "该用户不在待审核状态")

    user = await get_user(db, user_id)
    if not user:
        raise HTTPException(404, "用户不存在")

    ok = await reject_user(db, user_id, reason=req.reason)
    if not ok:
        raise HTTPException(500, "拒绝操作失败")

    # 发送拒绝通知邮件（含理由和自我介绍）
    if user.email:
        await send_rejection_email(user.email, user.username, req.reason, user.bio or "")

    return {"message": f"用户 {user.username} 已被拒绝"}


@router.get("/users")
async def list_users(
    page: int = 1,
    page_size: int = 20,
    search: str = "",
    admin: dict = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    """获取用户列表（分页，支持搜索）"""
    if search:
        from app.crud.users import get_user_by_username, get_user_by_email
        user = await get_user_by_username(db, search)
        if not user:
            user = await get_user_by_email(db, search)
        items = []
        if user:
            items = [{
                "id": user.id,
                "username": user.username,
                "email": user.email or "",
                "job_number": user.job_number,
                "bio": user.bio or "",
                "is_system": user.is_system,
                "created_at": user.created_at,
                "login_at": user.login_at,
                "is_admin": await is_user_admin(db, user.id),
                "is_banned": await is_user_banned(db, user.id),
                "is_rejected": await is_user_rejected(db, user.id),
                "is_pending": await is_user_pending(db, user.id),
            }]
        total = 1 if items else 0
    else:
        raw = await get_user_list(db, page=page, page_size=page_size)
        total = await count_users(db)
        items = []
        for u in raw:
            items.append({
                "id": u.id,
                "username": u.username,
                "email": u.email or "",
                "job_number": u.job_number,
                "bio": u.bio or "",
                "is_system": u.is_system,
                "created_at": u.created_at,
                "login_at": u.login_at,
                "is_admin": await is_user_admin(db, u.id),
                "is_banned": await is_user_banned(db, u.id),
                "is_rejected": await is_user_rejected(db, u.id),
                "is_pending": await is_user_pending(db, u.id),
            })
    return {"items": items, "total": total, "page": page, "page_size": page_size}
