from typing import Optional

from app.core.auth import auth_manager
from app.models.entities.user import User
from app.models.schemas.auth import LoginSchema, RegisterSchema, TokenSchema
from app.repositories.user.protocol import UserRepositoryProtocol
from app.services.auth.protocol import AuthServiceProtocol


class AuthService(AuthServiceProtocol):
    """Auth service implementation."""

    def __init__(self, user_repository: UserRepositoryProtocol):
        self.user_repository = user_repository

    async def register(self, data: RegisterSchema) -> User:
        """Register new user."""
        # Check if user already exists
        existing_user = await self.user_repository.get_by_username(data.username)
        if existing_user:
            raise ValueError(f"User with username '{data.username}' already exists")

        existing_email = await self.user_repository.get_by_email(data.email)
        if existing_email:
            raise ValueError(f"User with email '{data.email}' already exists")

        # Hash password
        hashed_password = auth_manager.get_password_hash(data.password)

        # Create user
        return await self.user_repository.create(
            username=data.username,
            email=data.email,
            password_hash=hashed_password,
            full_name=data.full_name,
        )

    async def login(self, data: LoginSchema) -> TokenSchema:
        """Login user."""
        # Get user by username
        user = await self.user_repository.get_by_username(data.username)
        if not user:
            raise ValueError("Invalid username or password")

        # Verify password
        if not auth_manager.verify_password(data.password, user.password_hash):
            raise ValueError("Invalid username or password")

        # Check if user is active
        if not user.is_active:
            raise ValueError("User account is disabled")

        # Create access token
        access_token = auth_manager.create_access_token(
            data={"sub": user.username, "user_id": user.id}
        )

        return TokenSchema(access_token=access_token)

    async def get_current_user(self, token: str) -> Optional[User]:
        """Get current user from token."""
        token_data = auth_manager.verify_token(token)
        if not token_data:
            return None

        user = await self.user_repository.get_by_id(token_data.user_id)
        if not user or not user.is_active:
            return None

        return user
