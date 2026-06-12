"""项目 API 路由"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.api.deps import get_current_user, require_active_user
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
from app.crud.projects import (
    get_project,
    get_project_by_name,
    create_project as crud_create_project,
    update_project as crud_update_project,
    delete_project as crud_delete_project,
    start_project as crud_start_project,
    close_project as crud_close_project,
    get_project_list,
    count_projects,
    get_project_tags,
    add_project_tag,
    remove_project_tag,
    sync_project_tags,
    get_all_project_tags,
    create_project_tag,
    update_project_tag,
    delete_project_tag,
    get_project_tag_by_name,
)

router = APIRouter(prefix="/api/projects", tags=["projects"])


# ── 辅助函数 ─────────────────────────────────────────────────────────

async def _get_project_or_404(db: AsyncSession, project_id: int):
    project = await get_project(db, project_id)
    if not project:
        raise HTTPException(404, "项目不存在")
    return project


async def _check_owner(project, user_id: int):
    """检查当前用户是否为项目所有者"""
    if project.owner_id != user_id:
        raise HTTPException(403, "只有项目所有者才能执行此操作")


async def _enrich_project_tags(db: AsyncSession, project) -> ProjectResponse:
    """获取项目标签并构造完整响应"""
    tags = await get_project_tags(db, project.id)
    tag_list = [
        ProjectTagResponse(
            id=t.id,
            name=t.name,
            background_color=t.background_color,
            text_color=t.text_color,
        )
        for t in tags
    ]
    return ProjectResponse(
        id=project.id,
        name=project.name,
        description=project.description,
        owner_id=project.owner_id,
        project_type=project.project_type,
        is_private=project.is_private,
        is_started=project.is_started,
        cover_image=project.cover_image,
        created_at=project.created_at,
        updated_at=project.updated_at,
        tags=tag_list,
    )


# ── 项目 CRUD ────────────────────────────────────────────────────────

@router.post("", response_model=ProjectResponse, status_code=201)
async def create_project(
    req: ProjectCreate,
    current_user: dict = Depends(require_active_user),
    db: AsyncSession = Depends(get_db),
):
    """创建新项目"""
    existing = await get_project_by_name(db, req.name)
    if existing:
        raise HTTPException(409, "项目名称已存在")

    project = await crud_create_project(
        db=db,
        name=req.name,
        owner_id=current_user["id"],
        description=req.description,
        project_type=req.project_type,
        is_private=req.is_private,
        cover_image_uuid=req.cover_image,
    )

    # 创建项目后自动添加项目所有者到成员表
    from app.crud.project_members import add_project_member
    from app.models.members import RoleType
    await add_project_member(db, project.id, current_user["id"], RoleType.OWNER)

    # 添加标签
    if req.tag_ids:
        await sync_project_tags(db, project.id, req.tag_ids)

    return await _enrich_project_tags(db, project)


@router.get("", response_model=ProjectListResponse)
async def list_projects(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    owner_id: int = Query(None),
    project_type: str = Query(None),
    is_private: bool = Query(None),
    is_started: bool = Query(None),
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """获取项目列表（分页，支持筛选）"""
    from app.models.projects import ProjectType as PT

    ptype = None
    if project_type:
        try:
            ptype = PT(project_type)
        except ValueError:
            raise HTTPException(400, f"无效的项目类型: {project_type}")

    projects = await get_project_list(
        db=db,
        page=page,
        page_size=page_size,
        owner_id=owner_id,
        project_type=ptype,
        is_private=is_private,
        is_started=is_started,
    )
    total = await count_projects(
        db=db,
        owner_id=owner_id,
        project_type=ptype,
        is_private=is_private,
        is_started=is_started,
    )

    items = [await _enrich_project_tags(db, p) for p in projects]
    return ProjectListResponse(items=items, total=total, page=page, page_size=page_size)


@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project_detail(
    project_id: int,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """获取项目详情（含标签）"""
    project = await _get_project_or_404(db, project_id)
    return await _enrich_project_tags(db, project)


@router.put("/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: int,
    req: ProjectUpdate,
    current_user: dict = Depends(require_active_user),
    db: AsyncSession = Depends(get_db),
):
    """更新项目信息"""
    project = await _get_project_or_404(db, project_id)
    await _check_owner(project, current_user["id"])

    # 如果重命名，检查是否冲突
    if req.name is not None and req.name != project.name:
        existing = await get_project_by_name(db, req.name)
        if existing:
            raise HTTPException(409, "项目名称已存在")

    updated = await crud_update_project(
        db=db,
        project_id=project_id,
        name=req.name,
        description=req.description,
        project_type=req.project_type,
        is_private=req.is_private,
        cover_image_uuid=req.cover_image,
    )
    return await _enrich_project_tags(db, updated)


@router.delete("/{project_id}")
async def delete_project(
    project_id: int,
    current_user: dict = Depends(require_active_user),
    db: AsyncSession = Depends(get_db),
):
    """删除项目"""
    project = await _get_project_or_404(db, project_id)
    await _check_owner(project, current_user["id"])

    ok = await crud_delete_project(db, project_id)
    if not ok:
        raise HTTPException(500, "删除项目失败")
    return {"message": "项目已删除"}


# ── 项目状态管理 ─────────────────────────────────────────────────────

@router.post("/{project_id}/start", response_model=ProjectResponse)
async def start_project(
    project_id: int,
    current_user: dict = Depends(require_active_user),
    db: AsyncSession = Depends(get_db),
):
    """启动项目"""
    project = await _get_project_or_404(db, project_id)
    await _check_owner(project, current_user["id"])
    updated = await crud_start_project(db, project_id)
    return await _enrich_project_tags(db, updated)


@router.post("/{project_id}/close", response_model=ProjectResponse)
async def close_project(
    project_id: int,
    current_user: dict = Depends(require_active_user),
    db: AsyncSession = Depends(get_db),
):
    """关闭项目"""
    project = await _get_project_or_404(db, project_id)
    await _check_owner(project, current_user["id"])
    updated = await crud_close_project(db, project_id)
    return await _enrich_project_tags(db, updated)


# ── 项目标签管理 ─────────────────────────────────────────────────────

@router.get("/{project_id}/tags", response_model=list[ProjectTagResponse])
async def get_project_tag_list(
    project_id: int,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """获取项目的标签列表"""
    await _get_project_or_404(db, project_id)
    tags = await get_project_tags(db, project_id)
    return [
        ProjectTagResponse(
            id=t.id,
            name=t.name,
            background_color=t.background_color,
            text_color=t.text_color,
        )
        for t in tags
    ]


@router.post("/{project_id}/tags", response_model=ProjectTagResponse)
async def add_tag_to_project(
    project_id: int,
    req: AddProjectTagRequest,
    current_user: dict = Depends(require_active_user),
    db: AsyncSession = Depends(get_db),
):
    """给项目添加标签（按 tag_id 或 tag_name）"""
    project = await _get_project_or_404(db, project_id)
    await _check_owner(project, current_user["id"])

    tag_id = req.tag_id
    if req.tag_name:
        tag = await get_project_tag_by_name(db, req.tag_name)
        if not tag:
            raise HTTPException(404, f"标签 '{req.tag_name}' 不存在")
        tag_id = tag.id

    if not tag_id:
        raise HTTPException(400, "请提供 tag_id 或 tag_name")

    relation = await add_project_tag(db, project_id, tag_id)
    from app.crud.projects import get_project_tag as get_tag
    tag = await get_tag(db, tag_id)
    return ProjectTagResponse(
        id=tag.id,
        name=tag.name,
        background_color=tag.background_color,
        text_color=tag.text_color,
    )


@router.delete("/{project_id}/tags/{tag_id}")
async def remove_tag_from_project(
    project_id: int,
    tag_id: int,
    current_user: dict = Depends(require_active_user),
    db: AsyncSession = Depends(get_db),
):
    """移除项目的标签"""
    project = await _get_project_or_404(db, project_id)
    await _check_owner(project, current_user["id"])

    ok = await remove_project_tag(db, project_id, tag_id)
    if not ok:
        raise HTTPException(404, "该项目没有此标签")
    return {"message": "标签已移除"}


@router.put("/{project_id}/tags", response_model=list[ProjectTagResponse])
async def sync_project_tag_list(
    project_id: int,
    req: SyncProjectTagsRequest,
    current_user: dict = Depends(require_active_user),
    db: AsyncSession = Depends(get_db),
):
    """同步项目标签（替换所有标签）"""
    project = await _get_project_or_404(db, project_id)
    await _check_owner(project, current_user["id"])

    tags = await sync_project_tags(db, project_id, req.tag_ids)
    return [
        ProjectTagResponse(
            id=t.id,
            name=t.name,
            background_color=t.background_color,
            text_color=t.text_color,
        )
        for t in tags
    ]


# ── 全局标签管理 ─────────────────────────────────────────────────────

@router.get("/tags/all", response_model=list[ProjectTagResponse])
async def get_all_tags(
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """获取所有可用标签"""
    tags = await get_all_project_tags(db)
    return [
        ProjectTagResponse(
            id=t.id,
            name=t.name,
            background_color=t.background_color,
            text_color=t.text_color,
        )
        for t in tags
    ]


@router.post("/tags", response_model=ProjectTagResponse, status_code=201)
async def create_tag(
    req: ProjectTagCreate,
    current_user: dict = Depends(require_active_user),
    db: AsyncSession = Depends(get_db),
):
    """创建新标签"""
    existing = await get_project_tag_by_name(db, req.name)
    if existing:
        raise HTTPException(409, "标签名称已存在")
    tag = await create_project_tag(
        db=db,
        name=req.name,
        background_color=req.background_color,
        text_color=req.text_color,
    )
    return ProjectTagResponse(
        id=tag.id,
        name=tag.name,
        background_color=tag.background_color,
        text_color=tag.text_color,
    )


@router.put("/tags/{tag_id}", response_model=ProjectTagResponse)
async def update_tag(
    tag_id: int,
    req: ProjectTagUpdate,
    current_user: dict = Depends(require_active_user),
    db: AsyncSession = Depends(get_db),
):
    """更新标签"""
    tag = await update_project_tag(
        db=db,
        tag_id=tag_id,
        name=req.name,
        background_color=req.background_color,
        text_color=req.text_color,
    )
    if not tag:
        raise HTTPException(404, "标签不存在")
    return ProjectTagResponse(
        id=tag.id,
        name=tag.name,
        background_color=tag.background_color,
        text_color=tag.text_color,
    )


@router.delete("/tags/{tag_id}")
async def delete_tag(
    tag_id: int,
    current_user: dict = Depends(require_active_user),
    db: AsyncSession = Depends(get_db),
):
    """删除标签"""
    ok = await delete_project_tag(db, tag_id)
    if not ok:
        raise HTTPException(404, "标签不存在")
    return {"message": "标签已删除"}
