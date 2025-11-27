"""Application services."""

from src.domain.entities import Client, Inbound, InboundTraffic, ServerStats
from src.domain.ports import VPNServerPort


class VPNManagementService:
    """VPN management service - application layer."""

    def __init__(self, vpn_server: VPNServerPort) -> None:
        self._vpn_server = vpn_server

    async def ensure_authenticated(self) -> None:
        """Ensure authentication with VPN server."""
        await self._vpn_server.authenticate()

    async def list_inbounds(self) -> list[Inbound]:
        """List all inbounds."""
        await self.ensure_authenticated()
        return await self._vpn_server.get_inbounds()

    async def get_inbound(self, inbound_id: int) -> Inbound:
        """Get inbound by ID."""
        await self.ensure_authenticated()
        return await self._vpn_server.get_inbound(inbound_id)

    async def create_inbound(self, inbound: Inbound) -> Inbound:
        """Create new inbound."""
        await self.ensure_authenticated()
        return await self._vpn_server.create_inbound(inbound)

    async def update_inbound(self, inbound_id: int, inbound: Inbound) -> Inbound:
        """Update existing inbound."""
        await self.ensure_authenticated()
        return await self._vpn_server.update_inbound(inbound_id, inbound)

    async def delete_inbound(self, inbound_id: int) -> bool:
        """Delete inbound."""
        await self.ensure_authenticated()
        return await self._vpn_server.delete_inbound(inbound_id)

    async def add_client(self, inbound_id: int, client: Client) -> Client:
        """Add client to inbound."""
        await self.ensure_authenticated()
        return await self._vpn_server.add_client(inbound_id, client)

    async def get_client(self, inbound_id: int, client_id: str) -> Client:
        """Get client from inbound."""
        await self.ensure_authenticated()
        return await self._vpn_server.get_client(inbound_id, client_id)

    async def update_client(self, inbound_id: int, client_id: str, client: Client) -> Client:
        """Update client in inbound."""
        await self.ensure_authenticated()
        return await self._vpn_server.update_client(inbound_id, client_id, client)

    async def delete_client(self, inbound_id: int, client_id: str) -> bool:
        """Delete client from inbound."""
        await self.ensure_authenticated()
        return await self._vpn_server.delete_client(inbound_id, client_id)

    async def get_traffic_stats(self) -> list[InboundTraffic]:
        """Get traffic statistics."""
        await self.ensure_authenticated()
        return await self._vpn_server.get_traffic_stats()

    async def get_server_stats(self) -> ServerStats:
        """Get server statistics."""
        await self.ensure_authenticated()
        return await self._vpn_server.get_server_stats()
