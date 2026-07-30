from fastapi import FastAPI
from app.api.weather_chat import router as weather_router

app=FastAPI(title="TravelPulse Weather Agent")
app.include_router(weather_router)

@app.get("/")
async def root():
    return {"service":"TravelPulse Weather Agent","status":"ok"}
