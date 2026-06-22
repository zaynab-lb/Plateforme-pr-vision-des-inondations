from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, HTTPException

from app.config import Config
from app.eureka_client import register_with_eureka
from app.services.static_feature_service import get_static_features
from app.services.prediction_orchestrator import predict_from_coordinates
from app.schemas.prediction_schema import (
    PredictionFromCoordinatesRequest,
    PredictionResponse,
    StaticFeaturesResponse
)

from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI(
    title=Config.APP_NAME,
    description="Service géospatial pour récupérer les variables statiques et orchestrer la prédiction",
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
        "version": Config.APP_VERSION,
        "status": "OK"
    }


@app.get("/health")
def health_check():
    return {
        "status": "UP",
        "service": Config.APP_NAME,
        "version": Config.APP_VERSION
    }


@app.get("/features/static", response_model=StaticFeaturesResponse)
def static_features(latitude: float, longitude: float):
    try:
        return get_static_features(latitude, longitude)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/predict/from-coordinates", response_model=PredictionResponse)
def predict(request: PredictionFromCoordinatesRequest):
    try:
        return predict_from_coordinates(request)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))