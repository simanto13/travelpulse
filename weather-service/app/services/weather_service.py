import httpx
from app.core.config import settings
from app.utils.weather_mapper import map_weather
from app.repositories.weather_repository import WeatherRepository

class WeatherService:

    def __init__(self,db):
        self.repo=WeatherRepository(db)

    async def get_current_weather(self,city:str):

        existing=self.repo.find_by_city(city)
        if existing:
            return existing

        async with httpx.AsyncClient() as client:
            response=await client.get(
                "https://api.weatherapi.com/v1/current.json",
                params={
                    "key":settings.WEATHER_API_KEY,
                    "q":city
                }
            )

        response.raise_for_status()

        weather=map_weather(response.json())

        return self.repo.save(weather)
