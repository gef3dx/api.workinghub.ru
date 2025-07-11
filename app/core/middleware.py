from typing import Optional

from litestar import Request
from litestar.exceptions import NotAuthorizedException
from litestar.connection import ASGIConnection

from app.core.auth import auth_manager
from app.models.entities.user import User
from app.models.schemas.auth import UserAuthSchema


async def get_current_user(request: Request) -> Optional[UserAuthSchema]:
    """Get current user from token."""
    authorization: str = request.headers.get("Authorization")

    if not authorization:
        return None

    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            return None
    except ValueError:
        return None

    token_data = auth_manager.verify_token(token)
    if not token_data:
        return None

    # Get user from database
    from app.core.dependencies import get_user_service
    from app.core.database import database_manager

    async with database_manager.async_session_maker() as session:
        from app.repositories.user.implementation import UserRepository
        from app.services.user.implementation import UserService

        user_repo = UserRepository(session)
        user_service = UserService(user_repo)

        user = await user_service.get_user_by_id(token_data.user_id)
        if not user or not user.is_active:
            return None

        return UserAuthSchema(
            id=user.id,
            username=user.username,
            email=user.email,
            full_name=user.full_name,
            is_active=user.is_active,
        )


def require_auth(connection: ASGIConnection, _: any) -> None:
    """Require authentication guard."""
    if not hasattr(connection, "user") or not connection.user:
        raise NotAuthorizedException("Authentication required")
