# 用户组系统 & 文件 API — 实现计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 引入用户组权限系统替代 is_admin/is_ban，完成文件 REST API。

**Architecture:**
- 新增 Group、GroupUserRelation、ProjectGroup、FileGroup 四个模型 → 对应的 CRUD → 对应的 API 路由
- 重构 FileService 的存储逻辑，使用 folder_name + uuid 路径规则，支持文件夹上限管理
- 启动时自动校验三个默认系统组（admin/default/ban），创建用户时自动加入 default 组

**Tech Stack:** FastAPI, SQLAlchemy async, MySQL (asyncmy), Snowflake IDs

---

## 文件结构

### 新建文件

| 文件 | 职责 |
|------|------|
| `backend/app/models/groups.py` | Group、GroupUserRelation、ProjectGroup、FileGroup 模型 |
| `backend/app/crud/groups.py` | 组 CRUD：增删改查、get_user_groups、ensure_default_groups |
| `backend/app/crud/group_user_relations.py` | 组成员关系 CRUD：增删改查角色、权限判断 |
| `backend/app/crud/file_access.py` | 项目/文件权限 CRUD：授权/撤销/查询 |
| `backend/app/services/file_access_service.py` | `check_file_access` — 5 步跨表访问判断 |
| `backend/app/api/files.py` | 文件 API 路由模块 |
| `backend/app/api/groups.py` | 用户组 API 路由模块 |

### 修改文件

| 文件 | 改动 |
|------|------|
| `backend/app/utils/snowflake.py` | 新增 4 个 ID 类型常量和生成函数 |
| `backend/app/models/users.py` | 删除 is_admin、is_ban 列 |
| `backend/app/models/files.py` | 删除 storage_path，追加 folder_name、target_type、target_id |
| `backend/app/models/__init__.py` | 添加 Group、GroupUserRelation、ProjectGroup、FileGroup |
| `backend/app/crud/users.py` | 去除 is_admin/is_ban 参数，创建用户时加入 default 组 |
| `backend/app/crud/files.py` | 适配 folder_name，移除 hard_delete 物理删除 |
| `backend/app/crud/__init__.py` | 更新导入导出 |
| `backend/app/services/file_service.py` | 重写存储逻辑 |
| `backend/app/core/database.py` | 创建系统用户时去掉 is_admin |
| `backend/main.py` | lifespan 增加 ensure_default_groups |
| `backend/app/api/__init__.py` | 注册新的路由模块 |
| `frontend/src/stores/useUserStore.js` | 删除 isAdmin/isBan |
| `backend/app/crud/__init__.py` | 添加新 CRUD 模块的导出 |

---

### Task 1: Snowflake ID 生成器 — 新增 4 个实体类型

**Files:**
- Modify: `backend/app/utils/snowflake.py`

在文件末尾的类型常量区域和预创建生成器区域，新增 Group、GroupUserRelation、ProjectGroup、FileGroup 四个类型。

```python
# === 类型常量定义（追加） ===
GROUP_ID_TYPE = 21  # 用户组
GROUP_USER_RELATION_ID_TYPE = 22  # 用户组成员关系
PROJECT_GROUP_ID_TYPE = 23  # 项目组权限
FILE_GROUP_ID_TYPE = 24  # 文件组权限

# === 预创建生成器（追加） ===
group_id_gen = TypedSnowflakeIDGenerator(type_id=GROUP_ID_TYPE)
group_user_relation_id_gen = TypedSnowflakeIDGenerator(type_id=GROUP_USER_RELATION_ID_TYPE)
project_group_id_gen = TypedSnowflakeIDGenerator(type_id=PROJECT_GROUP_ID_TYPE)
file_group_id_gen = TypedSnowflakeIDGenerator(type_id=FILE_GROUP_ID_TYPE)

# === 便捷函数（追加） ===
def generate_group_id() -> int:
    return group_id_gen.generate_id()

def generate_group_user_relation_id() -> int:
    return group_user_relation_id_gen.generate_id()

def generate_project_group_id() -> int:
    return project_group_id_gen.generate_id()

def generate_file_group_id() -> int:
    return file_group_id_gen.generate_id()
```

- [ ] 在文件末尾追加 4 个类型常量
- [ ] 在预创建生成器区域追加 4 个生成器
- [ ] 在便捷函数区域追加 4 个便捷函数

---

### Task 2: 新建 groups.py 模型文件

**Files:**
- Create: `backend/app/models/groups.py`

```python
"""
用户组相关表 - 组管理、组成员、项目/文件权限
"""
from app.core.database import Base
from sqlalchemy import Column, Integer, String, BigInteger, Boolean, ForeignKey, Enum, Index, UniqueConstraint
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
```

- [ ] 创建 `backend/app/models/groups.py`

---

### Task 3: 修改 User 模型

**Files:**
- Modify: `backend/app/models/users.py`

删除 `is_admin` 和 `is_ban` 两列定义。

```python
# 删除这两行：
    is_admin = Column(Boolean, default=False)
    is_ban = Column(Boolean, default=False)
```

- [ ] 在 `backend/app/models/users.py` 中删除 `is_admin` 和 `is_ban` 列

---

### Task 4: 修改 File 模型

**Files:**
- Modify: `backend/app/models/files.py`

