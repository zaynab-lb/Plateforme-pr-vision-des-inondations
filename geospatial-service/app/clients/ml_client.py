import requests
from app.config import Config


def call_ml_service(payload: dict) -> dict:
    response = requests.post(
        Config.ML_SERVICE_URL,
        json=payload,
        timeout=30
    )

    response.raise_for_status()
    return response.json()