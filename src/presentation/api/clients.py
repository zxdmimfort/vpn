"""Client management API endpoints."""

import uuid

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, HTTPException, status

from src.application.services import VPNManagementService
from src.domain.entities import Client, ClientFlow
from src.domain.exceptions import ClientNotFoundException, DomainException
from src.infrastructure.persistence import ClientMetadataRepository
from src.presentation.api.adapters import client_to_response
from src.presentation.api.schemas import (
    ClientCreateRequest,
    ClientResponse,
    ClientUpdateRequest,
)

router = APIRouter(
    prefix="/inbounds/{inbound_id}/clients",
    tags=["clients"],
    route_class=DishkaRoute,
)


def client_create_request_to_entity(request: ClientCreateRequest) -> Client:
    """Convert ClientCreateRequest to Client entity with generated UUID and email."""
    # Генерируем уникальный email на основе UUID
    client_uuid = uuid.uuid4()
    email = f"client-{client_uuid.hex[:16]}@vpn.local"

    return Client(
        id=str(client_uuid),  # Используем тот же UUID
        email=email,  # Генерируем email автоматически
        enable=True,
        flow=ClientFlow.XTLS_RPRX_VISION,
        limitIp=request.limit_ip,
        totalGB=request.total_gb,
        expireTime=request.expired,
        reset=0,
        subId="",
    )


@router.get("/{client_id}", response_model=ClientResponse, status_code=status.HTTP_200_OK)
async def get_client(
    inbound_id: int,
    client_id: str,
    service: FromDishka[VPNManagementService],
    metadata_repo: FromDishka[ClientMetadataRepository],
) -> ClientResponse:
    """Get client from inbound."""
    try:
        # Get inbound to access clientStats
        inbound = await service.get_inbound(inbound_id)
        client = await service.get_client(inbound_id, client_id)

        # Find client stats
        client_stat = next(
            (stat for stat in inbound.clientStats if stat.email == client.email), None
        )

        # Get metadata from database
        metadata = await metadata_repo.get_by_client_id(client_id)

        return client_to_response(client, client_stat, metadata)
    except ClientNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e
    except DomainException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        ) from e


@router.post("", response_model=ClientResponse, status_code=status.HTTP_201_CREATED)
async def add_client(
    inbound_id: int,
    request: ClientCreateRequest,
    service: FromDishka[VPNManagementService],
    metadata_repo: FromDishka[ClientMetadataRepository],
) -> ClientResponse:
    """Add client to inbound."""
    try:
        client = client_create_request_to_entity(request)
        await service.add_client(inbound_id, client)

        # Save metadata to database
        metadata = await metadata_repo.create(
            client_id=client.id,
            owner_ref=request.owner_ref,
        )

        # Get full inbound to get client with stats
        inbound = await service.get_inbound(inbound_id)
        client = await service.get_client(inbound_id, client.id)

        # Find client stats
        client_stat = next(
            (stat for stat in inbound.clientStats if stat.email == client.email), None
        )

        return client_to_response(client, client_stat, metadata)
    except DomainException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        ) from e


@router.put("/{client_id}", response_model=ClientResponse)
async def update_client(
    inbound_id: int,
    client_id: str,
    request: ClientUpdateRequest,
    service: FromDishka[VPNManagementService],
    metadata_repo: FromDishka[ClientMetadataRepository],
) -> ClientResponse:
    """Update client in inbound."""
    try:
        # Get existing inbound to find client
        inbound = await service.get_inbound(inbound_id)

        existing_client = None
        for client in inbound.settings.clients:
            if client.id == client_id:
                existing_client = client
                break

        if not existing_client:
            raise ClientNotFoundException(f"Client {client_id} not found")

        # Update only provided fields, mapping snake_case to camelCase
        update_data = request.model_dump(exclude_unset=True)

        # Update owner_ref in database if provided
        if "owner_ref" in update_data:
            await metadata_repo.update_owner_ref(client_id, update_data.pop("owner_ref"))

        field_mapping = {
            "limit_ip": "limitIp",
            "total_gb": "reset",
            "expire_time": "expireTime",
        }

        for field, value in update_data.items():
            # Map snake_case to camelCase if needed
            entity_field = field_mapping.get(field, field)
            setattr(existing_client, entity_field, value)

        updated_client = await service.update_client(inbound_id, client_id, existing_client)

        # Get updated inbound to get fresh stats
        updated_inbound = await service.get_inbound(inbound_id)
        client_stat = next(
            (stat for stat in updated_inbound.clientStats if stat.email == updated_client.email),
            None,
        )

        # Get metadata from database
        metadata = await metadata_repo.get_by_client_id(client_id)

        return client_to_response(updated_client, client_stat, metadata)
    except ClientNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e
    except DomainException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        ) from e


@router.delete("/{client_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_client(
    inbound_id: int,
    client_id: str,
    service: FromDishka[VPNManagementService],
    metadata_repo: FromDishka[ClientMetadataRepository],
) -> None:
    """Delete client from inbound."""
    try:
        await service.delete_client(inbound_id, client_id)
        # Also delete metadata from database
        await metadata_repo.delete(client_id)
    except ClientNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e
    except DomainException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        ) from e
