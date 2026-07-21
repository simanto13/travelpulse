from typing import Optional
from datetime import datetime
from app.clients.weather_client import fetch_current_weather_city
from app.schemas.weather import CurrentWeatherResponse
from app.core.config import settings


class WeatherService:
    def __init__(self, settings=None):
        self.settings = settings or settings

    async def get_current(self, city: str) -> Optional[CurrentWeatherResponse]:
        raw = await fetch_current_weather_city(city)
        if raw is None:
            return None
        # Normalize into schema
        return CurrentWeatherResponse(
            city=raw["city"],
            temperature_c=raw["temperature_c"],
            description=raw.get("description"),
            observed_at=datetime.fromisoformat(raw["observed_at"]),
        )
