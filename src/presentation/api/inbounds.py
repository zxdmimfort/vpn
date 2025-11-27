"""Inbound management API endpoints."""

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, HTTPException, status

from src.application.services import VPNManagementService
from src.domain.entities import Inbound, Settings
from src.domain.exceptions import DomainException, InboundNotFoundException
from src.presentation.api.adapters import inbound_to_response
from src.presentation.api.schemas import (
    InboundCreateRequest,
    InboundResponse,
    InboundUpdateRequest,
)

router = APIRouter(prefix="/inbounds", tags=["inbounds"], route_class=DishkaRoute)


@router.get("", response_model=list[InboundResponse])
async def list_inbounds(
    service: FromDishka[VPNManagementService],
) -> list[InboundResponse]:
    """List all inbounds."""
    try:
        inbounds = await service.list_inbounds()
        return [inbound_to_response(inbound) for inbound in inbounds]
    except DomainException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        ) from e


@router.get("/{inbound_id}", response_model=InboundResponse)
async def get_inbound(
    inbound_id: int,
    service: FromDishka[VPNManagementService],
) -> InboundResponse:
    """Get inbound by ID."""
    try:
        inbound = await service.get_inbound(inbound_id)
        return inbound_to_response(inbound)
    except InboundNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e
    except DomainException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        ) from e


@router.post("", response_model=InboundResponse, status_code=status.HTTP_201_CREATED)
async def create_inbound(
    request: InboundCreateRequest,
    service: FromDishka[VPNManagementService],
) -> InboundResponse:
    """Create new inbound."""
    try:
        inbound = Inbound(
            remark=request.remark,
            enable=request.enable,
            port=request.port,
            protocol=request.protocol,
            settings=Settings(**request.settings),
            stream_settings=request.stream_settings,
            sniffing=request.sniffing,
        )
        created = await service.create_inbound(inbound)
        return inbound_to_response(created)
    except DomainException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        ) from e


@router.put("/{inbound_id}", response_model=InboundResponse)
async def update_inbound(
    inbound_id: int,
    request: InboundUpdateRequest,
    service: FromDishka[VPNManagementService],
) -> InboundResponse:
    """Update existing inbound."""
    try:
        # Get existing inbound
        existing = await service.get_inbound(inbound_id)

        # Update only provided fields
        update_data = request.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            # Convert settings dict to Settings object if needed
            if field == "settings" and isinstance(value, dict):
                value = Settings(**value)
            setattr(existing, field, value)

        updated = await service.update_inbound(inbound_id, existing)
        return inbound_to_response(updated)
    except InboundNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e
    except DomainException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        ) from e


@router.delete("/{inbound_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_inbound(
    inbound_id: int,
    service: FromDishka[VPNManagementService],
) -> None:
    """Delete inbound."""
    try:
        await service.delete_inbound(inbound_id)
    except InboundNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e
    except DomainException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        ) from e
