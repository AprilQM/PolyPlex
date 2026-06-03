"""
Redis 客户端连接管理
"""
import os
import redis.asyncio as aioredis

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
REDIS_DB = int(os.getenv("REDIS_DB", "0"))

_redis_pool = None


async def get_redis() -> aioredis.Redis:
    """获取 Redis 连接（单例连接池）"""
    global _redis_pool
    if _redis_pool is None:
        _redis_pool = aioredis.ConnectionPool(
            host=REDIS_HOST,
            port=REDIS_PORT,
            db=REDIS_DB,
            decode_responses=True,
        )
    return aioredis.Redis(connection_pool=_redis_pool)


async def close_redis():
    """关闭 Redis 连接池"""
    global _redis_pool
    if _redis_pool:
        await _redis_pool.disconnect()
        _redis_pool = None
