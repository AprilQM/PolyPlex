"""
JWT 认证工具 + Git token 生成
"""
import os
import hashlib
import secrets
from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import jwt, JWTError

SECRET_KEY = os.getenv("SECRET_KEY", "default-secret-key-change-in-production")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440"))


def create_access_token(
    user_id: int,
    username: str,
    job_number: str,
    is_system: bool = False,
    expires_delta: Optional[timedelta] = None,
) -> str:
    """创建 JWT access token"""
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    payload = {
        "id": user_id,
        "sub": str(user_id),
        "name": username,
        "job_number": job_number,
        "is_system": is_system,
        "exp": expire,
        "iat": datetime.now(timezone.utc),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> Optional[dict]:
    """解码并验证 JWT token，返回 payload 或 None"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None


def generate_git_token() -> tuple[str, str]:
    """生成持久的 Git 令牌，返回 (raw_token, sha256_hash)

    raw_token 返回给用户（仅展示一次），sha256_hash 存入数据库用于查询。
    """
    raw = secrets.token_urlsafe(32)
    token_hash = hashlib.sha256(raw.encode()).hexdigest()
    return raw, token_hash
