from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.weather_service import WeatherService

router=APIRouter()

@router.get("/current")
async def current_weather(city:str,db:Session=Depends(get_db)):
    service=WeatherService(db)
    return await service.get_current_weather(city)
