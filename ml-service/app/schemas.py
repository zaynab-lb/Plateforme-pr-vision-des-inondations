from pydantic import BaseModel


class PredictionRequest(BaseModel):
    latitude: float
    longitude: float

    tp: float
    ro: float
    sro: float
    swvl1: float
    t2m: float
    dis24: float

    elevation: float
    slope: float

    clay_0_5cm: float
    sand_0_5cm: float
    silt_0_5cm: float
    bdod_0_5cm: float
    soc_0_5cm: float
    wv0033_0_5cm: float
    wv1500_0_5cm: float

    landcover: int

    riv_LENGTH_KM: float
    riv_DIST_DN_KM: float
    riv_DIST_UP_KM: float
    riv_CATCH_SKM: float
    riv_UPLAND_SKM: float
    riv_DIS_AV_CMS: float
    riv_ENDORHEIC: int
    riv_ORD_STRA: int
    riv_ORD_CLAS: int
    riv_ORD_FLOW: int

    bas_DIST_SINK: float
    bas_DIST_MAIN: float
    bas_SUB_AREA: float
    bas_UP_AREA: float
    bas_ENDO: int
    bas_COAST: int
    bas_ORDER: int


class PredictionResponse(BaseModel):
    risk_j1: float
    risk_j3: float
    risk_j7: float
    level_j1: str
    level_j3: str
    level_j7: str