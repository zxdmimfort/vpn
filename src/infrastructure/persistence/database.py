"""Database configuration and session management."""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.infrastructure.persistence.models import Base


class Database:
    """Database manager for SQLAlchemy async engine."""

    def __init__(self, database_url: str, echo: bool = False) -> None:
        """Initialize database with connection URL.

        Args:
            database_url: SQLAlchemy database URL (e.g., 'sqlite+aiosqlite:///./vpn.db')
            echo: Whether to echo SQL statements to stdout
        """
        self.engine: AsyncEngine = create_async_engine(
            database_url,
            echo=echo,
            future=True,
        )
        self.session_factory: async_sessionmaker[AsyncSession] = async_sessionmaker(
            self.engine,
            class_=AsyncSession,
            expire_on_commit=False,
            autoflush=False,
            autocommit=False,
        )

    async def create_tables(self) -> None:
        """Create all tables defined in models."""
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def drop_tables(self) -> None:
        """Drop all tables (use with caution!)."""
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

    @asynccontextmanager
    async def session(self) -> AsyncGenerator[AsyncSession, None]:
        """Get async database session.

        Usage:
            async with db.session() as session:
                result = await session.execute(...)
        """
        async with self.session_factory() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise

    async def close(self) -> None:
        """Close database engine."""
        await self.engine.dispose()
