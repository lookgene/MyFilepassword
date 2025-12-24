"""User service."""

from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_password_hash
from app.models.user import User, UserProfile, Membership
from app.models.user_types import MembershipPlan


class UserService:
    """User service class."""

    def __init__(self, db: AsyncSession):
        """Initialize user service.

        Args:
            db: Database session
        """
        self.db = db

    async def get_by_id(self, user_id: str) -> User | None:
        """Get user by ID.

        Args:
            user_id: User ID

        Returns:
            User object or None
        """
        result = await self.db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> User | None:
        """Get user by email.

        Args:
            email: User email

        Returns:
            User object or None
        """
        result = await self.db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def create(
        self,
        email: str,
        password: str,
        username: str | None = None,
    ) -> User:
        """Create a new user.

        Args:
            email: User email
            password: User password
            username: Optional username

        Returns:
            Created user object
        """
        # Create user
        user = User(
            email=email,
            password_hash=get_password_hash(password),
            username=username,
            is_active=True,
            is_verified=False,
        )
        self.db.add(user)

        # Create user profile
        profile = UserProfile(
            user_id=user.id,
            language="zh-CN",
            timezone="Asia/Shanghai",
            preferences={},
        )
        self.db.add(profile)

        # Create membership
        membership = Membership(
            user_id=user.id,
            plan=MembershipPlan.FREE,
        )
        self.db.add(membership)

        await self.db.commit()
        await self.db.refresh(user)

        return user

    async def update(self, user_id: str, **kwargs: Any) -> User | None:
        """Update user.

        Args:
            user_id: User ID
            **kwargs: Fields to update

        Returns:
            Updated user object or None
        """
        user = await self.get_by_id(user_id)
        if user is None:
            return None

        for key, value in kwargs.items():
            if hasattr(user, key):
                setattr(user, key, value)

        await self.db.commit()
        await self.db.refresh(user)

        return user

    async def update_password(self, user_id: str, new_password: str) -> bool:
        """Update user password.

        Args:
            user_id: User ID
            new_password: New password

        Returns:
            True if successful
        """
        user = await self.get_by_id(user_id)
        if user is None:
            return False

        user.password_hash = get_password_hash(new_password)
        await self.db.commit()

        return True

    async def delete(self, user_id: str) -> bool:
        """Delete user.

        Args:
            user_id: User ID

        Returns:
            True if successful
        """
        user = await self.get_by_id(user_id)
        if user is None:
            return False

        await self.db.delete(user)
        await self.db.commit()

        return True
