"""Task model type definitions."""

from enum import Enum


class TaskStatus(str, Enum):
    """Task status enum."""

    PENDING = "pending"
    QUEUED = "queued"
    ANALYZING = "analyzing"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class CrackType(str, Enum):
    """Crack type enum."""

    SIMPLE = "simple"
    NORMAL = "normal"
    ADVANCED = "advanced"


class LogLevel(str, Enum):
    """Log level enum."""

    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"
