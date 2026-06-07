import requests

from app.config import Config


def predict_flood_risk(features: dict) -> dict:
    response = requests.post(
        Config.ML_SERVICE_URL,
        json=features,
        timeout=30
    )

    response.raise_for_status()

    return response.json()