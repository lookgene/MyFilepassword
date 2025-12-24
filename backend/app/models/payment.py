"""Payment models."""

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    DateTime,
    String,
    Text,
    Numeric,
    ForeignKey,
    Enum as SQLEnum,
    Boolean,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import BaseModel, TimestampMixin
from app.models.payment_types import OrderStatus, PaymentMethod

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.task import Task
    from app.models.coupon import Coupon


class Order(BaseModel, TimestampMixin):
    """Order model."""

    __tablename__ = "orders"

    user_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    task_id: Mapped[str | None] = mapped_column(
        UUID(as_uuid=False),
        ForeignKey("tasks.id", ondelete="SET NULL"),
        nullable=True,
    )
    order_no: Mapped[str] = mapped_column(String(32), unique=True, nullable=False, index=True)
    amount: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    discount: Mapped[float] = mapped_column(Numeric(10, 2), default=0, nullable=False)
    final_amount: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(10), default="CNY", nullable=False)
    coupon_id: Mapped[str | None] = mapped_column(UUID(as_uuid=False), nullable=True)
    status: Mapped[OrderStatus] = mapped_column(
        SQLEnum(OrderStatus), default=OrderStatus.PENDING, nullable=False, index=True
    )
    payment_method: Mapped[PaymentMethod | None] = mapped_column(
        SQLEnum(PaymentMethod), nullable=True
    )
    payment_provider: Mapped[str | None] = mapped_column(String(20), nullable=True)
    transaction_id: Mapped[str | None] = mapped_column(String(100), nullable=True)
    paid_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="orders")
    task: Mapped["Task"] = relationship("Task", back_populates="orders")
    refunds: Mapped[list["Refund"]] = relationship(
        "Refund", back_populates="order", cascade="all, delete-orphan"
    )


class Refund(BaseModel, TimestampMixin):
    """Refund model."""

    __tablename__ = "refunds"

    order_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        ForeignKey("orders.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    user_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    refund_no: Mapped[str] = mapped_column(String(32), unique=True, nullable=False, index=True)
    amount: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    status: Mapped[OrderStatus] = mapped_column(
        SQLEnum(OrderStatus), default=OrderStatus.PENDING, nullable=False, index=True
    )
    reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    provider_refund_id: Mapped[str | None] = mapped_column(String(100), nullable=True)
    processed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    # Relationships
    order: Mapped["Order"] = relationship("Order", back_populates="refunds")
    user: Mapped["User"] = relationship("User", back_populates="refunds")
