"""Notification schemas."""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, EmailStr


class NotificationBase(BaseModel):
    """Base notification schema."""

    type: str
    title: str
    content: str | None = None
    data: dict[str, Any] | None = None


class NotificationResponse(NotificationBase):
    """Notification response schema."""

    notification_id: str
    user_id: str
    is_read: bool
    read_at: datetime | None
    created_at: datetime


class NotificationListResponse(BaseModel):
    """Notification list response schema."""

    items: list[NotificationResponse]
    total: int
    unread_count: int


class NotificationSettings(BaseModel):
    """Notification settings schema."""

    email: dict[str, bool] = {}
    sms: dict[str, bool] = {}
    webhook: dict[str, Any] = {}


class NotificationSettingsUpdate(BaseModel):
    """Notification settings update schema."""

    email: dict[str, bool] | None = None
    sms: dict[str, bool] | None = None
    webhook: dict[str, Any] | None = None
