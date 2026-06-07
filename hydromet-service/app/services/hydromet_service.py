from app.clients.weather_client import get_weather_forecast
from app.clients.flood_client import get_river_discharge
from app.clients.geospatial_client import get_static_features
from app.services.scs_cn_service import calculate_scs_runoff
from app.clients.ml_client import predict_flood_risk

def get_dynamic_features(latitude: float, longitude: float) -> dict:
    weather_data = get_weather_forecast(latitude, longitude)
    hourly = weather_data["hourly"]

    dis24 = get_river_discharge(latitude, longitude)

    return {
        "latitude": latitude,
        "longitude": longitude,
        "tp": hourly["precipitation"][0],
        "t2m": hourly["temperature_2m"][0],
        "swvl1": hourly["soil_moisture_0_to_1cm"][0],
        "dis24": dis24
    }


def get_all_features(latitude: float, longitude: float) -> dict:
    dynamic_features = get_dynamic_features(latitude, longitude)
    static_features = get_static_features(latitude, longitude)

    runoff_features = calculate_scs_runoff(
        tp=dynamic_features["tp"],
        clay=static_features["clay_0_5cm"],
        sand=static_features["sand_0_5cm"],
        silt=static_features["silt_0_5cm"],
        landcover=static_features["landcover"],
        swvl1=dynamic_features["swvl1"],
        slope=static_features["slope"]
    )

    return {
        **dynamic_features,
        **runoff_features,
        **static_features
    }

def predict_risk_from_coordinates(latitude: float, longitude: float) -> dict:
    features = get_all_features(latitude, longitude)

    ml_features = {
        "latitude": features["latitude"],
        "longitude": features["longitude"],
        "tp": features["tp"],
        "ro": features["ro"],
        "sro": features["sro"],
        "swvl1": features["swvl1"],
        "t2m": features["t2m"],
        "dis24": features["dis24"],

        "elevation": features["elevation"],
        "slope": features["slope"],

        "clay_0_5cm": features["clay_0_5cm"],
        "sand_0_5cm": features["sand_0_5cm"],
        "silt_0_5cm": features["silt_0_5cm"],
        "bdod_0_5cm": features["bdod_0_5cm"],
        "soc_0_5cm": features["soc_0_5cm"],
        "wv0033_0_5cm": features["wv0033_0_5cm"],
        "wv1500_0_5cm": features["wv1500_0_5cm"],

        "landcover": features["landcover"],

        "riv_LENGTH_KM": features["riv_length_km"],
        "riv_DIST_DN_KM": features["riv_dist_dn_km"],
        "riv_DIST_UP_KM": features["riv_dist_up_km"],
        "riv_CATCH_SKM": features["riv_catch_skm"],
        "riv_UPLAND_SKM": features["riv_upland_skm"],
        "riv_DIS_AV_CMS": features["riv_dis_av_cms"],
        "riv_ENDORHEIC": features["riv_endorheic"],
        "riv_ORD_STRA": features["riv_ord_stra"],
        "riv_ORD_CLAS": features["riv_ord_clas"],
        "riv_ORD_FLOW": features["riv_ord_flow"],

        "bas_DIST_SINK": features["bas_dist_sink"],
        "bas_DIST_MAIN": features["bas_dist_main"],
        "bas_SUB_AREA": features["bas_sub_area"],
        "bas_UP_AREA": features["bas_up_area"],
        "bas_ENDO": features["bas_endo"],
        "bas_COAST": features["bas_coast"],
        "bas_ORDER": features["bas_order"],
    }

    prediction = predict_flood_risk(ml_features)

    return {
        "latitude": latitude,
        "longitude": longitude,
        **prediction
    }