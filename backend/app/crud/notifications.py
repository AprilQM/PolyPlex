"""
通知 CRUD 操作
"""
from sqlalchemy import select, desc, func, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.notifications import Notification
from typing import Optional, List


# ========== Notification CRUD ==========

async def get_notification(
    db: AsyncSession,
    notification_id: int
) -> Optional[Notification]:
    """根据 ID 获取通知"""
    result = await db.execute(
        select(Notification).where(Notification.id == notification_id)
    )
    return result.scalar_one_or_none()


async def create_notification(
    db: AsyncSession,
    user_id: int,
    title: str,
    content: str,
) -> Notification:
    """创建通知"""
    notification = Notification(
        user_id=user_id,
        title=title,
        content=content,
    )
    db.add(notification)
    await db.commit()
    await db.refresh(notification)
    return notification


async def mark_notification_read(
    db: AsyncSession,
    notification_id: int,
) -> Optional[Notification]:
    """标记通知为已读"""
    notification = await get_notification(db, notification_id)
    if not notification:
        return None

    notification.is_read = True
    await db.commit()
    await db.refresh(notification)
    return notification


async def mark_notification_unread(
    db: AsyncSession,
    notification_id: int,
) -> Optional[Notification]:
    """标记通知为未读"""
    notification = await get_notification(db, notification_id)
    if not notification:
        return None

    notification.is_read = False
    await db.commit()
    await db.refresh(notification)
    return notification


async def delete_notification(
    db: AsyncSession,
    notification_id: int,
) -> bool:
    """删除通知"""
    notification = await get_notification(db, notification_id)
    if not notification:
        return False

    await db.delete(notification)
    await db.commit()
    return True


async def get_user_notifications(
    db: AsyncSession,
    user_id: int,
    is_read: Optional[bool] = None,
    page: int = 1,
    page_size: int = 20,
) -> List[Notification]:
    """获取用户的通知列表"""
    query = select(Notification).where(Notification.user_id == user_id)

    if is_read is not None:
        query = query.where(Notification.is_read == is_read)

    query = query.order_by(desc(Notification.created_at))
    query = query.offset((page - 1) * page_size).limit(page_size)

    result = await db.execute(query)
    return list(result.scalars().all())


async def count_user_notifications(
    db: AsyncSession,
    user_id: int,
    is_read: Optional[bool] = None,
) -> int:
    """统计用户的通知数量"""
    query = select(func.count(Notification.id)).where(
        Notification.user_id == user_id
    )

    if is_read is not None:
        query = query.where(Notification.is_read == is_read)

    result = await db.execute(query)
    return result.scalar()


async def get_unread_count(
    db: AsyncSession,
    user_id: int,
) -> int:
    """获取用户未读通知数量"""
    return await count_user_notifications(db, user_id, is_read=False)


async def mark_all_read(
    db: AsyncSession,
    user_id: int,
) -> int:
    """标记所有通知为已读"""
    result = await db.execute(
        update(Notification)
        .where(Notification.user_id == user_id)
        .where(Notification.is_read == False)
        .values(is_read=True)
    )
    await db.commit()
    return result.rowcount


async def delete_all_read(
    db: AsyncSession,
    user_id: int,
) -> int:
    """删除所有已读通知"""
    result = await db.execute(
        update(Notification)
        .where(Notification.user_id == user_id)
        .where(Notification.is_read == True)
        .values(is_read=True)  # 软删除时可以改为 is_deleted=True
    )
    # 实际删除
    delete_result = await db.execute(
        select(Notification)
        .where(Notification.user_id == user_id)
        .where(Notification.is_read == True)
    )
    notifications = delete_result.scalars().all()
    for notification in notifications:
        await db.delete(notification)

    await db.commit()
    return len(notifications)


async def batch_create_notifications(
    db: AsyncSession,
    notifications: List[dict],
) -> List[Notification]:
    """批量创建通知

    Args:
        notifications: 通知列表，每项包含 {user_id, title, content}
    """
    created = []
    for notif_data in notifications:
        notification = Notification(
            user_id=notif_data["user_id"],
            title=notif_data["title"],
            content=notif_data["content"],
        )
        db.add(notification)
        created.append(notification)

    await db.commit()
    for notification in created:
        await db.refresh(notification)

    return created
