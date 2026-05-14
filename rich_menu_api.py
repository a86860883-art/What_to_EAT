# rich_menu_api.py
# 執行這個 script 一次，自動在 LINE 建立並設定 Rich Menu
# 用法：python rich_menu_api.py
# 需要先設好 .env

from dotenv import load_dotenv
load_dotenv()

import os
import json
import httpx

TOKEN = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
HEADERS = {"Authorization": f"Bearer {TOKEN}"}
RICH_MENU_URL = "https://api.line.me/v2/bot/richmenu"


def create_rich_menu() -> str:
    """建立 Rich Menu 結構，回傳 richMenuId"""
    payload = {
        "size": {"width": 2500, "height": 1686},
        "selected": True,
        "name": "這餐吃什麼 Main Menu",
        "chatBarText": "這餐吃什麼",
        "areas": [
            # 上排左：開始推薦（傳位置）
            {
                "bounds": {"x": 0, "y": 0, "width": 833, "height": 843},
                "action": {
                    "type": "uri",
                    "uri": "https://line.me/R/nv/location"  # 開啟 LINE 定位選擇器
                }
            },
            # 上排中：🎲 隨機類別
            {
                "bounds": {"x": 833, "y": 0, "width": 834, "height": 843},
                "action": {
                    "type": "message",
                    "text": "__RANDOM_CAT__"
                }
            },
            # 上排右：🎯 隨機餐廳
            {
                "bounds": {"x": 1667, "y": 0, "width": 833, "height": 843},
                "action": {
                    "type": "message",
                    "text": "__RANDOM_PLACE__"
                }
            },
            # 下排左：⭐ 我的禁忌設定
            {
                "bounds": {"x": 0, "y": 843, "width": 833, "height": 843},
                "action": {
                    "type": "message",
                    "text": "__TABOO_MENU__"
                }
            },
            # 下排中：🔥 附近熱門
            {
                "bounds": {"x": 833, "y": 843, "width": 834, "height": 843},
                "action": {
                    "type": "message",
                    "text": "__NEARBY_HOT__"
                }
            },
            # 下排右：❓ 使用說明
            {
                "bounds": {"x": 1667, "y": 843, "width": 833, "height": 843},
                "action": {
                    "type": "message",
                    "text": "__HELP__"
                }
            },
        ]
    }

    resp = httpx.post(
        RICH_MENU_URL,
        headers={**HEADERS, "Content-Type": "application/json"},
        json=payload,
        timeout=15
    )
    resp.raise_for_status()
    rich_menu_id = resp.json()["richMenuId"]
    print(f"Rich Menu 建立成功：{rich_menu_id}")
    return rich_menu_id


def upload_image(rich_menu_id: str, image_path: str):
    """上傳 Rich Menu 圖片"""
    with open(image_path, "rb") as f:
        image_data = f.read()

    resp = httpx.post(
        f"https://api-data.line.me/v2/bot/richmenu/{rich_menu_id}/content",
        headers={**HEADERS, "Content-Type": "image/png"},
        content=image_data,
        timeout=30
    )
    resp.raise_for_status()
    print("圖片上傳成功")


def set_default(rich_menu_id: str):
    """設為預設 Rich Menu（所有使用者）"""
    resp = httpx.post(
        f"https://api.line.me/v2/bot/user/all/richmenu/{rich_menu_id}",
        headers=HEADERS,
        timeout=15
    )
    resp.raise_for_status()
    print("已設為預設 Rich Menu")


def delete_all_rich_menus():
    """清除所有舊的 Rich Menu（避免堆積）"""
    resp = httpx.get(RICH_MENU_URL, headers=HEADERS, timeout=15)
    menus = resp.json().get("richmenus", [])
    for m in menus:
        mid = m["richMenuId"]
        httpx.delete(f"{RICH_MENU_URL}/{mid}", headers=HEADERS, timeout=10)
        print(f"已刪除舊 Rich Menu：{mid}")


if __name__ == "__main__":
    image_path = "rich_menu.png"

    if not os.path.exists(image_path):
        print(f"找不到圖片：{image_path}")
        print("請先將 rich_menu.png 放在同目錄下，再執行此 script。")
        exit(1)

    print("清除舊 Rich Menu...")
    delete_all_rich_menus()

    print("建立新 Rich Menu...")
    rich_menu_id = create_rich_menu()

    print("上傳圖片...")
    upload_image(rich_menu_id, image_path)

    print("設為預設...")
    set_default(rich_menu_id)

    print(f"\n完成！Rich Menu ID：{rich_menu_id}")
