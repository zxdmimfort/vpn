"""Persistence layer for VPN service."""

from src.infrastructure.persistence.database import Database
from src.infrastructure.persistence.models import Base, ClientMetadata
from src.infrastructure.persistence.repository import ClientMetadataRepository

__all__ = [
    "Database",
    "Base",
    "ClientMetadata",
    "ClientMetadataRepository",
]
