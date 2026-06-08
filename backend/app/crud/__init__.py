# CRUD Operations

# 用户
from app.crud.users import (
    # User
    get_user, get_user_by_username, get_user_by_email, get_user_by_job_number, create_user, update_user,
    delete_user, update_user_login_time,
    get_user_list, count_users, get_users_by_ids,
    # UserTag
    get_user_tag, get_user_tag_by_name, create_user_tag, update_user_tag,
    delete_user_tag, get_all_user_tags,
    # UserTagRelation
    get_user_tag_relation, add_user_tag, remove_user_tag, get_user_tags,
    get_tag_users, batch_add_user_tags,
)

# 用户组
from app.crud.groups import (
    get_group, get_group_by_name, create_group, update_group, delete_group,
    get_user_groups, get_all_groups, ensure_default_groups,
)
from app.crud.group_user_relations import (
    add_member, remove_member, update_member_role,
    get_group_members, get_user_group_ids,
    is_user_in_group, is_user_admin, is_user_banned,
    is_admin, is_ban,
    add_user_to_pending, approve_user, reject_user,
    is_user_pending, get_pending_users,
)
from app.crud.file_access import (
    grant_project_access, revoke_project_access, get_project_groups,
    grant_file_access, revoke_file_access, get_file_groups,
)

# 项目
from app.crud.projects import (
    # Project
    get_project, get_project_by_name, create_project, update_project,
    delete_project, start_project, close_project, get_project_list, count_projects,
    # ProjectTag
    get_project_tag, get_project_tag_by_name, create_project_tag, update_project_tag,
    delete_project_tag, get_all_project_tags,
    # ProjectTagRelation
    get_project_tag_relation, add_project_tag, remove_project_tag, get_project_tags,
    get_tag_projects, batch_add_project_tags, sync_project_tags,
)

# 项目成员
from app.crud.project_members import (
    get_project_member, add_project_member, update_member_role, remove_project_member,
    get_project_members, get_user_projects, get_member_count, has_member_permission,
    is_project_owner, is_project_admin, is_project_contributor, is_project_editor,
    is_project_member, is_project_viewer, batch_add_project_members,
)

# 分支
from app.crud.branches import (
    get_branch, get_branch_by_name, create_branch, update_branch, delete_branch,
    update_branch_status, get_project_branches, get_branch_page, clone_branch_pages,
    get_main_branch, create_branch_from_template,
)

# 合并请求
from app.crud.merge_requests import (
    get_merge_request, create_merge_request, update_merge_request,
    approve_merge_request, reject_merge_request, merge_request, cancel_merge_request,
    get_merge_requests, count_merge_requests, get_pending_merge_requests, can_merge,
)

# 文件
from app.crud.files import (
    get_file, get_file_by_uuid, get_file_by_hash, create_file, delete_file,
    hard_delete_file, restore_file, get_user_files, count_user_files,
    get_user_storage_size, get_duplicate_file, get_files_by_type, batch_delete_files,
)

# 文件包
from app.crud.file_packages import (
    get_file_package, create_file_package, update_file_package, delete_file_package,
    get_project_packages, get_page_packages, add_file_to_package, remove_file_from_package,
    get_package_files, batch_add_files_to_package, extract_zip_package, create_zip_from_package,
)

# 分支版本
from app.crud.branch_versions import (
    get_branch_version, create_branch_version, create_branch_version_by_name, compare_branch_versions,
    get_branch_version_history, get_version_details, get_version_changes,
    get_current_version, detect_file_changes,
)

# 通知
from app.crud.notifications import (
    get_notification, create_notification, mark_notification_read, mark_notification_unread,
    delete_notification, get_user_notifications, count_user_notifications, get_unread_count,
    mark_all_read, delete_all_read, batch_create_notifications,
)

# 页面
from app.crud.pages import (
    get_page, create_page, update_page, delete_page,
    get_project_pages, get_page_folder_tree, move_page,
)

# 组件
from app.crud.components import (
    get_component, get_component_by_key, create_component, update_component,
    delete_component, get_page_component_relation, add_component_to_page,
    update_component_order, remove_component_from_page, get_page_components,
    batch_add_components_to_page, sync_page_components,
    get_components_by_type, get_component_type_stats,
)

