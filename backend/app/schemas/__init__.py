"""Schemas module."""

from app.schemas.common import ErrorResponse, SuccessResponse
from app.schemas.user import (
    UserCreate,
    UserUpdate,
    UserResponse,
    UserInResponse,
    LoginRequest,
    RegisterRequest,
    TokenResponse,
    ChangePasswordRequest,
    ForgotPasswordRequest,
    ResetPasswordRequest,
)
from app.schemas.file import (
    FileUploadRequest,
    FileUploadResponse,
    FileResponse,
    FileListResponse,
)
from app.schemas.task import (
    TaskCreate,
    TaskUpdate,
    TaskResponse,
    TaskListResponse,
    TaskStatusResponse,
)
from app.schemas.payment import (
    OrderCreate,
    OrderResponse,
    OrderListResponse,
    RefundCreate,
    RefundResponse,
)
from app.schemas.notification import (
    NotificationResponse,
    NotificationListResponse,
)

__all__ = [
    # Common
    "ErrorResponse",
    "SuccessResponse",
    # User
    "UserCreate",
    "UserUpdate",
    "UserResponse",
    "UserInResponse",
    "LoginRequest",
    "RegisterRequest",
    "TokenResponse",
    "ChangePasswordRequest",
    "ForgotPasswordRequest",
    "ResetPasswordRequest",
    # File
    "FileUploadRequest",
    "FileUploadResponse",
    "FileResponse",
    "FileListResponse",
    # Task
    "TaskCreate",
    "TaskUpdate",
    "TaskResponse",
    "TaskListResponse",
    "TaskStatusResponse",
    # Payment
    "OrderCreate",
    "OrderResponse",
    "OrderListResponse",
    "RefundCreate",
    "RefundResponse",
    # Notification
    "NotificationResponse",
    "NotificationListResponse",
]
