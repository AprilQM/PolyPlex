# 用户组系统 & 文件 API — 设计文档

## 目标

引入基于用户组（Group）的权限系统，替代目前 User 表上的 `is_admin`/`is_ban` 布尔字段；同时将已有的文件管理后端通过 REST API 暴露出来。

## 范围

1. 用户组模型及成员关系、角色权限
2. 用组成员身份替代 `is_admin`/`is_ban`
3. 项目级别和文件级别的组权限控制
4. 文件 REST API 端点（上传、下载、列表、删除、更新）
5. 启动时校验三大默认系统组
6. 创建用户时自动加入 default 组

## 模型

### Group（groups 表）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | BigInteger PK | Snowflake |
| name | String(100), unique, not null | 组名 |
| description | String(500), nullable | 描述 |
| group_type | Enum: system/user | system = 不可变（不可删除/改名） |
| created_at | BigInteger | Unix 时间戳 |
| updated_at | BigInteger | Unix 时间戳 |

启动时自动创建的三个系统组：
- **admin** — 管理员，拥有系统级权限
- **default** — 普通用户，创建用户时自动加入
- **ban** — 封禁用户，加入即视为封禁

### GroupUserRelation（group_user_relations 表）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | BigInteger PK | Snowflake |
| group_id | BigInteger FK → groups.id | 所属组 |
| user_id | BigInteger FK → users.id | 用户 |
| role | Enum: owner/admin/member | 应用层角色 |
| permissions | BigInteger | 位掩码，供未来细粒度权限扩展 |
| created_at | BigInteger | |
| updated_at | BigInteger | |

唯一约束：(group_id, user_id)。

各角色的默认权限位掩码：
- member: VIEW + EDIT（位 0-1）
- admin: + DELETE + MANAGE_MEMBERS（位 0-3）
- owner: + MANAGE_GROUP（位 0-4）

### ProjectGroup（project_groups 表）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | BigInteger PK | Snowflake |
| project_id | BigInteger FK → projects.id | 项目 |
| group_id | BigInteger FK → groups.id | 有权限的组 |
| created_at | BigInteger | |

唯一约束：(project_id, group_id)。

### FileGroup（file_groups 表）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | BigInteger PK | Snowflake |
| file_id | BigInteger FK → files.id | 文件 |
| group_id | BigInteger FK → groups.id | 额外授权的组 |
| created_at | BigInteger | |

唯一约束：(file_id, group_id)。

### File 模型改动

现有 `files` 表：
- 删除 `storage_path` 列
- 增加 `folder_name` String(36), not null — 文件所在文件夹的 UUID 名称
- 增加 `target_type` String(50), nullable — 关联目标类型，如 "project"、"page"
- 增加 `target_id` BigInteger, nullable — 关联目标 ID

磁盘存储规则：
- 文件路径：`{UPLOAD_DIR}/{folder_name}/{uuid}`
- uuid 即 File 记录的 uuid 字段（无后缀）
- 原始文件名（含后缀）存储在 `filename` 列
- 响应下载时从 DB 取原始文件名作为 Content-Disposition

## 文件存储策略

### 文件夹管理

- 上传目录结构：`{UPLOAD_DIR}/{folder_uuid}/{file_uuid}`
- 每个文件夹有存储上限（默认 1000 个文件，可通过 `FOLDER_FILE_LIMIT` 环境变量配置）
- 上传时获取当前可写入的文件夹（未达上限的最早文件夹），若无则新建 UUID 文件夹
- 文件夹元信息仅存在于 DB 的 `folder_name` 列和磁盘目录中，不作为独立资源暴露

### 文件哈希

- 前端可选传入 `X-File-Hash`（SHA-256 十六进制字符串）
- 若传入：后端直接用于去重判断，不做验证（节省服务器 CPU）
- 未传入：后端计算 SHA-256
- 哈希仅用于去重优化，非安全边界；伪造哈希最多导致重复存储

## 数据流 — 访问控制

```
文件访问判断（按顺序）：
1. 用户是上传者？ → 是：允许所有操作
2. 用户在 admin 组？ → 是：允许所有操作
3. 查 FileGroup：用户的组被直接授权？ → 是：允许
4. 通过 file.target 查 ProjectGroup：用户的组在项目级别有权限？ → 是：允许
5. → 拒绝访问
```

## API 端点

### 文件 API（`/api/files`）

