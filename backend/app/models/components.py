"""
组件相关表 - 页面组件存储和管理
"""
from app.core.database import Base
from sqlalchemy import Column, Integer, String, BigInteger, Boolean, ForeignKey, Index, JSON, UniqueConstraint
from app.utils.snowflake import generate_component_id, generate_page_component_relation_id
import time


class Component(Base):
    """组件表 - 独立存储组件数据"""
    __tablename__ = "components"

    id = Column(
        BigInteger,
        primary_key=True,
        default=generate_component_id,
        index=True,
        autoincrement=False
    )

    # 组件类型（如 paragraph, heading, table 等）
    component_type = Column(String(50), nullable=False, index=True)

    # 组件唯一标识符（用于页面内引用）
    component_key = Column(String(100), nullable=False, index=True)

    # 组件标题（可选）
    title = Column(String(200), nullable=True)

    # 组件描述（可选）
    description = Column(String(500), nullable=True)

    # 组件数据（JSON 格式）
    data = Column(JSON, nullable=False, default=dict)

    # 组件 schema 定义（JSON 格式）
    schema = Column(JSON, nullable=True)

    # 是否可见
    visible = Column(Boolean, nullable=False, default=True)

    # 创建人
    created_by = Column(BigInteger, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

    # 时间戳
    created_at = Column(BigInteger, default=lambda: int(time.time()), nullable=False)
    updated_at = Column(BigInteger, default=lambda: int(time.time()), onupdate=lambda: int(time.time()), nullable=False)

    __table_args__ = (
        Index('idx_component_type_key', 'component_type', 'component_key'),
    )


class PageComponentRelation(Base):
    """页面组件关系表 - 关联页面和组件，定义顺序"""
    __tablename__ = "page_component_relations"

    id = Column(
        BigInteger,
        primary_key=True,
        default=generate_page_component_relation_id,
        index=True,
        autoincrement=False
    )

    # 页面 ID
    page_id = Column(BigInteger, ForeignKey("project_pages.id", ondelete="CASCADE"), nullable=False)

    # 组件 ID
    component_id = Column(BigInteger, ForeignKey("components.id", ondelete="CASCADE"), nullable=False)

    # 组件在页面中的显示顺序
    order_index = Column(Integer, nullable=False, default=0)

    # 创建人
    created_by = Column(BigInteger, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

    # 时间戳
    created_at = Column(BigInteger, default=lambda: int(time.time()), nullable=False)
    updated_at = Column(BigInteger, default=lambda: int(time.time()), onupdate=lambda: int(time.time()), nullable=False)

    __table_args__ = (
        UniqueConstraint('page_id', 'component_id', name='uq_page_component'),
        Index('idx_relation_page_order', 'page_id', 'order_index'),
        Index('idx_relation_component', 'component_id'),
    )
