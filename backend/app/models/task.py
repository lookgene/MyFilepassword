from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.sql import func
from sqlalchemy import Enum
import enum
from app.core.database import Base

class CrackType(str, enum.Enum):
    SIMPLE = "simple"
    REGULAR = "regular"
    PROFESSIONAL = "professional"

class TaskStatus(str, enum.Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    CANCELLED = "cancelled"

class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    file_id = Column(Integer, ForeignKey("files.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    email = Column(String, nullable=True)  # 用户邮箱，用于通知
    crack_type = Column(SQLEnum(CrackType), nullable=False)
    status = Column(SQLEnum(TaskStatus), default=TaskStatus.PENDING)
    result = Column(String, nullable=True)
    estimated_time = Column(Integer, nullable=True)  # 估计时间（秒）
    actual_time = Column(Integer, nullable=True)  # 实际耗时（秒）
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)
