"""Application entry point."""

import uvicorn

from src.config import settings
from src.presentation.app import create_app


def main() -> None:
    """Run the application."""
    app = create_app()

    uvicorn.run(
        app,
        host=settings.host,
        port=settings.port,
        log_level="debug" if settings.debug else "info",
    )


if __name__ == "__main__":
    main()
