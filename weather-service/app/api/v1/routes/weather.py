from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional

from app.schemas.weather import CurrentWeatherResponse, WeatherReport, WeatherQuery
from app.services.weather_service import WeatherService
from app.api.v1.dependencies import get_settings

router = APIRouter()


@router.get("/current", response_model=CurrentWeatherResponse)
async def get_current_weather(city: str = Query(..., description="City name"), settings=Depends(get_settings)):
    svc = WeatherService(settings=settings)
    data = await svc.get_current(city)
    if data is None:
        raise HTTPException(status_code=404, detail="City not found")
    return data


@router.post("/report", response_model=WeatherReport, status_code=201)
async def report_weather(payload: WeatherReport):
    # For now, just echo back. In real app, persist and emit events.
    return payload
