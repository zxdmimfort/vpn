"""3x-ui API adapter."""

import json
import logging
from typing import Any

import httpx

from src.domain.entities import Client, Inbound, InboundTraffic, ServerStats, Settings
from src.domain.exceptions import (
    AuthenticationException,
    ClientNotFoundException,
    InboundNotFoundException,
    VPNServerException,
)
from src.domain.ports import VPNServerPort

logger = logging.getLogger(__name__)


class XUIAdapter(VPNServerPort):
    """Adapter for 3x-ui API."""

    def __init__(
        self,
        base_url: str,
        username: str,
        password: str,
        timeout: int = 30,
        verify_ssl: bool = True,
    ) -> None:
        self._base_url = base_url.rstrip("/")
        self._username = username
        self._password = password
        self._timeout = timeout
        self._verify_ssl = verify_ssl
        self._session: httpx.AsyncClient | None = None
        self._cookie: str | None = None

    async def _get_session(self) -> httpx.AsyncClient:
        """Get or create HTTP session."""
        if self._session is None:
            self._session = httpx.AsyncClient(
                base_url=self._base_url,
                timeout=self._timeout,
                follow_redirects=True,
                verify=self._verify_ssl,  # Отключаем проверку SSL если нужно
            )
        return self._session

    async def close(self) -> None:
        """Close HTTP session."""
        if self._session is not None:
            await self._session.aclose()
            self._session = None

    async def authenticate(self) -> bool:
        """Authenticate with 3x-ui panel."""
        session = await self._get_session()

        try:
            # 3x-ui ожидает JSON в теле запроса
            response = await session.post(
                "/login",
                json={
                    "username": self._username,
                    "password": self._password,
                },
            )
            response.raise_for_status()

            # Проверяем, что ответ не пустой
            if not response.text:
                # Если ответ пустой, но есть cookie - это может быть успех
                if "3x-ui" in response.cookies or "session" in response.cookies:
                    logger.info("Authentication successful (empty response but got cookies)")
                    self._cookie = response.cookies.get("3x-ui") or response.cookies.get("session")
                    return True
                else:
                    raise AuthenticationException(
                        "Empty response from server and no cookies received. "
                        "Check URL, username and password."
                    )

            # Пробуем распарсить JSON
            try:
                result = response.json()

                if not result.get("success"):
                    raise AuthenticationException(
                        f"Authentication failed: {result.get('msg', 'Unknown error')}"
                    )

                # Store session cookie
                self._cookie = response.cookies.get("3x-ui") or response.cookies.get("session")
                if not self._cookie:
                    logger.warning("No session cookie received, authentication may fail")

                return True

            except json.JSONDecodeError:
                # Если ответ не JSON, проверяем статус код и cookies
                if response.status_code == 200 and (
                    "3x-ui" in response.cookies or "session" in response.cookies
                ):
                    logger.info("Authentication successful (non-JSON response but got cookies)")
                    self._cookie = response.cookies.get("3x-ui") or response.cookies.get("session")
                    return True
                else:
                    raise AuthenticationException(
                        f"Invalid response format. Status: {response.status_code}, "
                        f"Response: {response.text[:200]}"
                    )

        except httpx.HTTPError as e:
            raise AuthenticationException(f"Authentication failed: {e}") from e

    async def _request(
        self,
        method: str,
        endpoint: str,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Make authenticated request to 3x-ui API."""
        session = await self._get_session()

        if self._cookie:
            kwargs.setdefault("cookies", {})["session"] = self._cookie
            # Также пробуем 3x-ui cookie
            kwargs["cookies"]["3x-ui"] = self._cookie

        try:
            logger.debug(f"API request: {method} {endpoint}")
            response = await session.request(method, endpoint, **kwargs)

            logger.debug(f"API response status: {response.status_code}")
            logger.debug(f"API response headers: {response.headers}")
            logger.debug(f"API response text: {response.text[:500]}")

            response.raise_for_status()

            # Проверяем, что ответ не пустой
            if not response.text:
                raise VPNServerException(
                    f"Empty response from {endpoint}. "
                    f"Status: {response.status_code}. "
                    f"Authentication may have failed or endpoint is incorrect."
                )

            result = response.json()
            logger.debug(f"API response JSON: {result}")

            if not result.get("success"):
                raise VPNServerException(result.get("msg", "Unknown error from 3x-ui API"))

            return result

        except json.JSONDecodeError as e:
            raise VPNServerException(
                f"Invalid JSON response from {endpoint}. Response: {response.text[:200]}"
            ) from e
        except httpx.HTTPError as e:
            raise VPNServerException(f"API request failed: {e}") from e

    async def get_inbounds(self) -> list[Inbound]:
        """Get all inbounds."""
        result = await self._request("GET", "/panel/api/inbounds/list")

        inbounds_data = result.get("obj", [])
        return [self._parse_inbound(data) for data in inbounds_data]

    async def get_inbound(self, inbound_id: int) -> Inbound:
        """Get inbound by ID."""
        result = await self._request("GET", f"/panel/api/inbounds/get/{inbound_id}")

        inbound_data = result.get("obj")
        if not inbound_data:
            raise InboundNotFoundException(f"Inbound {inbound_id} not found")

        return self._parse_inbound(inbound_data)

    async def create_inbound(self, inbound: Inbound) -> Inbound:
        """Create new inbound."""
        data = self._serialize_inbound(inbound)

        result = await self._request("POST", "/panel/api/inbounds/add", json=data)

        # Get created inbound
        inbound_id = result.get("obj", {}).get("id")
        if inbound_id:
            return await self.get_inbound(inbound_id)

        return inbound

    async def update_inbound(self, inbound_id: int, inbound: Inbound) -> Inbound:
        """Update existing inbound."""
        data = self._serialize_inbound(inbound)
        data["id"] = inbound_id

        await self._request("POST", f"/panel/api/inbounds/update/{inbound_id}", json=data)

        return await self.get_inbound(inbound_id)

    async def delete_inbound(self, inbound_id: int) -> bool:
        """Delete inbound."""
        await self._request("POST", f"/panel/api/inbounds/del/{inbound_id}")
        return True

    async def add_client(self, inbound_id: int, client: Client) -> Client:
        """Add client to inbound."""
        data = {"id": inbound_id, "settings": json.dumps({"clients": [client.model_dump()]})}

        await self._request("POST", "/panel/api/inbounds/addClient", json=data)

        return client

    async def get_client(self, inbound_id: int, client_id: str) -> Client:
        """Get client from inbound."""
        # Получаем inbound со всеми клиентами
        inbound: Inbound = await self.get_inbound(inbound_id)

        # Ищем клиента по ID в settings.clients
        for client in inbound.settings.clients:
            if client.id == client_id:
                return client

        # Если клиент не найден, выбрасываем исключение
        raise ClientNotFoundException(f"Client {client_id} not found in inbound {inbound_id}")

    async def update_client(self, inbound_id: int, client_id: str, client: Client) -> Client:
        """Update client in inbound."""
        data = {"id": inbound_id, "settings": json.dumps({"clients": [client.model_dump()]})}

        await self._request("POST", f"/panel/api/inbounds/updateClient/{client_id}", json=data)

        return client

    async def delete_client(self, inbound_id: int, client_id: str) -> bool:
        """Delete client from inbound."""
        await self._request("POST", f"/panel/api/inbounds/{inbound_id}/delClient/{client_id}")
        return True

    async def get_traffic_stats(self) -> list[InboundTraffic]:
        """Get traffic statistics for all inbounds."""
        inbounds = await self.get_inbounds()

        return [
            InboundTraffic(
                inbound_id=inbound.id or 0,
                up=inbound.up,
                down=inbound.down,
                total=inbound.total,
            )
            for inbound in inbounds
        ]

    async def get_server_stats(self) -> ServerStats:
        """Get server statistics."""
        result = await self._request("GET", "panel/api/server/status")

        obj = result.get("obj", {})

        return ServerStats(
            cpu_usage=obj.get("cpu", 0.0),
            memory_usage=obj.get("mem", {}).get("current", 0.0),
            disk_usage=obj.get("disk", {}).get("current", 0.0),
            uptime=obj.get("uptime", 0),
            network_up=obj.get("netIO", {}).get("up", 0),
            network_down=obj.get("netIO", {}).get("down", 0),
        )

    def _parse_inbound(self, data: dict[str, Any]) -> Inbound:
        """Parse inbound data from API response."""
        settings_raw = json.loads(data.get("settings", "{}"))
        stream_settings = json.loads(data.get("streamSettings", "{}"))
        sniffing = json.loads(data.get("sniffing", "{}"))

        # Парсим settings в объект Settings
        settings = Settings(**settings_raw) if isinstance(settings_raw, dict) else Settings()

        return Inbound(
            id=data.get("id"),
            up=data.get("up", 0),
            down=data.get("down", 0),
            total=data.get("total", 0),
            remark=data.get("remark", "reality"),
            enable=data.get("enable", True),
            port=data.get("port", 443),
            protocol=data.get("protocol", "vless"),
            settings=settings,
            stream_settings=stream_settings,
            sniffing=sniffing,
        )

    def _serialize_inbound(self, inbound: Inbound) -> dict[str, Any]:
        """Serialize inbound for API request."""
        return {
            "remark": inbound.remark,
            "enable": inbound.enable,
            "port": inbound.port,
            "protocol": inbound.protocol.value,
            "settings": json.dumps(inbound.settings.model_dump()),
            "streamSettings": json.dumps(inbound.stream_settings),
            "sniffing": json.dumps(inbound.sniffing),
        }
