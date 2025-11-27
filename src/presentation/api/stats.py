"""Statistics API endpoints."""

from dishka import FromDishka
from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter, HTTPException, status

from src.application.services import VPNManagementService
from src.domain.entities import InboundTraffic, ServerStats
from src.domain.exceptions import DomainException
from src.presentation.api.schemas import InboundTrafficResponse, ServerStatsResponse

router = APIRouter(prefix="/stats", tags=["statistics"], route_class=DishkaRoute)


@router.get("/traffic", response_model=list[InboundTrafficResponse])
async def get_traffic_stats(
    service: FromDishka[VPNManagementService],
) -> list[InboundTraffic]:
    """Get traffic statistics for all inbounds."""
    try:
        return await service.get_traffic_stats()
    except DomainException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        ) from e


@router.get("/server", response_model=ServerStatsResponse)
async def get_server_stats(
    service: FromDishka[VPNManagementService],
) -> ServerStats:
    """Get server statistics."""
    try:
        return await service.get_server_stats()
    except DomainException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        ) from e
