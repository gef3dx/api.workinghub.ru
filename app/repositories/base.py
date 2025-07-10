from typing import List, Optional, Protocol, runtime_checkable

from app.models.entities.user import User


@runtime_checkable
class BaseRepositoryProtocol(Protocol):
    """Base repository protocol."""

    async def create(self, **kwargs) -> User:
        """Create new entity."""
        ...

    async def get_by_id(self, entity_id: int) -> Optional[User]:
        """Get entity by ID."""
        ...

    async def get_by_uuid(self, entity_uuid: str) -> Optional[User]:
        """Get entity by UUID."""
        ...

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[User]:
        """Get all entities."""
        ...

    async def update(self, entity_id: int, **kwargs) -> Optional[User]:
        """Update entity."""
        ...

    async def delete(self, entity_id: int) -> bool:
        """Delete entity."""
        ...
