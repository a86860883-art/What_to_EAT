# flex_message.py
# 組裝 LINE Flex Message：推薦結果卡片 Carousel

def build_recommendation_carousel(recommendations: list[dict]) -> dict:
    """
    輸入 Claude 推薦結果清單，輸出 LINE Flex Message Carousel
    最多 10 個 bubble，建議傳入 3–5 筆
    """
    bubbles = [_build_bubble(r) for r in recommendations[:10]]
    return {
        "type": "flex",
        "altText": f"為你找到 {len(bubbles)} 間推薦餐廳！",
        "contents": {
            "type": "carousel",
            "contents": bubbles,
        }
    }


def build_random_category_message(category: str) -> dict:
    """
    🎲 隨機類別：簡單的 Flex bubble
    """
    return {
        "type": "flex",
        "altText": f"隨機推薦：{category}",
        "contents": {
            "type": "bubble",
            "size": "kilo",
            "body": {
                "type": "box",
                "layout": "vertical",
                "spacing": "md",
                "contents": [
                    {
                        "type": "box",
                        "layout": "horizontal",
                        "contents": [
                            {
                                "type": "box",
                                "layout": "vertical",
                                "backgroundColor": "#534AB7",
                                "cornerRadius": "6px",
                                "paddingAll": "4px",
                                "width": "36px",
                                "height": "36px",
                                "justifyContent": "center",
                                "contents": [
                                    {"type": "text", "text": "🎲", "size": "xl", "align": "center"}
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "paddingStart": "10px",
                                "contents": [
                                    {"type": "text", "text": "隨機推薦", "size": "xs", "color": "#888888"},
                                    {"type": "text", "text": category, "size": "xl", "weight": "bold", "color": "#1a1a1a"},
                                ]
                            }
                        ]
                    },
                    {"type": "text", "text": "就吃這個！不要再想了 😄", "size": "sm", "color": "#555555", "wrap": True},
                ]
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "button",
                        "action": {"type": "message", "label": "找這類附近店家", "text": f"__FIND__{category}"},
                        "style": "primary",
                        "color": "#534AB7",
                        "height": "sm",
                    },
                    {
                        "type": "button",
                        "action": {"type": "message", "label": "再隨機一次", "text": "__RANDOM_CAT__"},
                        "height": "sm",
                        "margin": "sm",
                    }
                ]
            }
        }
    }


def build_random_place_message(place: dict) -> dict:
    """
    🎯 隨機餐廳：直接給一間店的卡片
    """
    return {
        "type": "flex",
        "altText": f"隨機餐廳：{place.get('name', '附近餐廳')}",
        "contents": _build_bubble(place, show_reason=False, title_prefix="🎯 就去這間！"),
    }


def build_quiz_question(step: int, question: str, options: list[dict]) -> dict:
    """
    問卷步驟用的 Quick Reply wrapper
    options 格式：[{"label": "超餓", "text": "__ANS__very"}, ...]
    """
    return {
        "type": "text",
        "text": f"（{step}/7）{question}",
        "quickReply": {
            "items": [
                {
                    "type": "action",
                    "action": {"type": "message", "label": o["label"], "text": o["text"]}
                }
                for o in options
            ]
        }
    }


# ── 內部組裝 ────────────────────────────────────────────────

def _build_bubble(r: dict, show_reason: bool = True, title_prefix: str = "") -> dict:
    name = r.get("name", "")
    category = r.get("category", "")
    reason = r.get("reason", "")
    maps_url = r.get("maps_url", "")
    address = r.get("address", r.get("vicinity", ""))
    rating = r.get("rating")
    distance_m = r.get("distance_m")
    parking = r.get("parking_note") or r.get("parking", "未知")

    rating_str = f"⭐ {rating}" if rating else ""
    distance_str = f"📍 {distance_m}m" if distance_m else ""
    meta = "　".join(filter(None, [rating_str, distance_str]))

    header_contents = [
        {
            "type": "box",
            "layout": "horizontal",
            "contents": [
                {
                    "type": "box",
                    "layout": "vertical",
                    "backgroundColor": "#1D9E75",
                    "cornerRadius": "6px",
                    "paddingStart": "8px",
                    "paddingEnd": "8px",
                    "paddingTop": "3px",
                    "paddingBottom": "3px",
                    "contents": [
                        {"type": "text", "text": category, "size": "xs", "color": "#FFFFFF", "weight": "bold"}
                    ]
                }
            ]
        },
        {
            "type": "text",
            "text": (title_prefix + name) if title_prefix else name,
            "size": "lg",
            "weight": "bold",
            "color": "#1a1a1a",
            "wrap": True,
            "margin": "sm",
        },
    ]
    if meta:
        header_contents.append({"type": "text", "text": meta, "size": "xs", "color": "#888888", "margin": "sm"})

    body_contents = []
    if show_reason and reason:
        body_contents.append({"type": "text", "text": reason, "size": "sm", "color": "#444444", "wrap": True})
    if address:
        body_contents.append({
            "type": "box", "layout": "horizontal", "margin": "md",
            "contents": [
                {"type": "text", "text": "地址", "size": "xs", "color": "#888888", "flex": 2},
                {"type": "text", "text": address, "size": "xs", "color": "#444444", "wrap": True, "flex": 8},
            ]
        })
    body_contents.append({
        "type": "box", "layout": "horizontal", "margin": "sm",
        "contents": [
            {"type": "text", "text": "停車", "size": "xs", "color": "#888888", "flex": 2},
            {"type": "text", "text": parking, "size": "xs", "color": "#444444", "wrap": True, "flex": 8},
        ]
    })

    footer_contents = []
    if maps_url:
        footer_contents.append({
            "type": "button",
            "action": {"type": "uri", "label": "Google Maps 導航", "uri": maps_url},
            "style": "primary",
            "color": "#1D9E75",
            "height": "sm",
        })
    footer_contents.append({
        "type": "button",
        "action": {"type": "message", "label": "換一個推薦", "text": "__REROLL__"},
        "height": "sm",
        "margin": "sm",
    })

    return {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "spacing": "none",
            "contents": [
                {"type": "box", "layout": "vertical", "spacing": "none", "contents": header_contents},
                {
                    "type": "box", "layout": "vertical", "margin": "lg",
                    "spacing": "none", "contents": body_contents
                }
            ]
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "spacing": "none",
            "contents": footer_contents,
        }
    }
