"""合并请求相关 Pydantic 请求/响应模型"""
from pydantic import BaseModel
from typing import Optional
from app.models.merge_requests import MergeRequestStatus


class MergeRequestCreate(BaseModel):
    source_branch_id: int
    target_branch_id: int = 0
    title: str
    description: Optional[str] = None


class MergeRequestUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None


class MergeRequestReview(BaseModel):
    status: MergeRequestStatus  # APPROVED / REJECTED
    comment: Optional[str] = None


class MergeRequestResponse(BaseModel):
    id: int
    project_id: int
    source_branch_id: int
    target_branch_id: int
    title: str
    description: Optional[str] = None
    created_by: Optional[int] = None
    status: MergeRequestStatus
    reviewed_by: Optional[int] = None
    review_comment: Optional[str] = None
    merged_at: Optional[int] = None
    created_at: int
    updated_at: int

    class Config:
        from_attributes = True


class MergeRequestListResponse(BaseModel):
    items: list[MergeRequestResponse]
    total: int
