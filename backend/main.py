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
    print("数据库迁移检查完成！")

    await ensure_system_user_exists()  # 检查系统用户是否存在

    async with AsyncSessionLocal() as session:
        await ensure_default_groups(session)
        # 确保 email_verified 标签存在
        tag = await get_user_tag_by_name(session, "email_verified")
        if not tag:
            await create_user_tag(session, name="email_verified", color="#10b981")
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
app.include_router(files_router)
app.include_router(groups_router)
app.include_router(auth_router)
app.include_router(git_router)


if __name__ == "__main__":
    import uvicorn
    APP_HOST = os.getenv('APP_HOST', '0.0.0.0')
    APP_PORT = int(os.getenv('APP_PORT', '8000'))
    uvicorn.run(app, host=APP_HOST, port=APP_PORT)