删除 storage_path，追加 folder_name、target_type、target_id。

```python
# 删除：
    storage_path = Column(String(500), nullable=False)  # 存储路径

# 在 uploader_id 后面追加：
    folder_name = Column(String(36), nullable=False)  # 所在文件夹 UUID

# 在 deleted_at 后面追加：
    target_type = Column(String(50), nullable=True)   # 关联目标类型
    target_id = Column(BigInteger, nullable=True)      # 关联目标 ID
```

- [ ] 删除 `storage_path` 列
- [ ] 追加 `folder_name`、`target_type`、`target_id` 列

---

### Task 5: 更新 models/__init__.py

**Files:**
- Modify: `backend/app/models/__init__.py`

```python
# 用户组
from app.models.groups import Group, GroupUserRelation, ProjectGroup, FileGroup, GroupType, GroupRole

__all__ = [
    # ... 现有内容 ...
    # 用户组
    "Group", "GroupUserRelation", "ProjectGroup", "FileGroup", "GroupType", "GroupRole",
]
```

- [ ] 追加 Group、GroupUserRelation、ProjectGroup、FileGroup 的导入和导出

---

### Task 6: CRUD — groups.py

**Files:**
- Create: `backend/app/crud/groups.py`

```python
"""
用户组 CRUD 操作
"""
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.groups import Group, GroupType
from typing import Optional, List
import os


async def get_group(db: AsyncSession, group_id: int) -> Optional[Group]:
    """根据 ID 获取组"""
    result = await db.execute(select(Group).where(Group.id == group_id))
    return result.scalar_one_or_none()


async def get_group_by_name(db: AsyncSession, name: str) -> Optional[Group]:
    """根据名称获取组"""
    result = await db.execute(select(Group).where(Group.name == name))
    return result.scalar_one_or_none()


async def create_group(
    db: AsyncSession,
    name: str,
    description: Optional[str] = None,
    group_type: GroupType = GroupType.USER,
) -> Group:
    """创建组"""
    group = Group(
        name=name,
        description=description,
        group_type=group_type,
    )
    db.add(group)
    await db.commit()
    await db.refresh(group)
    return group


async def update_group(
    db: AsyncSession,
    group_id: int,
    name: Optional[str] = None,
    description: Optional[str] = None,
) -> Optional[Group]:
    """更新组（system 组禁止修改 name）"""
    group = await get_group(db, group_id)
    if not group:
        return None
    if group.group_type == GroupType.SYSTEM:
        return None  # system 组不可修改
    if name is not None:
        group.name = name
    if description is not None:
        group.description = description
    await db.commit()
    await db.refresh(group)
    return group


async def delete_group(db: AsyncSession, group_id: int) -> bool:
    """删除组（system 组禁止删除）"""
    group = await get_group(db, group_id)
    if not group or group.group_type == GroupType.SYSTEM:
        return False
    await db.delete(group)
    await db.commit()
    return True


async def get_user_groups(db: AsyncSession, user_id: int) -> List[Group]:
    """获取用户所属的所有组"""
    from app.models.groups import GroupUserRelation
    result = await db.execute(
        select(Group)
        .join(GroupUserRelation, GroupUserRelation.group_id == Group.id)
        .where(GroupUserRelation.user_id == user_id)
    )
    return list(result.scalars().all())


async def get_all_groups(
    db: AsyncSession,
    page: int = 1,
    page_size: int = 20,
) -> List[Group]:
    """获取所有组（分页）"""
    result = await db.execute(
        select(Group)
        .order_by(desc(Group.created_at))
        .offset((page - 1) * page_size)
        .limit(page_size)
    )
    return list(result.scalars().all())


async def ensure_default_groups(db: AsyncSession) -> dict[str, Group]:
    """确保三个默认系统组存在，返回 {name: group} 字典"""
    default_names = ["admin", "default", "ban"]
    groups = {}
    for name in default_names:
        group = await get_group_by_name(db, name)
        if not group:
            group = await create_group(
                db=db,
                name=name,
                description=f"System {name} group",
                group_type=GroupType.SYSTEM,
            )
        groups[name] = group
    return groups
```

- [ ] 创建 `backend/app/crud/groups.py`

---

### Task 7: CRUD — group_user_relations.py

**Files:**
- Create: `backend/app/crud/group_user_relations.py`

