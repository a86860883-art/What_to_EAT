# session.py
# 管理每位使用者的對話狀態，存在 /tmp/{user_id}.json
# 注意：Railway 重新部署後 /tmp/ 會清空，飲食禁忌建議改存 Railway Volume 或 Supabase

import json
import os
from datetime import datetime

SESSION_DIR = "/tmp"


def _path(user_id: str) -> str:
    return os.path.join(SESSION_DIR, f"{user_id}.json")


def load(user_id: str) -> dict:
    path = _path(user_id)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return _default(user_id)


def save(user_id: str, session: dict):
    with open(_path(user_id), "w", encoding="utf-8") as f:
        json.dump(session, f, ensure_ascii=False, indent=2)


def clear_quiz(user_id: str):
    """問卷結束或放棄時，清除問卷狀態，保留禁忌與歷史"""
    session = load(user_id)
    session["quiz"] = _empty_quiz()
    save(user_id, session)


def _empty_quiz() -> dict:
    return {
        "step": 0,
        "meal_time": None,       # breakfast | lunch | dinner | snack | drink | night
        "hunger": None,          # very | normal | light
        "texture": None,         # soup | dry | both
        "taste": None,           # savory | sweet | both
        "budget": None,          # low | mid | any
        "method": None,          # dine_in | takeout | delivery
        "distance": None,        # near | mid | far
        "extras": None,          # 自由輸入補充
        "location": None,        # {"lat": float, "lng": float}
        "weather": None,         # 天氣摘要字串
    }


def _default(user_id: str) -> dict:
    return {
        "user_id": user_id,
        "created_at": datetime.now().isoformat(),
        "taboo": {
            "categories": [],        # 類別禁忌 id 清單，例如 ["pork", "spicy"]
            "specific_foods": [],    # 點擊食物加入的禁忌名稱
            "custom": [],            # 自訂輸入禁忌
        },
        "last_location": None,       # {"lat": float, "lng": float}
        "meal_history": [],          # 最近推薦過的品項（避免重複）
        "quiz": _empty_quiz(),
    }


# ── 飲食禁忌對應規則（注入 Claude prompt 用）────────────────
TABOO_RULES = {
    "pork":       "完全不吃豬肉及豬肉製品（含豬油、豬血）",
    "beef":       "完全不吃牛肉及牛肉製品",
    "chicken":    "不吃雞肉（含雞腿、雞排、雞翅）",
    "seafood":    "完全不吃任何海鮮，排除魚類、蝦、貝類、蟹類、魷魚、章魚",
    "rawfish":    "不吃生魚片、生魚壽司、生魚蓋飯，但熟食魚類可以",
    "rawshrimp":  "不吃生蝦（含刺身蝦），熟蝦料理可以",
    "shellfish":  "不吃蛤蜊、牡蠣、蟹、龍蝦等貝甲類，其他魚類蝦類可以",
    "vegan":      "純素，不吃任何肉類、海鮮、蛋、奶製品",
    "vegetarian": "奶素，不吃肉類與海鮮，但可以吃蛋與奶製品",
    "spicy":      "不吃辣，排除麻辣、辣椒等辛辣食物",
    "gluten":     "不吃麩質，排除含小麥、大麥、燕麥的食物（含麵食、麵包）",
    "lactose":    "乳糖不耐，不吃含牛奶或奶製品的食物",
    "coriander":  "不吃香菜",
    "peanut":     "不吃花生及花生製品",
    "egg":        "不吃蛋及含蛋食品",
    "offal":      "不吃內臟（含豬血、豬肝、大腸等）",
    "onion":      "不吃蔥、薑、蒜",
}


def build_taboo_prompt(session: dict) -> str:
    """
    組合飲食禁忌文字，注入 Claude 推薦 prompt 前置段落
    """
    taboo = session.get("taboo", {})
    cat_ids = taboo.get("categories", [])
    specific = taboo.get("specific_foods", [])
    custom = taboo.get("custom", [])

    parts = []
    if cat_ids:
        rules = [TABOO_RULES[k] for k in cat_ids if k in TABOO_RULES]
        if rules:
            parts.append("【類別限制】" + "；".join(rules))
    if specific:
        parts.append("【不吃的食物】" + "、".join(specific))
    if custom:
        parts.append("【其他禁忌】" + "、".join(custom))

    if not parts:
        return ""
    return "使用者飲食限制（推薦時請完全排除以下項目）：\n" + "\n".join(parts)
