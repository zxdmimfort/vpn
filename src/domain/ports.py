"""Domain ports (interfaces)."""

from abc import ABC, abstractmethod

from src.domain.entities import Client, Inbound, InboundTraffic, ServerStats


class VPNServerPort(ABC):
    """Port for VPN server operations."""

    @abstractmethod
    async def authenticate(self) -> bool:
        """Authenticate with VPN server."""
        ...

    @abstractmethod
    async def get_inbounds(self) -> list[Inbound]:
        """Get all inbounds."""
        ...

    @abstractmethod
    async def get_inbound(self, inbound_id: int) -> Inbound:
        """Get inbound by ID."""
        ...

    @abstractmethod
    async def create_inbound(self, inbound: Inbound) -> Inbound:
        """Create new inbound."""
        ...

    @abstractmethod
    async def update_inbound(self, inbound_id: int, inbound: Inbound) -> Inbound:
        """Update existing inbound."""
        ...

    @abstractmethod
    async def delete_inbound(self, inbound_id: int) -> bool:
        """Delete inbound."""
        ...

    @abstractmethod
    async def add_client(self, inbound_id: int, client: Client) -> Client:
        """Add client to inbound."""
        ...

    @abstractmethod
    async def get_client(self, inbound_id: int, client_id: str) -> Client:
        """Get client from inbound."""
        ...

    @abstractmethod
    async def update_client(self, inbound_id: int, client_id: str, client: Client) -> Client:
        """Update client in inbound."""
        ...

    @abstractmethod
    async def delete_client(self, inbound_id: int, client_id: str) -> bool:
        """Delete client from inbound."""
        ...

    @abstractmethod
    async def get_traffic_stats(self) -> list[InboundTraffic]:
        """Get traffic statistics for all inbounds."""
        ...

    @abstractmethod
    async def get_server_stats(self) -> ServerStats:
        """Get server statistics."""
        ...
