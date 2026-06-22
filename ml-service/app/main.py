from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI

from app.config import Config
from app.schemas import PredictionRequest, PredictionResponse
from app.prediction import predict_flood_risk
from app.eureka_client import register_with_eureka
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI(
    title=Config.APP_NAME,
    description="Microservice IA pour la prédiction du risque d'inondation J+1, J+3 et J+7",
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

@app.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest):
    data = request.model_dump()
    result = predict_flood_risk(data)
    return result