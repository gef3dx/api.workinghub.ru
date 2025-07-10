from typing import List, Optional

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.entities.user import User
from app.repositories.user.protocol import UserRepositoryProtocol


class UserRepository(UserRepositoryProtocol):
    """User repository implementation."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, **kwargs) -> User:
        """Create new user."""
        user = User(**kwargs)
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def get_by_id(self, entity_id: int) -> Optional[User]:
        """Get user by ID."""
        query = select(User).where(User.id == entity_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_by_uuid(self, entity_uuid: str) -> Optional[User]:
        """Get user by UUID."""
        query = select(User).where(User.uuid == entity_uuid)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[User]:
        """Get all users."""
        query = select(User).offset(skip).limit(limit)
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def update(self, entity_id: int, **kwargs) -> Optional[User]:
        """Update user."""
        query = (
            update(User).where(User.id == entity_id).values(**kwargs).returning(User)
        )
        result = await self.session.execute(query)
        await self.session.commit()
        return result.scalar_one_or_none()

    async def delete(self, entity_id: int) -> bool:
        """Delete user."""
        query = delete(User).where(User.id == entity_id)
        result = await self.session.execute(query)
        await self.session.commit()
        return result.rowcount > 0

    async def get_by_username(self, username: str) -> Optional[User]:
        """Get user by username."""
        query = select(User).where(User.username == username)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        query = select(User).where(User.email == email)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_active_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        """Get active users."""
        query = select(User).where(User.is_active == True).offset(skip).limit(limit)
        result = await self.session.execute(query)
        return list(result.scalars().all())
