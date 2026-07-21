import asyncio
from datetime import datetime
from typing import Optional

# Placeholder client for external weather API calls.
# Replace this with actual HTTP client (aiohttp / httpx) and API key handling.


async def fetch_current_weather_city(city: str) -> Optional[dict]:
    # Fake implementation for demo; in production call external API.
    await asyncio.sleep(0.05)
    fake_db = {
        "london": {"temperature_c": 15.0, "description": "cloudy"},
        "paris": {"temperature_c": 18.5, "description": "sunny"},
        "new york": {"temperature_c": 22.1, "description": "partly cloudy"},
    }
    lower = city.lower()
    if lower not in fake_db:
        return None
    entry = fake_db[lower]
    return {
        "city": city,
        "temperature_c": entry["temperature_c"],
        "description": entry["description"],
        "observed_at": datetime.utcnow().isoformat(),
    }
