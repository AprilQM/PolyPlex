"""认证 API 路由 — 登录 / 注册 / 邮箱验证 / 公钥"""
import uuid
import json
from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from app.core.database import get_db
from app.core.auth import create_access_token, generate_git_token
from app.core.rsa_key import get_public_key_pem, decrypt_password
from app.core.redis_client import get_redis
from app.core.email import send_verify_email
from app.crud.users import (
    get_user_by_username, get_user_by_email, get_user_by_job_number,
    create_user, update_user_login_time, update_git_token_hash,
)
from app.crud.users import get_user_tag_by_name, add_user_tag, create_user_tag
from app.utils.hash import verify_password, hash_password
from app.api.deps import get_current_user

router = APIRouter(prefix="/api/auth", tags=["auth"])


class EncryptedLoginRequest(BaseModel):
    username: str
    encrypted_password: str


class EncryptedRegisterRequest(BaseModel):
    username: str
    encrypted_password: str
    email: str


class VerifyCodeRequest(BaseModel):
    code: str


# ────────────────────────────── 公钥 ──────────────────────────────

@router.get("/public-key")
async def public_key():
    """获取 RSA 公钥（PEM 格式）"""
    pem = await get_public_key_pem()
    return {"public_key": pem}


# ────────────────────────────── 登录 ──────────────────────────────

@router.post("/login")
async def login(req: EncryptedLoginRequest, db: AsyncSession = Depends(get_db)):
    user = await get_user_by_username(db, req.username)
    if not user:
        raise HTTPException(401, "用户名或密码错误")

    try:
        password = await decrypt_password(req.encrypted_password)
    except Exception:
        raise HTTPException(400, "密码解密失败")

    if not verify_password(password, user.password_hash):
        raise HTTPException(401, "用户名或密码错误")

    token = create_access_token(
        user_id=user.id,
        username=user.username,
        job_number=user.job_number,
        is_system=user.is_system,
    )

    await update_user_login_time(db, user.id)

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "job_number": user.job_number,
            "is_system": user.is_system,
        },
    }


# ────────────────────────────── 注册（发验证邮件） ─────────────────

@router.post("/register")
async def register(req: EncryptedRegisterRequest, request: Request, db: AsyncSession = Depends(get_db)):
    # 校验用户名
    existing = await get_user_by_username(db, req.username)
    if existing:
        raise HTTPException(409, "用户名已存在")

    # 校验邮箱
    existing_email = await get_user_by_email(db, req.email)
    if existing_email:
        raise HTTPException(409, "邮箱已被注册")

    # 校验 RSA 密文（尝试解密，提前发现格式错误）
    try:
        await decrypt_password(req.encrypted_password)
    except Exception:
        raise HTTPException(400, "密码解密失败")

    r = await get_redis()

    # 清除旧验证记录
    old_code = await r.get(f"emailRegister:{req.email}")
    if old_code:
        await r.delete(f"emailRegister:{old_code}")
        await r.delete(f"emailRegister:{req.email}")

    # 生成验证码，存 Redis
    code = uuid.uuid4().hex
    await r.hset(f"emailRegister:{code}", mapping={
        "username": req.username,
        "encrypted_password": req.encrypted_password,
        "email": req.email,
    })
    await r.expire(f"emailRegister:{code}", 1800)
    await r.set(f"emailRegister:{req.email}", code, ex=1800)

    # 发邮件 — 通过请求头重建前端地址（适配 nginx 反向代理）
    proto = request.headers.get("X-Forwarded-Proto", request.url.scheme)
    host = request.headers.get("X-Forwarded-Host") or request.headers.get("Host") or request.url.hostname
    # 去掉后端内部端口 :8000，确保邮件链接指向 nginx
    if host.endswith(":8000"):
        host = host[:host.rfind(":")]
    base_url = f"{proto}://{host}"
    ok = send_verify_email(req.email, code, req.username, base_url)
    if not ok:
        await r.delete(f"emailRegister:{code}")
        await r.delete(f"emailRegister:{req.email}")
        raise HTTPException(502, "验证邮件发送失败，请稍后重试")

    return {"message": "验证邮件已发送，请检查邮箱", "email": req.email}


# ────────────────────────────── 验证码确认 ─────────────────────────

