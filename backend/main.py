from fastapi import FastAPI
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv

load_dotenv()


# 配置数据库相关
from app.core.database import engine, Base, ensure_database_exists, ensure_system_user_exists, AsyncSessionLocal
from app.core.redis_client import close_redis
from app.crud.groups import ensure_default_groups
from app.crud.users import get_user_tag_by_name, create_user_tag
from app import models


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时执行
    await ensure_database_exists()  # 确保数据库存在

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("数据表创建/检查完成！")

    # 自动迁移：添加 git_path 列（若不存在）
    async with engine.begin() as conn:
        from sqlalchemy import text
        result = await conn.execute(
            text("SHOW COLUMNS FROM `files` LIKE 'git_path'")
        )
        if not result.fetchone():
            await conn.execute(
                text("ALTER TABLE `files` ADD COLUMN `git_path` VARCHAR(1024) NULL AFTER `folder_name`")
            )
            print("数据库迁移：files 表添加 git_path 列")

    # 自动迁移：添加 git_token_hash 列（若不存在）
    async with engine.begin() as conn:
        result = await conn.execute(
            text("SHOW COLUMNS FROM `users` LIKE 'git_token_hash'")
        )
        if not result.fetchone():
            await conn.execute(
                text("ALTER TABLE `users` ADD COLUMN `git_token_hash` VARCHAR(64) NULL AFTER `login_at`")
            )
            print("数据库迁移：users 表添加 git_token_hash 列")

    # 自动迁移：添加 bio 列（若不存在）
    async with engine.begin() as conn:
        result = await conn.execute(
            text("SHOW COLUMNS FROM `users` LIKE 'bio'")
        )
        if not result.fetchone():
            await conn.execute(
                text("ALTER TABLE `users` ADD COLUMN `bio` VARCHAR(500) NULL AFTER `git_token_hash`")
            )
            print("数据库迁移：users 表添加 bio 列")

    # 自动迁移：添加 reject_reason 列（若不存在）
    async with engine.begin() as conn:
        result = await conn.execute(
            text("SHOW COLUMNS FROM `users` LIKE 'reject_reason'")
        )
        if not result.fetchone():
            await conn.execute(
                text("ALTER TABLE `users` ADD COLUMN `reject_reason` VARCHAR(500) NULL AFTER `bio`")
            )
            print("数据库迁移：users 表添加 reject_reason 列")

    # 自动迁移：让 job_number 可为空（审核拒绝时会置 NULL）
    async with engine.begin() as conn:
        result = await conn.execute(
            text("SHOW COLUMNS FROM `users` WHERE Field = 'job_number'")
        )
        col = result.fetchone()
        if col and col[2] == 'NO':  # 第 3 列是 Null 标志
            await conn.execute(
                text("ALTER TABLE `users` MODIFY COLUMN `job_number` VARCHAR(20) NULL")
            )
            print("数据库迁移：users 表 job_number 改为可为空")
    print("数据库迁移检查完成！")

    await ensure_system_user_exists()  # 检查系统用户是否存在

    async with AsyncSessionLocal() as session:
        await ensure_default_groups(session)
        # 确保 email_verified 标签存在
        tag = await get_user_tag_by_name(session, "email_verified")
        if not tag:
            await create_user_tag(session, name="email_verified", color="#10b981")

        # 确保系统用户有管理员权限
        from app.crud.group_user_relations import add_member
        from app.models.groups import GroupRole
        from app.models.users import User
        from sqlalchemy import select
        system_user = (await session.execute(select(User).where(User.is_system == True))).scalar_one_or_none()
        if system_user:
            from app.crud.groups import get_group_by_name
            admin_group = await get_group_by_name(session, "admin")
            if admin_group:
                from app.crud.group_user_relations import is_user_in_group
                if not await is_user_in_group(session, system_user.id, admin_group.id):
                    await add_member(session, admin_group.id, system_user.id, GroupRole.OWNER)
                    print(f"系统用户 {system_user.username} 已加入 admin 组")
    print("默认用户组检查完成！")

    yield

    # 关闭时执行
    print("关闭数据库连接...")
    await engine.dispose()
    await close_redis()

app = FastAPI(lifespan=lifespan)

