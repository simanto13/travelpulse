from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "TravelPulse Weather Service"
    DATABASE_URL: str = "postgresql+psycopg://postgres:password@localhost:5432/travelpulse"
    WEATHER_API_KEY: str = ""

    class Config:
        env_file = ".env"

settings = Settings()
