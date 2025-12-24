"""Coupon models."""

from datetime import datetime
from typing import TYPE_CHECKING, List

from sqlalchemy import (
    DateTime,
    String,
    Text,
    Numeric,
    Integer,
    ForeignKey,
    Enum as SQLEnum,
    Boolean,
    ARRAY,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import BaseModel, TimestampMixin
from app.models.coupon_types import DiscountType, CouponStatus

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.payment import Order


class Coupon(BaseModel, TimestampMixin):
    """Coupon model."""

    __tablename__ = "coupons"

    code: Mapped[str] = mapped_column(String(20), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    discount_type: Mapped[DiscountType] = mapped_column(
        SQLEnum(DiscountType), nullable=False
    )
    discount_value: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    min_amount: Mapped[float | None] = mapped_column(Numeric(10, 2), nullable=True)
    max_discount: Mapped[float | None] = mapped_column(Numeric(10, 2), nullable=True)
    usage_limit: Mapped[int | None] = mapped_column(Integer, nullable=True)
    used_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    valid_from: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    valid_until: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)


class UserCoupon(BaseModel, TimestampMixin):
    """User coupon model."""

    __tablename__ = "user_coupons"

    user_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    coupon_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        ForeignKey("coupons.id", ondelete="CASCADE"),
        nullable=False,
    )
    status: Mapped[CouponStatus] = mapped_column(
        SQLEnum(CouponStatus), default=CouponStatus.AVAILABLE, nullable=False, index=True
    )
    used_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    order_id: Mapped[str | None] = mapped_column(UUID(as_uuid=False), nullable=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
