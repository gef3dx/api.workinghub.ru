from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool

from app.config.settings import settings
from app.models.entities.base import Base


class DatabaseManager:
    """Database connection manager."""

    def __init__(self, database_url: str):
        # SQLite specific configuration
        connect_args = {
            "check_same_thread": False,
        }

        self.engine = create_async_engine(
            database_url,
            poolclass=StaticPool,
            connect_args=connect_args,
            echo=settings.debug,
        )

        self.async_session_maker = async_sessionmaker(
            bind=self.engine, class_=AsyncSession, expire_on_commit=False
        )

    async def create_all(self) -> None:
        """Create all tables."""
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def drop_all(self) -> None:
        """Drop all tables."""
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """Get database session."""
        async with self.async_session_maker() as session:
            yield session

    async def close(self) -> None:
        """Close database connection."""
        await self.engine.dispose()


# Singleton instance
database_manager = DatabaseManager(settings.database_url)
