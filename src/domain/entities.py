"""Domain entities."""

from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class InboundProtocol(str, Enum):
    """VPN protocol types."""

    VMESS = "vmess"
    VLESS = "vless"
    TROJAN = "trojan"
    SHADOWSOCKS = "shadowsocks"


class InboundStatus(str, Enum):
    """Inbound status."""

    ACTIVE = "active"
    INACTIVE = "inactive"
    DISABLED = "disabled"


class TrafficResetStatus(str, Enum):
    """Inbound traffic reset status"""

    NEVER = "never"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"


class ClientFlow(str, Enum):
    XTLS_RPRX_VISION = "xtls-rprx-vision"
    XTLS_RPRX_VISION_UDP443 = "xtls-rprx-vision-udp443"
    NULL = ""


class Client(BaseModel):
    """VPN client entity."""

    comment: str = ""
    email: str
    created_at: int | None = None
    updated_at: int | None = None
    enable: bool = True
    expireTime: int = 0
    flow: ClientFlow = ClientFlow.XTLS_RPRX_VISION
    id: str
    limitIp: int = 0
    totalGB: int
    reset: int = 0
    subId: str = ""
    tgId: int = 0


class ClientStat(BaseModel):
    """Client stats section in Inbound"""

    id: int
    inboundId: int
    enable: bool
    email: str
    uuid: str
    subId: str
    up: int
    down: int
    allTime: int
    expiryTime: int
    total: int
    reset: int
    last: int


class Settings(BaseModel):
    """Settings section in Inbound"""

    clients: list[Client] = Field(default_factory=list)
    decryption: str = "none"
    encryption: str = "none"


class Sniffing(BaseModel):
    """Sniffing section in Inbound"""

    enabled: bool = True
    destOverride: list[str] = ["http", "tls", "quic", "fakedns"]
    metadataOnly: bool = False
    routeOnly: bool = False


class Inbound(BaseModel):
    """Inbound configuration entity."""

    id: int | None = None
    up: int = 0
    down: int = 0
    total: int = 0
    allTime: int = 0
    remark: str = "reality"
    enable: bool = True
    expiryTime: int = 0
    trafficReset: TrafficResetStatus = TrafficResetStatus.NEVER
    lastTrafficResetTime: int = 0
    listen: str = ""
    port: int = 443
    protocol: InboundProtocol = InboundProtocol.VLESS
    settings: Settings
    tag: str = "inbound-443"
    clientStats: list[ClientStat] = Field(default_factory=list)
    stream_settings: dict[str, Any] = Field(default_factory=dict)
    sniffing: dict[str, Any] = Field(default_factory=dict)


class InboundTraffic(BaseModel):
    """Inbound traffic statistics."""

    inbound_id: int
    up: int
    down: int
    total: int


class ServerStats(BaseModel):
    """Server statistics."""

    cpu_usage: float
    memory_usage: float
    disk_usage: float
    uptime: int
    network_up: int
    network_down: int
