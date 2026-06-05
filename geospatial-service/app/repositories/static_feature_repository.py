from app.database import get_connection


def find_nearest_static_features(latitude: float, longitude: float) -> dict:
    query = """
    SELECT
        latitude,
        longitude,
        elevation,
        slope,
        clay_0_5cm,
        sand_0_5cm,
        silt_0_5cm,
        bdod_0_5cm,
        soc_0_5cm,
        wv0033_0_5cm,
        wv1500_0_5cm,
        landcover,
        riv_length_km,
        riv_dist_dn_km,
        riv_dist_up_km,
        riv_catch_skm,
        riv_upland_skm,
        riv_endorheic,
        riv_dis_av_cms,
        riv_ord_stra,
        riv_ord_clas,
        riv_ord_flow,
        bas_dist_sink,
        bas_dist_main,
        bas_sub_area,
        bas_up_area,
        bas_endo,
        bas_coast,
        bas_order,
        ST_DistanceSphere(
            geom,
            ST_SetSRID(ST_MakePoint(%s, %s), 4326)
        ) / 1000 AS distance_km
    FROM static_features
    ORDER BY geom <-> ST_SetSRID(ST_MakePoint(%s, %s), 4326)
    LIMIT 1;
    """

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(query, (longitude, latitude, longitude, latitude))
        row = cursor.fetchone()

        if row is None:
            return {}

        columns = [desc[0] for desc in cursor.description]
        return dict(zip(columns, row))

    finally:
        cursor.close()
        conn.close()