from app.clients.ml_client import call_ml_service
from app.services.static_feature_service import get_static_features
from app.schemas.prediction_schema import PredictionFromCoordinatesRequest


def predict_from_coordinates(request: PredictionFromCoordinatesRequest) -> dict:
    static_data = get_static_features(
        latitude=request.latitude,
        longitude=request.longitude
    )

    payload = {
        "latitude": static_data["latitude"],
        "longitude": static_data["longitude"],

        "tp": request.tp,
        "ro": request.ro,
        "sro": request.sro,
        "swvl1": request.swvl1,
        "t2m": request.t2m,
        "dis24": request.dis24,

        "elevation": static_data["elevation"],
        "slope": static_data["slope"],

        "clay_0_5cm": static_data["clay_0_5cm"],
        "sand_0_5cm": static_data["sand_0_5cm"],
        "silt_0_5cm": static_data["silt_0_5cm"],
        "bdod_0_5cm": static_data["bdod_0_5cm"],
        "soc_0_5cm": static_data["soc_0_5cm"],
        "wv0033_0_5cm": static_data["wv0033_0_5cm"],
        "wv1500_0_5cm": static_data["wv1500_0_5cm"],

        "landcover": static_data["landcover"],

        "riv_LENGTH_KM": static_data["riv_length_km"],
        "riv_DIST_DN_KM": static_data["riv_dist_dn_km"],
        "riv_DIST_UP_KM": static_data["riv_dist_up_km"],
        "riv_CATCH_SKM": static_data["riv_catch_skm"],
        "riv_UPLAND_SKM": static_data["riv_upland_skm"],
        "riv_DIS_AV_CMS": static_data["riv_dis_av_cms"],
        "riv_ENDORHEIC": static_data["riv_endorheic"],
        "riv_ORD_STRA": static_data["riv_ord_stra"],
        "riv_ORD_CLAS": static_data["riv_ord_clas"],
        "riv_ORD_FLOW": static_data["riv_ord_flow"],

        "bas_DIST_SINK": static_data["bas_dist_sink"],
        "bas_DIST_MAIN": static_data["bas_dist_main"],
        "bas_SUB_AREA": static_data["bas_sub_area"],
        "bas_UP_AREA": static_data["bas_up_area"],
        "bas_ENDO": static_data["bas_endo"],
        "bas_COAST": static_data["bas_coast"],
        "bas_ORDER": static_data["bas_order"],
    }

    return call_ml_service(payload)