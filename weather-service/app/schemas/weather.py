from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class WeatherQuery(BaseModel):
    city: str


class CurrentWeatherResponse(BaseModel):
    city: str
    temperature_c: float = Field(..., description="Temperature in Celsius")
    description: Optional[str] = None
    observed_at: datetime


class WeatherReport(BaseModel):
    city: str
    temperature_c: float
    description: Optional[str] = None
    reported_by: Optional[str] = None
    reported_at: Optional[datetime]
