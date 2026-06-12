"""分支 API 路由"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.api.deps import get_current_user, require_active_user
from app.schemas.branches import (
    BranchCreate,
    BranchUpdate,
    BranchUpdateStatus,
    BranchResponse,
    BranchListResponse,
)
from app.crud.branches import (
    get_branch,
    get_branch_by_name,
    create_branch as crud_create_branch,
    update_branch as crud_update_branch,
    delete_branch as crud_delete_branch,
    update_branch_status,
    get_project_branches,
    clone_branch_pages,
    create_branch_from_template,
)
from app.crud.projects import get_project
from app.crud.project_members import is_project_admin, is_project_contributor

router = APIRouter(prefix="/api/projects/{project_id}/branches", tags=["branches"])


# ── 辅助函数 ─────────────────────────────────────────────────────────

async def _get_project_or_404(db: AsyncSession, project_id: int):
    project = await get_project(db, project_id)
    if not project:
        raise HTTPException(404, "项目不存在")
    return project


async def _get_branch_or_404(db: AsyncSession, branch_id: int):
    branch = await get_branch(db, branch_id)
    if not branch:
        raise HTTPException(404, "分支不存在")
    return branch


async def _require_admin(
    db: AsyncSession, project_id: int, user_id: int,
):
    """要求当前用户是项目管理员（或所有者）"""
    if not await is_project_admin(db, project_id, user_id) and not await is_project_contributor(db, project_id, user_id):
        raise HTTPException(403, "没有权限执行此操作")


async def _build_branch_response(branch) -> BranchResponse:
    return BranchResponse(
        id=branch.id,
        project_id=branch.project_id,
        name=branch.name,
        description=branch.description,
        created_by=branch.created_by,
        status=branch.status,
        base_version=branch.base_version,
        created_at=branch.created_at,
        updated_at=branch.updated_at,
    )


# ── 分支 CRUD ────────────────────────────────────────────────────────

@router.get("", response_model=BranchListResponse)
async def list_branches(
    project_id: int,
    status: str = Query(None),
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """获取项目的分支列表"""
    await _get_project_or_404(db, project_id)

    from app.models.branches import BranchStatus as BS
    status_filter = None
    if status:
        try:
            status_filter = BS(status)
        except ValueError:
            raise HTTPException(400, f"无效的分支状态: {status}")

    branches = await get_project_branches(db, project_id, status=status_filter)
    items = [_build_branch_response(b) for b in branches]
    return BranchListResponse(items=items, total=len(items))


@router.post("", response_model=BranchResponse, status_code=201)
async def create_branch(
    project_id: int,
    req: BranchCreate,
    current_user: dict = Depends(require_active_user),
    db: AsyncSession = Depends(get_db),
):
    """创建分支（可选从源分支克隆或从模板创建）"""
    project = await _get_project_or_404(db, project_id)
    user_id = current_user["id"]

    # 检查名称唯一性
    existing = await get_branch_by_name(db, project_id, req.name)
    if existing:
        raise HTTPException(409, f"分支 '{req.name}' 已存在")

    # 检查权限（项目所有者或管理员）
    if project.owner_id != user_id and not await is_project_admin(db, project_id, user_id):
        raise HTTPException(403, "只有项目所有者和管理员才能创建分支")

    # 创建分支
    if req.source_branch_id:
        # 从源分支克隆
        source = await _get_branch_or_404(db, req.source_branch_id)
        if source.project_id != project_id:
            raise HTTPException(400, "源分支不属于该项目")
        branch = await crud_create_branch(
            db=db, project_id=project_id, name=req.name,
            created_by=user_id, description=req.description,
        )
        await clone_branch_pages(
            db=db,
            source_branch_id=req.source_branch_id,
            target_branch_id=branch.id,
            created_by=user_id,
        )
    else:
        # 普通创建（空分支）
        branch = await crud_create_branch(
            db=db, project_id=project_id, name=req.name,
            created_by=user_id, description=req.description,
        )

    return _build_branch_response(branch)


@router.post("/from-template", response_model=BranchResponse, status_code=201)
async def create_branch_from_template_route(
    project_id: int,
    req: BranchCreate,
    category: str = Query("general", description="页面模板分类"),
    current_user: dict = Depends(require_active_user),
    db: AsyncSession = Depends(get_db),
):
    """从模板创建分支（自动初始化页面）"""
    project = await _get_project_or_404(db, project_id)
    user_id = current_user["id"]

    existing = await get_branch_by_name(db, project_id, req.name)
    if existing:
        raise HTTPException(409, f"分支 '{req.name}' 已存在")

    if project.owner_id != user_id and not await is_project_admin(db, project_id, user_id):
        raise HTTPException(403, "只有项目所有者和管理员才能创建分支")

    branch = await create_branch_from_template(
        db=db,
        project_id=project_id,
        name=req.name,
        created_by=user_id,
        category=category,
        description=req.description,
    )
    return _build_branch_response(branch)


@router.get("/{branch_id}", response_model=BranchResponse)
async def get_branch_detail(
    project_id: int,
    branch_id: int,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """获取分支详情"""
    branch = await _get_branch_or_404(db, branch_id)
    if branch.project_id != project_id:
        raise HTTPException(404, "该项目下不存在此分支")
    return _build_branch_response(branch)


@router.put("/{branch_id}", response_model=BranchResponse)
async def update_branch_info(
    project_id: int,
    branch_id: int,
    req: BranchUpdate,
    current_user: dict = Depends(require_active_user),
    db: AsyncSession = Depends(get_db),
):
    """更新分支信息"""
    branch = await _get_branch_or_404(db, branch_id)
    if branch.project_id != project_id:
        raise HTTPException(404, "该项目下不存在此分支")

    user_id = current_user["id"]
    project = await _get_project_or_404(db, project_id)
    if project.owner_id != user_id and not await is_project_admin(db, project_id, user_id):
        raise HTTPException(403, "只有项目所有者和管理员才能更新分支")

    if req.name is not None and req.name != branch.name:
        existing = await get_branch_by_name(db, project_id, req.name)
        if existing:
            raise HTTPException(409, f"分支名 '{req.name}' 已存在")

    updated = await crud_update_branch(
        db=db, branch_id=branch_id,
        name=req.name, description=req.description,
    )
    return _build_branch_response(updated)


@router.delete("/{branch_id}")
async def delete_branch_route(
    project_id: int,
    branch_id: int,
    current_user: dict = Depends(require_active_user),
    db: AsyncSession = Depends(get_db),
):
    """删除分支"""
    branch = await _get_branch_or_404(db, branch_id)
    if branch.project_id != project_id:
        raise HTTPException(404, "该项目下不存在此分支")

    user_id = current_user["id"]
    project = await _get_project_or_404(db, project_id)
    if project.owner_id != user_id and not await is_project_admin(db, project_id, user_id):
        raise HTTPException(403, "只有项目所有者和管理员才能删除分支")

    ok = await crud_delete_branch(db, branch_id)
    if not ok:
        raise HTTPException(500, "删除分支失败")
    return {"message": "分支已删除"}


@router.put("/{branch_id}/status", response_model=BranchResponse)
async def update_branch_status_route(
    project_id: int,
    branch_id: int,
    req: BranchUpdateStatus,
    current_user: dict = Depends(require_active_user),
    db: AsyncSession = Depends(get_db),
):
    """更新分支状态"""
    branch = await _get_branch_or_404(db, branch_id)
    if branch.project_id != project_id:
        raise HTTPException(404, "该项目下不存在此分支")

    user_id = current_user["id"]
    project = await _get_project_or_404(db, project_id)
    if project.owner_id != user_id and not await is_project_admin(db, project_id, user_id):
        raise HTTPException(403, "只有项目所有者和管理员才能更新分支状态")

    updated = await update_branch_status(db, branch_id, req.status)
    return _build_branch_response(updated)
