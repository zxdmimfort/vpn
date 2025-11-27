"""API request/response schemas."""

from typing import Any

from pydantic import BaseModel, Field

from src.domain.entities import InboundProtocol


class ClientCreateRequest(BaseModel):
    """Request schema for creating a client."""

    limit_ip: int = 0
    total_gb: int = 0
    expired: int = 0
    owner_ref: str | None = None  # user_id из биллинга для отладки и логгирования


class ClientUpdateRequest(BaseModel):
    """Request schema for updating a client."""

    email: str | None = None
    enable: bool | None = None
    flow: str | None = None
    limit_ip: int | None = None
    total_gb: int | None = None
    expire_time: int | None = None
    owner_ref: str | None = None  # user_id из биллинга для отладки и логгирования


class ClientResponse(BaseModel):
    """Response schema for client."""

    id: str
    email: str
    enable: bool
    limit_ip: int
    total_gb: int  # up + down
    all_time_gb: int  # allTime
    expire_time: int
    owner_ref: str | None = None  # user_id из биллинга для отладки и логгирования


class InboundCreateRequest(BaseModel):
    """Request schema for creating an inbound."""

    remark: str
    enable: bool = True
    port: int
    protocol: InboundProtocol
    settings: dict[str, Any] = Field(default_factory=dict)
    stream_settings: dict[str, Any] = Field(default_factory=dict)
    sniffing: dict[str, Any] = Field(default_factory=dict)


class InboundUpdateRequest(BaseModel):
    """Request schema for updating an inbound."""

    remark: str | None = None
    enable: bool | None = None
    port: int | None = None
    settings: dict[str, Any] | None = None
    stream_settings: dict[str, Any] | None = None
    sniffing: dict[str, Any] | None = None


class InboundResponse(BaseModel):
    """Response schema for inbound."""

    id: int | None
    up: int
    down: int
    total: int
    remark: str
    enable: bool
    port: int
    protocol: InboundProtocol
    settings: dict[str, Any]
    stream_settings: dict[str, Any]
    sniffing: dict[str, Any]
    clients: list[ClientResponse]


class InboundTrafficResponse(BaseModel):
    """Response schema for inbound traffic."""

    inbound_id: int
    up: int
    down: int
    total: int


class ServerStatsResponse(BaseModel):
    """Response schema for server statistics."""

    cpu_usage: float
    memory_usage: float
    disk_usage: float
    uptime: int
    network_up: int
    network_down: int


class ErrorResponse(BaseModel):
    """Error response schema."""

    detail: str
