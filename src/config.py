"""Application configuration."""

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # Application settings
    app_name: str = "VPN Management Service"
    app_version: str = "0.1.0"
    debug: bool = False

    # Server settings
    host: str = "0.0.0.0"
    port: int = 8000

    # 3x-ui API settings
    x_ui_base_url: str = Field(..., description="3x-ui panel base URL")
    x_ui_username: str = Field(..., description="3x-ui admin username")
    x_ui_password: str = Field(..., description="3x-ui admin password")
    x_ui_timeout: int = Field(default=30, description="Request timeout in seconds")
    x_ui_verify_ssl: bool = Field(
        default=True, description="Verify SSL certificate for 3x-ui panel"
    )

    # Database settings
    database_url: str = Field(
        default="sqlite+aiosqlite:///./vpn.db", description="Database connection URL"
    )
    database_echo: bool = Field(
        default=False, description="Echo SQL statements to stdout (for debugging)"
    )

    # Security
    api_key: str | None = Field(default=None, description="API key for authentication")


settings = Settings()