```python
"""
用户组成员关系 CRUD 操作
"""
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.groups import GroupUserRelation, GroupRole, Group
from typing import Optional, List


async def add_member(
    db: AsyncSession,
    group_id: int,
    user_id: int,
    role: GroupRole = GroupRole.MEMBER,
) -> GroupUserRelation:
    """添加成员到组"""
    # 检查是否已存在
    existing = await db.execute(
        select(GroupUserRelation)
        .where(GroupUserRelation.group_id == group_id)
        .where(GroupUserRelation.user_id == user_id)
    )
    if existing.scalar_one_or_none():
        raise ValueError("User is already a member of this group")

    relation = GroupUserRelation(
        group_id=group_id,
        user_id=user_id,
        role=role,
    )
    db.add(relation)
    await db.commit()
    await db.refresh(relation)
    return relation


async def remove_member(db: AsyncSession, group_id: int, user_id: int) -> bool:
    """从组移除成员"""
    result = await db.execute(
        select(GroupUserRelation)
        .where(GroupUserRelation.group_id == group_id)
        .where(GroupUserRelation.user_id == user_id)
    )
    relation = result.scalar_one_or_none()
    if not relation:
        return False
    await db.delete(relation)
    await db.commit()
    return True


async def update_member_role(
    db: AsyncSession,
    group_id: int,
    user_id: int,
    role: GroupRole,
) -> Optional[GroupUserRelation]:
    """更新成员角色"""
    result = await db.execute(
        select(GroupUserRelation)
        .where(GroupUserRelation.group_id == group_id)
        .where(GroupUserRelation.user_id == user_id)
    )
    relation = result.scalar_one_or_none()
    if not relation:
        return None
    relation.role = role
    await db.commit()
    await db.refresh(relation)
    return relation


async def get_group_members(
    db: AsyncSession,
    group_id: int,
    page: int = 1,
    page_size: int = 20,
) -> List[dict]:
    """获取组成员列表（分页，含用户基本信息）"""
    from app.models.users import User
    result = await db.execute(
        select(GroupUserRelation, User)
        .join(User, GroupUserRelation.user_id == User.id)
        .where(GroupUserRelation.group_id == group_id)
        .order_by(GroupUserRelation.created_at)
        .offset((page - 1) * page_size)
        .limit(page_size)
    )
    rows = result.all()
    return [
        {
            "relation_id": rel.id,
            "user_id": user.id,
            "username": user.username,
            "email": user.email,
            "job_number": user.job_number,
            "role": rel.role.value,
            "created_at": rel.created_at,
        }
        for rel, user in rows
    ]


async def get_user_group_ids(db: AsyncSession, user_id: int) -> List[int]:
    """快速查询用户所属的组 ID 列表"""
    result = await db.execute(
        select(GroupUserRelation.group_id)
        .where(GroupUserRelation.user_id == user_id)
    )
    return list(result.scalars().all())


async def is_user_in_group(db: AsyncSession, user_id: int, group_id: int) -> bool:
    """判断用户是否在某组中"""
    result = await db.execute(
        select(GroupUserRelation)
        .where(GroupUserRelation.group_id == group_id)
        .where(GroupUserRelation.user_id == user_id)
    )
    return result.scalar_one_or_none() is not None


async def is_user_admin(db: AsyncSession, user_id: int) -> bool:
    """判断用户是否为管理员（在 admin 组中）"""
    group_result = await db.execute(
        select(Group).where(Group.name == "admin").where(Group.group_type == "system")
    )
    admin_group = group_result.scalar_one_or_none()
    if not admin_group:
        return False
    return await is_user_in_group(db, user_id, admin_group.id)


async def is_user_banned(db: AsyncSession, user_id: int) -> bool:
    """判断用户是否被封禁（在 ban 组中）"""
    group_result = await db.execute(
        select(Group).where(Group.name == "ban").where(Group.group_type == "system")
    )
    ban_group = group_result.scalar_one_or_none()
    if not ban_group:
        return False
    return await is_user_in_group(db, user_id, ban_group.id)
```

- [ ] 创建 `backend/app/crud/group_user_relations.py`

---

### Task 8: CRUD — file_access.py

**Files:**
- Create: `backend/app/crud/file_access.py`

```python
"""
文件/项目访问权限 CRUD 操作
"""
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.groups import ProjectGroup, FileGroup
from typing import List


# ========== 项目权限 ==========

async def grant_project_access(
    db: AsyncSession,
    project_id: int,
    group_id: int,
) -> ProjectGroup:
    """赋予组对项目的访问权限"""
    existing = await db.execute(
        select(ProjectGroup)
        .where(ProjectGroup.project_id == project_id)
        .where(ProjectGroup.group_id == group_id)
    )
    if existing.scalar_one_or_none():
        raise ValueError("Group already has access to this project")

    pg = ProjectGroup(project_id=project_id, group_id=group_id)
    db.add(pg)
    await db.commit()
    await db.refresh(pg)
    return pg


async def revoke_project_access(db: AsyncSession, project_id: int, group_id: int) -> bool:
    """撤销组对项目的访问权限"""
    result = await db.execute(
        select(ProjectGroup)
        .where(ProjectGroup.project_id == project_id)
        .where(ProjectGroup.group_id == group_id)
    )
    pg = result.scalar_one_or_none()
    if not pg:
        return False
    await db.delete(pg)
    await db.commit()
    return True


async def get_project_groups(db: AsyncSession, project_id: int) -> List[ProjectGroup]:
    """获取有权访问项目的所有组"""
    result = await db.execute(
        select(ProjectGroup).where(ProjectGroup.project_id == project_id)
    )
    return list(result.scalars().all())


# ========== 文件权限 ==========

async def grant_file_access(
    db: AsyncSession,
    file_id: int,
    group_id: int,
) -> FileGroup:
    """赋予组对文件的访问权限"""
    existing = await db.execute(
        select(FileGroup)
        .where(FileGroup.file_id == file_id)
        .where(FileGroup.group_id == group_id)
    )
    if existing.scalar_one_or_none():
        raise ValueError("Group already has access to this file")

    fg = FileGroup(file_id=file_id, group_id=group_id)
    db.add(fg)
    await db.commit()
    await db.refresh(fg)
    return fg


async def revoke_file_access(db: AsyncSession, file_id: int, group_id: int) -> bool:
    """撤销组对文件的访问权限"""
    result = await db.execute(
        select(FileGroup)
        .where(FileGroup.file_id == file_id)
        .where(FileGroup.group_id == group_id)
    )
    fg = result.scalar_one_or_none()
    if not fg:
        return False
    await db.delete(fg)
    await db.commit()
    return True


async def get_file_groups(db: AsyncSession, file_id: int) -> List[FileGroup]:
    """获取有权访问文件的所有组"""
    result = await db.execute(
        select(FileGroup).where(FileGroup.file_id == file_id)
    )
    return list(result.scalars().all())
```

