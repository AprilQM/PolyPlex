"""
合并请求 CRUD 操作
"""
from sqlalchemy import select, desc, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.merge_requests import MergeRequest, MergeRequestStatus
from app.models.branches import Branch
from typing import Optional, List


# ========== MergeRequest CRUD ==========

async def get_merge_request(
    db: AsyncSession,
    mr_id: int
) -> Optional[MergeRequest]:
    """根据 ID 获取合并请求"""
    result = await db.execute(
        select(MergeRequest).where(MergeRequest.id == mr_id)
    )
    return result.scalar_one_or_none()


async def create_merge_request(
    db: AsyncSession,
    project_id: int,
    source_branch_id: int,
    target_branch_id: int,
    title: str,
    created_by: int,
    description: Optional[str] = None,
) -> MergeRequest:
    """创建合并请求"""
    mr = MergeRequest(
        project_id=project_id,
        source_branch_id=source_branch_id,
        target_branch_id=target_branch_id,
        title=title,
        description=description,
        created_by=created_by,
    )
    db.add(mr)
    await db.commit()
    await db.refresh(mr)
    return mr


async def update_merge_request(
    db: AsyncSession,
    mr_id: int,
    title: Optional[str] = None,
    description: Optional[str] = None,
    status: Optional[MergeRequestStatus] = None,
) -> Optional[MergeRequest]:
    """更新合并请求"""
    mr = await get_merge_request(db, mr_id)
    if not mr:
        return None

    if title is not None:
        mr.title = title
    if description is not None:
        mr.description = description
    if status is not None:
        mr.status = status

    await db.commit()
    await db.refresh(mr)
    return mr


async def approve_merge_request(
    db: AsyncSession,
    mr_id: int,
    reviewed_by: int,
    review_comment: Optional[str] = None,
) -> Optional[MergeRequest]:
    """批准合并请求"""
    import time
    mr = await get_merge_request(db, mr_id)
    if not mr:
        return None

    mr.status = MergeRequestStatus.APPROVED
    mr.reviewed_by = reviewed_by
    mr.review_comment = review_comment

    await db.commit()
    await db.refresh(mr)
    return mr


async def reject_merge_request(
    db: AsyncSession,
    mr_id: int,
    reviewed_by: int,
    review_comment: Optional[str] = None,
) -> Optional[MergeRequest]:
    """拒绝合并请求"""
    mr = await get_merge_request(db, mr_id)
    if not mr:
        return None

    mr.status = MergeRequestStatus.REJECTED
    mr.reviewed_by = reviewed_by
    mr.review_comment = review_comment

    await db.commit()
    await db.refresh(mr)
    return mr


async def merge_request(
    db: AsyncSession,
    mr_id: int,
    merged_by: int,
) -> Optional[MergeRequest]:
    """执行合并操作"""
    import time
    mr = await get_merge_request(db, mr_id)
    if not mr:
        return None

    if mr.status != MergeRequestStatus.APPROVED:
        raise ValueError("只有已批准的合并请求才能执行合并")

    mr.status = MergeRequestStatus.MERGED
    mr.merged_at = int(time.time())

    await db.commit()
    await db.refresh(mr)
    return mr


async def cancel_merge_request(
    db: AsyncSession,
    mr_id: int,
) -> Optional[MergeRequest]:
    """取消合并请求"""
    return await update_merge_request(db, mr_id, status=MergeRequestStatus.PENDING)


async def get_merge_requests(
    db: AsyncSession,
    project_id: int,
    status: Optional[MergeRequestStatus] = None,
    source_branch_id: Optional[int] = None,
    target_branch_id: Optional[int] = None,
    page: int = 1,
    page_size: int = 20,
) -> List[MergeRequest]:
    """获取合并请求列表"""
    query = select(MergeRequest).where(
        MergeRequest.project_id == project_id
    )

    if status is not None:
        query = query.where(MergeRequest.status == status)
    if source_branch_id is not None:
        query = query.where(MergeRequest.source_branch_id == source_branch_id)
    if target_branch_id is not None:
        query = query.where(MergeRequest.target_branch_id == target_branch_id)

    query = query.order_by(desc(MergeRequest.created_at))
    query = query.offset((page - 1) * page_size).limit(page_size)

    result = await db.execute(query)
    return list(result.scalars().all())


async def count_merge_requests(
    db: AsyncSession,
    project_id: int,
    status: Optional[MergeRequestStatus] = None,
) -> int:
    """统计合并请求数量"""
    query = select(func.count(MergeRequest.id)).where(
        MergeRequest.project_id == project_id
    )

    if status is not None:
        query = query.where(MergeRequest.status == status)

    result = await db.execute(query)
    return result.scalar()


async def get_pending_merge_requests(
    db: AsyncSession,
    project_id: int,
) -> List[MergeRequest]:
    """获取待处理的合并请求"""
    result = await db.execute(
        select(MergeRequest)
        .where(MergeRequest.project_id == project_id)
        .where(MergeRequest.status == MergeRequestStatus.PENDING)
        .order_by(desc(MergeRequest.created_at))
    )
    return list(result.scalars().all())


async def can_merge(
    db: AsyncSession,
    mr_id: int,
) -> dict:
    """检查合并请求是否可以合并"""
    mr = await get_merge_request(db, mr_id)
    if not mr:
        return {"can_merge": False, "reason": "合并请求不存在"}

    if mr.status != MergeRequestStatus.APPROVED:
        return {"can_merge": False, "reason": "合并请求尚未批准"}

    source_branch = await db.get(Branch, mr.source_branch_id)
    if not source_branch:
        return {"can_merge": False, "reason": "源分支不存在"}

    target_branch = await db.get(Branch, mr.target_branch_id)
    if not target_branch:
        return {"can_merge": False, "reason": "目标分支不存在"}

    return {"can_merge": True, "reason": ""}
