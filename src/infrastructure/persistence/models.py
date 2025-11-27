"""SQLAlchemy models for persistence layer."""

from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Base class for all models."""

    pass


class ClientMetadata(Base):
    """Client metadata model.

    Stores additional metadata about VPN clients that is not stored in 3x-ui.
    This includes billing information and other application-specific data.
    """

    __tablename__ = "client_metadata"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    client_id: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    owner_ref: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    def __repr__(self) -> str:
        return f"<ClientMetadata(client_id={self.client_id}, owner_ref={self.owner_ref})>"
