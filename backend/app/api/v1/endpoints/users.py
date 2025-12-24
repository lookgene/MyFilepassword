"""User endpoints."""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_current_active_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.common import success_response
from app.schemas.user import UserResponse, UserUpdate
from app.services.user_service import UserService

router = APIRouter()


@router.get("/me", response_model=dict)
async def get_current_user_info(
    current_user: User = Depends(get_current_active_user),
):
    """Get current user information.

    Args:
        current_user: Current authenticated user

    Returns:
        User information
    """
    return success_response(
        data=UserResponse.model_validate(current_user).model_dump()
    )


@router.patch("/me", response_model=dict)
async def update_current_user(
    user_data: UserUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Update current user information.

    Args:
        user_data: User update data
        current_user: Current authenticated user
        db: Database session

    Returns:
        Updated user information
    """
    user_service = UserService(db)
    user = await user_service.update(current_user.id, **user_data.model_dump(exclude_unset=True))

    return success_response(
        data=UserResponse.model_validate(user).model_dump(),
        message="更新成功",
    )


@router.get("/me/stats", response_model=dict)
async def get_user_stats(
    current_user: User = Depends(get_current_active_user),
):
    """Get user statistics.

    Args:
        current_user: Current authenticated user

    Returns:
        User statistics
    """
    # TODO: Implement user statistics
    stats = {
        "total_tasks": 0,
        "success_tasks": 0,
        "failed_tasks": 0,
        "total_spent": 0.0,
    }

    return success_response(data=stats)
