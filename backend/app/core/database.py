# database.py - 数据库连接配置
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy import text
import os
import logging
from app.utils import hash

logger = logging.getLogger(__name__)

DATABASE_USERNAME = os.getenv('DATABASE_USERNAME', 'root')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD', 'root')
DATABASE_HOST = os.getenv('DATABASE_HOST', '127.0.0.1')
DATABASE_PORT = os.getenv('DATABASE_PORT', '3306')
DATABASE_NAME = os.getenv('DATABASE_NAME', 'polyplex')

# 不指定数据库的 URL（用于创建数据库）
BASE_DATABASE_URL = f"mysql+asyncmy://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}"
# 指定数据库的 URL（用于实际操作）
DATABASE_URL = f"mysql+asyncmy://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"

# 创建异步引擎（先用于检查/创建数据库）
base_engine = create_async_engine(BASE_DATABASE_URL, echo=True)

# 创建实际的数据库引擎（用于业务操作）
engine = create_async_engine(DATABASE_URL, echo=True)

# 创建异步会话工厂
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# 声明式基类
Base = declarative_base()


async def ensure_database_exists():
    """确保数据库存在，如果不存在则创建"""
    try:
        async with base_engine.connect() as conn:
            # 使用参数化查询
            result = await conn.execute(
                text("SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = :db_name"),
                {"db_name": DATABASE_NAME}
            )
            exists = result.fetchone()

            if not exists:
                logger.info(f"数据库 {DATABASE_NAME} 不存在，正在创建...")
                # 创建数据库（使用 utf8mb4 字符集支持 emoji 和中文）
                await conn.execute(
                    text(f"CREATE DATABASE {DATABASE_NAME} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
                )
                await conn.commit()
                logger.info(f"数据库 {DATABASE_NAME} 创建成功")
            else:
                logger.info(f"数据库 {DATABASE_NAME} 已存在")
    except Exception as e:
        logger.error(f"创建数据库失败: {e}")
        raise
    finally:
        await base_engine.dispose()


async def ensure_system_user_exists():
    """确保系统用户存在"""
    try:
        async with AsyncSessionLocal() as session:
            # 直接查询，不导入 CRUD
            from sqlalchemy import select
            from app.models.users import User

            # 查询系统用户
            result = await session.execute(
                select(User).where(User.is_system == True)
            )
            system_user = result.scalar_one_or_none()

            if not system_user:
                username = os.getenv('SYSTEM_USERNAME', 'System')
                password = os.getenv('SYSTEM_USER_PASSWORD', 'System_260419')

                # 检查密码长度
                if len(password.encode('utf-8')) > 72:
                    logger.warning(f"密码超过72字节，将被截断")
                    password = password[:72]

                password_hash = hash.hash_password(password)

                logger.info(f"系统用户 {username} 不存在，正在创建...")

                # 直接创建用户
                from app.models.users import User

                new_user = User(
                    username=username,
                    password_hash=password_hash,
                    is_system=True,  # 设置为系统用户
                    job_number="10000"
                )

                session.add(new_user)
                await session.commit()
                await session.refresh(new_user)

                logger.info(f"系统用户 {username} 创建成功 (ID: {new_user.id})")
            else:
                logger.info(f"系统用户已存在 (ID: {system_user.id}, 用户名: {system_user.username})")

    except Exception as e:
        logger.error(f"创建系统用户失败: {e}")
        raise


# 依赖注入：获取数据库会话
async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session