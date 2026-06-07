import requests

from app.config import Config


def get_river_discharge(latitude: float, longitude: float):

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "daily": "river_discharge",
        "timezone": "GMT"
    }

    response = requests.get(
        Config.FLOOD_API_URL,
        params=params,
        timeout=20
    )

    response.raise_for_status()

    data = response.json()

    return data["daily"]["river_discharge"][0]