"""项目相关 Pydantic 请求/响应模型"""
from pydantic import BaseModel
from typing import Optional
from app.models.projects import ProjectType


class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None
    project_type: ProjectType = ProjectType.OTHER
    is_private: bool = False
    cover_image: Optional[str] = None
    tag_ids: Optional[list[int]] = None


class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    project_type: Optional[ProjectType] = None
    is_private: Optional[bool] = None
    cover_image: Optional[str] = None


class ProjectTagResponse(BaseModel):
    id: int
    name: str
    background_color: str
    text_color: str

    class Config:
        from_attributes = True


class ProjectResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    owner_id: int
    project_type: ProjectType
    is_private: bool
    is_started: bool
    cover_image: Optional[str] = None
    created_at: int
    updated_at: int
    tags: Optional[list[ProjectTagResponse]] = None

    class Config:
        from_attributes = True


class ProjectListResponse(BaseModel):
    items: list[ProjectResponse]
    total: int
    page: int
    page_size: int


class ProjectTagCreate(BaseModel):
    name: str
    background_color: str = "#808080"
    text_color: str = "#ffffff"


class ProjectTagUpdate(BaseModel):
    name: Optional[str] = None
    background_color: Optional[str] = None
    text_color: Optional[str] = None


class AddProjectTagRequest(BaseModel):
    tag_id: Optional[int] = None
    tag_name: Optional[str] = None


class SyncProjectTagsRequest(BaseModel):
    tag_ids: list[int]
