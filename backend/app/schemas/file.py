"""File schemas."""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class FileUploadRequest(BaseModel):
    """File upload request schema."""

    file_name: str = Field(..., max_length=255)
    file_size: int = Field(..., gt=0)
    content_type: str = Field(..., max_length=100)


class FileUploadResponse(BaseModel):
    """File upload response schema."""

    upload_url: str
    file_id: str
    expires_in: int
    max_file_size: int


class FileBase(BaseModel):
    """Base file schema."""

    file_name: str
    file_size: int
    file_type: str
    mime_type: str


class FileResponse(FileBase):
    """File response schema."""

    file_id: str
    user_id: str
    storage_key: str
    storage_provider: str
    md5_hash: str | None
    sha256_hash: str | None
    is_encrypted: bool
    encryption_info: dict[str, Any] | None
    scan_status: str
    scan_result: str | None
    status: str
    task_id: str | None
    created_at: datetime
    expires_at: datetime | None


class FileListResponse(BaseModel):
    """File list response schema."""

    items: list[FileResponse]
    total: int
    page: int
    page_size: int
    pages: int


class VirusScanStatus(BaseModel):
    """Virus scan status schema."""

    file_id: str
    scan_status: str
    scan_result: str | None
    scanned_at: datetime | None
