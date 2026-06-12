"""组件相关 Pydantic 请求/响应模型"""
from pydantic import BaseModel, Field
from typing import Optional


class ComponentCreate(BaseModel):
    component_type: str
    component_key: str
    data: dict = {}
    title: Optional[str] = None
    description: Optional[str] = None
    schema_: Optional[dict] = Field(None, alias="schema")
    visible: bool = True

    model_config = {"populate_by_name": True}


class ComponentUpdate(BaseModel):
    data: Optional[dict] = None
    title: Optional[str] = None
    description: Optional[str] = None
    schema_: Optional[dict] = Field(None, alias="schema")
    visible: Optional[bool] = None

    model_config = {"populate_by_name": True}


class ComponentResponse(BaseModel):
    id: int
    component_type: str
    component_key: str
    title: Optional[str] = None
    description: Optional[str] = None
    data: dict
    schema_: Optional[dict] = Field(None, alias="schema")
    visible: bool
    created_by: Optional[int] = None
    created_at: int
    updated_at: int

    model_config = {"from_attributes": True, "populate_by_name": True}


class AddComponentToPageRequest(BaseModel):
    component_id: int
    order_index: int = 0


class UpdateComponentOrderRequest(BaseModel):
    component_id: int
    order_index: int


class PageComponentResponse(BaseModel):
    id: int
    component_type: str
    component_key: str
    title: Optional[str] = None
    description: Optional[str] = None
    data: dict
    schema_: Optional[dict] = Field(None, alias="schema")
    visible: bool
    order_index: int
    created_at: int
    updated_at: int

    model_config = {"from_attributes": True, "populate_by_name": True}


class SyncPageComponentsRequest(BaseModel):
    components: list[ComponentCreate]
