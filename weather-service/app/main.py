from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings

app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def health():
    return {
        "service": settings.APP_NAME,
        "status": "UP"
    }

# Example:
# from app.api.weather import router as weather_router
# app.include_router(weather_router, prefix="/weather", tags=["Weather"])
