import pytest
from httpx import AsyncClient
from app.main import app


@pytest.mark.asyncio
async def test_health():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.get("/api/v1/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


@pytest.mark.asyncio
async def test_weather_current_route_is_registered(monkeypatch):
    async def fake_get_current_weather(self, city):
        return {"city": city, "temp_c": 20}

    monkeypatch.setattr(
        "app.services.weather_service.WeatherService.get_current_weather",
        fake_get_current_weather,
    )

    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.get("/api/v1/weather/current?city=London")

    assert r.status_code == 200
    assert r.json() == {"city": "London", "temp_c": 20}
