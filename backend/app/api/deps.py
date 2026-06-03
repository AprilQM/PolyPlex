"""API 依赖项"""
from fastapi import Header, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.auth import decode_access_token
from app.crud.users import get_user

bearer_scheme = HTTPBearer(auto_error=False)


async def get_current_user_id(x_user_id: int = Header(...)) -> int:
    """从 X-User-Id 请求头获取用户 ID（临时方案）"""
    return x_user_id


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
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
