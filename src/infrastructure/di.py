"""Dependency injection container using dishka."""

from collections.abc import AsyncIterator

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.services import VPNManagementService
from src.config import Settings, settings
from src.domain.ports import VPNServerPort
from src.infrastructure.persistence import ClientMetadataRepository, Database
from src.infrastructure.x_ui_adapter import XUIAdapter


class InfrastructureProvider(Provider):
    """Provider for infrastructure dependencies."""

    @provide(scope=Scope.APP)
    def provide_settings(self) -> Settings:
        """Provide application settings."""
        return settings

    @provide(scope=Scope.APP)
    async def provide_database(self, settings: Settings) -> AsyncIterator[Database]:
        """Provide database instance."""
        db = Database(
            database_url=settings.database_url,
            echo=settings.database_echo,
        )
        # Create tables on startup
        await db.create_tables()
        yield db
        await db.close()

    @provide(scope=Scope.REQUEST)
    async def provide_db_session(self, database: Database) -> AsyncIterator[AsyncSession]:
        """Provide database session for each request."""
        async with database.session() as session:
            yield session

    @provide(scope=Scope.REQUEST)
    def provide_client_metadata_repository(self, session: AsyncSession) -> ClientMetadataRepository:
        """Provide client metadata repository."""
        return ClientMetadataRepository(session)

    @provide(scope=Scope.APP)
    async def provide_vpn_server(self, settings: Settings) -> AsyncIterator[VPNServerPort]:
        """Provide VPN server adapter."""
        adapter = XUIAdapter(
            base_url=settings.x_ui_base_url,
            username=settings.x_ui_username,
            password=settings.x_ui_password,
            timeout=settings.x_ui_timeout,
            verify_ssl=settings.x_ui_verify_ssl,
        )
        yield adapter
        await adapter.close()


class ApplicationProvider(Provider):
    """Provider for application services."""

    @provide(scope=Scope.REQUEST)
    def provide_vpn_management_service(self, vpn_server: VPNServerPort) -> VPNManagementService:
        """Provide VPN management service."""
        return VPNManagementService(vpn_server)
