"""Adapters for converting between domain entities and API schemas."""

from src.domain.entities import Client, ClientStat, Inbound
from src.infrastructure.persistence.models import ClientMetadata
from src.presentation.api.schemas import ClientResponse, InboundResponse


def client_to_response(
    client: Client,
    client_stat: ClientStat | None = None,
    metadata: ClientMetadata | None = None,
) -> ClientResponse:
    """Convert Client entity to ClientResponse schema.

    Maps camelCase entity fields to snake_case API fields.
    Uses ClientStat for traffic statistics if provided.
    Uses ClientMetadata for owner_ref if provided.
    """
    # Get traffic stats from ClientStat or use defaults
    up = client_stat.up if client_stat else 0
    down = client_stat.down if client_stat else 0
    all_time = client_stat.allTime if client_stat else 0

    return ClientResponse(
        id=client.id,
        email=client.email,
        enable=client.enable,
        limit_ip=client.limitIp,
        total_gb=up + down,  # Сумма входящего и исходящего трафика
        all_time_gb=all_time,  # Весь трафик за все время
        expire_time=client.expireTime,
        owner_ref=metadata.owner_ref if metadata else None,
    )


def inbound_to_response(inbound: Inbound) -> InboundResponse:
    """Convert Inbound entity to InboundResponse schema.

    Maps camelCase entity fields to snake_case API fields and converts clients.
    Enriches client data with statistics from clientStats.
    """
    # Create a mapping of email to ClientStat for quick lookup
    stats_by_email = {stat.email: stat for stat in inbound.clientStats}

    # Convert clients with their stats
    clients = [
        client_to_response(client, stats_by_email.get(client.email))
        for client in inbound.settings.clients
    ]

    return InboundResponse(
        id=inbound.id,
        up=inbound.up,
        down=inbound.down,
        total=inbound.total,
        remark=inbound.remark,
        enable=inbound.enable,
        port=inbound.port,
        protocol=inbound.protocol,
        settings=inbound.settings.model_dump(),
        stream_settings=inbound.stream_settings,
        sniffing=inbound.sniffing,
        clients=clients,
    )
