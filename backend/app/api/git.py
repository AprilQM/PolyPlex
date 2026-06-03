"""
Git HTTP Smart Protocol API

实现 Git Smart HTTP 协议，允许标准 Git 客户端通过 HTTP 进行 clone/fetch/push。
每个 Git 仓库关联到一个 GitRepoComponent 实例。
"""
import base64
import hashlib
import logging

from fastapi import APIRouter, Request, Response, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.core.auth import decode_access_token
from app.core.git_config import get_repo_path
from app.services.git_service import GitService
from app.models.components import Component
from app.page_components.base import ComponentType
from app.crud.users import get_user_by_git_token

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/git", tags=["git"])


# ── 认证 ─────────────────────────────────────────────────────────────

async def git_auth(request: Request, db: AsyncSession = Depends(get_db)) -> dict:
    """从请求中提取并验证用户身份

    兼容 Git 的 Basic Auth 和标准 Bearer token。
    Git 发送:  Authorization: Basic base64(any:token)
    标准:      Authorization: Bearer <token>

    验证顺序：JWT → git_token（持久令牌）
    """
    auth_header = request.headers.get("Authorization", "")

    token = None
    if auth_header.startswith("Bearer "):
        token = auth_header[7:]
    elif auth_header.startswith("Basic "):
        try:
            decoded = base64.b64decode(auth_header[6:]).decode("utf-8")
            _, token = decoded.split(":", 1)
        except (ValueError, base64.binascii.Error):
            raise HTTPException(401, "Invalid Basic Auth format")

    if not token:
        raise HTTPException(401, "Authorization required")

    # 1) 先尝试 JWT
    payload = decode_access_token(token)
    if payload:
        return payload

    # 2) 回退：作为 git_token 查找
    token_hash = hashlib.sha256(token.encode()).hexdigest()
    user = await get_user_by_git_token(db, token_hash)
    if user:
        return {
            "id": user.id,
            "username": user.username,
            "job_number": user.job_number,
            "is_system": user.is_system,
        }

    raise HTTPException(401, "Invalid or expired token")


# ── Helper ───────────────────────────────────────────────────────────

async def _resolve_repo_to_component(repo_name: str, db: AsyncSession) -> Component:
    """将仓库名解析为 GitRepoComponent 实例

    格式: "123456" 或 "123456.git" → component_id = 123456
    验证组件存在且类型为 git_repo
    """
    name = repo_name
    if name.endswith(".git"):
        name = name[:-4]

    try:
        component_id = int(name)
    except ValueError:
        raise HTTPException(404, f"Repository not found: {repo_name}")

    result = await db.execute(
        select(Component).where(Component.id == component_id)
    )
    component = result.scalar_one_or_none()
    if not component:
        raise HTTPException(404, "Component not found")

    if component.component_type != ComponentType.GIT_REPO.value:
        raise HTTPException(400, "Component is not a Git repository")

    return component


# ── Info/Refs（advertise refs）─────────────────────────────────────

@router.get("/{repo_name}/info/refs")
async def git_info_refs(
    repo_name: str,
    service: str,
    request: Request,
    user: dict = Depends(git_auth),
    db: AsyncSession = Depends(get_db),
):
    """Git Smart HTTP — 返回 refs 列表（git-upload-pack / git-receive-pack）"""
    if service not in ("git-upload-pack", "git-receive-pack"):
        raise HTTPException(400, f"Invalid service: {service}")

    component = await _resolve_repo_to_component(repo_name, db)
    repo_id = component.id

    repo_path = get_repo_path(repo_id)
    if not repo_path.exists():
        await GitService.init_repo(repo_id)

    rc, stdout, stderr = await GitService._git_async(
        service, "--advertise-refs", str(repo_path),
    )
    if rc != 0:
        logger.error(f"git {service} --advertise-refs failed: {stderr.decode()}")
        raise HTTPException(500, "Internal Git error")

    content_type = f"application/x-git-{service}-advertisement"
    return Response(
        content=stdout,
        media_type=content_type,
        headers={
            "Cache-Control": "no-cache",
            "Expires": "Fri, 01 Jan 1980 00:00:00 GMT",
            "Pragma": "no-cache",
        },
    )


# ── Upload Pack（clone / fetch）────────────────────────────────────

@router.post("/{repo_name}/git-upload-pack")
async def git_upload_pack(
    repo_name: str,
    request: Request,
    user: dict = Depends(git_auth),
    db: AsyncSession = Depends(get_db),
):
    """Git Smart HTTP — 接收 wants/haves，返回 packfile（clone/fetch）"""
    component = await _resolve_repo_to_component(repo_name, db)
    repo_id = component.id

    repo_path = get_repo_path(repo_id)
    if not repo_path.exists():
        await GitService.init_repo(repo_id)

    body = await request.body()

    rc, stdout, stderr = await GitService._git_async(
        "upload-pack", "--stateless-rpc", str(repo_path),
        stdin=body,
    )
    if rc != 0:
        logger.error(f"git upload-pack failed: {stderr.decode()}")
        raise HTTPException(500, "Internal Git error")

    return Response(
        content=stdout,
        media_type="application/x-git-upload-pack-result",
        headers={
            "Cache-Control": "no-cache",
            "Expires": "Fri, 01 Jan 1980 00:00:00 GMT",
            "Pragma": "no-cache",
        },
    )


# ── Receive Pack（push）────────────────────────────────────────────

@router.post("/{repo_name}/git-receive-pack")
async def git_receive_pack(
    repo_name: str,
    request: Request,
    user: dict = Depends(git_auth),
    db: AsyncSession = Depends(get_db),
):
    """Git Smart HTTP — 接收 push 的 packfile，更新 refs 并同步到 File DB"""
    component = await _resolve_repo_to_component(repo_name, db)
    repo_id = component.id

    repo_path = get_repo_path(repo_id)
    if not repo_path.exists():
        await GitService.init_repo(repo_id)

    body = await request.body()

    # 获取用户 ID
    user_id = user.get("id")
    if not user_id:
        raise HTTPException(401, "Invalid user")

    # 执行 git receive-pack
    rc, stdout, stderr = await GitService._git_async(
        "receive-pack", "--stateless-rpc", str(repo_path),
        stdin=body,
    )
    if rc != 0:
        logger.error(f"git receive-pack failed: {stderr.decode()}")
        raise HTTPException(500, "Internal Git error")

    # push 成功后，同步文件到 File DB
    try:
        await GitService.sync_push_to_db(repo_id, db, uploader_id=user_id)
    except Exception as e:
        logger.error(f"sync_push_to_db failed for repo {repo_id}: {e}")

    return Response(
        content=stdout,
        media_type="application/x-git-receive-pack-result",
        headers={
            "Cache-Control": "no-cache",
            "Expires": "Fri, 01 Jan 1980 00:00:00 GMT",
            "Pragma": "no-cache",
        },
    )
