import os


class Config:
    APP_NAME = os.getenv("APP_NAME", "GEOSPATIAL-SERVICE")
    APP_PORT = int(os.getenv("APP_PORT", "8082"))
    APP_VERSION = os.getenv("APP_VERSION", "1.0.0")

    EUREKA_SERVER = os.getenv("EUREKA_SERVER", "http://localhost:8761/eureka/")

    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = int(os.getenv("DB_PORT", "5432"))
    DB_NAME = os.getenv("DB_NAME", "flood_db")
    DB_USER = os.getenv("DB_USER", "flood_user")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "flood_password")

    INSTANCE_HOST = os.getenv("INSTANCE_HOST", "localhost")

    ML_SERVICE_URL = os.getenv(
        "ML_SERVICE_URL",
        "http://localhost:8080/ml-service/predict"
    )