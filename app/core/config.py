from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Centralized application configuration.
    Values are loaded from environment variables / .env file.
    """

    # App metadata
    app_name: str = "MedQuery AI"
    app_version: str = "1.0.0"
    app_description: str = (
        "Enterprise Clinical Knowledge Assistant powered by "
        "Retrieval-Augmented Generation (RAG)"
    )

    # Environment
    environment: str = "development"  # development | staging | production
    debug: bool = True

    # API
    api_v1_prefix: str = "/api/v1"

    # Logging
    log_level: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


@lru_cache
def get_settings() -> Settings:
    """
    Returns a cached Settings instance so the .env file
    is only read once per process, not on every request.
    """
    return Settings()