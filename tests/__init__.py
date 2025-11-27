"""Tests for domain entities."""

from src.domain.entities import Client, Inbound, InboundProtocol


def test_client_creation() -> None:
    """Test client entity creation."""
    client = Client(
        id="test-id",
        email="test@example.com",
        enable=True,
        total_gb=10737418240,
    )

    assert client.id == "test-id"
    assert client.email == "test@example.com"
    assert client.enable is True
    assert client.total_gb == 10737418240


def test_inbound_creation() -> None:
    """Test inbound entity creation."""
    inbound = Inbound(
        remark="Test Server",
        port=443,
        protocol=InboundProtocol.VLESS,
    )

    assert inbound.remark == "Test Server"
    assert inbound.port == 443
    assert inbound.protocol == InboundProtocol.VLESS
    assert inbound.enable is True
    assert inbound.clients == []
