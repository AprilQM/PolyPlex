"""API 依赖项"""
from typing import Optional
from fastapi import Header, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.auth import decode_access_token
from app.crud.users import get_user
from app.crud.group_user_relations import is_admin, is_ban, is_user_pending, is_user_rejected

bearer_scheme = HTTPBearer(auto_error=False)


async def get_current_user_id(x_user_id: int = Header(...)) -> int:
    """从 X-User-Id 请求头获取用户 ID（临时方案）"""
    return x_user_id


async def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(bearer_scheme),
    db: AsyncSession = Depends(get_db),
) -> dict:
    """从 JWT Bearer token 获取当前用户信息"""
    if not credentials:
        raise HTTPException(401, "未提供认证信息")

    payload = decode_access_token(credentials.credentials)
    if not payload:
        raise HTTPException(401, "无效的 token")

    user_id = payload.get("id")
    if not user_id:
        raise HTTPException(401, "无效的 token payload")

    user = await get_user(db, user_id)
    if not user:
        raise HTTPException(401, "用户不存在")

    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "job_number": user.job_number,
        "is_system": user.is_system,
    }


# ── 权限检查依赖 ─────────────────────────────────────────────────────────


async def require_admin(
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict:
    """要求当前用户是管理员，否则 403"""
    if not await is_admin(db, current_user["id"]):
        raise HTTPException(403, "需要管理员权限")
    return current_user


async def require_not_banned(
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict:
    """要求当前用户未被封禁，否则 403"""
    if await is_ban(db, current_user["id"]):
        raise HTTPException(403, "账号已被封禁")
    return current_user


async def require_approved(
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict:
    """要求用户已通过管理员审核，否则 403"""
    if await is_user_pending(db, current_user["id"]):
        raise HTTPException(403, "账号正在等待管理员审核，请稍后再试")
    if await is_user_rejected(db, current_user["id"]):
        raise HTTPException(403, "审核未通过")
    return current_user


async def require_active_user(
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict:
    """组合：未被封禁 + 未拒绝 + 已审核"""
    if await is_ban(db, current_user["id"]):
        raise HTTPException(403, "账号已被封禁")
    if await is_user_rejected(db, current_user["id"]):
        raise HTTPException(403, "审核未通过")
    if await is_user_pending(db, current_user["id"]):
        raise HTTPException(403, "账号正在等待管理员审核，请稍后再试")
    return current_user
