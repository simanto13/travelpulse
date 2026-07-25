from sqlalchemy.orm import Session
from app.models.weather_current import WeatherCurrent

class WeatherRepository:

    def __init__(self,db:Session):
        self.db=db

    def find_by_city(self,city:str):
        return self.db.query(WeatherCurrent).filter(
            WeatherCurrent.city.ilike(city)
        ).order_by(WeatherCurrent.id.desc()).first()

    def save(self,weather:WeatherCurrent):
        self.db.add(weather)
        self.db.commit()
        self.db.refresh(weather)
        return weather
