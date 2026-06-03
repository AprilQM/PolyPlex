"""
分支相关表 - 项目分支管理
"""
from app.core.database import Base
from sqlalchemy import Column, Integer, String, BigInteger, Boolean, ForeignKey, Index, UniqueConstraint, Enum
from app.utils.snowflake import generate_project_branch_id
import time
from enum import Enum as PyEnum


class BranchStatus(str, PyEnum):
    """分支状态"""
    DRAFT = "draft"          # 草稿
    PENDING = "pending"      # 待审核
    MERGED = "merged"        # 已合并
    REJECTED = "rejected"    # 已拒绝


class Branch(Base):
    """项目分支表"""
    __tablename__ = "branches"

    id = Column(
        BigInteger,
        primary_key=True,
        default=generate_project_branch_id,
        index=True,
        autoincrement=False
    )
    project_id = Column(BigInteger, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(String(500), nullable=True)
    created_by = Column(BigInteger, ForeignKey("users.id", ondelete="RESTRICT"), nullable=False)
    status = Column(Enum(BranchStatus), default=BranchStatus.DRAFT, nullable=False)

    # 分支基于哪个主分支版本
    base_version = Column(Integer, default=1)

    created_at = Column(BigInteger, default=lambda: int(time.time()), nullable=False)
    updated_at = Column(BigInteger, default=lambda: int(time.time()), onupdate=lambda: int(time.time()), nullable=False)

    __table_args__ = (
        UniqueConstraint('project_id', 'name', name='uq_project_branch_name'),
        Index('idx_branch_project', 'project_id', 'status'),
    )
