# time_utils.py
# 台灣時間的時段判斷與使用者顯示文字

from datetime import datetime
import pytz

TW_TZ = pytz.timezone("Asia/Taipei")

MEAL_CONFIG = {
    "breakfast": {
        "label":   "早餐",
        "range":   "06:00–10:30",
        "emoji":   "🌅",
        "maps_type": "cafe",
        "maps_keyword": "早餐",
    },
    "lunch": {
        "label":   "午餐",
        "range":   "10:30–14:30",
        "emoji":   "☀️",
        "maps_type": "restaurant",
        "maps_keyword": "餐廳",
    },
    "snack": {
        "label":   "點心／飲料",
        "range":   "14:30–17:30",
        "emoji":   "🧋",
        "maps_type": "cafe",
        "maps_keyword": "飲料 甜點",
    },
    "dinner": {
        "label":   "晚餐",
        "range":   "17:30–21:00",
        "emoji":   "🌙",
        "maps_type": "restaurant",
        "maps_keyword": "餐廳",
    },
    "night": {
        "label":   "宵夜／夜市",
        "range":   "21:00 以後",
        "emoji":   "🏮",
        "maps_type": "meal_takeaway",
        "maps_keyword": "夜市 宵夜",
    },
}

# 使用者可以手動切換的全部選項（包含「飲料」獨立選項）
ALL_MEAL_OPTIONS = ["breakfast", "lunch", "snack", "dinner", "night"]


def get_tw_now() -> datetime:
    return datetime.now(TW_TZ)


def get_default_meal(now: datetime = None) -> str:
    """依目前台灣時間判斷預設時段"""
    if now is None:
        now = get_tw_now()
    h = now.hour + now.minute / 60
    if 6 <= h < 10.5:
        return "breakfast"
    if 10.5 <= h < 14.5:
        return "lunch"
    if 14.5 <= h < 17.5:
        return "snack"
    if 17.5 <= h < 21:
        return "dinner"
    return "night"


def build_time_greeting(now: datetime = None) -> str:
    """
    組合推播給使用者的時段問候文字
    範例輸出：
        現在時間 21:35 🏮
        預設推薦「宵夜／夜市」（21:00 以後）

        也可以換個方向：
        [早餐] [午餐] [點心飲料] [晚餐] [宵夜夜市]
    """
    if now is None:
        now = get_tw_now()
    time_str = now.strftime("%H:%M")
    default = get_default_meal(now)
    cfg = MEAL_CONFIG[default]

    lines = [
        f"現在時間 {time_str} {cfg['emoji']}",
        f"預設推薦「{cfg['label']}」（{cfg['range']}）",
        "",
        "也可以換個方向，請選擇：",
    ]
    return "\n".join(lines)


def get_quick_reply_meals(current: str) -> list[dict]:
    """
    回傳 LINE Quick Reply 用的時段選項（排除目前預設的那個）
    格式符合 LINE SDK QuickReply item
    """
    items = []
    for meal_id in ALL_MEAL_OPTIONS:
        cfg = MEAL_CONFIG[meal_id]
        items.append({
            "type": "action",
            "action": {
                "type": "message",
                "label": cfg["emoji"] + " " + cfg["label"],
                "text": f"__MEAL__{meal_id}",  # Bot 內部辨識用前綴
            }
        })
    return items
