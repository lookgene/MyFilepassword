from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from enum import Enum

class CrackType(str, Enum):
    SIMPLE = "simple"
    REGULAR = "regular"
    PROFESSIONAL = "professional"

class TaskStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    CANCELLED = "cancelled"

class TaskBase(BaseModel):
    file_id: int
    crack_type: CrackType
    user_id: Optional[int] = None

class TaskCreate(TaskBase):
    email: str

class Task(TaskBase):
    id: int
    status: TaskStatus
    result: Optional[str] = None
    estimated_time: Optional[int] = None
    actual_time: Optional[int] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class TaskResponse(BaseModel):
    id: int
    file_id: int
    crack_type: CrackType
    status: TaskStatus
    created_at: datetime
    estimated_time: Optional[int] = None

    class Config:
        from_attributes = True
