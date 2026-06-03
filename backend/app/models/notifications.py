from app.core.database import Base
from sqlalchemy import Column, Integer, String, BigInteger, Boolean, event, ForeignKey, Index
from app.utils.snowflake import generate_notification_id
import time


class Notification(Base):
    """通知表"""
    __tablename__ = "notifications"
    id = Column(
        BigInteger,
        primary_key=True,
        default=generate_notification_id,
        index=True,
        autoincrement=False
    )
    user_id = Column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(50), nullable=False)
    content = Column(String(500), nullable=False)
    is_read = Column(Boolean, default=False, nullable=False)
    created_at = Column(BigInteger, default=lambda: int(time.time()), nullable=False)
    updated_at = Column(BigInteger, default=lambda: int(time.time()), onupdate=lambda: int(time.time()), nullable=False)

    __table_args__ = (
        Index('idx_notification_user', 'user_id', 'is_read'),
    )