@router.post("/register/resend")
async def resend_register(request: Request):
    """重新发送注册验证邮件"""
    body = await request.json()
    email = body.get("email")
    if not email:
        raise HTTPException(400, "缺少邮箱参数")

    r = await get_redis()

    # 查找该邮箱已有的注册数据
    code = await r.get(f"emailRegister:{email}")
    if not code:
        raise HTTPException(400, "验证邮件已过期，请重新注册")

    data = await r.hgetall(f"emailRegister:{code}")
    username = data.get("username")
    encrypted_password = data.get("encrypted_password")

    if not all([username, encrypted_password]):
        raise HTTPException(400, "注册数据不完整，请重新注册")

    # 删除旧记录
    await r.delete(f"emailRegister:{code}")
    await r.delete(f"emailRegister:{email}")

    # 生成新验证码
    new_code = uuid.uuid4().hex
    await r.hset(f"emailRegister:{new_code}", mapping={
        "username": username,
        "encrypted_password": encrypted_password,
        "email": email,
    })
    await r.expire(f"emailRegister:{new_code}", 1800)
    await r.set(f"emailRegister:{email}", new_code, ex=1800)

    # 发邮件
    proto = request.headers.get("X-Forwarded-Proto", request.url.scheme)
    host = request.headers.get("X-Forwarded-Host") or request.headers.get("Host") or request.url.hostname
    if host.endswith(":8000"):
        host = host[:host.rfind(":")]
    base_url = f"{proto}://{host}"
    ok = send_verify_email(email, new_code, username, base_url)
    if not ok:
        await r.delete(f"emailRegister:{new_code}")
        await r.delete(f"emailRegister:{email}")
        raise HTTPException(502, "验证邮件发送失败，请稍后重试")

    return {"message": "验证邮件已重新发送", "email": email}


@router.post("/verify-code")
async def verify_code(req: VerifyCodeRequest, db: AsyncSession = Depends(get_db)):
    r = await get_redis()
    key = f"emailRegister:{req.code}"
    used_key = f"usedCode:{req.code}"

    if not await r.exists(key):
        # 检查是否已被使用过
        if await r.exists(used_key):
            raise HTTPException(400, "该验证码已被使用")
        raise HTTPException(400, "验证码无效或已过期")

    data = await r.hgetall(key)
    username = data.get("username")
    encrypted_password = data.get("encrypted_password")
    email = data.get("email")

    if not all([username, encrypted_password, email]):
        raise HTTPException(400, "验证码数据不完整")

    # 标记已使用（防止并发重复验证）
    await r.set(used_key, "1", ex=3600)

    # 解密密码
    try:
        password = await decrypt_password(encrypted_password)
    except Exception:
        raise HTTPException(400, "密码解密失败")

    # 再次检查邮箱是否已被注册（防并发）
    existing = await get_user_by_email(db, email)
    if existing:
        await r.delete(key)
        await r.delete(f"emailRegister:{email}")
        raise HTTPException(409, "邮箱已被其他账号注册")

    password_hash = hash_password(password)
    user = await create_user(
        db=db,
        username=username,
        password_hash=password_hash,
    )

    # 写入邮箱
    user.email = email
    await db.commit()

    # 标记验证码已用
    await r.hset(key, "is_verify", "True")

    # 打上 email_verified 标签
    tag = await get_user_tag_by_name(db, "email_verified")
    if tag:
        await add_user_tag(db, user.id, tag.id)

    # 清理 Redis
    await r.delete(key)
    await r.delete(f"emailRegister:{email}")

    token = create_access_token(
        user_id=user.id,
        username=user.username,
        job_number=user.job_number,
        is_system=user.is_system,
    )

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "job_number": user.job_number,
            "is_system": user.is_system,
        },
    }


# ────────────────────────────── 验证状态查询 ───────────────────────

@router.get("/verify-state")
async def verify_state(email: str = Query(...)):
    r = await get_redis()
    code = await r.get(f"emailRegister:{email}")
    if not code:
        return {"state": "expired"}
    if await r.hexists(f"emailRegister:{code}", "is_verify"):
        return {"state": "verified"}
    return {"state": "pending"}


# ────────────────────────────── 验证信息查询（用于前端回显） ───────

@router.get("/verify-info")
async def verify_info(code: str = Query(...)):
    r = await get_redis()
    key = f"emailRegister:{code}"
    if not await r.exists(key):
        raise HTTPException(400, "验证码无效或已过期")
    data = await r.hgetall(key)
    return {
        "username": data.get("username"),
        "email": data.get("email"),
    }


# ────────────────────────────── 当前用户 ───────────────────────────

@router.get("/me")
async def get_me(current_user: dict = Depends(get_current_user)):
    return {"user": current_user}


# ────────────────────────────── Git 令牌 ────────────────────────────

@router.get("/git-token")
async def get_git_token_status(
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """查询当前用户是否已设置 Git 令牌"""
    from app.crud.users import get_user
    user = await get_user(db, current_user["id"])
    return {"has_token": bool(user and user.git_token_hash)}


@router.post("/git-token")
async def create_git_token(
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """生成（或重新生成）当前用户的 Git 令牌，返回原值（仅此一次）"""
    raw_token, token_hash = generate_git_token()
    await update_git_token_hash(db, current_user["id"], token_hash)
    return {
        "git_token": raw_token,
        "message": "请立即保存此令牌，再次查看需要重新生成",
    }
