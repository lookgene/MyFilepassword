"""Notification model type definitions."""

from enum import Enum


class NotificationType(str, Enum):
    """Notification type enum."""

    TASK_CREATED = "task_created"
    TASK_STARTED = "task_started"
    TASK_COMPLETED = "task_completed"
    TASK_FAILED = "task_failed"
    PAYMENT_SUCCESS = "payment_success"
    PAYMENT_FAILED = "payment_failed"
    REFUND_COMPLETED = "refund_completed"
    SYSTEM_ANNOUNCEMENT = "system_announcement"
