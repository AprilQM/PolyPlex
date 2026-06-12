"""通知相关 Pydantic 请求/响应模型"""
from pydantic import BaseModel
from typing import Optional


class NotificationResponse(BaseModel):
    id: int
    user_id: int
    title: str
    content: Optional[str] = None
    type: str
    is_read: bool
    related_id: Optional[int] = None
    created_at: int

    class Config:
        from_attributes = True


class NotificationListResponse(BaseModel):
    items: list[NotificationResponse]
    total: int
    unread_count: int
