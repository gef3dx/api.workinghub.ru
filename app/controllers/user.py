from typing import List

from litestar import Controller, delete, get, post, put
from litestar.exceptions import HTTPException
from litestar.status_codes import HTTP_200_OK, HTTP_201_CREATED, HTTP_404_NOT_FOUND

from app.core.dependencies import get_user_service
from app.models.schemas.user import (
    UserCreateSchema,
    UserUpdateSchema,
    UserResponseSchema,
)
from app.services.user.protocol import UserServiceProtocol


class UserController(Controller):
    """User controller."""

    path = "/users"

    @post("/", status_code=HTTP_201_CREATED)
    async def create_user(
        self, data: UserCreateSchema, user_service: UserServiceProtocol
    ) -> UserResponseSchema:
        """Create new user."""
        try:
            user = await user_service.create_user(data)
            return UserResponseSchema.from_entity(user)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    @get("/{user_id:int}", status_code=HTTP_200_OK)
    async def get_user_by_id(
        self, user_id: int, user_service: UserServiceProtocol
    ) -> UserResponseSchema:
        """Get user by ID."""
        user = await user_service.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="User not found")
        return UserResponseSchema.from_entity(user)

    @get("/uuid/{user_uuid:str}", status_code=HTTP_200_OK)
    async def get_user_by_uuid(
        self, user_uuid: str, user_service: UserServiceProtocol
    ) -> UserResponseSchema:
        """Get user by UUID."""
        user = await user_service.get_user_by_uuid(user_uuid)
        if not user:
            raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="User not found")
        return UserResponseSchema.from_entity(user)

    @get("/username/{username:str}", status_code=HTTP_200_OK)
    async def get_user_by_username(
        self, username: str, user_service: UserServiceProtocol
    ) -> UserResponseSchema:
        """Get user by username."""
        user = await user_service.get_user_by_username(username)
        if not user:
            raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="User not found")
        return UserResponseSchema.from_entity(user)

    @get("/", status_code=HTTP_200_OK)
    async def get_all_users(
        self, user_service: UserServiceProtocol, skip: int = 0, limit: int = 100
    ) -> List[UserResponseSchema]:
        """Get all users."""
        users = await user_service.get_all_users(skip=skip, limit=limit)
        return [UserResponseSchema.from_entity(user) for user in users]

    @put("/{user_id:int}", status_code=HTTP_200_OK)
    async def update_user(
        self, user_id: int, data: UserUpdateSchema, user_service: UserServiceProtocol
    ) -> UserResponseSchema:
        """Update user."""
        try:
            user = await user_service.update_user(user_id, data)
            if not user:
                raise HTTPException(
                    status_code=HTTP_404_NOT_FOUND, detail="User not found"
                )
            return UserResponseSchema.from_entity(user)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    @delete("/{user_id:int}", status_code=HTTP_200_OK)
    async def delete_user(
        self, user_id: int, user_service: UserServiceProtocol
    ) -> dict:
        """Delete user."""
        deleted = await user_service.delete_user(user_id)
        if not deleted:
            raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="User not found")
        return {"message": "User deleted successfully"}
