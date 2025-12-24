"""User model type definitions."""

from enum import Enum


class MembershipPlan(str, Enum):
    """Membership plan enum."""

    FREE = "free"
    BASIC = "basic"
    PREMIUM = "premium"
    ENTERPRISE = "enterprise"


class UserRole(str, Enum):
    """User role enum."""

    USER = "user"
    ADMIN = "admin"
    SUPER_ADMIN = "super_admin"
