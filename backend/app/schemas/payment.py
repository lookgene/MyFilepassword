"""Payment schemas."""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field

from app.models.payment_types import OrderStatus, PaymentMethod


class OrderCreate(BaseModel):
    """Order creation schema."""

    task_id: str | None = None
    crack_type: str | None = None
    payment_method: PaymentMethod
    coupon_code: str | None = Field(None, max_length=20)


class OrderPayment(BaseModel):
    """Order payment schema."""

    method: PaymentMethod
    qr_code: str | None = None
    payment_url: str | None = None


class OrderResponse(BaseModel):
    """Order response schema."""

    order_id: str
    order_no: str
    user_id: str
    task: dict[str, Any] | None
    amount: float
    discount: float
    final_amount: float
    currency: str
    status: OrderStatus
    payment_method: PaymentMethod | None
    payment: OrderPayment | None = None
    paid_at: datetime | None
    expires_at: datetime | None
    created_at: datetime


class OrderListResponse(BaseModel):
    """Order list response schema."""

    items: list[OrderResponse]
    total: int
    page: int
    page_size: int
    pages: int


class RefundCreate(BaseModel):
    """Refund creation schema."""

    reason: str = Field(..., max_length=500)
    amount: float | None = None


class RefundResponse(BaseModel):
    """Refund response schema."""

    refund_id: str
    order_id: str
    user_id: str
    refund_no: str
    amount: float
    status: OrderStatus
    reason: str
    created_at: datetime
    completed_at: datetime | None


class CouponValidate(BaseModel):
    """Coupon validation schema."""

    coupon_code: str


class CouponInfo(BaseModel):
    """Coupon info schema."""

    coupon_code: str
    discount_type: str
    discount_value: float
    min_amount: float | None
    max_discount: float | None
    expires_at: datetime
    usable: bool
