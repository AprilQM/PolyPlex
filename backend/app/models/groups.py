"""
用户组相关表 - 组管理、组成员、项目/文件权限
"""
from app.core.database import Base
from sqlalchemy import Column, String, BigInteger, ForeignKey, Enum, Index, UniqueConstraint
from app.utils.snowflake import (
    generate_group_id,
    generate_group_user_relation_id,
    generate_project_group_id,
    generate_file_group_id,
)
import time
from enum import Enum as PyEnum


class GroupType(str, PyEnum):
    """组类型"""
    SYSTEM = "system"  # 系统组，不可删除/改名
    USER = "user"      # 用户创建组


class GroupRole(str, PyEnum):
    """组成员角色（应用层三级）"""
    OWNER = "owner"
    ADMIN = "admin"
    MEMBER = "member"


class Group(Base):
    """用户组表"""
    __tablename__ = "groups"

    id = Column(
        BigInteger,
        primary_key=True,
        default=generate_group_id,
        index=True,
        autoincrement=False
    )
    name = Column(String(100), unique=True, index=True, nullable=False)
    description = Column(String(500), nullable=True)
    group_type = Column(Enum(GroupType), default=GroupType.USER, nullable=False)
    created_at = Column(BigInteger, default=lambda: int(time.time()), nullable=False)
    updated_at = Column(BigInteger, default=lambda: int(time.time()), onupdate=lambda: int(time.time()), nullable=False)


class GroupUserRelation(Base):
    """用户组成员关系表"""
    __tablename__ = "group_user_relations"

    id = Column(
        BigInteger,
        primary_key=True,
        default=generate_group_user_relation_id,
        index=True,
        autoincrement=False
    )
    group_id = Column(BigInteger, ForeignKey("groups.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    role = Column(Enum(GroupRole), default=GroupRole.MEMBER, nullable=False)
    permissions = Column(BigInteger, default=0b11)  # 位掩码，默认 VIEW+EDIT
    created_at = Column(BigInteger, default=lambda: int(time.time()), nullable=False)
    updated_at = Column(BigInteger, default=lambda: int(time.time()), onupdate=lambda: int(time.time()), nullable=False)

    __table_args__ = (
        UniqueConstraint('group_id', 'user_id', name='uq_group_user'),
        Index('idx_group_user_group', 'group_id'),
        Index('idx_group_user_user', 'user_id'),
    )


class ProjectGroup(Base):
    """项目-组权限表"""
    __tablename__ = "project_groups"

    id = Column(
        BigInteger,
        primary_key=True,
        default=generate_project_group_id,
        index=True,
        autoincrement=False
    )
    project_id = Column(BigInteger, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    group_id = Column(BigInteger, ForeignKey("groups.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(BigInteger, default=lambda: int(time.time()), nullable=False)

    __table_args__ = (
        UniqueConstraint('project_id', 'group_id', name='uq_project_group'),
        Index('idx_project_group_project', 'project_id'),
        Index('idx_project_group_group', 'group_id'),
    )


class FileGroup(Base):
    """文件-组权限表"""
    __tablename__ = "file_groups"

    id = Column(
        BigInteger,
        primary_key=True,
        default=generate_file_group_id,
        index=True,
        autoincrement=False
    )
    file_id = Column(BigInteger, ForeignKey("files.id", ondelete="CASCADE"), nullable=False)
    group_id = Column(BigInteger, ForeignKey("groups.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(BigInteger, default=lambda: int(time.time()), nullable=False)

    __table_args__ = (
        UniqueConstraint('file_id', 'group_id', name='uq_file_group'),
        Index('idx_file_group_file', 'file_id'),
        Index('idx_file_group_group', 'group_id'),
    )
