"""
RSA 密钥管理 — 密钥对存储在 Redis 中
"""
import base64
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.backends import default_backend
from app.core.redis_client import get_redis

REDIS_RSA_KEY = "rsa_key_pair"


async def get_or_generate_rsa_keys() -> dict:
    """从 Redis 获取 RSA 密钥对，不存在则生成并存储"""
    redis = await get_redis()
    stored = await redis.get(REDIS_RSA_KEY)
    if stored:
        import json
        return json.loads(stored)

    # 生成 2048 位 RSA 密钥对
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend(),
    )

    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    ).decode("utf-8")

    public_pem = private_key.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    ).decode("utf-8")

    key_data = {"private_key": private_pem, "public_key": public_pem}
    import json
    await redis.set(REDIS_RSA_KEY, json.dumps(key_data))
    return key_data


async def get_public_key_pem() -> str:
    """获取 RSA 公钥（PEM 格式）"""
    keys = await get_or_generate_rsa_keys()
    return keys["public_key"]


def decrypt_with_private_key(encrypted_b64: str, private_key_pem: str) -> str:
    """
    使用 RSA 私钥解密 base64 编码的密文
    返回原始字符串（如密码）
    """
    private_key = serialization.load_pem_private_key(
        private_key_pem.encode("utf-8"),
        password=None,
        backend=default_backend(),
    )
    encrypted_bytes = base64.b64decode(encrypted_b64)
    decrypted = private_key.decrypt(
        encrypted_bytes,
        padding.PKCS1v15(),
    )
    return decrypted.decode("utf-8")


async def decrypt_password(encrypted_password: str) -> str:
    """从 Redis 获取私钥并解密密码"""
    keys = await get_or_generate_rsa_keys()
    return decrypt_with_private_key(encrypted_password, keys["private_key"])
