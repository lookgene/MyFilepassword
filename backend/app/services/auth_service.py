"""Authentication service."""

import secrets
from datetime import datetime, timedelta

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import verify_password
from app.models.user import User
from app.services.user_service import UserService


class AuthService:
    """Authentication service class."""

    def __init__(self, db: AsyncSession):
        """Initialize auth service.

        Args:
            db: Database session
        """
        self.db = db
        self.user_service = UserService(db)

    async def register(
        self,
        email: str,
        password: str,
        username: str | None = None,
        invite_code: str | None = None,
    ) -> User:
        """Register a new user.

        Args:
            email: User email
            password: User password
            username: Optional username
            invite_code: Optional invite code

        Returns:
            Created user object

        Raises:
            ValueError: If email already exists
        """
        # Check if email already exists
        existing_user = await self.user_service.get_by_email(email)
        if existing_user:
            raise ValueError("Email already registered")

        # Create user
        user = await self.user_service.create(
            email=email,
            password=password,
            username=username or email.split("@")[0],
        )

        # TODO: Send verification email

        return user

    async def authenticate(
        self,
        email: str,
        password: str,
    ) -> User:
        """Authenticate user.

        Args:
            email: User email
            password: User password

        Returns:
            Authenticated user object

        Raises:
            ValueError: If credentials are invalid
        """
        user = await self.user_service.get_by_email(email)
        if not user:
            raise ValueError("Invalid email or password")

        if not verify_password(password, user.password_hash):
            raise ValueError("Invalid email or password")

        if not user.is_active:
            raise ValueError("User account is disabled")

        # Update last login time
        from sqlalchemy import update
        from app.models.user import User as UserModel

        await self.db.execute(
            update(UserModel)
            .where(UserModel.id == user.id)
            .values(last_login_at=datetime.utcnow())
        )
        await self.db.commit()

        return user

    async def send_password_reset_email(self, email: str) -> None:
        """Send password reset email.

        Args:
            email: User email
        """
        user = await self.user_service.get_by_email(email)
        if not user:
            # Don't reveal whether email exists
            return

        # Generate reset token
        reset_token = secrets.token_urlsafe(32)

        # Store reset token in cache (Redis)
        # TODO: Implement Redis cache for reset tokens

        # TODO: Send email with reset link

    async def reset_password(self, token: str, new_password: str) -> None:
        """Reset password with token.

        Args:
            token: Reset token
            new_password: New password

        Raises:
            ValueError: If token is invalid
        """
        # TODO: Verify token from cache
        # TODO: Update user password
        pass
