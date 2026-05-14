# app.py
# FastAPI 主程式：LINE Bot Webhook 處理
# 架構原則：Webhook 立即回覆，耗時任務全部丟 BackgroundTasks，完成後 push

from dotenv import load_dotenv
load_dotenv()

import os
import hmac
import hashlib
import base64
import asyncio
import httpx
from fastapi import FastAPI, Request, BackgroundTasks

from session import load as load_session, save as save_session, clear_quiz
from time_utils import get_tw_now, get_default_meal, build_time_greeting, get_quick_reply_meals, MEAL_CONFIG
from maps_client import nearby_search, enrich_parking, random_nearby
from recommender import get_recommendation, get_random_category
from flex_message import (
    build_recommendation_carousel,
    build_random_category_message,
    build_random_place_message,
    build_quiz_question,
)

app = FastAPI()

LINE_SECRET      = os.environ["LINE_CHANNEL_SECRET"]
LINE_TOKEN       = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
LINE_USER_ID     = os.environ["LINE_USER_ID"]
LINE_REPLY_URL   = "https://api.line.me/v2/bot/message/reply"
LINE_PUSH_URL    = "https://api.line.me/v2/bot/message/push"
LINE_HEADERS     = {"Authorization": f"Bearer {LINE_TOKEN}", "Content-Type": "application/json"}

QUIZ_STEPS = [
    # (step, question, options)
    (1, "食慾如何？", [
        {"label": "超餓 🍱", "text": "__ANS__hunger__very"},
        {"label": "普通", "text": "__ANS__hunger__normal"},
        {"label": "嘴饞就好", "text": "__ANS__hunger__light"},
    ]),
    (2, "想吃湯的還是乾的？", [
        {"label": "湯式 🍜", "text": "__ANS__texture__soup"},
        {"label": "乾式 🍛", "text": "__ANS__texture__dry"},
        {"label": "都可以", "text": "__ANS__texture__both"},
    ]),
    (3, "口味方向？", [
        {"label": "鹹食 🧂", "text": "__ANS__taste__savory"},
        {"label": "甜食 🍮", "text": "__ANS__taste__sweet"},
        {"label": "都可以", "text": "__ANS__taste__both"},
    ]),
    (4, "預算大概？", [
        {"label": "$100 以下", "text": "__ANS__budget__low"},
        {"label": "$300 以下", "text": "__ANS__budget__mid"},
        {"label": "不限", "text": "__ANS__budget__any"},
    ]),
    (5, "內用還是外帶？", [
        {"label": "內用 🪑", "text": "__ANS__method__dine_in"},
        {"label": "外帶 🛍", "text": "__ANS__method__takeout"},
        {"label": "外送 🛵", "text": "__ANS__method__delivery"},
    ]),
    (6, "可以走多遠？", [
        {"label": "5 分鐘內", "text": "__ANS__distance__near"},
        {"label": "15 分鐘內", "text": "__ANS__distance__mid"},
        {"label": "遠一點也行", "text": "__ANS__distance__far"},
    ]),
    (7, "有什麼特別想吃或不想吃的嗎？（可跳過）", [
        {"label": "跳過直接推薦", "text": "__ANS__extras__skip"},
    ]),
]


# ── Health check ────────────────────────────────────────────
@app.get("/")
async def health():
    return {"status": "running"}


@app.get("/test")
async def test():
    return {"line_token": LINE_TOKEN[:10] + "...", "status": "ok"}


# ── Webhook ─────────────────────────────────────────────────
@app.get("/webhook")
async def webhook_verify():
    return {"status": "ok"}
@app.post("/webhook")
async def webhook(request: Request, background_tasks: BackgroundTasks):
    body = await request.body()

    # 驗證 LINE 簽名
    sig = request.headers.get("X-Line-Signature", "")
    digest = hmac.new(LINE_SECRET.encode(), body, hashlib.sha256).digest()
    expected = base64.b64encode(digest).decode()
    if not hmac.compare_digest(sig, expected):
        return {"status": "invalid signature"}

    import json
    data = json.loads(body)
    for event in data.get("events", []):
        background_tasks.add_task(handle_event, event)

    return {"status": "ok"}


