from app.repositories.static_feature_repository import find_nearest_static_features


MAX_DISTANCE_KM = 50


def get_static_features(latitude: float, longitude: float) -> dict:
    features = find_nearest_static_features(latitude, longitude)

    if not features:
        raise ValueError("Aucune donnée statique trouvée pour ces coordonnées")

    distance_km = features.get("distance_km")

    if distance_km is not None and distance_km > MAX_DISTANCE_KM:
        raise ValueError(
            f"Les coordonnées sont hors de la zone couverte par les données. "
            f"Point le plus proche à {round(distance_km, 2)} km."
        )

    features.pop("distance_km", None)

    return features