import json
import joblib

from app.config import Config

def load_model(model_path: str):
    return joblib.load(model_path)


def load_features(features_path: str):
    with open(features_path, "r", encoding="utf-8") as file:
        return json.load(file)

model_j1 = load_model(Config.MODEL_J1_PATH)
model_j3 = load_model(Config.MODEL_J3_PATH)
model_j7 = load_model(Config.MODEL_J7_PATH)

features_j1 = load_features(Config.FEATURES_J1_PATH)
features_j3 = load_features(Config.FEATURES_J3_PATH)
features_j7 = load_features(Config.FEATURES_J7_PATH)