# ── 事件主路由 ───────────────────────────────────────────────
async def handle_event(event: dict):
    etype = event.get("type")
    user_id = event.get("source", {}).get("userId", "")
    reply_token = event.get("replyToken", "")

    if etype == "message":
        msg = event.get("message", {})
        mtype = msg.get("type")

        if mtype == "location":
            await handle_location(user_id, reply_token, msg)

        elif mtype == "text":
            text = msg.get("text", "").strip()
            await handle_text(user_id, reply_token, text)

    elif etype == "follow":
        await handle_follow(user_id, reply_token)


# ── 定位訊息 ─────────────────────────────────────────────────
async def handle_location(user_id: str, reply_token: str, msg: dict):
    lat = msg.get("latitude")
    lng = msg.get("longitude")
    session = load_session(user_id)
    session["last_location"] = {"lat": lat, "lng": lng}
    session["quiz"]["location"] = {"lat": lat, "lng": lng}
    save_session(user_id, session)

    now = get_tw_now()
    default_meal = get_default_meal(now)
    greeting = build_time_greeting(now)
    quick_replies = get_quick_reply_meals(default_meal)

    await reply_messages(reply_token, [
        {"type": "text", "text": greeting + f"\n\n請選擇這一餐的方向：", "quickReply": {"items": quick_replies}}
    ])


# ── 文字訊息路由 ─────────────────────────────────────────────
async def handle_text(user_id: str, reply_token: str, text: str):
    session = load_session(user_id)

    # ── 時段選擇 ──
    if text.startswith("__MEAL__"):
        meal_id = text.replace("__MEAL__", "")
        session["quiz"]["meal_time"] = meal_id
        session["quiz"]["step"] = 1
        save_session(user_id, session)
        cfg = MEAL_CONFIG.get(meal_id, {})
        await reply_messages(reply_token, [
            {"type": "text", "text": f"好！找「{cfg.get('label', meal_id)}」的推薦 {cfg.get('emoji', '')}"},
            _make_quiz_msg(1),
        ])
        return

    # ── 問卷回答 ──
    if text.startswith("__ANS__"):
        await handle_quiz_answer(user_id, reply_token, text, session)
        return

    # ── 隨機功能 ──
    if text == "__RANDOM_CAT__" or text == "隨機類別":
        await reply_messages(reply_token, [{"type": "text", "text": "隨機選一個類別中..."}])
        category = await get_random_category(session)
        await push_messages(user_id, [build_random_category_message(category)])
        return

    if text == "__RANDOM_PLACE__" or text == "隨機餐廳":
        loc = session.get("last_location")
        if not loc:
            await reply_messages(reply_token, [
                {"type": "text", "text": "請先傳送你的位置，我才能找附近的店 📍"}
            ])
            return
        await reply_messages(reply_token, [{"type": "text", "text": "幫你隨機挑一間..."}])
        meal_id = session["quiz"].get("meal_time") or get_default_meal()
        place = await random_nearby(loc["lat"], loc["lng"], meal_id)
        if place:
            await push_messages(user_id, [build_random_place_message(place)])
        else:
            await push_messages(user_id, [{"type": "text", "text": "附近找不到店家，請換個位置試試。"}])
        return

    # ── 找特定類別附近店家 ──
    if text.startswith("__FIND__"):
        category = text.replace("__FIND__", "")
        loc = session.get("last_location")
        if not loc:
            await reply_messages(reply_token, [{"type": "text", "text": "請先傳送位置 📍"}])
            return
        await reply_messages(reply_token, [{"type": "text", "text": f"搜尋附近的「{category}」中..."}])
        session["quiz"]["meal_time"] = session["quiz"].get("meal_time") or get_default_meal()
        session["quiz"]["extras"] = category
        save_session(user_id, session)
        await run_recommendation(user_id, session)
        return

    # ── 重新推薦 ──
    if text == "__REROLL__":
        await reply_messages(reply_token, [{"type": "text", "text": "重新找其他選項中..."}])
        await run_recommendation(user_id, session)
        return

    # ── 設定禁忌（文字輸入，來自 Rich Menu 偏好設定頁） ──
    if text.startswith("__TABOO_ADD__"):
        val = text.replace("__TABOO_ADD__", "").strip()
        if val and val not in session["taboo"]["custom"]:
            session["taboo"]["custom"].append(val)
            save_session(user_id, session)
        await reply_messages(reply_token, [{"type": "text", "text": f"已加入禁忌：{val} ✅"}])
        return

    if text.startswith("__TABOO_CAT__"):
        cat_id = text.replace("__TABOO_CAT__", "").strip()
        cats = session["taboo"]["categories"]
        if cat_id in cats:
            cats.remove(cat_id)
            msg = f"已移除類別禁忌：{cat_id}"
        else:
            cats.append(cat_id)
            msg = f"已設定類別禁忌：{cat_id} ✅"
        save_session(user_id, session)
        await reply_messages(reply_token, [{"type": "text", "text": msg}])
        return

    # ── 預設：提示操作 ──
    await reply_messages(reply_token, [
        {"type": "text", "text": "請傳送位置開始推薦，或使用下方 Rich Menu 選擇功能 📍"}
    ])


