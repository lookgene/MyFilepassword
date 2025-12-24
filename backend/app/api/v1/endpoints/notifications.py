"""Notification endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_current_active_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.common import success_response
from app.schemas.notification import NotificationSettingsUpdate
from app.services.notification_service import NotificationService

router = APIRouter()


@router.get("", response_model=dict)
async def list_notifications(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """List user notifications.

    Args:
        current_user: Current authenticated user
        db: Database session

    Returns:
        List of notifications
    """
    notification_service = NotificationService(db)
    notifications = await notification_service.list_notifications(current_user.id)

    return success_response(data=notifications)


@router.post("/{notification_id}/read", response_model=dict)
async def mark_notification_read(
    notification_id: str,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Mark notification as read.

    Args:
        notification_id: Notification ID
        current_user: Current authenticated user
        db: Database session

    Returns:
        Success message
    """
    notification_service = NotificationService(db)
    success = await notification_service.mark_as_read(notification_id, current_user.id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found",
        )

    return success_response(message="已标记为已读")


@router.delete("/{notification_id}", response_model=dict)
async def delete_notification(
    notification_id: str,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Delete notification.

    Args:
        notification_id: Notification ID
        current_user: Current authenticated user
        db: Database session

    Returns:
        Success message
    """
    notification_service = NotificationService(db)
    success = await notification_service.delete_notification(notification_id, current_user.id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found",
        )

    return success_response(message="通知已删除")


@router.get("/settings", response_model=dict)
async def get_notification_settings(
    current_user: User = Depends(get_current_active_user),
):
    """Get notification settings.

    Args:
        current_user: Current authenticated user

    Returns:
        Notification settings
    """
    # TODO: Get from user profile preferences
    settings = {
        "email": {
            "task_created": True,
            "task_started": True,
            "task_completed": True,
            "task_failed": True,
        },
        "sms": {
            "task_completed": False,
        },
        "webhook": {
            "enabled": False,
            "url": "",
        },
    }

    return success_response(data=settings)


@router.patch("/settings", response_model=dict)
async def update_notification_settings(
    settings_data: NotificationSettingsUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Update notification settings.

    Args:
        settings_data: Notification settings update data
        current_user: Current authenticated user
        db: Database session

    Returns:
        Success message
    """
    notification_service = NotificationService(db)
    await notification_service.update_settings(current_user.id, settings_data)

    return success_response(message="设置已更新")
