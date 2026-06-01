import pandas as pd

from app.model_loader import (
    model_j1,
    model_j3,
    model_j7,
    features_j1,
    features_j3,
    features_j7
)


def get_risk_level(probability: float) -> str:
    if probability < 0.40:
        return "Faible"
    elif probability < 0.70:
        return "Moyen"
    else:
        return "Élevé"


def prepare_input(data: dict, features: list) -> pd.DataFrame:
    row = {}

    for feature in features:
        row[feature] = data[feature]

    return pd.DataFrame([row], columns=features)


def predict_flood_risk(data: dict):
    input_j1 = prepare_input(data, features_j1)
    input_j3 = prepare_input(data, features_j3)
    input_j7 = prepare_input(data, features_j7)

    risk_j1 = float(model_j1.predict_proba(input_j1)[0][1])
    risk_j3 = float(model_j3.predict_proba(input_j3)[0][1])
    risk_j7 = float(model_j7.predict_proba(input_j7)[0][1])

    return {
        "risk_j1": round(risk_j1, 4),
        "risk_j3": round(risk_j3, 4),
        "risk_j7": round(risk_j7, 4),
        "level_j1": get_risk_level(risk_j1),
        "level_j3": get_risk_level(risk_j3),
        "level_j7": get_risk_level(risk_j7)
    }