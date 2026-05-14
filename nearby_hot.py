# nearby_hot.py
# 附近熱門：不需問卷，直接依評分排序列出附近高分餐廳

import httpx
import os
import math

MAPS_KEY = os.environ.get("GOOGLE_MAPS_API_KEY", "")
NEARBY_URL = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"


async def get_nearby_hot(lat: float, lng: float, radius: int = 1000, max_results: int = 5) -> list[dict]:
    """
    搜尋附近評分 4.0 以上、依評分排序的熱門餐廳
    radius: 搜尋半徑（公尺），預設 1km
    """
    params = {
        "location": f"{lat},{lng}",
        "radius": radius,
        "type": "restaurant",
        "language": "zh-TW",
        "key": MAPS_KEY,
    }

    async with httpx.AsyncClient(timeout=15) as client:
        resp = await client.get(NEARBY_URL, params=params)
    resp.raise_for_status()
    data = resp.json()

    places = []
    for p in data.get("results", []):
        rating = p.get("rating")
        if not rating or rating < 4.0:
            continue
        place_id = p.get("place_id", "")
        dist = _haversine(
            lat, lng,
            p["geometry"]["location"]["lat"],
            p["geometry"]["location"]["lng"]
        )
        places.append({
            "place_id":    place_id,
            "name":        p.get("name", ""),
            "vicinity":    p.get("vicinity", ""),
            "rating":      rating,
            "user_ratings_total": p.get("user_ratings_total", 0),
            "distance_m":  round(dist),
            "maps_url":    f"https://www.google.com/maps/place/?q=place_id:{place_id}",
            "category":    _infer_category(p.get("types", [])),
            "parking":     "未知",
        })

    # 依評分降序，評分相同則依評論數降序
    places.sort(key=lambda x: (-x["rating"], -x["user_ratings_total"]))
    return places[:max_results]


def _haversine(lat1, lng1, lat2, lng2) -> float:
    R = 6371000
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lng2 - lng1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))


def _infer_category(types: list[str]) -> str:
    mapping = {
        "japanese_restaurant": "日式料理",
        "chinese_restaurant":  "中式料理",
        "korean_restaurant":   "韓式料理",
        "thai_restaurant":     "泰式料理",
        "italian_restaurant":  "義式料理",
        "american_restaurant": "美式料理",
        "cafe":                "咖啡廳",
        "bakery":              "麵包烘焙",
        "meal_takeaway":       "外帶小吃",
        "bar":                 "餐酒館",
    }
    for t in types:
        if t in mapping:
            return mapping[t]
    return "餐廳"


def build_nearby_hot_flex(places: list[dict]) -> dict:
    """
    組裝附近熱門的 Flex Message Carousel
    """
    if not places:
        return {
            "type": "text",
            "text": "附近暫時找不到評分 4.0 以上的餐廳，要試試更大範圍嗎？\n回覆「熱門 2km」可擴大搜尋。"
        }

    bubbles = [_hot_bubble(p) for p in places]
    return {
        "type": "flex",
        "altText": f"附近熱門餐廳 Top {len(bubbles)}",
        "contents": {
            "type": "carousel",
            "contents": bubbles,
        }
    }


def _hot_bubble(p: dict) -> dict:
    stars = _star_bar(p["rating"])
    reviews = f"（{p['user_ratings_total']} 則評論）" if p.get("user_ratings_total") else ""

    return {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "spacing": "none",
            "contents": [
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {
                            "type": "box",
                            "layout": "vertical",
                            "backgroundColor": "#D85A30",
                            "cornerRadius": "6px",
                            "paddingStart": "8px",
                            "paddingEnd": "8px",
                            "paddingTop": "3px",
                            "paddingBottom": "3px",
                            "contents": [
                                {"type": "text", "text": p["category"], "size": "xs", "color": "#FFFFFF", "weight": "bold"}
                            ]
                        }
                    ]
                },
                {
                    "type": "text",
                    "text": p["name"],
                    "size": "lg",
                    "weight": "bold",
                    "color": "#1a1a1a",
                    "wrap": True,
                    "margin": "sm",
                },
                {
                    "type": "text",
                    "text": f"{stars} {p['rating']} {reviews}",
                    "size": "sm",
                    "color": "#BA7517",
                    "margin": "sm",
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "margin": "md",
                    "contents": [
                        {"type": "text", "text": "距離", "size": "xs", "color": "#888888", "flex": 2},
                        {"type": "text", "text": f"{p['distance_m']} 公尺", "size": "xs", "color": "#444444", "flex": 8},
                    ]
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "margin": "sm",
                    "contents": [
                        {"type": "text", "text": "地址", "size": "xs", "color": "#888888", "flex": 2},
                        {"type": "text", "text": p.get("vicinity", ""), "size": "xs", "color": "#444444", "wrap": True, "flex": 8},
                    ]
                },
            ]
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "spacing": "none",
            "contents": [
                {
                    "type": "button",
                    "action": {"type": "uri", "label": "Google Maps 導航", "uri": p["maps_url"]},
                    "style": "primary",
                    "color": "#D85A30",
                    "height": "sm",
                },
                {
                    "type": "button",
                    "action": {"type": "message", "label": "用這個時段問卷篩選", "text": "__QUIZ_FROM_HOT__"},
                    "height": "sm",
                    "margin": "sm",
                }
            ]
        }
    }


def _star_bar(rating: float) -> str:
    full = int(rating)
    half = 1 if (rating - full) >= 0.5 else 0
    empty = 5 - full - half
    return "★" * full + "½" * half + "☆" * empty
