from typing import List, Optional

from app.models.entities.user import User
from app.models.schemas.user import UserCreateSchema, UserUpdateSchema
from app.repositories.user.protocol import UserRepositoryProtocol
from app.services.user.protocol import UserServiceProtocol


class UserService(UserServiceProtocol):
    """User service implementation."""

    def __init__(self, user_repository: UserRepositoryProtocol):
        self.user_repository = user_repository

    async def create_user(self, data: UserCreateSchema) -> User:
        """Create new user."""
        # Check if user already exists
        existing_user = await self.user_repository.get_by_username(data.username)
        if existing_user:
            raise ValueError(f"User with username '{data.username}' already exists")

        existing_email = await self.user_repository.get_by_email(data.email)
        if existing_email:
            raise ValueError(f"User with email '{data.email}' already exists")

        return await self.user_repository.create(
            username=data.username, email=data.email, full_name=data.full_name
        )

    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID."""
        return await self.user_repository.get_by_id(user_id)

    async def get_user_by_uuid(self, user_uuid: str) -> Optional[User]:
        """Get user by UUID."""
        return await self.user_repository.get_by_uuid(user_uuid)

    async def get_user_by_username(self, username: str) -> Optional[User]:
        """Get user by username."""
        return await self.user_repository.get_by_username(username)

    async def get_all_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        """Get all users."""
        return await self.user_repository.get_all(skip=skip, limit=limit)

    async def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        return await self.user_repository.get_by_email(email)

    async def update_user(self, user_id: int, data: UserUpdateSchema) -> Optional[User]:
        """Update user."""
        update_data = {}

        if data.username is not None:
            # Check if username is taken by another user
            existing_user = await self.user_repository.get_by_username(data.username)
            if existing_user and existing_user.id != user_id:
                raise ValueError(f"Username '{data.username}' is already taken")
            update_data["username"] = data.username

        if data.email is not None:
            # Check if email is taken by another user
            existing_user = await self.user_repository.get_by_email(data.email)
            if existing_user and existing_user.id != user_id:
                raise ValueError(f"Email '{data.email}' is already taken")
            update_data["email"] = data.email

        if data.full_name is not None:
            update_data["full_name"] = data.full_name

        if data.is_active is not None:
            update_data["is_active"] = data.is_active

        if not update_data:
            return await self.user_repository.get_by_id(user_id)

        return await self.user_repository.update(user_id, **update_data)

    async def delete_user(self, user_id: int) -> bool:
        """Delete user."""
        return await self.user_repository.delete(user_id)
