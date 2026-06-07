def determine_hsg(clay: float, sand: float, silt: float) -> str:
    """
    Détermination simplifiée du groupe hydrologique du sol.
    A : infiltration élevée
    B : infiltration moyenne
    C : infiltration faible
    D : infiltration très faible
    """

    total = clay + sand + silt

    if total <= 0:
        return "C"

    clay_pct = (clay / total) * 100
    sand_pct = (sand / total) * 100

    if sand_pct >= 70 and clay_pct < 15:
        return "A"
    elif sand_pct >= 50 and clay_pct < 25:
        return "B"
    elif clay_pct < 40:
        return "C"
    else:
        return "D"


def get_base_cn(landcover: float, hsg: str) -> float:
    """
    CN simplifié selon landcover + groupe hydrologique.
    """

    landcover = int(landcover)

    cn_table = {
        # ESA WorldCover approximatif
        # 10 Tree cover
        10: {"A": 30, "B": 55, "C": 70, "D": 77},

        # 20 Shrubland
        20: {"A": 39, "B": 61, "C": 74, "D": 80},

        # 30 Grassland
        30: {"A": 49, "B": 69, "C": 79, "D": 84},

        # 40 Cropland
        40: {"A": 67, "B": 78, "C": 85, "D": 89},

        # 50 Built-up
        50: {"A": 77, "B": 85, "C": 90, "D": 92},

        # 60 Bare / sparse vegetation
        60: {"A": 68, "B": 79, "C": 86, "D": 89},

        # 80 Permanent water bodies
        80: {"A": 100, "B": 100, "C": 100, "D": 100},

        # 90 Herbaceous wetland
        90: {"A": 78, "B": 85, "C": 89, "D": 91},

        # 95 Mangroves
        95: {"A": 70, "B": 80, "C": 87, "D": 90},

        # 100 Moss and lichen
        100: {"A": 60, "B": 74, "C": 82, "D": 86},

        # 200 Bare areas / desert
        200: {"A": 68, "B": 79, "C": 86, "D": 89},

        # 210 Water
        210: {"A": 100, "B": 100, "C": 100, "D": 100},
    }

    default_cn = {"A": 60, "B": 75, "C": 85, "D": 90}

    return cn_table.get(landcover, default_cn).get(hsg, 85)


def adjust_cn_by_soil_moisture(cn: float, swvl1: float) -> float:
    """
    Ajustement simplifié du CN selon l'humidité du sol.
    """

    if swvl1 < 0.10:
        return max(30, cn - 10)
    elif swvl1 > 0.30:
        return min(100, cn + 10)
    else:
        return cn


def adjust_cn_by_slope(cn: float, slope: float) -> float:
    """
    Ajustement léger selon la pente.
    """

    if slope > 15:
        return min(100, cn + 5)
    elif slope > 8:
        return min(100, cn + 3)
    elif slope > 2:
        return min(100, cn + 1)
    else:
        return cn


def calculate_scs_runoff(
    tp: float,
    clay: float,
    sand: float,
    silt: float,
    landcover: float,
    swvl1: float,
    slope: float
) -> dict:
    """
    Calcule ro et sro avec une approximation SCS-CN.
    tp est en mm.
    """

    hsg = determine_hsg(clay, sand, silt)

    cn = get_base_cn(landcover, hsg)
    cn = adjust_cn_by_soil_moisture(cn, swvl1)
    cn = adjust_cn_by_slope(cn, slope)

    cn = max(1, min(cn, 100))

    s = (25400 / cn) - 254
    ia = 0.2 * s

    if tp <= ia:
        q = 0.0
    else:
        q = ((tp - ia) ** 2) / (tp - ia + s)

    return {
        "ro": round(q, 6),
        "sro": round(q, 6),
        "cn": round(cn, 2),
        "hsg": hsg
    }