- [ ] 创建 `backend/app/crud/file_access.py`

---

### Task 9: 修改 crud/users.py

**Files:**
- Modify: `backend/app/crud/users.py`

改动概览：
1. `create_user` 去掉 `is_admin` 参数，创建后自动加入 default 组
2. `update_user` 去掉 `is_admin`、`is_ban` 参数
3. 删除 `set_user_admin`、`ban_user` 方法
4. `get_user_list`、`count_users` 去掉 `is_admin`、`is_ban` 筛选参数

```python
# create_user 改动：
async def create_user(
    db: AsyncSession,
    username: str,
    password_hash: str,
    job_number: Optional[str] = None,
) -> User:
    user = User(
        username=username,
        password_hash=password_hash,
        job_number=job_number,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)

    # 自动加入 default 组
    from app.crud.groups import get_group_by_name
    from app.crud.group_user_relations import add_member
    from app.models.groups import GroupRole
    default_group = await get_group_by_name(db, "default")
    if default_group:
        await add_member(db, default_group.id, user.id, GroupRole.MEMBER)

    return user


# update_user 去掉 is_admin、is_ban 参数：
async def update_user(
    db: AsyncSession,
    user_id: int,
    username: Optional[str] = None,
    email: Optional[str] = None,
    password_hash: Optional[str] = None,
    job_number: Optional[str] = None,
) -> Optional[User]:
    user = await get_user(db, user_id)
    if not user:
        return None
    if username is not None:
        user.username = username
    if email is not None:
        user.email = email
    if password_hash is not None:
        user.password_hash = password_hash
    if job_number is not None:
        user.job_number = job_number
    await db.commit()
    await db.refresh(user)
    return user


# 删除这两个方法：
# set_user_admin  → 删除
# ban_user        → 删除


# get_user_list 去掉 is_admin、is_ban 参数：
async def get_user_list(
    db: AsyncSession,
    page: int = 1,
    page_size: int = 20,
) -> List[User]:
    query = select(User)
    query = query.order_by(desc(User.created_at))
    query = query.offset((page - 1) * page_size).limit(page_size)
    result = await db.execute(query)
    return list(result.scalars().all())


# count_users 去掉 is_admin、is_ban 参数：
async def count_users(db: AsyncSession) -> int:
    from sqlalchemy import func
    result = await db.execute(select(func.count(User.id)))
    return result.scalar()
```

- [ ] 修改 `create_user` — 去掉 is_admin 参数，加入 default 组
- [ ] 修改 `update_user` — 去掉 is_admin、is_ban 参数
- [ ] 删除 `set_user_admin`、`ban_user` 方法
- [ ] 修改 `get_user_list` — 去掉筛选参数
- [ ] 修改 `count_users` — 去掉筛选参数

---

### Task 10: 修改 crud/files.py

**Files:**
- Modify: `backend/app/crud/files.py`

改动：`create_file` 增加 `folder_name` 参数；`hard_delete_file` 不再删磁盘文件。

```python
# create_file 增加 folder_name 参数：
async def create_file(
    db: AsyncSession,
    filename: str,
    file_size: int,
    file_type: str,
    file_ext: str,
    folder_name: str,
    uploader_id: int,
    file_hash: Optional[str] = None,
    target_type: Optional[str] = None,
    target_id: Optional[int] = None,
) -> File:
    file = File(
        filename=filename,
        file_size=file_size,
        file_type=file_type,
        file_ext=file_ext,
        file_hash=file_hash,
        folder_name=folder_name,
        uploader_id=uploader_id,
        target_type=target_type,
        target_id=target_id,
    )
    db.add(file)
    await db.commit()
    await db.refresh(file)
    return file


# hard_delete_file 改为仅删数据库记录（物理文件由独立清理任务处理）：
async def hard_delete_file(db: AsyncSession, file_id: int) -> bool:
    """彻底删除文件记录（不删磁盘文件）"""
    file = await get_file(db, file_id)
    if not file:
        return False
    await db.delete(file)
    await db.commit()
    return True
```

- [ ] 修改 `create_file` — 增加 `folder_name` 等参数
- [ ] 修改 `hard_delete_file` — 移除删磁盘的逻辑

---

### Task 11: 重写 Services — file_service.py

**Files:**
- Modify: `backend/app/services/file_service.py`

