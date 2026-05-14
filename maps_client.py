# maps_client.py

import os, math, random
import httpx

MAPS_KEY    = os.environ.get("GOOGLE_MAPS_API_KEY", "")
NEARBY_URL  = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
DETAILS_URL = "https://maps.googleapis.com/maps/api/place/details/json"

DISTANCE_MAP = {"near": 600, "mid": 1500, "far": 3000}


async def nearby_search(lat: float, lng: float, meal_id: str,
                        distance_pref: str = "mid", max_results: int = 15) -> list[dict]:
    from time_utils import MEAL_CONFIG
    cfg    = MEAL_CONFIG.get(meal_id, MEAL_CONFIG["lunch"])
    radius = DISTANCE_MAP.get(distance_pref, 1500)

    params = {
        "location": f"{lat},{lng}",
        "radius":   radius,
        "type":     cfg["maps_type"],
        "keyword":  cfg["maps_keyword"],
        "language": "zh-TW",
        "key":      MAPS_KEY,
    }
    async with httpx.AsyncClient(timeout=15) as client:
        resp = await client.get(NEARBY_URL, params=params)
    resp.raise_for_status()

    places = []
    for p in resp.json().get("results", [])[:max_results]:
        place_id = p.get("place_id", "")
        dist = _haversine(lat, lng,
                          p["geometry"]["location"]["lat"],
                          p["geometry"]["location"]["lng"])
        places.append({
            "place_id":          place_id,
            "name":              p.get("name", ""),
            "vicinity":          p.get("vicinity", ""),
            "formatted_address": "",
            "rating":            p.get("rating"),
            "distance_m":        round(dist),
            "maps_url":          f"https://www.google.com/maps/place/?q=place_id:{place_id}",
            "parking":           "未知",
        })
    return places


async def enrich_details(places: list[dict]) -> list[dict]:
    async with httpx.AsyncClient(timeout=20) as client:
        for p in places:
            if not p.get("place_id"):
                p["formatted_address"] = p.get("vicinity", "")
                continue
            try:
                resp = await client.get(DETAILS_URL, params={
                    "place_id": p["place_id"],
                    "fields":   "formatted_address,opening_hours",
                    "language": "zh-TW",
                    "key":      MAPS_KEY,
                })
                result = resp.json().get("result", {})
                addr   = result.get("formatted_address", "").strip()
                addr   = addr.removeprefix("台灣").strip()
                p["formatted_address"] = addr or p.get("vicinity", "")
                p["parking"] = _infer_parking(p["formatted_address"])
            except Exception:
                p["formatted_address"] = p.get("vicinity", "")
                p["parking"] = "建議點地圖確認"
    return places


async def enrich_parking(places: list[dict]) -> list[dict]:
    return await enrich_details(places)


async def random_nearby(lat: float, lng: float, meal_id: str) -> dict | None:
    places = await nearby_search(lat, lng, meal_id, distance_pref="mid", max_results=20)
    places = await enrich_details(places)
    good   = [p for p in places if (p.get("rating") or 0) >= 4.0]
    pool   = good if good else places
    if not pool:
        return None
    random.shuffle(pool)
    return pool[0]


def _haversine(lat1, lng1, lat2, lng2) -> float:
    R = 6371000
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi       = math.radians(lat2 - lat1)
    dlambda    = math.radians(lng2 - lng1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))


def _infer_parking(address: str) -> str:
    if not address:
        return "建議點地圖確認"
    kw_yes = ["購物中心", "百貨", "廣場", "商場", "園區", "大樓", "停車"]
    kw_no  = ["巷", "弄", "夜市", "老街", "市場", "攤"]
    for kw in kw_yes:
        if kw in address:
            return "周邊有停車場，建議提前確認"
    for kw in kw_no:
        if kw in address:
            return "路邊停車為主，假日較難停"
    return "建議點地圖查詢附近停車場"
