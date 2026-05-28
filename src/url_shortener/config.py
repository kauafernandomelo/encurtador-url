from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Encurtador de URL"
    base_url: str = Field(default="http://localhost:8000")
    database_url: str = Field(default="sqlite:///./url_shortener.db")
    short_code_size: int = Field(default=7, ge=4, le=16)

    model_config = SettingsConfigDict(env_file=".env", env_prefix="APP_")


@lru_cache
def get_settings() -> Settings:
    return Settings()
