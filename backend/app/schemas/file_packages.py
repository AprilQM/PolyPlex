"""文件包相关 Pydantic 请求/响应模型"""
from pydantic import BaseModel
from typing import Optional


class FilePackageCreate(BaseModel):
    name: str
    description: Optional[str] = None
    project_id: Optional[int] = None
    page_id: Optional[int] = None


class FilePackageUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class FilePackageResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    project_id: Optional[int] = None
    page_id: Optional[int] = None
    created_by: Optional[int] = None
    file_count: int
    total_size: int
    created_at: int
    updated_at: int

    class Config:
        from_attributes = True


class AddFileToPackageRequest(BaseModel):
    file_uuid: str
    file_path: Optional[str] = None
    display_name: Optional[str] = None


class ExtractZipRequest(BaseModel):
    file_uuid: str
    package_id: int
