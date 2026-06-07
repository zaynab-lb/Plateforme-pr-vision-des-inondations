import requests

from app.config import Config


def get_weather_forecast(latitude: float, longitude: float) -> dict:
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": "temperature_2m,precipitation,soil_moisture_0_to_1cm",
        "timezone": "GMT"
    }

    response = requests.get(Config.WEATHER_API_URL, params=params, timeout=20)
    response.raise_for_status()

    return response.json()