重写存储逻辑，核心改动：
1. 使用 `folder_name` + 文件 `uuid` 构建磁盘路径
2. 自动管理文件夹上限
3. 接受可选哈希，未传则后端计算
4. 移除 `storage_path` 相关逻辑

```python
import os
import hashlib
import uuid as uuid_lib
from pathlib import Path
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from fastapi import UploadFile, HTTPException

from app.crud.files import create_file, get_file_by_uuid
from app.models.files import File


class FileService:
    """文件统一管理服务"""

    UPLOAD_DIR = os.getenv("FILE_PATH", "./uploads")
    MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE", "50")) * 1024 * 1024
    FOLDER_FILE_LIMIT = int(os.getenv("FOLDER_FILE_LIMIT", "1000"))

    ALLOWED_EXTENSIONS = {
        '.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg', '.bmp', '.ico',
        '.pdf', '.doc', '.docx', '.txt', '.md',
        '.mp3', '.wav', '.flac', '.mp4', '.avi', '.mov',
        '.zip', '.rar', '.7z', '.tar', '.gz',
        '.py', '.js', '.ts', '.json', '.xml', '.html', '.css',
    }

    def __init__(self, db: AsyncSession):
        self.db = db
        self._ensure_upload_dir()

    def _ensure_upload_dir(self):
        Path(self.UPLOAD_DIR).mkdir(parents=True, exist_ok=True)

    async def _get_writable_folder(self) -> str:
        """获取可写入的文件夹 UUID（未达上限的最早文件夹），若无则新建"""
        # 按 folder_name 分组统计文件数
        result = await self.db.execute(
            select(File.folder_name, func.count(File.id))
            .where(File.is_deleted == False)
            .group_by(File.folder_name)
            .order_by(func.min(File.created_at))
        )
        rows = result.all()
        for folder_name, count in rows:
            if count < self.FOLDER_FILE_LIMIT:
                return folder_name

        # 所有文件夹都满了或没有文件夹，新建一个
        new_folder = str(uuid_lib.uuid4())
        Path(self.UPLOAD_DIR, new_folder).mkdir(parents=True, exist_ok=True)
        return new_folder

    async def _compute_hash(self, content: bytes) -> str:
        return hashlib.sha256(content).hexdigest()

    async def upload_file(
        self,
        file: UploadFile,
        uploader_id: int,
        target_type: Optional[str] = None,
        target_id: Optional[int] = None,
        file_hash: Optional[str] = None,
        allow_duplicate: bool = False,
    ) -> File:
        content = await file.read()
        file_size = len(content)

        if file_size > self.MAX_FILE_SIZE:
            raise HTTPException(413, f"File too large (max {self.MAX_FILE_SIZE // 1024 // 1024}MB)")

        filename = file.filename or "unnamed"
        ext = os.path.splitext(filename)[1].lower()
        if ext not in self.ALLOWED_EXTENSIONS:
            raise HTTPException(415, f"Unsupported file type: {ext}")

        # 哈希：前端传入或后端计算
        if not file_hash:
            file_hash = await self._compute_hash(content)

        # 去重
        if not allow_duplicate:
            from app.crud.files import get_file_by_hash
            existing = await get_file_by_hash(self.db, file_hash)
            if existing:
                return existing

        # 获取可写文件夹
        folder_name = await self._get_writable_folder()

        # 创建 DB 记录（先 flush 获取 uuid）
        file_record = await create_file(
            db=self.db,
            filename=filename,
            file_size=file_size,
            file_type=file.content_type or "application/octet-stream",
            file_ext=ext,
            folder_name=folder_name,
            uploader_id=uploader_id,
            file_hash=file_hash,
            target_type=target_type,
            target_id=target_id,
        )

        # 写入磁盘：{UPLOAD_DIR}/{folder_name}/{uuid}
        disk_path = Path(self.UPLOAD_DIR, folder_name, str(file_record.uuid))
        with open(disk_path, "wb") as f:
            f.write(content)

        return file_record

    async def get_file_by_uuid(self, uuid: str) -> Optional[File]:
        return await get_file_by_uuid(self.db, uuid)

    async def get_file_content(self, file_record: File) -> Optional[bytes]:
        disk_path = Path(self.UPLOAD_DIR, file_record.folder_name, str(file_record.uuid))
        if not disk_path.exists():
            return None
        with open(disk_path, "rb") as f:
            return f.read()

    async def delete_file(self, file_id: int) -> bool:
        from app.crud.files import delete_file as crud_delete
        return await crud_delete(self.db, file_id)

    async def batch_upload(
        self,
        files: List[UploadFile],
        uploader_id: int,
        target_type: Optional[str] = None,
        target_id: Optional[int] = None,
    ) -> List[File]:
        results = []
        for f in files:
            record = await self.upload_file(
                file=f,
                uploader_id=uploader_id,
                target_type=target_type,
                target_id=target_id,
            )
            results.append(record)
        return results
```

- [ ] 重写 `backend/app/services/file_service.py`

---

### Task 12: Service — file_access_service.py

**Files:**
- Create: `backend/app/services/file_access_service.py`

