"""分支相关 Pydantic 请求/响应模型"""
from pydantic import BaseModel
from typing import Optional
from app.models.branches import BranchStatus


class BranchCreate(BaseModel):
    name: str
    description: Optional[str] = None
    source_branch_id: Optional[int] = None


class BranchUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class BranchUpdateStatus(BaseModel):
    status: BranchStatus


class BranchResponse(BaseModel):
    id: int
    project_id: int
    name: str
    description: Optional[str] = None
    created_by: int
    status: BranchStatus
    base_version: int
    created_at: int
    updated_at: int

    class Config:
        from_attributes = True


class BranchListResponse(BaseModel):
    items: list[BranchResponse]
    total: int
