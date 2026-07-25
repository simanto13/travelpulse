from app.models.weather_current import WeatherCurrent

def map_weather(api:dict)->WeatherCurrent:
    loc=api["location"]
    cur=api["current"]

    return WeatherCurrent(
        city=loc["name"],
        country=loc["country"],
        temperature_c=cur["temp_c"],
        temperature_f=cur["temp_f"],
        feels_like_c=cur["feelslike_c"],
        humidity=cur["humidity"],
        wind_kph=cur["wind_kph"],
        pressure_mb=cur["pressure_mb"],
        visibility_km=cur["vis_km"],
        uv=cur["uv"],
        condition=cur["condition"]["text"],
        icon=cur["condition"]["icon"],
        last_updated=cur["last_updated"]
    )
