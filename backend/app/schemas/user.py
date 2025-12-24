"""User schemas."""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, EmailStr, Field, field_validator

from app.models.user_types import MembershipPlan


class UserBase(BaseModel):
    """Base user schema."""

    username: str | None = Field(None, min_length=2, max_length=50)
    email: EmailStr


class UserCreate(UserBase):
    """User creation schema."""

    password: str = Field(..., min_length=8, max_length=100)
    confirm_password: str = Field(..., min_length=8, max_length=100)
    invite_code: str | None = Field(None, max_length=20)

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        """Validate password strength."""
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(c.islower() for c in v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one digit")
        return v

    @field_validator("confirm_password")
    @classmethod
    def passwords_match(cls, v: str, info: Any) -> str:
        """Validate passwords match."""
        if "password" in info.data and v != info.data["password"]:
            raise ValueError("Passwords do not match")
        return v


class UserUpdate(BaseModel):
    """User update schema."""

    username: str | None = Field(None, min_length=2, max_length=50)
    avatar: str | None = Field(None, max_length=500)
    phone: str | None = Field(None, max_length=20)


class UserResponse(BaseModel):
    """User response schema."""

    user_id: str
    email: str
    username: str | None
    avatar: str | None
    is_active: bool
    is_verified: bool
    membership: MembershipPlan
    created_at: datetime
    updated_at: datetime

    class Config:
        """Pydantic config."""

        from_attributes = True


class UserProfileResponse(BaseModel):
    """User profile response schema."""

    avatar: str | None
    phone: str | None
    country: str | None
    language: str
    timezone: str
    preferences: dict[str, Any]


class MembershipResponse(BaseModel):
    """Membership response schema."""

    plan: MembershipPlan
    expire_at: datetime | None
    auto_renew: bool
    benefits: dict[str, Any] | None = None


class UserInResponse(UserResponse):
    """User in response with additional info."""

    profile: UserProfileResponse
    membership: MembershipResponse
    stats: dict[str, Any] | None = None


class LoginRequest(BaseModel):
    """Login request schema."""

    email: EmailStr
    password: str


class RegisterRequest(UserCreate):
    """Register request schema."""

    pass


class TokenResponse(BaseModel):
    """Token response schema."""

    user_id: str
    email: str
    username: str | None
    avatar: str | None
    membership: MembershipPlan
    access_token: str
    refresh_token: str
    expires_in: int


class ChangePasswordRequest(BaseModel):
    """Change password request schema."""

    old_password: str = Field(..., min_length=8)
    new_password: str = Field(..., min_length=8, max_length=100)


class ForgotPasswordRequest(BaseModel):
    """Forgot password request schema."""

    email: EmailStr


class ResetPasswordRequest(BaseModel):
    """Reset password request schema."""

    token: str
    password: str = Field(..., min_length=8, max_length=100)
    confirm_password: str = Field(..., min_length=8, max_length=100)
