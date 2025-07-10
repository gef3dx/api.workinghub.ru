from typing import AsyncGenerator

from litestar.di import Provide
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import database_manager
from app.repositories.user.implementation import UserRepository
from app.services.user.implementation import UserService


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Get database session."""
    async for session in database_manager.get_session():
        yield session


async def get_user_repository(
    session: AsyncSession = Provide(get_db_session),
) -> UserRepository:
    """Get user repository."""
    return UserRepository(session)


async def get_user_service(
    user_repository: UserRepository = Provide(get_user_repository),
) -> UserService:
    """Get user service."""
    return UserService(user_repository)


# Dependency providers
dependencies = {
    "session": Provide(get_db_session),
    "user_repository": Provide(get_user_repository),
    "user_service": Provide(get_user_service),
}
