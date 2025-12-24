"""Initialize database."""

import asyncio

from sqlalchemy import select

from app.core.security import get_password_hash
from app.db.session import AsyncSessionLocal
from app.models.user import User, UserProfile, Membership
from app.models.user_types import MembershipPlan


async def create_admin_user() -> None:
    """Create admin user."""
    async with AsyncSessionLocal() as db:
        # Check if admin already exists
        result = await db.execute(select(User).where(User.email == "admin@example.com"))
        existing_admin = result.scalar_one_or_none()

        if existing_admin:
            print("Admin user already exists")
            return

        # Create admin user
        admin = User(
            email="admin@example.com",
            password_hash=get_password_hash("Admin123!"),
            username="Admin",
            is_active=True,
            is_verified=True,
            is_admin=True,
        )
        db.add(admin)

        # Create profile
        profile = UserProfile(
            user_id=admin.id,
            language="zh-CN",
            timezone="Asia/Shanghai",
        )
        db.add(profile)

        # Create membership
        membership = Membership(
            user_id=admin.id,
            plan=MembershipPlan.ENTERPRISE,
        )
        db.add(membership)

        await db.commit()
        print(f"Admin user created: {admin.id}")
        print("Email: admin@example.com")
        print("Password: Admin123!")


async def init_db() -> None:
    """Initialize database."""
    print("Initializing database...")
    await create_admin_user()
    print("Database initialized successfully")


if __name__ == "__main__":
    asyncio.run(init_db())