```python
"""
文件访问权限服务 — 5 步访问判断
"""
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.files import File
from app.models.groups import FileGroup, ProjectGroup


async def check_file_access(
    db: AsyncSession,
    file: File,
    user_id: int,
) -> bool:
    """检查用户是否有权访问文件（5 步判断）"""
    # 1. 上传者直接通过
    if file.uploader_id == user_id:
        return True

    # 2. admin 组直接通过
    from app.crud.group_user_relations import is_user_admin
    if await is_user_admin(db, user_id):
        return True

    # 3. 查 FileGroup：用户的组被直接授权
    from app.crud.group_user_relations import get_user_group_ids
    user_group_ids = await get_user_group_ids(db, user_id)
    if user_group_ids:
        fg_result = await db.execute(
            select(FileGroup)
            .where(FileGroup.file_id == file.id)
            .where(FileGroup.group_id.in_(user_group_ids))
        )
        if fg_result.scalar_one_or_none():
            return True

    # 4. 通过 file.target 查 ProjectGroup
    if file.target_type == "project" and file.target_id and user_group_ids:
        pg_result = await db.execute(
            select(ProjectGroup)
            .where(ProjectGroup.project_id == file.target_id)
            .where(ProjectGroup.group_id.in_(user_group_ids))
        )
        if pg_result.scalar_one_or_none():
            return True

    # 5. 拒绝
    return False
```

- [ ] 创建 `backend/app/services/file_access_service.py`

---

### Task 13: 修改 database.py

**Files:**
- Modify: `backend/app/core/database.py`

在 `ensure_system_user_exists` 中，去掉 `is_admin=True`：

```python
# 将：
new_user = User(
    username=username,
    password_hash=password_hash,
    is_admin=True,
    is_system=True,
    job_number="10000"
)

# 改为：
new_user = User(
    username=username,
    password_hash=password_hash,
    is_system=True,
    job_number="10000"
)
```

- [ ] 去掉 `is_admin=True`

---

### Task 14: 修改 main.py — 启动时校验默认组

**Files:**
- Modify: `backend/main.py`

在 lifespan 的 `ensure_system_user_exists()` 之后添加：

```python
from app.crud.groups import ensure_default_groups

@asynccontextmanager
async def lifespan(app: FastAPI):
    await ensure_database_exists()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("数据表创建/检查完成！")

    await ensure_system_user_exists()

    async with AsyncSessionLocal() as session:
        await ensure_default_groups(session)
    print("默认用户组检查完成！")

    yield
    print("关闭数据库连接...")
    await engine.dispose()
```

- [ ] 在 lifespan 中调用 `ensure_default_groups`

---

### Task 15: API 路由 — 通用鉴权依赖

**Files:**
- Create: `backend/app/api/deps.py`

```python
"""API 依赖项"""
from fastapi import Header, HTTPException


async def get_current_user_id(x_user_id: int = Header(...)) -> int:
    """从 X-User-Id 请求头获取用户 ID（临时方案，后续替换为 JWT 中间件）"""
    return x_user_id
```

- [ ] 创建 `backend/app/api/deps.py`

---

### Task 16: API 路由 — files.py

**Files:**
- Create: `backend/app/api/files.py`