from app.api.files import router as files_router
from app.api.groups import router as groups_router
from app.api.auth import router as auth_router
from app.api.git import router as git_router
from app.api.admin import router as admin_router
app.include_router(files_router)
app.include_router(groups_router)
app.include_router(auth_router)
app.include_router(git_router)
app.include_router(admin_router)


# ── OpenAPI 中文本地化 ──────────────────────────────────────────

_OPENAPI_SUMMARIES = {
    # 认证
    "/api/auth/public-key:get": "获取 RSA 公钥",
    "/api/auth/login:post": "用户登录",
    "/api/auth/register:post": "注册并发送验证邮件",
    "/api/auth/register/resend:post": "重新发送验证邮件",
    "/api/auth/verify-code:post": "验证邮箱验证码",
    "/api/auth/verify-state:get": "查询邮箱验证状态",
    "/api/auth/verify-info:get": "查询验证信息（前端回显用）",
    "/api/auth/me:get": "获取当前用户信息",
    "/api/auth/approval-status:get": "查询管理员审核状态",
    "/api/auth/user-status:get": "查询用户完整状态（pending/approved/rejected/banned）",
    "/api/auth/git-token:get": "查询 Git 令牌是否存在",
    "/api/auth/git-token:post": "生成（或重新生成）Git 令牌",
    # 文件
    "/api/files/upload:post": "上传文件",
    "/api/files/{file_uuid}:get": "获取文件元信息",
    "/api/files/{file_uuid}:delete": "删除文件（移入回收站）",
    "/api/files/{file_uuid}:put": "更新文件信息",
    "/api/files/{file_uuid}/download:get": "下载文件",
    "/api/files/{file_uuid}/restore:put": "恢复已删除文件",
    "/api/files:get": "获取文件列表（分页）",
    "/api/files/batch-delete:post": "批量删除文件",
    # 用户组
    "/api/groups:post": "创建用户组",
    "/api/groups:get": "获取用户组列表",
    "/api/groups/{group_id}:get": "获取用户组详情",
    "/api/groups/{group_id}:put": "更新用户组信息",
    "/api/groups/{group_id}:delete": "删除用户组",
    "/api/groups/{group_id}/members:post": "添加组成员",
    "/api/groups/{group_id}/members/{member_user_id}:delete": "移除组成员",
    "/api/groups/{group_id}/members/{member_user_id}:put": "更新组成员角色",
    "/api/groups/{group_id}/projects/{project_id}:post": "授予项目访问权限",
    "/api/groups/{group_id}/projects/{project_id}:delete": "撤销项目访问权限",
    "/api/groups/{group_id}/files/{file_uuid}:post": "授予文件访问权限",
    "/api/groups/{group_id}/files/{file_uuid}:delete": "撤销文件访问权限",
    # Git
    "/api/git/{repo_name}/info/refs:get": "Git 获取引用列表",
    "/api/git/{repo_name}/git-upload-pack:post": "Git 获取数据包（clone/fetch）",
    "/api/git/{repo_name}/git-receive-pack:post": "Git 接收推送数据包（push）",
    # 管理员
    "/api/admin/pending-users:get": "获取待审核用户列表",
    "/api/admin/approve-user/{user_id}:post": "审核通过用户",
    "/api/admin/reject-user/{user_id}:post": "拒绝用户（移至 ban 组，邮件告知理由）",
    "/api/admin/stats:get": "管理后台仪表盘统计数据",
    "/api/admin/users:get": "获取用户列表（分页，支持搜索）",
}


def _custom_openapi():
    from fastapi.openapi.utils import get_openapi
    if app.openapi_schema:
        return app.openapi_schema
    schema = get_openapi(
        title="PolyPlex API",
        version="1.0.0",
        description="AI-native 灵感集存与项目共创平台后端 API",
        routes=app.routes,
    )
    for path in schema.get("paths", {}):
        for method in ("get", "post", "put", "delete"):
            op = schema["paths"][path].get(method)
            if op is None:
                continue
            key = f"{path}:{method}"
            if key in _OPENAPI_SUMMARIES:
                op["summary"] = _OPENAPI_SUMMARIES[key]
    app.openapi_schema = schema
    return schema


app.openapi = _custom_openapi


if __name__ == "__main__":
    import uvicorn
    APP_HOST = os.getenv('APP_HOST', '0.0.0.0')
    APP_PORT = int(os.getenv('APP_PORT', '8000'))
    uvicorn.run(app, host=APP_HOST, port=APP_PORT)