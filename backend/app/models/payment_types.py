"""Payment model type definitions."""

from enum import Enum


class OrderStatus(str, Enum):
    """Order status enum."""

    PENDING = "pending"
    PROCESSING = "processing"
    PAID = "paid"
    FAILED = "failed"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"
    EXPIRED = "expired"


class PaymentMethod(str, Enum):
    """Payment method enum."""

    WECHAT = "wechat"
    ALIPAY = "alipay"
    STRIPE = "stripe"
    CREDIT_CARD = "credit_card"
    BANK_TRANSFER = "bank_transfer"


class DiscountType(str, Enum):
    """Discount type enum."""

    PERCENT = "percent"
    FIXED = "fixed"
