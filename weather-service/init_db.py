# weather-service/init_db.py
from app.database import engine, Base
from app.models.weather_current import WeatherCurrent

def init_db():
    """Create all tables in the database."""
    Base.metadata.create_all(bind=engine)
    print("✓ Database tables created successfully")

if __name__ == "__main__":
    init_db()