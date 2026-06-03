"""
合并请求表 - 分支合并管理
"""
from app.core.database import Base
from sqlalchemy import Column, Integer, String, BigInteger, ForeignKey, Index, Enum
from app.utils.snowflake import generate_project_merge_request_id
import time
from enum import Enum as PyEnum


class MergeRequestStatus(str, PyEnum):
    """合并请求状态"""
    PENDING = "pending"      # 待审核
    APPROVED = "approved"    # 已通过
    REJECTED = "rejected"    # 已拒绝
    MERGED = "merged"        # 已合并


class MergeRequest(Base):
    """合并请求表"""
    __tablename__ = "merge_requests"

    id = Column(
        BigInteger,
        primary_key=True,
        default=generate_project_merge_request_id,
        index=True,
        autoincrement=False
    )
    project_id = Column(BigInteger, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    source_branch_id = Column(BigInteger, ForeignKey("branches.id", ondelete="CASCADE"), nullable=False)
    target_branch_id = Column(BigInteger, ForeignKey("branches.id", ondelete="CASCADE"), nullable=False, default=0)  # 0 = main
    title = Column(String(200), nullable=False)
    description = Column(String(1000), nullable=True)
    created_by = Column(BigInteger, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    status = Column(Enum(MergeRequestStatus), default=MergeRequestStatus.PENDING, nullable=False)
    reviewed_by = Column(BigInteger, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    review_comment = Column(String(500), nullable=True)
    merged_at = Column(BigInteger, nullable=True)
    created_at = Column(BigInteger, default=lambda: int(time.time()), nullable=False)
    updated_at = Column(BigInteger, default=lambda: int(time.time()), onupdate=lambda: int(time.time()), nullable=False)

    __table_args__ = (
        Index('idx_mr_project', 'project_id', 'status'),
        Index('idx_mr_branch', 'source_branch_id', 'target_branch_id'),
    )
