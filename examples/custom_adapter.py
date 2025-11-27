"""Example of creating a custom adapter for a different VPN panel."""

from src.domain.entities import Client, Inbound, InboundTraffic, ServerStats
from src.domain.ports import VPNServerPort


class CustomVPNAdapter(VPNServerPort):
    """Example adapter for a custom VPN panel API.

    This is a template showing how to implement a new adapter
    for a different VPN panel while maintaining the same domain interface.
    """

    def __init__(self, base_url: str, api_token: str) -> None:
        self._base_url = base_url
        self._api_token = api_token

    async def authenticate(self) -> bool:
        """Authenticate with the VPN panel."""
        # Implement your authentication logic here
        raise NotImplementedError("Implement authentication for your VPN panel")

    async def get_inbounds(self) -> list[Inbound]:
        """Get all inbounds."""
        raise NotImplementedError("Implement get_inbounds for your VPN panel")

    async def get_inbound(self, inbound_id: int) -> Inbound:
        """Get inbound by ID."""
        raise NotImplementedError("Implement get_inbound for your VPN panel")

    async def create_inbound(self, inbound: Inbound) -> Inbound:
        """Create new inbound."""
        raise NotImplementedError("Implement create_inbound for your VPN panel")

    async def update_inbound(self, inbound_id: int, inbound: Inbound) -> Inbound:
        """Update existing inbound."""
        raise NotImplementedError("Implement update_inbound for your VPN panel")

    async def delete_inbound(self, inbound_id: int) -> bool:
        """Delete inbound."""
        raise NotImplementedError("Implement delete_inbound for your VPN panel")

    async def add_client(self, inbound_id: int, client: Client) -> Client:
        """Add client to inbound."""
        raise NotImplementedError("Implement add_client for your VPN panel")

    async def update_client(self, inbound_id: int, client_id: str, client: Client) -> Client:
        """Update client in inbound."""
        raise NotImplementedError("Implement update_client for your VPN panel")

    async def delete_client(self, inbound_id: int, client_id: str) -> bool:
        """Delete client from inbound."""
        raise NotImplementedError("Implement delete_client for your VPN panel")

    async def get_traffic_stats(self) -> list[InboundTraffic]:
        """Get traffic statistics for all inbounds."""
        raise NotImplementedError("Implement get_traffic_stats for your VPN panel")

    async def get_server_stats(self) -> ServerStats:
        """Get server statistics."""
        raise NotImplementedError("Implement get_server_stats for your VPN panel")
