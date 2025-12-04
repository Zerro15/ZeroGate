"""Application configuration using Pydantic settings."""
import os
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    # Project info
    PROJECT_NAME: str = "ZeroGate"
    VERSION: str = "0.1.0"
    API_V1_PREFIX: str = "/api"

    # JWT
    JWT_SECRET_KEY: str = Field("changeme-secret", env="JWT_SECRET_KEY")
    JWT_ALGORITHM: str = Field("HS256", env="JWT_ALGORITHM")
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(60 * 24, env="JWT_ACCESS_TOKEN_EXPIRE_MINUTES")

    # Database
    DATABASE_URL: str = Field("sqlite+aiosqlite:///./zerrogate.db", env="DATABASE_URL")

    # Seed admin
    FIRST_ADMIN_EMAIL: str = Field("admin@local", env="FIRST_ADMIN_EMAIL")
    FIRST_ADMIN_PASSWORD: str = Field("admin123", env="FIRST_ADMIN_PASSWORD")
    SEED_ADMIN_ON_STARTUP: bool = Field(True, env="SEED_ADMIN_ON_STARTUP")

    # Debug
    debug: bool = Field(False, env="DEBUG")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()

# Normalize sqlite DATABASE_URL to absolute path
try:
    db_url = settings.DATABASE_URL
    prefix = "sqlite+aiosqlite:///"
    if isinstance(db_url, str) and db_url.startswith(prefix):
        db_path = db_url[len(prefix) :]
        if db_path and not Path(db_path).is_absolute():
            abs_path = Path(os.getcwd()) / db_path
            settings.DATABASE_URL = f"{prefix}{abs_path.as_posix()}"
except Exception:
    pass
