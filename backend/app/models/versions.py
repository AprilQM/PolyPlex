"""
版本相关表 - Git 风格的分支版本管理
"""
from app.core.database import Base
from sqlalchemy import Column, Integer, String, BigInteger, ForeignKey, Index, JSON, Text
from app.utils.snowflake import generate_branch_version_id, generate_branch_version_change_id
import time


class BranchVersion(Base):
    """分支版本表 - 类似 Git commit，记录分支的变更"""
    __tablename__ = "branch_versions"

    id = Column(
        BigInteger,
        primary_key=True,
        default=generate_branch_version_id,
        index=True,
        autoincrement=False
    )

    # 分支 ID
    branch_id = Column(BigInteger, ForeignKey("branches.id", ondelete="CASCADE"), nullable=False, index=True)

    # 项目名称（冗余，便于查询）
    project_id = Column(BigInteger, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)

    # 父版本 ID（类似 Git 的 parent commit）
    parent_version_id = Column(BigInteger, ForeignKey("branch_versions.id", ondelete="SET NULL"), nullable=True, index=True)

    # 版本名称（可选，如 "v1.0", "release-2024-01"）
    version_name = Column(String(50), nullable=True)

    # 提交信息
    message = Column(String(1000), nullable=False)

    # 变更摘要（JSON 格式）
    # {"pages_added": 1, "pages_modified": 2, "pages_deleted": 0, "files_changed": 5}
    summary = Column(JSON, nullable=True)

    # 创建人
    created_by = Column(BigInteger, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

    # 创建时间
    created_at = Column(BigInteger, default=lambda: int(time.time()), nullable=False)

    __table_args__ = (
        Index('idx_branch_version_branch', 'branch_id', 'created_at'),
        Index('idx_branch_version_parent', 'parent_version_id'),
    )


class BranchVersionChange(Base):
    """版本变更表 - 记录每个版本中页面的具体变更"""
    __tablename__ = "branch_version_changes"

    id = Column(
        BigInteger,
        primary_key=True,
        default=generate_branch_version_change_id,
        index=True,
        autoincrement=False
    )

    # 分支版本 ID
    version_id = Column(BigInteger, ForeignKey("branch_versions.id", ondelete="CASCADE"), nullable=False, index=True)

    # 页面 ID
    page_id = Column(BigInteger, ForeignKey("project_pages.id", ondelete="CASCADE"), nullable=False)

    # 变更类型：create/update/delete
    change_type = Column(String(20), nullable=False)

    # 变更的组件 ID 列表（可选，记录哪些组件被修改）
    changed_components = Column(JSON, nullable=True)

    # 文件 UUID 变化（仅当页面包含 FileListComponent 时）
    # {"added": ["uuid1", "uuid2"], "removed": ["uuid3"]}
    file_uuids_changed = Column(JSON, nullable=True)

    # 变更摘要
    summary = Column(String(500), nullable=True)

    # 创建时间
    created_at = Column(BigInteger, default=lambda: int(time.time()), nullable=False)

    __table_args__ = (
        Index('idx_version_change_version', 'version_id', 'page_id'),
    )
