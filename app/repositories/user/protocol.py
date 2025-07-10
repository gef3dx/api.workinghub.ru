from typing import Protocol, runtime_checkable, Optional, List

from app.models.entities.user import User
from app.repositories.base import BaseRepositoryProtocol


@runtime_checkable
class UserRepositoryProtocol(BaseRepositoryProtocol, Protocol):
    """User repository protocol."""

    async def get_by_username(self, username: str) -> Optional[User]:
        """Get user by username."""
        ...

    async def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        ...

    async def get_active_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        """Get active users."""
        ...