# 分支版本管理服务层（一键式方法）
from app.services.branch_service import (
    commit,
    commit_by_name,
    create_branch_clone,
    execute_merge,
)

__all__ = [
    # 用户
    "get_user", "get_user_by_username", "get_user_by_email", "get_user_by_job_number", "create_user", "update_user",
    "delete_user", "update_user_login_time",
    "get_user_list", "count_users", "get_users_by_ids",
    "get_user_tag", "get_user_tag_by_name", "create_user_tag", "update_user_tag",
    "delete_user_tag", "get_all_user_tags",
    "get_user_tag_relation", "add_user_tag", "remove_user_tag", "get_user_tags",
    "get_tag_users", "batch_add_user_tags",
    # 项目
    "get_project", "get_project_by_name", "create_project", "update_project",
    "delete_project", "start_project", "close_project", "get_project_list", "count_projects",
    "get_project_tag", "get_project_tag_by_name", "create_project_tag", "update_project_tag",
    "delete_project_tag", "get_all_project_tags",
    "get_project_tag_relation", "add_project_tag", "remove_project_tag", "get_project_tags",
    "get_tag_projects", "batch_add_project_tags", "sync_project_tags",
    # 项目成员
    "get_project_member", "add_project_member", "update_member_role", "remove_project_member",
    "get_project_members", "get_user_projects", "get_member_count", "has_member_permission",
    "is_project_owner", "is_project_admin", "is_project_contributor", "is_project_editor",
    "is_project_member", "is_project_viewer", "batch_add_project_members",
    # 分支
    "get_branch", "get_branch_by_name", "create_branch", "update_branch", "delete_branch",
    "update_branch_status", "get_project_branches", "get_branch_page", "clone_branch_pages",
    "get_main_branch", "create_branch_from_template",
    # 合并请求
    "get_merge_request", "create_merge_request", "update_merge_request",
    "approve_merge_request", "reject_merge_request", "merge_request", "cancel_merge_request",
    "get_merge_requests", "count_merge_requests", "get_pending_merge_requests", "can_merge",
    # 用户组
    "get_group", "get_group_by_name", "create_group", "update_group", "delete_group",
    "get_user_groups", "get_all_groups", "ensure_default_groups",
    "add_member", "remove_member", "update_member_role",
    "get_group_members", "get_user_group_ids",
    "is_user_in_group", "is_user_admin", "is_user_banned",
    "is_admin", "is_ban",
    "add_user_to_pending", "approve_user", "reject_user",
    "is_user_pending", "get_pending_users",
    "grant_project_access", "revoke_project_access", "get_project_groups",
    "grant_file_access", "revoke_file_access", "get_file_groups",
    # 文件
    "get_file", "get_file_by_uuid", "get_file_by_hash", "create_file", "delete_file",
    "hard_delete_file", "restore_file", "get_user_files", "count_user_files",
    "get_user_storage_size", "get_duplicate_file", "get_files_by_type", "batch_delete_files",
    # 文件包
    "get_file_package", "create_file_package", "update_file_package", "delete_file_package",
    "get_project_packages", "get_page_packages", "add_file_to_package", "remove_file_from_package",
    "get_package_files", "batch_add_files_to_package", "extract_zip_package", "create_zip_from_package",
    # 分支版本
    "get_branch_version", "create_branch_version", "create_branch_version_by_name", "compare_branch_versions",
    "get_branch_version_history", "get_version_details", "get_version_changes",
    "get_current_version", "detect_file_changes",
    # 通知
    "get_notification", "create_notification", "mark_notification_read", "mark_notification_unread",
    "delete_notification", "get_user_notifications", "count_user_notifications", "get_unread_count",
    "mark_all_read", "delete_all_read", "batch_create_notifications",
    # 页面
    "get_page", "create_page", "update_page", "delete_page",
    "get_project_pages", "get_page_folder_tree", "move_page",
    # 组件
    "get_component", "get_component_by_key", "create_component", "update_component",
    "delete_component", "get_page_component_relation", "add_component_to_page",
    "update_component_order", "remove_component_from_page", "get_page_components",
    "batch_add_components_to_page", "sync_page_components",
    "get_components_by_type", "get_component_type_stats",
    # 分支版本管理服务层
    "commit", "commit_by_name", "create_branch_clone", "execute_merge",
]
