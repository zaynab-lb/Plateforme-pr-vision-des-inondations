from pydantic import BaseModel


class PredictionFromCoordinatesRequest(BaseModel):
    latitude: float
    longitude: float

    tp: float
    ro: float
    sro: float
    swvl1: float
    t2m: float
    dis24: float


class StaticFeaturesResponse(BaseModel):
    latitude: float
    longitude: float

    elevation: float
    slope: float

    clay_0_5cm: float
    sand_0_5cm: float
    silt_0_5cm: float
    bdod_0_5cm: float
    soc_0_5cm: float
    wv0033_0_5cm: float
    wv1500_0_5cm: float

    landcover: float

    riv_length_km: float
    riv_dist_dn_km: float
    riv_dist_up_km: float
    riv_catch_skm: float
    riv_upland_skm: float
    riv_endorheic: float
    riv_dis_av_cms: float
    riv_ord_stra: float
    riv_ord_clas: float
    riv_ord_flow: float

    bas_dist_sink: float
    bas_dist_main: float
    bas_sub_area: float
    bas_up_area: float
    bas_endo: float
    bas_coast: float
    bas_order: float


class PredictionResponse(BaseModel):
    risk_j1: float
    risk_j3: float
    risk_j7: float

    level_j1: str
    level_j3: str
    level_j7: str