"""认证相关 Pydantic 请求/响应模型"""
from pydantic import BaseModel


class EncryptedLoginRequest(BaseModel):
    username: str
    encrypted_password: str


class EncryptedRegisterRequest(BaseModel):
    username: str
    encrypted_password: str
    email: str
    bio: str = ""


class VerifyCodeRequest(BaseModel):
    code: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: dict


class RegisterResponse(BaseModel):
    message: str
    email: str


class UserInfo(BaseModel):
    id: int
    username: str
    email: str
    job_number: str | None = None
    is_system: bool = False
