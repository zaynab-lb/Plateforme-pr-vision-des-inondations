import requests

from app.config import Config


def get_static_features(latitude: float, longitude: float) -> dict:
    url = f"{Config.GEOSPATIAL_SERVICE_URL}/features/static"

    params = {
        "latitude": latitude,
        "longitude": longitude
    }

    response = requests.get(url, params=params, timeout=20)
    response.raise_for_status()

    return response.json()