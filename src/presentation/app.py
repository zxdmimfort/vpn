"""FastAPI application factory."""

import logging
import traceback
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.security import APIKeyHeader

from src.config import settings
from src.infrastructure.di import ApplicationProvider, InfrastructureProvider
from src.presentation.api import clients, inbounds, stats
from src.presentation.middleware import api_key_middleware

# Настройка логирования
logging.basicConfig(
    level=logging.DEBUG if settings.debug else logging.INFO,
    format="%(asctime)s - %(filename)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Определяем схему безопасности для API ключа
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Application lifespan manager."""
    yield
    # Cleanup will be handled by dishka


def create_app() -> FastAPI:
    """Create FastAPI application."""
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        debug=settings.debug,
        lifespan=lifespan,
        swagger_ui_parameters={"persistAuthorization": True},
    )

    # Добавляем схему безопасности в OpenAPI
    if settings.api_key:
        app.openapi_schema = None  # Сбросим кеш схемы

        # Переопределяем схему OpenAPI для добавления security
        def custom_openapi():
            if app.openapi_schema:
                return app.openapi_schema

            from fastapi.openapi.utils import get_openapi

            openapi_schema = get_openapi(
                title=app.title,
                version=app.version,
                routes=app.routes,
            )

            # Добавляем схему безопасности
            openapi_schema["components"]["securitySchemes"] = {
                "APIKeyHeader": {
                    "type": "apiKey",
                    "in": "header",
                    "name": "X-API-Key",
                }
            }

            # Применяем security ко всем операциям
            for path in openapi_schema["paths"].values():
                for operation in path.values():
                    if isinstance(operation, dict) and "tags" in operation:
                        operation["security"] = [{"APIKeyHeader": []}]

            app.openapi_schema = openapi_schema
            return app.openapi_schema

        app.openapi = custom_openapi

    # Setup dependency injection
    container = make_async_container(
        InfrastructureProvider(),
        ApplicationProvider(),
    )
    setup_dishka(container, app)

    # Add middleware
    app.middleware("http")(api_key_middleware)

    # Include routers
    app.include_router(inbounds.router, prefix="/api/v1")
    app.include_router(clients.router, prefix="/api/v1")
    app.include_router(stats.router, prefix="/api/v1")

    @app.get("/health")
    async def health() -> dict[str, str]:
        """Health check endpoint."""
        return {"status": "ok"}

    # Добавляем обработчик исключений для логирования
    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        """Global exception handler with traceback logging."""
        logger.error(
            f"Unhandled exception on {request.method} {request.url.path}",
            exc_info=True,  # Это добавит полный traceback в логи
        )

        # В режиме отладки возвращаем traceback в ответе
        detail = str(exc)
        if settings.debug:
            detail = {
                "error": str(exc),
                "traceback": traceback.format_exc(),
            }

        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": detail},
        )

    return app