| 方法 | 路径 | 鉴权 | 说明 |
|------|------|------|------|
| POST | `/api/files/upload` | X-User-Id, X-File-Hash(可选) | 上传文件（支持单文件/批量 multipart），可选传入 SHA-256 哈希 |
| GET | `/api/files/{uuid}` | X-User-Id | 获取文件元信息 |
| GET | `/api/files/{uuid}/download` | X-User-Id | 下载文件内容（Content-Disposition 使用原始文件名） |
| GET | `/api/files` | X-User-Id | 获取用户文件列表（分页，可按类型筛选） |
| DELETE | `/api/files/{uuid}` | X-User-Id | 软删除文件 |
| PUT | `/api/files/{uuid}/restore` | X-User-Id | 恢复已删除文件 |
| PUT | `/api/files/{uuid}` | X-User-Id | 更新文件元信息（target_type、target_id） |
| POST | `/api/files/batch-delete` | X-User-Id | 批量软删除 |

鉴权方式暂用 `X-User-Id` 请求头（JWT 中间件单独规划）。

### 用户组 API（`/api/groups`）

| 方法 | 路径 | 鉴权 | 说明 |
|------|------|------|------|
| POST | `/api/groups` | X-User-Id | 创建组 |
| GET | `/api/groups` | X-User-Id | 获取用户所在的组列表 |
| GET | `/api/groups/{id}` | X-User-Id | 获取组详情（含成员列表） |
| PUT | `/api/groups/{id}` | X-User-Id | 更新组信息（system 组禁止修改） |
| DELETE | `/api/groups/{id}` | X-User-Id | 删除组（system 组禁止删除） |
| POST | `/api/groups/{id}/members` | X-User-Id | 添加成员到组 |
| DELETE | `/api/groups/{id}/members/{user_id}` | X-User-Id | 移除组成员 |
| PUT | `/api/groups/{id}/members/{user_id}` | X-User-Id | 更新成员角色 |
| POST | `/api/groups/{id}/projects/{project_id}` | X-User-Id | 赋予组对项目的访问权限 |
| DELETE | `/api/groups/{id}/projects/{project_id}` | X-User-Id | 撤销组对项目的访问权限 |
| POST | `/api/groups/{id}/files/{file_uuid}` | X-User-Id | 赋予组对文件的访问权限 |
| DELETE | `/api/groups/{id}/files/{file_uuid}` | X-User-Id | 撤销组对文件的访问权限 |

## 启动改动

在 `main.py` 的 lifespan 中，创建完数据库和系统用户后：
1. 确保三个默认组存在（按 name 查询，缺失则创建）
2. 标记 `group_type = "system"`

## CRUD 模块

### groups.py
- `get_group`、`get_group_by_name`、`create_group`、`update_group`、`delete_group`
- `get_user_groups` — 用户所属的所有组
- `get_all_groups` — 分页列表
- `ensure_default_groups` — 幂等启动函数

### group_user_relations.py
- `add_member`、`remove_member`、`update_member_role`
- `get_group_members` — 分页成员列表含角色
- `get_user_group_ids` — 快速查询用户所属组 ID
- `is_user_in_group`、`is_user_admin`、`is_user_banned`

### file_access.py
- `check_file_access` — 5 步访问判断函数（放置于 services 层，因需跨表查询）
- `grant_project_access`、`revoke_project_access`、`get_project_groups`
- `grant_file_access`、`revoke_file_access`、`get_file_groups`

## 需修改的文件

- `backend/app/models/users.py` — 删除 `is_admin`、`is_ban`
- `backend/app/models/files.py` — 追加 `target_type`、`target_id`、`folder_name`；删除 `storage_path`
- `backend/app/models/__init__.py` — 添加 Group、GroupUserRelation、ProjectGroup、FileGroup
- `backend/app/crud/users.py` — 去除 is_admin/is_ban 参数，创建用户时加入 default 组
- `backend/app/crud/files.py` — 适配 folder_name 替代 storage_path，移除 hard_delete 中删磁盘的逻辑（后续由文件清理服务处理）
- `backend/app/crud/__init__.py` — 更新导入导出
- `backend/app/services/file_service.py` — 重写存储逻辑（文件夹管理、hash 策略、新路径规则）
- `backend/app/core/database.py` — 创建系统用户时不再设置 is_admin
- `backend/main.py` — lifespan 增加 ensure_default_groups
- `backend/app/api/__init__.py` — 注册路由
- `frontend/src/stores/useUserStore.js` — 删除 isAdmin/isBan

## 不在此范围内的内容

- JWT 认证中间件（独立任务）
- 前端组管理界面
- 前端文件管理界面
- 文件关联关系（如文件与页面、项目的关联逻辑，后续开发中完善）
- Redis / ChromaDB 集成
- AI 集成
