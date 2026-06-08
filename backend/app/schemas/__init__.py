"""Pydantic 请求/响应模型

分层规范：
- api/ 层从 schemas 导入 request/response 模型
- 所有接口函数的参数和返回值都应使用 schema 类型标注
"""

from app.schemas.auth import (
    EncryptedLoginRequest,
    EncryptedRegisterRequest,
    VerifyCodeRequest,
    LoginResponse,
    RegisterResponse,
    UserInfo,
)

__all__ = [
    # Auth
    "EncryptedLoginRequest",
    "EncryptedRegisterRequest",
    "VerifyCodeRequest",
    "LoginResponse",
    "RegisterResponse",
    "UserInfo",
]
