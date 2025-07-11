from litestar import Controller, post, get, Request
from litestar.exceptions import HTTPException
from litestar.status_codes import HTTP_200_OK, HTTP_201_CREATED

from app.core.dependencies import get_auth_service
from app.core.middleware import get_current_user
from app.models.schemas.auth import (
    LoginSchema,
    RegisterSchema,
    TokenSchema,
    UserAuthSchema,
)
from app.models.schemas.user import UserResponseSchema
from app.services.auth.protocol import AuthServiceProtocol


class AuthController(Controller):
    """Auth controller."""

    path = "/auth"

    @post("/register", status_code=HTTP_201_CREATED)
    async def register(
        self, data: RegisterSchema, auth_service: AuthServiceProtocol
    ) -> UserResponseSchema:
        """Register new user."""
        try:
            user = await auth_service.register(data)
            return UserResponseSchema.from_entity(user)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    @post("/login", status_code=HTTP_200_OK)
    async def login(
        self, data: LoginSchema, auth_service: AuthServiceProtocol
    ) -> TokenSchema:
        """Login user."""
        try:
            token = await auth_service.login(data)
            return token
        except ValueError as e:
            raise HTTPException(status_code=401, detail=str(e))

    @get("/me", status_code=HTTP_200_OK)
    async def get_current_user_info(self, request: Request) -> UserAuthSchema:
        """Get current user info."""
        user = await get_current_user(request)
        if not user:
            raise HTTPException(status_code=401, detail="Not authenticated")
        return user
