from pydantic import BaseModel
class WeatherResponse(BaseModel):
    location:str
    data:dict
