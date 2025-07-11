from typing import Optional, Protocol, runtime_checkable

from app.models.entities.user import User
from app.models.schemas.auth import LoginSchema, RegisterSchema, TokenSchema


@runtime_checkable
class AuthServiceProtocol(Protocol):
    """Auth service protocol."""

    async def register(self, data: RegisterSchema) -> User:
        """Register new user."""
        ...

    async def login(self, data: LoginSchema) -> TokenSchema:
        """Login user."""
        ...

    async def get_current_user(self, token: str) -> Optional[User]:
        """Get current user from token."""
        ...
