"""页面相关 Pydantic 请求/响应模型"""
from pydantic import BaseModel
from typing import Optional
from app.models.projects import PagePower


class PageCreate(BaseModel):
    title: str
    page_type: str
    icon: Optional[str] = None
    parent_id: Optional[int] = None
    is_folder: bool = False
    branch_id: int = 0
    control_power: Optional[PagePower] = None
    edit_power: Optional[PagePower] = None
    view_power: Optional[PagePower] = None
    order_index: int = 0
    is_hidden: bool = False


class PageUpdate(BaseModel):
    title: Optional[str] = None
    icon: Optional[str] = None
    parent_id: Optional[int] = None
    control_power: Optional[PagePower] = None
    edit_power: Optional[PagePower] = None
    view_power: Optional[PagePower] = None
    order_index: Optional[int] = None
    is_hidden: Optional[bool] = None


class PageResponse(BaseModel):
    id: int
    project_id: int
    branch_id: int
    title: str
    page_type: str
    icon: Optional[str] = None
    parent_id: Optional[int] = None
    is_folder: bool
    control_power: Optional[PagePower] = None
    edit_power: Optional[PagePower] = None
    view_power: Optional[PagePower] = None
    order_index: int
    is_hidden: bool
    created_by: Optional[int] = None
    updated_by: Optional[int] = None
    created_at: int
    updated_at: int

    class Config:
        from_attributes = True


class PageTreeItem(BaseModel):
    id: int
    project_id: int
    branch_id: int
    title: str
    page_type: str
    icon: Optional[str] = None
    parent_id: Optional[int] = None
    is_folder: bool
    order_index: int
    is_hidden: bool
    children: list["PageTreeItem"] = []

    class Config:
        from_attributes = True


class MovePageRequest(BaseModel):
    parent_id: Optional[int] = None
    order_index: int = 0
