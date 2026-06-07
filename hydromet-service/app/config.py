import os


class Config:
    APP_NAME = os.getenv("APP_NAME", "HYDROMET-SERVICE")
    APP_PORT = int(os.getenv("APP_PORT", "8083"))
    APP_VERSION = os.getenv("APP_VERSION", "1.0.0")

    EUREKA_SERVER = os.getenv("EUREKA_SERVER", "http://localhost:8761/eureka/")


    WEATHER_API_URL = os.getenv(
        "WEATHER_API_URL",
        "https://api.open-meteo.com/v1/forecast"
    )

    FLOOD_API_URL = os.getenv(
        "FLOOD_API_URL",
        "https://flood-api.open-meteo.com/v1/flood"
    )

    GEOSPATIAL_SERVICE_URL = os.getenv(
        "GEOSPATIAL_SERVICE_URL",
        "http://localhost:8080/geospatial-service"
    )

    ML_SERVICE_URL = os.getenv(
        "ML_SERVICE_URL",
        "http://localhost:8080/ml-service/predict"
    )