"""Application configuration using Pydantic settings."""
from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """Global settings for backend."""

    app_name: str = Field("ZerroGate Backend", description="Public app name")
    debug: bool = Field(False, description="Enable debug mode")
    version: str = Field("0.1.0", description="Version of the backend")
    secret_key: str = Field("change-me", description="Secret key for JWT")
    access_token_expire_minutes: int = Field(60, description="Access token lifetime")
    database_url: str = Field(
        "sqlite+aiosqlite:///./zerrogate.db", description="SQLAlchemy database URL"
    )
    admin_email: str = Field("admin@zerrogate.local", description="Default admin email")
    admin_password: str = Field("admin", description="Default admin password")

    class Config:
        env_file = ".env"


settings = Settings()
