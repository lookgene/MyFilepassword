"""File model."""

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, String, Text, BigInteger, ForeignKey, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import BaseModel, TimestampMixin

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.task import Task


class File(BaseModel, TimestampMixin):
    """File model."""

    __tablename__ = "files"

    user_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    file_name: Mapped[str] = mapped_column(String(255), nullable=False)
    file_size: Mapped[int] = mapped_column(BigInteger, nullable=False)
    file_type: Mapped[str] = mapped_column(String(20), nullable=False)
    mime_type: Mapped[str] = mapped_column(String(100), nullable=False)
    storage_key: Mapped[str] = mapped_column(String(500), nullable=False, unique=True)
    storage_provider: Mapped[str] = mapped_column(String(20), default="minio", nullable=False)
    md5_hash: Mapped[str | None] = mapped_column(String(32), nullable=True)
    sha256_hash: Mapped[str | None] = mapped_column(String(64), nullable=True)
    is_encrypted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    encryption_info: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    scan_status: Mapped[str] = mapped_column(String(20), default="pending", nullable=False)
    scan_result: Mapped[str | None] = mapped_column(Text, nullable=True)
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, index=True)

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="files")
    tasks: Mapped[list["Task"]] = relationship("Task", back_populates="file")
