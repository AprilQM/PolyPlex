"""Pydantic 请求/响应模型

分层规范：
- api/ 层从 schemas 导入 request/response 模型
- 所有接口函数的参数和返回值都应使用 schema 类型标注
"""

from app.schemas.auth import (
    EncryptedLoginRequest,
    EncryptedRegisterRequest,
    VerifyCodeRequest,
    LoginResponse,
    RegisterResponse,
    UserInfo,
)
from app.schemas.projects import (
    ProjectCreate,
    ProjectUpdate,
    ProjectResponse,
    ProjectListResponse,
    ProjectTagCreate,
    ProjectTagUpdate,
    ProjectTagResponse,
    AddProjectTagRequest,
    SyncProjectTagsRequest,
)
from app.schemas.members import (
    AddMemberRequest,
    BatchAddMembersRequest,
    UpdateMemberRoleRequest,
    MemberResponse,
    MemberListResponse,
)
from app.schemas.branches import (
    BranchCreate,
    BranchUpdate,
    BranchUpdateStatus,
    BranchResponse,
    BranchListResponse,
)
from app.schemas.pages import (
    PageCreate,
    PageUpdate,
    PageResponse,
    PageTreeItem,
    MovePageRequest,
)
from app.schemas.components import (
    ComponentCreate,
    ComponentUpdate,
    ComponentResponse,
    AddComponentToPageRequest,
    UpdateComponentOrderRequest,
    PageComponentResponse,
    SyncPageComponentsRequest,
)
from app.schemas.merge_requests import (
    MergeRequestCreate,
    MergeRequestUpdate,
    MergeRequestReview,
    MergeRequestResponse,
    MergeRequestListResponse,
)
from app.schemas.branch_versions import (
    PageChangeItem,
    VersionCreate,
    VersionResponse,
    VersionHistoryResponse,
    ChangeDetail,
    VersionDiffResponse,
)
from app.schemas.notifications import (
    NotificationResponse,
    NotificationListResponse,
)
from app.schemas.file_packages import (
    FilePackageCreate,
    FilePackageUpdate,
    FilePackageResponse,
    AddFileToPackageRequest,
    ExtractZipRequest,
)

__all__ = [
    # Auth
    "EncryptedLoginRequest",
    "EncryptedRegisterRequest",
    "VerifyCodeRequest",
    "LoginResponse",
    "RegisterResponse",
    "UserInfo",
    # Projects
    "ProjectCreate",
    "ProjectUpdate",
    "ProjectResponse",
    "ProjectListResponse",
    "ProjectTagCreate",
    "ProjectTagUpdate",
    "ProjectTagResponse",
    "AddProjectTagRequest",
    "SyncProjectTagsRequest",
    # Members
    "AddMemberRequest",
    "BatchAddMembersRequest",
    "UpdateMemberRoleRequest",
    "MemberResponse",
    "MemberListResponse",
    # Branches
    "BranchCreate",
    "BranchUpdate",
    "BranchUpdateStatus",
    "BranchResponse",
    "BranchListResponse",
    # Pages
    "PageCreate",
    "PageUpdate",
    "PageResponse",
    "PageTreeItem",
    "MovePageRequest",
    # Components
    "ComponentCreate",
    "ComponentUpdate",
    "ComponentResponse",
    "AddComponentToPageRequest",
    "UpdateComponentOrderRequest",
    "PageComponentResponse",
    "SyncPageComponentsRequest",
    # Merge Requests
    "MergeRequestCreate",
    "MergeRequestUpdate",
    "MergeRequestReview",
    "MergeRequestResponse",
    "MergeRequestListResponse",
    # Branch Versions
    "PageChangeItem",
    "VersionCreate",
    "VersionResponse",
    "VersionHistoryResponse",
    "ChangeDetail",
    "VersionDiffResponse",
    # Notifications
    "NotificationResponse",
    "NotificationListResponse",
    # File Packages
    "FilePackageCreate",
    "FilePackageUpdate",
    "FilePackageResponse",
    "AddFileToPackageRequest",
    "ExtractZipRequest",
]
