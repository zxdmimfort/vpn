"""Domain exceptions."""


class DomainException(Exception):
    """Base domain exception."""

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)


class VPNServerException(DomainException):
    """VPN server related exception."""


class AuthenticationException(DomainException):
    """Authentication failed exception."""


class InboundNotFoundException(DomainException):
    """Inbound not found exception."""


class ClientNotFoundException(DomainException):
    """Client not found exception."""


class InvalidConfigurationException(DomainException):
    """Invalid configuration exception."""