# ── 問卷回答處理 ─────────────────────────────────────────────
async def handle_quiz_answer(user_id: str, reply_token: str, text: str, session: dict):
    # 格式：__ANS__欄位__值
    parts = text.replace("__ANS__", "").split("__")
    if len(parts) < 2:
        return
    field, value = parts[0], parts[1]

    quiz = session["quiz"]
    if field == "extras" and value == "skip":
        quiz["extras"] = None
    else:
        quiz[field] = value

    current_step = quiz.get("step", 1)
    next_step = current_step + 1
    quiz["step"] = next_step
    save_session(user_id, session)

    if next_step <= len(QUIZ_STEPS):
        await reply_messages(reply_token, [_make_quiz_msg(next_step)])
    else:
        # 問卷完成
        loc = quiz.get("location") or session.get("last_location")
        if not loc:
            await reply_messages(reply_token, [
                {"type": "text", "text": "請先傳送你的位置 📍，我才能找附近的店！"}
            ])
            return
        await reply_messages(reply_token, [{"type": "text", "text": "分析中，稍等一下... 🔍"}])
        await run_recommendation(user_id, session)


async def run_recommendation(user_id: str, session: dict):
    """背景執行：Maps 搜尋 + Claude 推薦 + Push"""
    try:
        quiz = session["quiz"]
        loc = quiz.get("location") or session.get("last_location")
        meal_id = quiz.get("meal_time") or get_default_meal()
        distance_pref = quiz.get("distance") or "mid"

        places = await nearby_search(loc["lat"], loc["lng"], meal_id, distance_pref)
        places = await enrich_parking(places)

        recommendations = await get_recommendation(session, places)

        # 更新 meal_history
        session["meal_history"] = (session.get("meal_history") or []) + [r.get("name", "") for r in recommendations]
        session["meal_history"] = session["meal_history"][-30:]
        clear_quiz(user_id)
        save_session(user_id, session)

        carousel = build_recommendation_carousel(recommendations)
        await push_messages(user_id, [
            {"type": "text", "text": f"為你找到 {len(recommendations)} 間推薦 🎉"},
            carousel,
        ])
    except Exception as e:
        await push_messages(user_id, [{"type": "text", "text": f"推薦時發生錯誤，請稍後再試。（{type(e).__name__}）"}])


# ── 新使用者關注 ─────────────────────────────────────────────
async def handle_follow(user_id: str, reply_token: str):
    await reply_messages(reply_token, [
        {"type": "text", "text": "歡迎！我是「這餐吃什麼」Bot 🍱\n\n請傳送你的位置，我來幫你找附近的美食 📍\n\n或點下方 Rich Menu 選擇功能！"}
    ])


# ── LINE API 工具函式 ────────────────────────────────────────
def _make_quiz_msg(step: int) -> dict:
    s = QUIZ_STEPS[step - 1]
    return build_quiz_question(s[0], s[1], s[2])


async def reply_messages(reply_token: str, messages: list[dict]):
    async with httpx.AsyncClient(timeout=10) as client:
        await client.post(LINE_REPLY_URL, headers=LINE_HEADERS, json={
            "replyToken": reply_token,
            "messages": messages[:5],  # LINE 單次最多 5 則
        })


async def push_messages(user_id: str, messages: list[dict]):
    async with httpx.AsyncClient(timeout=10) as client:
        await client.post(LINE_PUSH_URL, headers=LINE_HEADERS, json={
            "to": user_id,
            "messages": messages[:5],
        })
