"""File endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_current_active_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.common import success_response, PaginationParams
from app.schemas.file import FileUploadRequest, FileResponse
from app.services.file_service import FileService

router = APIRouter()


@router.post("/upload-url", response_model=dict)
async def get_upload_url(
    file_data: FileUploadRequest,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Get presigned upload URL.

    Args:
        file_data: File information
        current_user: Current authenticated user
        db: Database session

    Returns:
        Upload URL and file ID
    """
    file_service = FileService(db)
    upload_info = await file_service.get_upload_url(current_user.id, file_data)

    return success_response(data=upload_info)


@router.post("/{file_id}/confirm", response_model=dict)
async def confirm_upload(
    file_id: str,
    etag: str,
    file_size: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Confirm file upload completion.

    Args:
        file_id: File ID
        etag: File ETag
        file_size: File size
        current_user: Current authenticated user
        db: Database session

    Returns:
        File information
    """
    file_service = FileService(db)
    file_info = await file_service.confirm_upload(
        file_id, current_user.id, etag, file_size
    )

    return success_response(data=file_info, message="文件上传成功")


@router.get("", response_model=dict)
async def list_files(
    pagination: PaginationParams = Depends(),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """List user's files.

    Args:
        pagination: Pagination parameters
        current_user: Current authenticated user
        db: Database session

    Returns:
        List of files
    """
    file_service = FileService(db)
    files = await file_service.list_files(current_user.id, pagination)

    return success_response(data=files)


@router.get("/{file_id}", response_model=dict)
async def get_file(
    file_id: str,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Get file information.

    Args:
        file_id: File ID
        current_user: Current authenticated user
        db: Database session

    Returns:
        File information
    """
    file_service = FileService(db)
    file = await file_service.get_file(file_id, current_user.id)

    if file is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found",
        )

    return success_response(data=file)


@router.delete("/{file_id}", response_model=dict)
async def delete_file(
    file_id: str,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Delete file.

    Args:
        file_id: File ID
        current_user: Current authenticated user
        db: Database session

    Returns:
        Success message
    """
    file_service = FileService(db)
    success = await file_service.delete_file(file_id, current_user.id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found",
        )

    return success_response(message="文件已删除")
