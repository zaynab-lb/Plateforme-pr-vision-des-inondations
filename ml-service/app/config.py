import os


class Config:

    # Application
    APP_NAME = os.getenv(
        "APP_NAME",
        "ML-SERVICE"
    )

    APP_PORT = int(
        os.getenv(
            "APP_PORT",
            "8081"
        )
    )

    APP_VERSION = os.getenv(
        "APP_VERSION",
        "1.0.0"
    )

    # Logging
    LOG_LEVEL = os.getenv(
        "LOG_LEVEL",
        "INFO"
    )

    # Eureka
    EUREKA_SERVER = os.getenv(
        "EUREKA_SERVER",
        "http://discovery-service:8761/eureka"
    )

    # Models
    MODEL_J1_PATH = os.getenv(
        "MODEL_J1_PATH",
        "models/j1.joblib"
    )

    MODEL_J3_PATH = os.getenv(
        "MODEL_J3_PATH",
        "models/j3.joblib"
    )

    MODEL_J7_PATH = os.getenv(
        "MODEL_J7_PATH",
        "models/j7.joblib"
    )

    # Features
    FEATURES_J1_PATH = os.getenv(
        "FEATURES_J1_PATH",
        "models/features_j1.json"
    )

    FEATURES_J3_PATH = os.getenv(
        "FEATURES_J3_PATH",
        "models/features_j3.json"
    )

    FEATURES_J7_PATH = os.getenv(
        "FEATURES_J7_PATH",
        "models/features_j7.json"
    )