"""项目成员相关 Pydantic 请求/响应模型"""
from pydantic import BaseModel
from typing import Optional
from app.models.members import RoleType


class AddMemberRequest(BaseModel):
    user_id: int
    role: RoleType


class BatchAddMembersRequest(BaseModel):
    members: list[AddMemberRequest]


class UpdateMemberRoleRequest(BaseModel):
    role: RoleType


class MemberResponse(BaseModel):
    id: int
    user_id: int
    username: str
    email: Optional[str] = None
    role: RoleType
    created_at: int

    class Config:
        from_attributes = True


class MemberListResponse(BaseModel):
    items: list[MemberResponse]
    total: int
