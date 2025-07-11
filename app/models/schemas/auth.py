from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class LoginSchema:
    """Login schema."""

    username: str
    password: str


@dataclass(frozen=True)
class RegisterSchema:
    """Register schema."""

    username: str
    email: str
    password: str
    full_name: Optional[str] = None


@dataclass(frozen=True)
class TokenSchema:
    """Token schema."""

    access_token: str
    token_type: str = "bearer"


@dataclass(frozen=True)
class TokenDataSchema:
    """Token data schema."""

    username: Optional[str] = None
    user_id: Optional[int] = None


@dataclass(frozen=True)
class UserAuthSchema:
    """User auth schema."""

    id: int
    username: str
    email: str
    full_name: Optional[str]
    is_active: bool