```python
"""文件 API 路由"""
import uuid
from typing import Optional
from fastapi import APIRouter, Depends, UploadFile, File as FileForm, Form, HTTPException, Query, Body
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import Response

from app.core.database import get_db
from app.api.deps import get_current_user_id
from app.services.file_service import FileService
from app.services.file_access_service import check_file_access
from app.crud.files import get_file_by_uuid, get_user_files, count_user_files

router = APIRouter(prefix="/api/files", tags=["files"])


@router.post("/upload")
async def upload_file(
    file: UploadFile = FileForm(...),
    target_type: Optional[str] = Form(None),
    target_id: Optional[int] = Form(None),
    x_file_hash: Optional[str] = Header(None),
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    svc = FileService(db)
    record = await svc.upload_file(
        file=file,
        uploader_id=user_id,
        target_type=target_type,
        target_id=target_id,
        file_hash=x_file_hash,
    )
    return {
        "uuid": record.uuid,
        "filename": record.filename,
        "file_size": record.file_size,
        "file_type": record.file_type,
        "file_ext": record.file_ext,
    }


@router.get("/{file_uuid}")
async def get_file_meta(
    file_uuid: str,
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    record = await get_file_by_uuid(db, file_uuid)
    if not record or record.is_deleted:
        raise HTTPException(404, "File not found")
    if not await check_file_access(db, record, user_id):
        raise HTTPException(403, "Access denied")
    return {
        "uuid": record.uuid,
        "filename": record.filename,
        "file_size": record.file_size,
        "file_type": record.file_type,
        "file_ext": record.file_ext,
        "uploader_id": record.uploader_id,
        "target_type": record.target_type,
        "target_id": record.target_id,
        "created_at": record.created_at,
    }


@router.get("/{file_uuid}/download")
async def download_file(
    file_uuid: str,
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    svc = FileService(db)
    record = await svc.get_file_by_uuid(file_uuid)
    if not record or record.is_deleted:
        raise HTTPException(404, "File not found")
    if not await check_file_access(db, record, user_id):
        raise HTTPException(403, "Access denied")

    content = await svc.get_file_content(record)
    if content is None:
        raise HTTPException(404, "File content not found on disk")

    return Response(
        content=content,
        media_type=record.file_type,
        headers={
            "Content-Disposition": f'attachment; filename="{record.filename}"'
        },
    )


@router.get("")
async def list_files(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    file_type: Optional[str] = Query(None),
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    if file_type:
        from app.crud.files import get_files_by_type
        files = await get_files_by_type(db, file_type, page, page_size)
        total = len(files)
    else:
        files = await get_user_files(db, user_id, page, page_size)
        total = await count_user_files(db, user_id)

    return {
        "items": [
            {
                "uuid": f.uuid,
                "filename": f.filename,
                "file_size": f.file_size,
                "file_type": f.file_type,
                "file_ext": f.file_ext,
                "target_type": f.target_type,
                "target_id": f.target_id,
                "folder_name": f.folder_name,
                "created_at": f.created_at,
            }
            for f in files
        ],
        "total": total,
        "page": page,
        "page_size": page_size,
    }


@router.delete("/{file_uuid}")
async def delete_file_route(
    file_uuid: str,
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    svc = FileService(db)
    record = await svc.get_file_by_uuid(file_uuid)
    if not record or record.is_deleted:
        raise HTTPException(404, "File not found")
    if record.uploader_id != user_id:
        raise HTTPException(403, "Only the uploader can delete this file")
    await svc.delete_file(record.id)
    return {"message": "File deleted"}


@router.put("/{file_uuid}/restore")
async def restore_file_route(
    file_uuid: str,
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    record = await get_file_by_uuid(db, file_uuid)
    if not record:
        raise HTTPException(404, "File not found")
    if record.uploader_id != user_id:
        raise HTTPException(403, "Only the uploader can restore this file")
    from app.crud.files import restore_file as crud_restore
    await crud_restore(db, record.id)
    return {"message": "File restored"}


@router.put("/{file_uuid}")
async def update_file_meta(
    file_uuid: str,
    target_type: Optional[str] = Body(None),
    target_id: Optional[int] = Body(None),
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    record = await get_file_by_uuid(db, file_uuid)
    if not record or record.is_deleted:
        raise HTTPException(404, "File not found")
    if record.uploader_id != user_id:
        raise HTTPException(403, "Only the uploader can update this file")
    if target_type is not None:
        record.target_type = target_type
    if target_id is not None:
        record.target_id = target_id
    await db.commit()
    return {"message": "File updated"}


@router.post("/batch-delete")
async def batch_delete_files(
    uuids: list[str],
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    from app.crud.files import batch_delete_files as crud_batch_delete
    from sqlalchemy import select
    result = await db.execute(
        select(File.id).where(File.uuid.in_(uuids)).where(File.uploader_id == user_id)
    )
    file_ids = list(result.scalars().all())
    if not file_ids:
        raise HTTPException(404, "No files found")
    count = await crud_batch_delete(db, file_ids, uploader_id=user_id)
    return {"deleted_count": count}
```

**注意：** `restore_file` 和 `update_user` 需要在 `crud/files.py` 中导出或修复导入。实际上 `restore_file` 已经存在，但需要确认导出。让我用正确的导入：

```python
from app.crud.files import restore_file as crud_restore
```

而 `update_user` 不需要 — `update_file_meta` 路由中直接操作 `record` 属性。

- [ ] 创建 `backend/app/api/files.py`

---

### Task 17: API 路由 — groups.py

**Files:**
- Create: `backend/app/api/groups.py`

