"""
项目成员表 - 项目成员和权限管理
"""
from app.core.database import Base
from sqlalchemy import Column, Integer, String, BigInteger, ForeignKey, Index, UniqueConstraint, Enum
from app.utils.snowflake import generate_project_user_relation_id
import time
from enum import Enum as PyEnum


class RoleType(str, PyEnum):
    """成员角色"""
    OWNER = "owner"          # 所有者 - 拥有项目最高权限，可转让所有权
    ADMIN = "admin"          # 管理员 - 可审核批准合并/入项请求，管理成员
    CONTRIBUTOR = "contributor"  # 贡献者 - 可创建分支，编辑内容，发起请求
    VIEWER = "viewer"        # 游客 - 只读浏览


class ProjectMember(Base):
    """项目成员表"""
    __tablename__ = "project_members"

    id = Column(
        BigInteger,
        primary_key=True,
        default=generate_project_user_relation_id,
        index=True,
        autoincrement=False
    )
    project_id = Column(BigInteger, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    role = Column(Enum(RoleType), default=RoleType.VIEWER, nullable=False)
    created_at = Column(BigInteger, default=lambda: int(time.time()), nullable=False)
    updated_at = Column(BigInteger, default=lambda: int(time.time()), onupdate=lambda: int(time.time()), nullable=False)

    __table_args__ = (
        UniqueConstraint('project_id', 'user_id', name='uq_project_user'),
        Index('idx_project_members', 'project_id', 'role'),
        Index('idx_user_projects', 'user_id'),
    )
