"""Repository for client metadata persistence."""

from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.persistence.models import ClientMetadata


class ClientMetadataRepository:
    """Repository for managing client metadata in database."""

    def __init__(self, session: AsyncSession) -> None:
        """Initialize repository with database session.

        Args:
            session: SQLAlchemy async session
        """
        self.session = session

    async def create(self, client_id: str, owner_ref: Optional[str] = None) -> ClientMetadata:
        """Create new client metadata record.

        Args:
            client_id: VPN client UUID
            owner_ref: User ID from billing system

        Returns:
            Created ClientMetadata instance
        """
        metadata = ClientMetadata(
            client_id=client_id,
            owner_ref=owner_ref,
        )
        self.session.add(metadata)
        await self.session.flush()
        return metadata

    async def get_by_client_id(self, client_id: str) -> Optional[ClientMetadata]:
        """Get client metadata by VPN client ID.

        Args:
            client_id: VPN client UUID

        Returns:
            ClientMetadata if found, None otherwise
        """
        stmt = select(ClientMetadata).where(ClientMetadata.client_id == client_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_owner_ref(self, owner_ref: str) -> list[ClientMetadata]:
        """Get all client metadata records for a specific owner.

        Args:
            owner_ref: User ID from billing system

        Returns:
            List of ClientMetadata instances
        """
        stmt = select(ClientMetadata).where(ClientMetadata.owner_ref == owner_ref)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def update_owner_ref(
        self, client_id: str, owner_ref: Optional[str]
    ) -> Optional[ClientMetadata]:
        """Update owner_ref for existing client.

        Args:
            client_id: VPN client UUID
            owner_ref: New user ID from billing system

        Returns:
            Updated ClientMetadata if found, None otherwise
        """
        metadata = await self.get_by_client_id(client_id)
        if metadata:
            metadata.owner_ref = owner_ref
            await self.session.flush()
        return metadata

    async def delete(self, client_id: str) -> bool:
        """Delete client metadata.

        Args:
            client_id: VPN client UUID

        Returns:
            True if deleted, False if not found
        """
        metadata = await self.get_by_client_id(client_id)
        if metadata:
            await self.session.delete(metadata)
            await self.session.flush()
            return True
        return False
