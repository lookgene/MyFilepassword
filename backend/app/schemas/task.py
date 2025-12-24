"""Task schemas."""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field

from app.models.task_types import TaskStatus, CrackType


class CrackConfig(BaseModel):
    """Crack configuration schema."""

    password_length: int | None = None
    password_type: str | None = None
    charset: str | None = None
    password_hint: str | None = None
    enable_mask: bool = False
    mask_pattern: str | None = None


class TaskCreate(BaseModel):
    """Task creation schema."""

    task_name: str = Field(..., min_length=1, max_length=255)
    file_id: str
    crack_type: CrackType
    crack_config: CrackConfig = Field(default_factory=CrackConfig)
    notification: dict[str, Any] | None = None


class TaskUpdate(BaseModel):
    """Task update schema."""

    task_name: str | None = Field(None, min_length=1, max_length=255)
    crack_config: CrackConfig | None = None


class TaskFile(BaseModel):
    """Task file schema."""

    file_id: str
    file_name: str
    file_size: int
    file_type: str


class TaskResult(BaseModel):
    """Task result schema."""

    password: str | None
    attempts: int | None
    duration: int | None
    method: str | None


class TaskResponse(BaseModel):
    """Task response schema."""

    task_id: str
    user_id: str
    file: TaskFile
    task_name: str
    crack_type: CrackType
    crack_config: CrackConfig
    status: TaskStatus
    priority: int
    progress: int
    result: TaskResult | None
    error_message: str | None
    estimated_time: int | None
    cost: float | None = None
    created_at: datetime
    started_at: datetime | None
    completed_at: datetime | None


class TaskListResponse(BaseModel):
    """Task list response schema."""

    items: list[TaskResponse]
    total: int
    page: int
    page_size: int
    pages: int


class TaskStatusResponse(BaseModel):
    """Task status response schema."""

    task_id: str
    status: TaskStatus
    progress: int
    current_password: str | None = None
    estimated_completion: datetime | None


class TaskProgress(BaseModel):
    """Task progress schema."""

    task_id: str
    progress: int
    status: TaskStatus
    current_password: str | None
    message: str | None


class TaskLog(BaseModel):
    """Task log schema."""

    log_id: str
    level: str
    message: str
    timestamp: datetime
