"""分支版本相关 Pydantic 请求/响应模型"""
from pydantic import BaseModel
from typing import Optional


class PageChangeItem(BaseModel):
    page_id: int
    change_type: str  # create / update / delete
    changed_components: Optional[list[int]] = None
    file_uuids_changed: Optional[dict] = None
    summary: Optional[str] = None


class VersionCreate(BaseModel):
    message: str
    version_name: Optional[str] = None
    page_changes: Optional[list[PageChangeItem]] = None


class VersionResponse(BaseModel):
    id: int
    branch_id: int
    project_id: int
    parent_version_id: Optional[int] = None
    version_name: Optional[str] = None
    message: str
    summary: Optional[dict] = None
    created_by: Optional[int] = None
    created_at: int

    class Config:
        from_attributes = True


class VersionHistoryResponse(BaseModel):
    items: list[VersionResponse]
    total: int
    page: int
    page_size: int


class ChangeDetail(BaseModel):
    page_id: int
    page_title: str
    change_type: str
    summary: Optional[str] = None


class VersionDiffResponse(BaseModel):
    version_id: int
    changes: list[ChangeDetail]
