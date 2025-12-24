"""Authentication endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_current_user
from app.core.security import create_access_token, create_refresh_token, verify_password
from app.db.session import get_db
from app.models.user import User
from app.schemas.common import success_response
from app.schemas.user import (
    LoginRequest,
    RegisterRequest,
    TokenResponse,
    ChangePasswordRequest,
    ForgotPasswordRequest,
    ResetPasswordRequest,
)
from app.services.user_service import UserService
from app.services.auth_service import AuthService

router = APIRouter()


@router.post("/register", response_model=dict)
async def register(
    user_data: RegisterRequest,
    db: AsyncSession = Depends(get_db),
):
    """Register a new user.

    Args:
        user_data: User registration data
        db: Database session

    Returns:
        Created user data with tokens
    """
    auth_service = AuthService(db)
    user = await auth_service.register(
        email=user_data.email,
        password=user_data.password,
        username=user_data.username,
        invite_code=user_data.invite_code,
    )

    # Create tokens
    access_token = create_access_token(subject=user.id)
    refresh_token = create_refresh_token(subject=user.id)

    return success_response(
        data=TokenResponse(
            user_id=user.id,
            email=user.email,
            username=user.username,
            avatar=None,
            membership=user.memberships[0].plan if user.memberships else None,
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=30 * 60,  # 30 minutes
        ).model_dump(),
        message="注册成功",
    )


@router.post("/login", response_model=dict)
async def login(
    credentials: LoginRequest,
    db: AsyncSession = Depends(get_db),
):
    """User login.

    Args:
        credentials: Login credentials
        db: Database session

    Returns:
        User data with tokens
    """
    auth_service = AuthService(db)
    user = await auth_service.authenticate(
        email=credentials.email,
        password=credentials.password,
    )

    # Create tokens
    access_token = create_access_token(subject=user.id)
    refresh_token = create_refresh_token(subject=user.id)

    return success_response(
        data=TokenResponse(
            user_id=user.id,
            email=user.email,
            username=user.username,
            avatar=None,
            membership=user.memberships[0].plan if user.memberships else None,
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=30 * 60,
        ).model_dump(),
        message="登录成功",
    )


@router.post("/refresh", response_model=dict)
async def refresh_token(
    refresh_token: str,
    db: AsyncSession = Depends(get_db),
):
    """Refresh access token.

    Args:
        refresh_token: Refresh token
        db: Database session

    Returns:
        New access token
    """
    from app.core.security import verify_token

    payload = verify_token(refresh_token, token_type="refresh")
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )

    user_id: str = payload.get("sub")
    user_service = UserService(db)
    user = await user_service.get_by_id(user_id)

    if user is None or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive",
        )

    # Create new access token
    access_token = create_access_token(subject=user.id)

    return success_response(
        data={"access_token": access_token, "expires_in": 30 * 60},
        message="Token refreshed",
    )


@router.post("/logout", response_model=dict)
async def logout(
    current_user: User = Depends(get_current_user),
):
    """User logout.

    Args:
        current_user: Current authenticated user

    Returns:
        Success message
    """
    # In a JWT-based system, logout is handled client-side by removing the token
    # If using refresh token rotation, you would invalidate the refresh token here
    return success_response(message="登出成功")


@router.post("/forgot-password", response_model=dict)
async def forgot_password(
    request: ForgotPasswordRequest,
    db: AsyncSession = Depends(get_db),
):
    """Send password reset email.

    Args:
        request: Forgot password request
        db: Database session

    Returns:
        Success message
    """
    auth_service = AuthService(db)
    await auth_service.send_password_reset_email(request.email)

    return success_response(message="重置邮件已发送")


@router.post("/reset-password", response_model=dict)
async def reset_password(
    request: ResetPasswordRequest,
    db: AsyncSession = Depends(get_db),
):
    """Reset password with token.

    Args:
        request: Reset password request
        db: Database session

    Returns:
        Success message
    """
    auth_service = AuthService(db)
    await auth_service.reset_password(
        token=request.token,
        new_password=request.password,
    )

    return success_response(message="密码重置成功")


@router.post("/change-password", response_model=dict)
async def change_password(
    request: ChangePasswordRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Change password.

    Args:
        request: Change password request
        current_user: Current authenticated user
        db: Database session

    Returns:
        Success message
    """
    user_service = UserService(db)

    # Verify old password
    if not verify_password(request.old_password, current_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect",
        )

    # Update password
    await user_service.update_password(current_user.id, request.new_password)

    return success_response(message="密码修改成功")
