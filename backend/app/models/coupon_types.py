"""Coupon model type definitions."""

from enum import Enum


class CouponStatus(str, Enum):
    """User coupon status enum."""

    AVAILABLE = "available"
    USED = "used"
    EXPIRED = "expired"
