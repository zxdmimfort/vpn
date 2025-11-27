"""FastAPI middleware."""

from typing import Callable

from fastapi import Request, Response, status
from fastapi.responses import JSONResponse

from src.config import settings

# Публичные пути, которые не требуют API ключа
PUBLIC_PATHS = {
    "/docs",
    "/redoc",
    "/openapi.json",
    "/health",
}


async def api_key_middleware(request: Request, call_next: Callable) -> Response:
    """Validate API key if configured."""
    # Пропускаем публичные пути
    if request.url.path in PUBLIC_PATHS:
        response = await call_next(request)
        return response

    if settings.api_key:
        api_key = request.headers.get("X-API-Key")

        if api_key != settings.api_key:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Invalid or missing API key"},
            )

    response = await call_next(request)
    return response