```python
"""用户组 API 路由"""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.api.deps import get_current_user_id
from app.crud.groups import (
    get_group, get_group_by_name, create_group, update_group, delete_group,
    get_user_groups, get_all_groups,
)
from app.crud.group_user_relations import (
    add_member, remove_member, update_member_role, get_group_members,
    is_user_in_group,
)
from app.crud.file_access import (
    grant_project_access, revoke_project_access,
    grant_file_access, revoke_file_access,
)
from app.models.groups import GroupType, GroupRole
from app.models.files import File
from sqlalchemy import select

router = APIRouter(prefix="/api/groups", tags=["groups"])


@router.post("")
async def create_group_route(
    name: str,
    description: Optional[str] = None,
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    existing = await get_group_by_name(db, name)
    if existing:
        raise HTTPException(409, "Group name already exists")
    group = await create_group(db, name=name, description=description)
    return {"id": group.id, "name": group.name, "group_type": group.group_type.value}


@router.get("")
async def list_groups(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    groups = await get_user_groups(db, user_id)
    return {
        "items": [
            {"id": g.id, "name": g.name, "group_type": g.group_type.value}
            for g in groups
        ],
        "total": len(groups),
    }


@router.get("/{group_id}")
async def get_group_route(
    group_id: int,
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    group = await get_group(db, group_id)
    if not group:
        raise HTTPException(404, "Group not found")
    members = await get_group_members(db, group_id, page=1, page_size=100)
    return {
        "id": group.id,
        "name": group.name,
        "description": group.description,
        "group_type": group.group_type.value,
        "members": members,
        "created_at": group.created_at,
    }


@router.put("/{group_id}")
async def update_group_route(
    group_id: int,
    name: Optional[str] = None,
    description: Optional[str] = None,
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    group = await update_group(db, group_id, name=name, description=description)
    if not group:
        raise HTTPException(404, "Group not found or is a system group")
    return {"id": group.id, "name": group.name}


@router.delete("/{group_id}")
async def delete_group_route(
    group_id: int,
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    success = await delete_group(db, group_id)
    if not success:
        raise HTTPException(404, "Group not found or is a system group")
    return {"message": "Group deleted"}


@router.post("/{group_id}/members")
async def add_member_route(
    group_id: int,
    member_user_id: int,
    role: str = "member",
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    group = await get_group(db, group_id)
    if not group:
        raise HTTPException(404, "Group not found")
    try:
        relation = await add_member(db, group_id, member_user_id, GroupRole(role))
        return {"relation_id": relation.id, "user_id": member_user_id, "role": role}
    except ValueError as e:
        raise HTTPException(409, str(e))


@router.delete("/{group_id}/members/{member_user_id}")
async def remove_member_route(
    group_id: int,
    member_user_id: int,
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    success = await remove_member(db, group_id, member_user_id)
    if not success:
        raise HTTPException(404, "Member not found in group")
    return {"message": "Member removed"}


@router.put("/{group_id}/members/{member_user_id}")
async def update_member_role_route(
    group_id: int,
    member_user_id: int,
    role: str,
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    relation = await update_member_role(db, group_id, member_user_id, GroupRole(role))
    if not relation:
        raise HTTPException(404, "Member not found in group")
    return {"relation_id": relation.id, "role": role}


@router.post("/{group_id}/projects/{project_id}")
async def grant_project_route(
    group_id: int,
    project_id: int,
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    try:
        pg = await grant_project_access(db, project_id, group_id)
        return {"id": pg.id}
    except ValueError as e:
        raise HTTPException(409, str(e))


@router.delete("/{group_id}/projects/{project_id}")
async def revoke_project_route(
    group_id: int,
    project_id: int,
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    success = await revoke_project_access(db, project_id, group_id)
    if not success:
        raise HTTPException(404, "Access rule not found")
    return {"message": "Access revoked"}


@router.post("/{group_id}/files/{file_uuid}")
async def grant_file_route(
    group_id: int,
    file_uuid: str,
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    file_result = await db.execute(select(File).where(File.uuid == file_uuid))
    file = file_result.scalar_one_or_none()
    if not file:
        raise HTTPException(404, "File not found")
    try:
        fg = await grant_file_access(db, file.id, group_id)
        return {"id": fg.id}
    except ValueError as e:
        raise HTTPException(409, str(e))


@router.delete("/{group_id}/files/{file_uuid}")
async def revoke_file_route(
    group_id: int,
    file_uuid: str,
    user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    file_result = await db.execute(select(File).where(File.uuid == file_uuid))
    file = file_result.scalar_one_or_none()
    if not file:
        raise HTTPException(404, "File not found")
    success = await revoke_file_access(db, file.id, group_id)
    if not success:
        raise HTTPException(404, "Access rule not found")
    return {"message": "Access revoked"}
```

- [ ] 创建 `backend/app/api/groups.py`

---

### Task 18: 注册路由

**Files:**
- Modify: `backend/app/api/__init__.py`

```python
# API Routes
from app.api.files import router as files_router
from app.api.groups import router as groups_router
```

- [ ] 在 `backend/app/api/__init__.py` 中导入两个路由模块

修改 `backend/main.py`，注册路由：

```python
# 在 app = FastAPI(lifespan=lifespan) 后面添加：
from app.api.files import router as files_router
from app.api.groups import router as groups_router
app.include_router(files_router)
app.include_router(groups_router)
```

- [ ] 在 `backend/main.py` 中 include_router

---

### Task 19: 更新 crud/__init__.py

**Files:**
- Modify: `backend/app/crud/__init__.py`

```python
# 用户组
from app.crud.groups import (
    get_group, get_group_by_name, create_group, update_group, delete_group,
    get_user_groups, get_all_groups, ensure_default_groups,
)
from app.crud.group_user_relations import (
    add_member, remove_member, update_member_role,
    get_group_members, get_user_group_ids,
    is_user_in_group, is_user_admin, is_user_banned,
)
from app.crud.file_access import (
    grant_project_access, revoke_project_access, get_project_groups,
    grant_file_access, revoke_file_access, get_file_groups,
)

# 在 __all__ 中添加：
    # 用户组
    "get_group", "get_group_by_name", "create_group", "update_group", "delete_group",
    "get_user_groups", "get_all_groups", "ensure_default_groups",
    "add_member", "remove_member", "update_member_role",
    "get_group_members", "get_user_group_ids",
    "is_user_in_group", "is_user_admin", "is_user_banned",
    "grant_project_access", "revoke_project_access", "get_project_groups",
    "grant_file_access", "revoke_file_access", "get_file_groups",
```

同时在 users CRUD 的导出中删除 `set_user_admin`、`ban_user`：

- [ ] 更新 `backend/app/crud/__init__.py` 导入和导出

---

### Task 20: 前端 — useUserStore

**Files:**
- Modify: `frontend/src/stores/useUserStore.js`

```javascript
// 删除这两行：
const isAdmin = ref(false)
const isBan = ref(false)

// 从 return 中删除：
    isAdmin,
    isBan,
```

- [ ] 删除 isAdmin、isBan 响应式变量和返回值
