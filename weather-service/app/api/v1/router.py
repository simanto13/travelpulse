from fastapi import APIRouter

from .routes import health, weather

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(weather.router, prefix="/weather", tags=["weather"])
