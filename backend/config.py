from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    OPENROUTER_API_KEY: str
    OPENROUTER_DEFAULT_MODEL: str = "anthropic/claude-3.5-sonnet"
    KALSHI_API_KEY_ID: Optional[str] = None
    KALSHI_PRIVATE_KEY: Optional[str] = None

    # Database configuration
    DATABASE_URL: str = "sqlite:///./kalshi_council.db"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()
