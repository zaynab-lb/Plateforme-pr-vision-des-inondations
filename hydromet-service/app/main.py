from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from app.config import Config
from app.eureka_client import register_with_eureka

from app.services.hydromet_service import (
    get_dynamic_features,
    get_all_features,
    predict_risk_from_coordinates
)

from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI(
    title=Config.APP_NAME,
    version=Config.APP_VERSION
)

Instrumentator().instrument(app).expose(app)

@app.on_event("startup")
async def startup_event():
    await register_with_eureka()

@app.get("/")
def home():
    return {
        "message": f"{Config.APP_NAME} is running",
        "service": Config.APP_NAME,
        "version": Config.APP_VERSION
    }


@app.get("/health")
def health():
    return {
        "status": "UP",
        "service": Config.APP_NAME,
        "version": Config.APP_VERSION
    }

@app.get("/dynamic-features")
def dynamic_features(latitude: float, longitude: float):
    return get_dynamic_features(latitude, longitude)

@app.get("/all-features")
def all_features(latitude: float, longitude: float):
    return get_all_features(latitude, longitude)

@app.get("/predict-risk")
def predict_risk(latitude: float, longitude: float):
    return predict_risk_from_coordinates(latitude, longitude)