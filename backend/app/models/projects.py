"""
项目核心表 - 项目、标签和页面管理
"""
from app.core.database import Base
from sqlalchemy import Column, Integer, String, BigInteger, Boolean, ForeignKey, JSON, Enum, UniqueConstraint, Index, CheckConstraint, Text
from app.utils.snowflake import (
    generate_project_id,
    generate_project_tag_id,
    generate_project_page_id,
    generate_project_tag_relation_id,
)
import time
from enum import Enum as PyEnum

# 从 project_templates 导入页面类型定义
from app.project_templates import ALL_PAGE_TYPES, PAGE_TYPES_BY_CATEGORY, get_page_type_info, get_page_types_by_category


# ========== 枚举定义 ==========

class ProjectType(str, PyEnum):
    """项目类型"""
    CODE = "code"
    WRITING = "writing"
    DESIGN = "design"
    BUSINESS = "business"
    LIFESTYLE = "lifestyle"
    ACADEMIC = "academic"
    MEDIA = "media"
    EDUCATION = "education"
    MARKETING = "marketing"
    MUSIC = "music"
    OTHER = "other"


class PagePower(str, PyEnum):
    """页面权限级别"""
    OWNER = "owner"          # 仅发起者
    EDITOR = "editor"        # 发起者 + 编辑者
    VIEWER = "viewer"        # 所有人


# 生成 page_type 的 CheckConstraint 值列表
_page_type_values = [f"'{v}'" for v in ALL_PAGE_TYPES.keys()]
_page_type_check = f"page_type IN ({','.join(_page_type_values)})"


# ========== 项目核心表 ==========

class Project(Base):
    """项目信息表"""
    __tablename__ = "projects"

    id = Column(
        BigInteger,
        primary_key=True,
        default=generate_project_id,
        index=True,
        autoincrement=False
    )
    name = Column(String(100), unique=True, index=True, nullable=False)
    description = Column(String(5000), nullable=True)
    owner_id = Column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)

    # 隐私与状态
    is_private = Column(Boolean, default=False)
    is_started = Column(Boolean, default=False)

    # 项目类型
    project_type = Column(Enum(ProjectType), default=ProjectType.OTHER, nullable=False)

    # 封面图
    cover_image = Column(String(36), ForeignKey("files.uuid", ondelete="SET NULL"), nullable=True)

    # 时间戳
    created_at = Column(BigInteger, default=lambda: int(time.time()), nullable=False)
    updated_at = Column(BigInteger, default=lambda: int(time.time()), onupdate=lambda: int(time.time()), nullable=False)

    # 索引
    __table_args__ = (
        Index('idx_project_owner', 'owner_id', 'is_started'),
        Index('idx_project_type', 'project_type', 'is_private'),
    )


# ========== 标签相关表 ==========

class ProjectTag(Base):
    """项目标签表"""
    __tablename__ = "project_tags"

    id = Column(
        BigInteger,
        primary_key=True,
        default=generate_project_tag_id,
        index=True,
        autoincrement=False
    )
    name = Column(String(50), unique=True, index=True, nullable=False)
    background_color = Column(String(20), nullable=False, default="#808080")
    text_color = Column(String(20), nullable=False, default="#ffffff")
    created_at = Column(BigInteger, default=lambda: int(time.time()), nullable=False)
    updated_at = Column(BigInteger, default=lambda: int(time.time()), onupdate=lambda: int(time.time()), nullable=False)


class ProjectTagRelation(Base):
    """项目标签关系表"""
    __tablename__ = "project_tag_relations"

    id = Column(
        BigInteger,
        primary_key=True,
        default=generate_project_tag_relation_id,
        index=True,
        autoincrement=False
    )
    project_id = Column(BigInteger, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    tag_id = Column(BigInteger, ForeignKey("project_tags.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(BigInteger, default=lambda: int(time.time()), nullable=False)
    updated_at = Column(BigInteger, default=lambda: int(time.time()), onupdate=lambda: int(time.time()), nullable=False)

    __table_args__ = (
        UniqueConstraint('project_id', 'tag_id', name='uq_project_tag'),
        Index('idx_project_tag', 'project_id', 'tag_id'),
    )


# ========== 页面相关表 ==========

class ProjectPage(Base):
    """项目页面表"""
    __tablename__ = "project_pages"

    id = Column(
        BigInteger,
        primary_key=True,
        default=generate_project_page_id,
        index=True,
        autoincrement=False
    )
    project_id = Column(BigInteger, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    branch_id = Column(BigInteger, ForeignKey("branches.id", ondelete="CASCADE"), nullable=False, default=0)
    # branch_id = 0 表示主分支（main）

    # 基础信息
    title = Column(String(100), nullable=False)
    page_type = Column(String(50), nullable=False, default="announcement")
    icon = Column(String(10), nullable=True)

    # 文件夹支持
    parent_id = Column(BigInteger, ForeignKey("project_pages.id", ondelete="SET NULL"), nullable=True, index=True, default=None)
    is_folder = Column(Boolean, nullable=False, default=False)

    # 页面级权限（NULL 表示继承项目权限）
    control_power = Column(Enum(PagePower), nullable=True)
    edit_power = Column(Enum(PagePower), nullable=True)
    view_power = Column(Enum(PagePower), nullable=True)

    # 展示配置
    order_index = Column(Integer, nullable=False, default=0)
    is_hidden = Column(Boolean, nullable=False, default=False)

    # 操作人
    created_by = Column(BigInteger, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    updated_by = Column(BigInteger, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

    # 时间戳
    created_at = Column(BigInteger, default=lambda: int(time.time()), nullable=False)
    updated_at = Column(BigInteger, default=lambda: int(time.time()), onupdate=lambda: int(time.time()), nullable=False)

    __table_args__ = (
        CheckConstraint(_page_type_check, name='check_page_type_valid'),
        Index('idx_page_project_branch', 'project_id', 'branch_id', 'is_hidden'),
        Index('idx_page_order', 'project_id', 'order_index'),
        Index('idx_page_type', 'project_id', 'page_type'),
    )
