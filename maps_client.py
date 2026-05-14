# maps_client.py
# Google Maps Nearby Search + Place Details（停車資訊）

import os
import math
import httpx

MAPS_KEY = os.environ["GOOGLE_MAPS_API_KEY"]
NEARBY_URL = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
DETAILS_URL = "https://maps.googleapis.com/maps/api/place/details/json"

DISTANCE_MAP = {
    "near": 500,
    "mid":  1500,
    "far":  3000,
}


async def nearby_search(lat: float, lng: float, meal_id: str, distance_pref: str = "mid", max_results: int = 15) -> list[dict]:
    """
    依時段與距離搜尋附近店家，回傳清單供 Claude 挑選
    """
    from time_utils import MEAL_CONFIG
    cfg = MEAL_CONFIG.get(meal_id, MEAL_CONFIG["lunch"])
    radius = DISTANCE_MAP.get(distance_pref, 1500)

    params = {
        "location": f"{lat},{lng}",
        "radius": radius,
        "type": cfg["maps_type"],
        "keyword": cfg["maps_keyword"],
        "language": "zh-TW",
        "key": MAPS_KEY,
    }

    async with httpx.AsyncClient(timeout=15) as client:
        resp = await client.get(NEARBY_URL, params=params)
    resp.raise_for_status()
    data = resp.json()

    places = []
    for p in data.get("results", [])[:max_results]:
        place_id = p.get("place_id", "")
        dist = _haversine(lat, lng, p["geometry"]["location"]["lat"], p["geometry"]["location"]["lng"])
        places.append({
            "place_id":   place_id,
            "name":       p.get("name", ""),
            "vicinity":   p.get("vicinity", ""),
            "rating":     p.get("rating"),
            "distance_m": round(dist),
            "maps_url":   f"https://www.google.com/maps/place/?q=place_id:{place_id}",
            "parking":    "未知",  # 由 enrich_parking 補充
        })

    return places


async def enrich_parking(places: list[dict]) -> list[dict]:
    """
    對評分 4.0 以上的前 5 間店抓 Place Details，補充停車資訊
    """
    top = sorted([p for p in places if (p.get("rating") or 0) >= 4.0], key=lambda x: -x["distance_m"])[:5]
    top_ids = {p["place_id"] for p in top}

    async with httpx.AsyncClient(timeout=15) as client:
        for p in places:
            if p["place_id"] not in top_ids:
                continue
            try:
                resp = await client.get(DETAILS_URL, params={
                    "place_id": p["place_id"],
                    "fields": "name,parking_lot,formatted_address,opening_hours",
                    "language": "zh-TW",
                    "key": MAPS_KEY,
                })
                detail = resp.json().get("result", {})
                # Maps API 沒有直接的停車場欄位，用 formatted_address 附近關鍵字判斷
                addr = detail.get("formatted_address", "")
                p["parking"] = _infer_parking(addr, detail)
            except Exception:
                pass
    return places


async def random_nearby(lat: float, lng: float, meal_id: str) -> dict | None:
    """
    🎯 隨機給一間附近評分 4.0 以上的店
    """
    places = await nearby_search(lat, lng, meal_id, distance_pref="mid", max_results=20)
    good = [p for p in places if (p.get("rating") or 0) >= 4.0]
    if not good:
        good = places
    if not good:
        return None
    import random
    return random.choice(good)


def _haversine(lat1, lng1, lat2, lng2) -> float:
    """計算兩點距離（公尺）"""
    R = 6371000
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lng2 - lng1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))


def _infer_parking(address: str, detail: dict) -> str:
    """
    Maps API 停車場資訊有限，做簡單推斷
    有 parking_lot 欄位就用；否則依地址猜測
    """
    if detail.get("parking_lot"):
        return "附設停車場"
    keywords_yes = ["購物中心", "百貨", "廣場", "商場", "停車"]
    keywords_no  = ["巷", "弄", "老街", "市場"]
    for kw in keywords_yes:
        if kw in address:
            return "周邊可能有停車場，建議事先確認"
    for kw in keywords_no:
        if kw in address:
            return "路邊停車為主，假日可能難停"
    return "未知，建議使用 Google Maps 確認"
