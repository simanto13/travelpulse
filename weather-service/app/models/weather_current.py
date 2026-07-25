from sqlalchemy import Column,Integer,Float,String,DateTime
from app.database import Base

class WeatherCurrent(Base):
    __tablename__="weather_current"

    id=Column(Integer,primary_key=True,index=True)
    city=Column(String(100),index=True)
    country=Column(String(100))
    temperature_c=Column(Float)
    temperature_f=Column(Float)
    feels_like_c=Column(Float)
    humidity=Column(Integer)
    wind_kph=Column(Float)
    pressure_mb=Column(Float)
    visibility_km=Column(Float)
    uv=Column(Float)
    condition=Column(String(100))
    icon=Column(String(255))
    last_updated=Column(DateTime)
