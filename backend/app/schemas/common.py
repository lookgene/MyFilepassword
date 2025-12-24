"""Common schemas."""

from datetime import datetime
from typing import Any, Generic, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class SuccessResponse(BaseModel, Generic[T]):
    """Success response schema."""

    code: int = Field(0, description="Response code, 0 means success")
    message: str = Field("success", description="Response message")
    data: T | None = Field(None, description="Response data")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Response timestamp")


class ErrorResponse(BaseModel):
    """Error response schema."""

    code: int = Field(..., description="Error code")
    message: str = Field(..., description="Error message")
    errors: dict[str, Any] | None = Field(None, description="Detailed error information")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Response timestamp")


class PaginationParams(BaseModel):
    """Pagination parameters."""

    page: int = Field(1, ge=1, description="Page number")
    page_size: int = Field(20, ge=1, le=100, description="Number of items per page")


class PaginatedResponse(BaseModel, Generic[T]):
    """Paginated response schema."""

    items: list[T] = Field(..., description="List of items")
    total: int = Field(..., description="Total number of items")
    page: int = Field(..., description="Current page number")
    page_size: int = Field(..., description="Number of items per page")
    pages: int = Field(..., description="Total number of pages")


def success_response(data: T | None = None, message: str = "success") -> dict[str, Any]:
    """Create success response.

    Args:
        data: Response data
        message: Response message

    Returns:
        Success response dictionary
    """
    return {
        "code": 0,
        "message": message,
        "data": data,
        "timestamp": datetime.utcnow().isoformat(),
    }
