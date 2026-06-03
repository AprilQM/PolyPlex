"""
文件相关表 - 文件和文件包管理
"""
from app.core.database import Base
from sqlalchemy import Column, Integer, String, BigInteger, Boolean, ForeignKey, Index, UniqueConstraint
from app.utils.snowflake import generate_file_id, generate_file_package_id, generate_file_package_relation_id
import time
import uuid


class File(Base):
    """用户文件统一管理表"""
    __tablename__ = "files"

    # ========== 主键 ==========
    id = Column(
        BigInteger,
        primary_key=True,
        default=generate_file_id,
        index=True,
        autoincrement=False
    )
    # 对外公开的 UUID（不暴露自增 ID）
    uuid = Column(String(36), unique=True, index=True, default=lambda: str(uuid.uuid4()))

    # ========== 文件基本信息 ==========
    filename = Column(String(255), nullable=False)  # 原始文件名
    file_size = Column(BigInteger, nullable=False)  # 文件大小（字节）
    file_type = Column(String(100), nullable=False)  # MIME 类型，如 image/png
    file_ext = Column(String(20), nullable=False)  # 扩展名，如 .png

    # 文件哈希（用于去重）
    file_hash = Column(String(64), nullable=True)  # SHA256 哈希值

    # ========== 存储信息 ==========
    folder_name = Column(String(36), nullable=False)  # 所在文件夹 UUID 或 "git:{project_id}"
    git_path = Column(String(1024), nullable=True)  # 在 Git 仓库中的相对路径（如 "src/main.py"）

    # ========== 关联信息 ==========
    uploader_id = Column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    # ========== 文件状态 ==========
    is_deleted = Column(Boolean, default=False, nullable=False)
    deleted_at = Column(BigInteger, nullable=True)  # 删除时间（软删除）

    # ========== 关联目标 ==========
    target_type = Column(String(50), nullable=True)   # 关联目标类型，如 "project"、"page"
    target_id = Column(BigInteger, nullable=True)      # 关联目标 ID

    # ========== 时间戳 ==========
    created_at = Column(BigInteger, default=lambda: int(time.time()), nullable=False)
    updated_at = Column(BigInteger, default=lambda: int(time.time()), onupdate=lambda: int(time.time()), nullable=False)

    # ========== 索引 ==========
    __table_args__ = (
        Index('idx_file_uploader', 'uploader_id'),
        Index('idx_file_created', 'created_at'),
        Index('idx_file_hash', 'file_hash'),  # 用于去重查询
    )


class FilePackage(Base):
    """文件包表 - 用于组织多个文件，支持压缩包上传/下载"""
    __tablename__ = "file_packages"

    id = Column(
        BigInteger,
        primary_key=True,
        default=generate_file_package_id,
        index=True,
        autoincrement=False
    )

    # 包名称
    name = Column(String(200), nullable=False)

    # 描述
    description = Column(String(1000), nullable=True)

    # 关联的项目 ID（可选）
    project_id = Column(BigInteger, ForeignKey("projects.id", ondelete="CASCADE"), nullable=True)

    # 关联的页面 ID（可选，用于页面组件引用）
    page_id = Column(BigInteger, ForeignKey("project_pages.id", ondelete="CASCADE"), nullable=True)

    # 创建人
    created_by = Column(BigInteger, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

    # 文件总数
    file_count = Column(Integer, default=0, nullable=False)

    # 总大小（字节）
    total_size = Column(BigInteger, default=0, nullable=False)

    # 时间戳
    created_at = Column(BigInteger, default=lambda: int(time.time()), nullable=False)
    updated_at = Column(BigInteger, default=lambda: int(time.time()), onupdate=lambda: int(time.time()), nullable=False)

    __table_args__ = (
        Index('idx_package_project', 'project_id'),
        Index('idx_package_page', 'page_id'),
    )


class FilePackageRelation(Base):
    """文件包与文件关系表"""
    __tablename__ = "file_package_relations"

    id = Column(
        BigInteger,
        primary_key=True,
        default=generate_file_package_relation_id,
        index=True,
        autoincrement=False
    )

    # 文件包 ID
    package_id = Column(BigInteger, ForeignKey("file_packages.id", ondelete="CASCADE"), nullable=False)

    # 文件 ID（引用 files 表）
    file_id = Column(BigInteger, ForeignKey("files.id", ondelete="CASCADE"), nullable=False)

    # 文件在包中的路径（支持目录结构）
    file_path = Column(String(500), nullable=True)

    # 显示名称
    display_name = Column(String(255), nullable=True)

    # 排序
    order_index = Column(Integer, default=0, nullable=False)

    # 创建时间
    created_at = Column(BigInteger, default=lambda: int(time.time()), nullable=False)

    __table_args__ = (
        UniqueConstraint('package_id', 'file_id', name='uq_package_file'),
        Index('idx_relation_package', 'package_id', 'order_index'),
        Index('idx_relation_file', 'file_id'),
    )
