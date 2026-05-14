# recommender.py
# 組裝 Claude prompt 並呼叫 API 取得餐廳推薦

import os
import json
import httpx
from food_db import get_food_names_for_prompt
from session import build_taboo_prompt

ANTHROPIC_API_KEY = os.environ["ANTHROPIC_API_KEY"]
CLAUDE_MODEL = "claude-haiku-4-5-20251001"


async def get_recommendation(session: dict, maps_results: list[dict]) -> dict:
    """
    組裝 prompt，呼叫 Claude，回傳推薦結果 dict
    maps_results: Google Maps Nearby Search 回傳的候選餐廳清單
    """
    quiz = session["quiz"]
    taboo_block = build_taboo_prompt(session)
    meal_id = quiz.get("meal_time", "lunch")
    food_names = get_food_names_for_prompt(
        meal_id=meal_id,
        taboo_flags=session["taboo"]["categories"],
        custom_taboos=session["taboo"]["custom"] + session["taboo"]["specific_foods"],
    )

    maps_text = _format_maps_for_prompt(maps_results)
    quiz_text = _format_quiz_for_prompt(quiz)
    history_text = ""
    if session.get("meal_history"):
        history_text = f"\n最近已推薦過（請避免重複）：{'、'.join(session['meal_history'][-10:])}"

    prompt = f"""你是一個台灣在地美食推薦助手，請根據以下條件推薦 3 到 5 間適合的餐廳或食物。

{taboo_block}

【用餐情境】
{quiz_text}

【可推薦的食物品項範圍】
{food_names}
{history_text}

【附近可選的店家（來自 Google Maps）】
{maps_text}

請從上方店家清單中選出 3 到 5 間最符合條件的推薦，每間店請以 JSON 格式輸出，包含以下欄位：
- name: 店名
- category: 食物類別（例：拉麵、鹽酥雞、咖啡）
- reason: 一句話說明為何推薦（20 字以內，符合使用者當下情境）
- maps_url: Google Maps 連結（從輸入資料取得）
- address: 地址
- rating: 評分（從輸入資料取得，沒有則填 null）
- distance_m: 距離公尺數（整數）
- parking_note: 停車資訊（從 Maps 資料取得，無則填「未知」）

只輸出 JSON 陣列，不要有任何說明文字或 markdown code block。"""

    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": ANTHROPIC_API_KEY,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            },
            json={
                "model": CLAUDE_MODEL,
                "max_tokens": 1500,
                "messages": [{"role": "user", "content": prompt}],
            },
        )
    resp.raise_for_status()
    raw = resp.json()["content"][0]["text"].strip()

    # 去除可能殘留的 markdown fence
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    raw = raw.strip()

    return json.loads(raw)


async def get_random_category(session: dict) -> str:
    """
    🎲 隨機給一個食物類別（不需要 Maps，純 Claude）
    """
    meal_id = session["quiz"].get("meal_time") or "lunch"
    taboo_block = build_taboo_prompt(session)
    food_names = get_food_names_for_prompt(
        meal_id=meal_id,
        taboo_flags=session["taboo"]["categories"],
        custom_taboos=session["taboo"]["custom"] + session["taboo"]["specific_foods"],
    )

    prompt = f"""你是美食推薦助手。

{taboo_block}

現在是「{'早餐' if meal_id == 'breakfast' else '午餐' if meal_id == 'lunch' else '晚餐' if meal_id == 'dinner' else '點心' if meal_id == 'snack' else '宵夜'}」時間。

可選的食物範圍：{food_names}

請從上方範圍中隨機選一個食物類別，直接回答食物名稱，不要有任何其他文字。例如：拉麵"""

    async with httpx.AsyncClient(timeout=20) as client:
        resp = await client.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": ANTHROPIC_API_KEY,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            },
            json={
                "model": CLAUDE_MODEL,
                "max_tokens": 20,
                "messages": [{"role": "user", "content": prompt}],
            },
        )
    resp.raise_for_status()
    return resp.json()["content"][0]["text"].strip()


def _format_quiz_for_prompt(quiz: dict) -> str:
    hunger_map = {"very": "超餓", "normal": "普通", "light": "只是嘴饞"}
    texture_map = {"soup": "湯式", "dry": "乾式", "both": "湯乾都可以"}
    taste_map = {"savory": "鹹食", "sweet": "甜食", "both": "鹹甜都可以"}
    budget_map = {"low": "100 元以下", "mid": "300 元以下", "any": "不限預算"}
    method_map = {"dine_in": "內用", "takeout": "外帶", "delivery": "外送"}
    distance_map = {"near": "步行 5 分鐘內", "mid": "步行 15 分鐘內", "far": "不限距離"}
    weather = quiz.get("weather") or "未知"

    lines = [
        f"時段：{quiz.get('meal_time', '未知')}",
        f"食慾：{hunger_map.get(quiz.get('hunger'), '未知')}",
        f"口感：{texture_map.get(quiz.get('texture'), '未知')}",
        f"口味：{taste_map.get(quiz.get('taste'), '未知')}",
        f"預算：{budget_map.get(quiz.get('budget'), '未知')}",
        f"用餐方式：{method_map.get(quiz.get('method'), '未知')}",
        f"距離：{distance_map.get(quiz.get('distance'), '未知')}",
        f"天氣：{weather}",
    ]
    if quiz.get("extras"):
        lines.append(f"補充：{quiz['extras']}")
    return "\n".join(lines)


def _format_maps_for_prompt(places: list[dict]) -> str:
    if not places:
        return "（無 Maps 資料，請從食物品項範圍中自由推薦）"
    lines = []
    for i, p in enumerate(places, 1):
        lines.append(
            f"{i}. {p.get('name')} | 評分 {p.get('rating', '無')} | "
            f"距離 {p.get('distance_m', '?')}m | "
            f"地址：{p.get('vicinity', '')} | "
            f"Maps：{p.get('maps_url', '')} | "
            f"停車：{p.get('parking', '未知')}"
        )
    return "\n".join(lines)
