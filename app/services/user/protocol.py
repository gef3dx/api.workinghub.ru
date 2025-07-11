from typing import List, Optional, Protocol, runtime_checkable

from app.models.entities.user import User
from app.models.schemas.user import UserCreateSchema, UserUpdateSchema


@runtime_checkable
class UserServiceProtocol(Protocol):
    """User service protocol."""

    async def create_user(self, data: UserCreateSchema) -> User:
        """Create new user."""
        ...

    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID."""
        ...

    async def get_user_by_uuid(self, user_uuid: str) -> Optional[User]:
        """Get user by UUID."""
        ...

    async def get_user_by_username(self, username: str) -> Optional[User]:
        """Get user by username."""
        ...

    async def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        ...

    async def get_all_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        """Get all users."""
        ...

    async def update_user(self, user_id: int, data: UserUpdateSchema) -> Optional[User]:
        """Update user."""
        ...

    async def delete_user(self, user_id: int) -> bool:
        """Delete user."""
        ...
