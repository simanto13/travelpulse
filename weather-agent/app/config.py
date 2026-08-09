from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):

    openai_api_key: str
    openai_model: str = "gpt-5"

    mcp_server_path: str

    database_url: str | None = None

    weather_service_url: str = "http://127.0.0.1:8001"

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


settings = Settings()