from app.core.database import Base
from sqlalchemy import Column, Integer, String, BigInteger, Boolean, event, ForeignKey, Index
from app.utils.snowflake import generate_user_id, generate_user_tag_id, generate_user_tag_relation_id
import time


class User(Base):
    """用户表"""
    __tablename__ = "users"

    id = Column(
        BigInteger,
        primary_key=True,
        default=generate_user_id,
        index=True,
        autoincrement=False
    )
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(50), unique=True, index=True)
    password_hash = Column(String(128), nullable=False)
    job_number = Column(String(20), unique=True, index=True, nullable=True)
    is_system = Column(Boolean, default=False)
    login_at = Column(BigInteger, default=0)
    git_token_hash = Column(String(64), nullable=True, index=True)
    bio = Column(String(500), nullable=True)
    reject_reason = Column(String(500), nullable=True)
    created_at = Column(BigInteger, default=lambda: int(time.time()), nullable=False)
    updated_at = Column(BigInteger, default=lambda: int(time.time()), nullable=False)


@event.listens_for(User, 'before_update')
def set_updated_at(mapper, connection, target):
    """每次修改用户信息的时候都修改updated_at"""
    target.updated_at = int(time.time())


class UserTag(Base):
    """用户标签表"""
    __tablename__ = "user_tags"

    id = Column(
        BigInteger,
        primary_key=True,
        default=generate_user_tag_id,
        index=True,
        autoincrement=False
    )
    name = Column(String(50), unique=True, index=True, nullable=False)
    color = Column(String(50), nullable=False)
    created_at = Column(BigInteger, default=lambda: int(time.time()), nullable=False)
    updated_at = Column(BigInteger, default=lambda: int(time.time()), onupdate=lambda: int(time.time()), nullable=False)


class UserTagRelation(Base):
    """用户标签关系表"""
    __tablename__ = "user_tag_relations"

    id = Column(
        BigInteger,
        primary_key=True,
        default=generate_user_tag_relation_id,
        index=True,
        autoincrement=False
    )
    user_id = Column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    tag_id = Column(BigInteger, ForeignKey("user_tags.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(BigInteger, default=lambda: int(time.time()), nullable=False)
    updated_at = Column(BigInteger, default=lambda: int(time.time()), onupdate=lambda: int(time.time()), nullable=False)

    __table_args__ = (
        Index('idx_user_tag', 'user_id', 'tag_id'),
    )