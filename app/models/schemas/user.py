from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from app.models.entities.user import User


@dataclass(frozen=True)
class UserCreateSchema:
    """User creation schema."""

    username: str
    email: str
    full_name: Optional[str] = None


@dataclass(frozen=True)
class UserUpdateSchema:
    """User update schema."""

    username: Optional[str] = None
    email: Optional[str] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = None


@dataclass(frozen=True)
class UserResponseSchema:
    """User response schema."""

    id: int
    uuid: str
    username: str
    email: str
    full_name: Optional[str]
    is_active: bool
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_entity(cls, user: User) -> "UserResponseSchema":
        """Create schema from entity."""
        return cls(
            id=user.id,
            uuid=user.uuid,
            username=user.username,
            email=user.email,
            full_name=user.full_name,
            is_active=user.is_active,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )
