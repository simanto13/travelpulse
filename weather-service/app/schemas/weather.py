from pydantic import BaseModel
from datetime import datetime

class WeatherResponse(BaseModel):
    city:str
    country:str
    temperature_c:float
    temperature_f:float
    feels_like_c:float
    humidity:int
    wind_kph:float
    pressure_mb:float
    visibility_km:float
    uv:float
    condition:str
    icon:str
    last_updated:datetime
