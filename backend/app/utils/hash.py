from passlib.context import CryptContext
import os

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__truncate_error=True  # 自动处理超长密码
)

def hash_password(password: str) -> str:
    """
    对明文密码进行哈希
    """
    # 检查并处理超长密码
    if len(password.encode('utf-8')) > 72:
        password = password[:72]
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    验证明文密码与哈希是否匹配
    """
    # 同样处理超长密码
    if len(plain_password.encode('utf-8')) > 72:
        plain_password = plain_password[:72]
    return pwd_context.verify(plain_password, hashed_password)
