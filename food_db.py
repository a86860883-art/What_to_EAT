# food_db.py
# 食物資料庫：每筆資料包含名稱、標籤、適用時段、禁忌旗標
# meals 可跨多個時段；taboo_flags 用於推薦時快速過濾

FOOD_DB = [
    # ── 早餐：台式 ──────────────────────────────────────────
    {"name": "蛋餅",          "tags": ["breakfast", "tw"],     "meals": ["breakfast"],                    "taboo_flags": ["egg"]},
    {"name": "蘿蔔糕",        "tags": ["breakfast", "trad"],   "meals": ["breakfast", "night"],           "taboo_flags": []},
    {"name": "燒餅油條",      "tags": ["breakfast", "trad"],   "meals": ["breakfast"],                    "taboo_flags": ["gluten"]},
    {"name": "飯糰",          "tags": ["breakfast", "tw"],     "meals": ["breakfast"],                    "taboo_flags": []},
    {"name": "鐵板麵",        "tags": ["breakfast", "tw"],     "meals": ["breakfast"],                    "taboo_flags": []},
    {"name": "蔥抓餅",        "tags": ["breakfast", "street"], "meals": ["breakfast", "night"],           "taboo_flags": ["gluten", "onion"]},
    {"name": "肉蛋吐司",      "tags": ["breakfast", "tw"],     "meals": ["breakfast"],                    "taboo_flags": ["egg", "gluten", "pork"]},
    {"name": "厚片吐司",      "tags": ["breakfast", "tw"],     "meals": ["breakfast", "snack"],           "taboo_flags": ["gluten"]},
    {"name": "潤餅（春捲）",  "tags": ["breakfast", "trad", "street"], "meals": ["breakfast", "lunch", "night"], "taboo_flags": ["peanut", "gluten"]},

    # ── 早餐：西式 ──────────────────────────────────────────
    {"name": "漢堡",          "tags": ["breakfast", "west"],   "meals": ["breakfast", "lunch"],           "taboo_flags": ["gluten"]},
    {"name": "三明治",        "tags": ["breakfast", "west"],   "meals": ["breakfast", "lunch"],           "taboo_flags": ["gluten"]},
    {"name": "可頌",          "tags": ["breakfast", "west"],   "meals": ["breakfast", "snack"],           "taboo_flags": ["gluten", "lactose"]},
    {"name": "貝果",          "tags": ["breakfast", "west"],   "meals": ["breakfast", "snack"],           "taboo_flags": ["gluten"]},
    {"name": "鬆餅",          "tags": ["breakfast", "sweet"],  "meals": ["breakfast", "snack"],           "taboo_flags": ["gluten", "egg", "lactose"]},
    {"name": "法式吐司",      "tags": ["breakfast", "west"],   "meals": ["breakfast", "snack"],           "taboo_flags": ["gluten", "egg", "lactose"]},
    {"name": "班尼迪克蛋",    "tags": ["breakfast", "west"],   "meals": ["breakfast"],                    "taboo_flags": ["egg", "lactose", "gluten"]},
    {"name": "歐姆蛋",        "tags": ["breakfast", "west"],   "meals": ["breakfast"],                    "taboo_flags": ["egg", "lactose"]},

    # ── 早餐：中式 ──────────────────────────────────────────
    {"name": "稀飯",          "tags": ["breakfast", "cn"],     "meals": ["breakfast"],                    "taboo_flags": []},
    {"name": "小米粥",        "tags": ["breakfast", "cn"],     "meals": ["breakfast"],                    "taboo_flags": []},
    {"name": "饅頭",          "tags": ["breakfast", "cn"],     "meals": ["breakfast"],                    "taboo_flags": ["gluten"]},
    {"name": "包子",          "tags": ["breakfast", "cn"],     "meals": ["breakfast", "lunch"],           "taboo_flags": ["gluten", "pork"]},
    {"name": "豆漿",          "tags": ["breakfast", "drink"],  "meals": ["breakfast"],                    "taboo_flags": []},
    {"name": "米漿",          "tags": ["breakfast", "drink"],  "meals": ["breakfast"],                    "taboo_flags": []},
    {"name": "燒餅",          "tags": ["breakfast", "cn"],     "meals": ["breakfast"],                    "taboo_flags": ["gluten"]},
    {"name": "蔥油餅",        "tags": ["breakfast", "cn"],     "meals": ["breakfast"],                    "taboo_flags": ["gluten", "onion"]},

    # ── 午晚餐：飯類 ────────────────────────────────────────
    {"name": "排骨飯",        "tags": ["rice", "tw"],          "meals": ["lunch", "dinner"],              "taboo_flags": ["pork"]},
    {"name": "雞腿飯",        "tags": ["rice", "tw"],          "meals": ["lunch", "dinner"],              "taboo_flags": ["chicken"]},
    {"name": "滷肉飯",        "tags": ["rice", "trad"],        "meals": ["lunch", "dinner"],              "taboo_flags": ["pork"]},
    {"name": "咖哩飯",        "tags": ["rice"],                "meals": ["lunch", "dinner"],              "taboo_flags": []},
    {"name": "炒飯",          "tags": ["rice"],                "meals": ["lunch", "dinner"],              "taboo_flags": ["egg"]},
    {"name": "丼飯",          "tags": ["rice", "japanese"],    "meals": ["lunch", "dinner"],              "taboo_flags": []},
    {"name": "壽司",          "tags": ["rice", "japanese"],    "meals": ["lunch", "dinner"],              "taboo_flags": ["rawfish", "seafood"]},
    {"name": "生魚片丼",      "tags": ["rice", "japanese"],    "meals": ["lunch", "dinner"],              "taboo_flags": ["rawfish", "seafood"]},
    {"name": "燉飯",          "tags": ["rice", "west"],        "meals": ["lunch", "dinner"],              "taboo_flags": ["lactose"]},
    {"name": "海南雞飯",      "tags": ["rice", "foreign"],     "meals": ["lunch", "dinner"],              "taboo_flags": ["chicken"]},
    {"name": "親子丼",        "tags": ["rice", "japanese"],    "meals": ["lunch", "dinner"],              "taboo_flags": ["chicken", "egg"]},

    # ── 午晚餐：麵食 ────────────────────────────────────────
    {"name": "拉麵",          "tags": ["noodle", "japanese"],  "meals": ["lunch", "dinner"],              "taboo_flags": ["gluten", "pork"]},
    {"name": "烏龍麵",        "tags": ["noodle", "japanese"],  "meals": ["lunch", "dinner"],              "taboo_flags": ["gluten"]},
    {"name": "蕎麥麵",        "tags": ["noodle", "japanese"],  "meals": ["lunch", "dinner"],              "taboo_flags": []},
    {"name": "義大利麵",      "tags": ["noodle", "west"],      "meals": ["lunch", "dinner"],              "taboo_flags": ["gluten"]},
    {"name": "河粉",          "tags": ["noodle", "viet"],      "meals": ["lunch", "dinner"],              "taboo_flags": []},
    {"name": "米線",          "tags": ["noodle"],              "meals": ["lunch", "dinner"],              "taboo_flags": []},
    {"name": "炒麵",          "tags": ["noodle"],              "meals": ["lunch", "dinner"],              "taboo_flags": ["gluten"]},
    {"name": "刀削麵",        "tags": ["noodle", "cn"],        "meals": ["lunch", "dinner"],              "taboo_flags": ["gluten"]},
    {"name": "陽春麵",        "tags": ["noodle", "trad"],      "meals": ["lunch", "dinner"],              "taboo_flags": ["gluten"]},
    {"name": "板條",          "tags": ["noodle", "trad"],      "meals": ["lunch", "dinner"],              "taboo_flags": []},
    {"name": "麻辣燙",        "tags": ["noodle", "cn", "spicy"], "meals": ["lunch", "dinner"],            "taboo_flags": ["spicy"]},
    {"name": "當歸鴨麵線",    "tags": ["noodle", "trad"],      "meals": ["lunch", "dinner"],              "taboo_flags": ["gluten"]},

    # ── 午晚餐：餃包 ────────────────────────────────────────
    {"name": "水餃",          "tags": ["dumpling"],            "meals": ["lunch", "dinner"],              "taboo_flags": ["gluten", "pork"]},
    {"name": "鍋貼",          "tags": ["dumpling"],            "meals": ["lunch", "dinner"],              "taboo_flags": ["gluten", "pork"]},
    {"name": "小籠包",        "tags": ["dumpling", "trad"],    "meals": ["lunch", "dinner"],              "taboo_flags": ["gluten", "pork"]},
    {"name": "蒸餃",          "tags": ["dumpling"],            "meals": ["lunch", "dinner"],              "taboo_flags": ["gluten"]},
    {"name": "煎餃",          "tags": ["dumpling"],            "meals": ["lunch", "dinner"],              "taboo_flags": ["gluten", "pork"]},
    {"name": "燒賣",          "tags": ["dumpling", "cn"],      "meals": ["lunch", "dinner"],              "taboo_flags": ["gluten", "pork"]},
    {"name": "刈包",          "tags": ["dumpling", "trad", "street"], "meals": ["lunch", "night"],        "taboo_flags": ["gluten", "pork"]},

    # ── 午晚餐：湯品鍋物 ────────────────────────────────────
    {"name": "火鍋",          "tags": ["hotpot"],              "meals": ["lunch", "dinner"],              "taboo_flags": []},
    {"name": "麻辣鍋",        "tags": ["hotpot", "spicy"],     "meals": ["lunch", "dinner"],              "taboo_flags": ["spicy"]},
    {"name": "涮涮鍋",        "tags": ["hotpot", "japanese"],  "meals": ["lunch", "dinner"],              "taboo_flags": []},
    {"name": "豆腐鍋",        "tags": ["hotpot", "korean"],    "meals": ["lunch", "dinner"],              "taboo_flags": ["spicy"]},
    {"name": "壽喜燒",        "tags": ["hotpot", "japanese"],  "meals": ["dinner"],                       "taboo_flags": ["beef", "egg"]},
    {"name": "起司火鍋",      "tags": ["hotpot", "west"],      "meals": ["dinner"],                       "taboo_flags": ["lactose"]},
    {"name": "薑母鴨",        "tags": ["hotpot", "trad"],      "meals": ["dinner"],                       "taboo_flags": []},
    {"name": "羊肉爐",        "tags": ["hotpot", "trad"],      "meals": ["dinner"],                       "taboo_flags": []},

    # ── 午晚餐：便當 ────────────────────────────────────────
    {"name": "自助餐",        "tags": ["bento"],               "meals": ["lunch"],                        "taboo_flags": []},
    {"name": "鐵路便當",      "tags": ["bento", "trad"],       "meals": ["lunch"],                        "taboo_flags": ["pork"]},
    {"name": "日式定食",      "tags": ["bento", "japanese"],   "meals": ["lunch", "dinner"],              "taboo_flags": []},
    {"name": "韓式定食",      "tags": ["bento", "korean"],     "meals": ["lunch", "dinner"],              "taboo_flags": []},
    {"name": "關東煮",        "tags": ["bento", "japanese"],   "meals": ["lunch", "night"],               "taboo_flags": []},

    # ── 晚餐：台灣料理 ──────────────────────────────────────
    {"name": "三杯雞",        "tags": ["tw"],                  "meals": ["dinner"],                       "taboo_flags": ["chicken"]},
    {"name": "蔥爆牛肉",      "tags": ["tw"],                  "meals": ["dinner"],                       "taboo_flags": ["beef", "onion"]},
    {"name": "台式熱炒",      "tags": ["tw"],                  "meals": ["dinner"],                       "taboo_flags": []},
    {"name": "麻婆豆腐",      "tags": ["tw", "cn", "spicy"],   "meals": ["dinner"],                       "taboo_flags": ["spicy", "pork"]},

    # ── 晚餐：異國料理 ──────────────────────────────────────
    {"name": "泰式料理",      "tags": ["foreign", "spicy"],    "meals": ["lunch", "dinner"],              "taboo_flags": ["spicy", "seafood"]},
    {"name": "越南料理",      "tags": ["foreign", "viet"],     "meals": ["lunch", "dinner"],              "taboo_flags": ["seafood"]},
    {"name": "印度料理",      "tags": ["foreign", "spicy"],    "meals": ["lunch", "dinner"],              "taboo_flags": ["spicy"]},
    {"name": "韓式料理",      "tags": ["foreign", "korean"],   "meals": ["lunch", "dinner"],              "taboo_flags": ["spicy"]},
    {"name": "日式料理",      "tags": ["foreign", "japanese"], "meals": ["lunch", "dinner"],              "taboo_flags": []},
    {"name": "港式點心",      "tags": ["foreign", "cn"],       "meals": ["lunch", "dinner"],              "taboo_flags": ["pork", "gluten"]},
    {"name": "墨西哥料理",    "tags": ["foreign", "west"],     "meals": ["lunch", "dinner"],              "taboo_flags": ["spicy"]},
    {"name": "中東料理",      "tags": ["foreign", "middle-east"], "meals": ["lunch", "dinner"],           "taboo_flags": []},

    # ── 晚餐：西式 ──────────────────────────────────────────
    {"name": "Pizza",         "tags": ["west"],                "meals": ["lunch", "dinner"],              "taboo_flags": ["gluten", "lactose"]},
    {"name": "牛排",          "tags": ["west"],                "meals": ["dinner"],                       "taboo_flags": ["beef"]},
    {"name": "義式料理",      "tags": ["west"],                "meals": ["lunch", "dinner"],              "taboo_flags": ["gluten"]},
    {"name": "法式料理",      "tags": ["west"],                "meals": ["dinner"],                       "taboo_flags": ["lactose"]},
    {"name": "沙拉碗",        "tags": ["west", "light"],       "meals": ["lunch", "snack"],               "taboo_flags": []},

    # ── 晚餐：傳統 ──────────────────────────────────────────
    {"name": "碗粿",          "tags": ["trad"],                "meals": ["lunch", "dinner", "night"],     "taboo_flags": ["pork"]},
    {"name": "筒仔米糕",      "tags": ["trad"],                "meals": ["lunch", "dinner", "night"],     "taboo_flags": ["pork"]},
    {"name": "肉圓",          "tags": ["trad", "street"],      "meals": ["lunch", "night"],               "taboo_flags": ["pork"]},
    {"name": "蚵嗲",          "tags": ["trad", "seafood"],     "meals": ["lunch", "night"],               "taboo_flags": ["seafood", "shellfish"]},
    {"name": "魚丸湯",        "tags": ["trad", "seafood"],     "meals": ["lunch", "dinner"],              "taboo_flags": ["seafood"]},
    {"name": "廣東粥",        "tags": ["trad", "cn"],          "meals": ["lunch", "dinner"],              "taboo_flags": []},

    # ── 燒烤串燒 ────────────────────────────────────────────
    {"name": "烤肉燒烤",      "tags": ["grill"],               "meals": ["dinner", "night"],              "taboo_flags": []},
    {"name": "串燒",          "tags": ["grill", "japanese", "street"], "meals": ["dinner", "night"],      "taboo_flags": []},
    {"name": "沙威瑪",        "tags": ["grill", "street", "middle-east"], "meals": ["snack", "night"],    "taboo_flags": []},
    {"name": "烤玉米",        "tags": ["grill", "street"],     "meals": ["night"],                        "taboo_flags": []},
    {"name": "烤香腸",        "tags": ["grill", "street"],     "meals": ["night"],                        "taboo_flags": ["pork"]},
    {"name": "烤魷魚",        "tags": ["grill", "seafood", "street"], "meals": ["night"],                "taboo_flags": ["seafood"]},
    {"name": "生蠔燒",        "tags": ["grill", "seafood"],    "meals": ["night"],                        "taboo_flags": ["seafood", "shellfish"]},

    # ── 夜市炸物 ────────────────────────────────────────────
    {"name": "鹹酥雞",        "tags": ["fried", "street"],     "meals": ["snack", "night"],               "taboo_flags": ["chicken"]},
    {"name": "鹹水雞",        "tags": ["street", "light"],     "meals": ["snack", "night"],               "taboo_flags": ["chicken"]},
    {"name": "地瓜球",        "tags": ["fried", "street", "sweet"], "meals": ["snack", "night"],          "taboo_flags": []},
    {"name": "無骨鳳爪",      "tags": ["fried", "street"],     "meals": ["snack", "night"],               "taboo_flags": ["chicken"]},
    {"name": "章魚燒",        "tags": ["fried", "japanese", "street", "seafood"], "meals": ["snack", "night"], "taboo_flags": ["seafood"]},
    {"name": "炸雞排",        "tags": ["fried", "street"],     "meals": ["snack", "lunch", "night"],      "taboo_flags": ["chicken"]},
    {"name": "臭豆腐",        "tags": ["fried", "street"],     "meals": ["night"],                        "taboo_flags": []},
    {"name": "甜不辣",        "tags": ["fried", "street", "seafood"], "meals": ["snack", "night"],        "taboo_flags": ["seafood"]},
    {"name": "炸花枝",        "tags": ["fried", "seafood"],    "meals": ["night"],                        "taboo_flags": ["seafood"]},
    {"name": "炸蝦",          "tags": ["fried", "seafood"],    "meals": ["snack", "night"],               "taboo_flags": ["seafood"]},
    {"name": "起司條",        "tags": ["fried", "street"],     "meals": ["snack", "night"],               "taboo_flags": ["lactose"]},

    # ── 夜市小吃 ────────────────────────────────────────────
    {"name": "蚵仔煎",        "tags": ["trad", "street", "seafood"], "meals": ["dinner", "night"],        "taboo_flags": ["seafood", "shellfish", "egg"]},
    {"name": "蚵仔麵線",      "tags": ["trad", "street", "seafood"], "meals": ["dinner", "night"],        "taboo_flags": ["seafood", "shellfish", "gluten", "offal"]},
    {"name": "大腸包小腸",    "tags": ["street"],              "meals": ["snack", "night"],               "taboo_flags": ["pork", "offal"]},
    {"name": "滷味",          "tags": ["street"],              "meals": ["snack", "night"],               "taboo_flags": []},
    {"name": "豬血糕",        "tags": ["street"],              "meals": ["night"],                        "taboo_flags": ["pork", "offal"]},
    {"name": "糯米腸",        "tags": ["street"],              "meals": ["night"],                        "taboo_flags": ["pork"]},
    {"name": "米血糕",        "tags": ["street", "trad"],      "meals": ["night"],                        "taboo_flags": ["pork", "offal"]},
    {"name": "車輪餅",        "tags": ["street", "sweet"],     "meals": ["snack", "night"],               "taboo_flags": ["gluten"]},
    {"name": "草仔粿",        "tags": ["trad", "street"],      "meals": ["night"],                        "taboo_flags": []},
    {"name": "花生捲冰淇淋",  "tags": ["sweet", "street"],     "meals": ["snack", "night"],               "taboo_flags": ["peanut"]},

    # ── 點心甜食 ────────────────────────────────────────────
    {"name": "剉冰",          "tags": ["sweet", "dessert"],    "meals": ["snack"],                        "taboo_flags": []},
    {"name": "豆花",          "tags": ["sweet", "dessert", "trad"], "meals": ["snack"],                   "taboo_flags": []},
    {"name": "芋圓",          "tags": ["sweet", "dessert"],    "meals": ["snack"],                        "taboo_flags": []},
    {"name": "湯圓",          "tags": ["sweet", "dessert", "trad"], "meals": ["snack"],                   "taboo_flags": ["peanut"]},
    {"name": "燒仙草",        "tags": ["sweet", "dessert", "trad"], "meals": ["snack"],                   "taboo_flags": []},
    {"name": "粉圓",          "tags": ["sweet", "dessert"],    "meals": ["snack"],                        "taboo_flags": []},
    {"name": "杏仁豆腐",      "tags": ["sweet", "dessert"],    "meals": ["snack"],                        "taboo_flags": []},
    {"name": "芒果冰",        "tags": ["sweet", "dessert"],    "meals": ["snack"],                        "taboo_flags": []},
    {"name": "蛋糕",          "tags": ["sweet", "dessert", "west"], "meals": ["snack"],                   "taboo_flags": ["gluten", "egg", "lactose"]},
    {"name": "馬卡龍",        "tags": ["sweet", "dessert", "west"], "meals": ["snack"],                   "taboo_flags": ["egg", "lactose"]},
    {"name": "可麗餅",        "tags": ["sweet", "dessert", "west"], "meals": ["snack"],                   "taboo_flags": ["gluten", "egg", "lactose"]},
    {"name": "冰淇淋",        "tags": ["sweet", "dessert", "west"], "meals": ["snack"],                   "taboo_flags": ["lactose"]},
    {"name": "提拉米蘇",      "tags": ["sweet", "dessert", "west"], "meals": ["snack"],                   "taboo_flags": ["lactose", "egg", "gluten"]},
    {"name": "布丁",          "tags": ["sweet", "dessert"],    "meals": ["snack"],                        "taboo_flags": ["egg", "lactose"]},
    {"name": "甜甜圈",        "tags": ["sweet", "dessert", "west"], "meals": ["snack"],                   "taboo_flags": ["gluten", "egg"]},
    {"name": "水果切盤",      "tags": ["sweet", "light"],      "meals": ["snack"],                        "taboo_flags": []},
    {"name": "草莓大福",      "tags": ["sweet", "dessert", "japanese"], "meals": ["snack"],               "taboo_flags": []},
    {"name": "水果塔",        "tags": ["sweet", "dessert", "west"], "meals": ["snack"],                   "taboo_flags": ["gluten", "egg", "lactose"]},

    # ── 飲料：茶飲 ──────────────────────────────────────────
    {"name": "珍珠奶茶",      "tags": ["drink", "tea"],        "meals": ["breakfast", "snack", "lunch", "dinner"], "taboo_flags": ["lactose"]},
    {"name": "綠茶",          "tags": ["drink", "tea"],        "meals": ["snack", "lunch", "dinner"],     "taboo_flags": []},
    {"name": "烏龍茶",        "tags": ["drink", "tea"],        "meals": ["snack", "lunch", "dinner"],     "taboo_flags": []},
    {"name": "鮮奶茶",        "tags": ["drink", "tea"],        "meals": ["breakfast", "snack"],           "taboo_flags": ["lactose"]},
    {"name": "冬瓜茶",        "tags": ["drink", "tea"],        "meals": ["snack"],                        "taboo_flags": []},
    {"name": "多多綠",        "tags": ["drink", "tea"],        "meals": ["snack"],                        "taboo_flags": []},
    {"name": "港式奶茶",      "tags": ["drink", "tea"],        "meals": ["breakfast", "snack"],           "taboo_flags": ["lactose"]},
    {"name": "四季春",        "tags": ["drink", "tea"],        "meals": ["snack"],                        "taboo_flags": []},

    # ── 飲料：咖啡 ──────────────────────────────────────────
    {"name": "美式咖啡",      "tags": ["drink", "coffee"],     "meals": ["breakfast", "snack"],           "taboo_flags": []},
    {"name": "拿鐵",          "tags": ["drink", "coffee"],     "meals": ["breakfast", "snack"],           "taboo_flags": ["lactose"]},
    {"name": "卡布奇諾",      "tags": ["drink", "coffee"],     "meals": ["breakfast", "snack"],           "taboo_flags": ["lactose"]},
    {"name": "燕麥奶拿鐵",    "tags": ["drink", "coffee"],     "meals": ["breakfast", "snack"],           "taboo_flags": []},
    {"name": "冰滴咖啡",      "tags": ["drink", "coffee"],     "meals": ["snack"],                        "taboo_flags": []},
    {"name": "摩卡",          "tags": ["drink", "coffee"],     "meals": ["breakfast", "snack"],           "taboo_flags": ["lactose"]},

    # ── 飲料：果汁冷飲 ──────────────────────────────────────
    {"name": "柳橙汁",        "tags": ["drink", "juice"],      "meals": ["breakfast", "snack"],           "taboo_flags": []},
    {"name": "西瓜汁",        "tags": ["drink", "juice"],      "meals": ["snack"],                        "taboo_flags": []},
    {"name": "芒果汁",        "tags": ["drink", "juice"],      "meals": ["snack"],                        "taboo_flags": []},
    {"name": "檸檬汁",        "tags": ["drink", "juice"],      "meals": ["snack"],                        "taboo_flags": []},
    {"name": "蔬果汁",        "tags": ["drink", "juice"],      "meals": ["breakfast", "snack"],           "taboo_flags": []},
    {"name": "椰子水",        "tags": ["drink", "juice"],      "meals": ["snack"],                        "taboo_flags": []},
    {"name": "蘆薈飲",        "tags": ["drink", "juice"],      "meals": ["snack"],                        "taboo_flags": []},

    # ── 飲料：熱飲 ──────────────────────────────────────────
    {"name": "熱可可",        "tags": ["drink", "hot"],        "meals": ["breakfast", "snack"],           "taboo_flags": ["lactose"]},
    {"name": "薑茶",          "tags": ["drink", "hot"],        "meals": ["snack", "night"],               "taboo_flags": []},
    {"name": "菊花茶",        "tags": ["drink", "hot"],        "meals": ["snack"],                        "taboo_flags": []},
    {"name": "桂圓紅棗茶",    "tags": ["drink", "hot"],        "meals": ["snack"],                        "taboo_flags": []},
    {"name": "黑糖薑母茶",    "tags": ["drink", "hot"],        "meals": ["snack", "night"],               "taboo_flags": []},
    {"name": "玫瑰花茶",      "tags": ["drink", "hot"],        "meals": ["snack"],                        "taboo_flags": []},
]


def get_foods_for_meal(meal_id: str, taboo_flags: list[str] = None, custom_taboos: list[str] = None) -> list[dict]:
    """
    根據時段與禁忌過濾食物清單
    meal_id: breakfast | lunch | dinner | snack | drink | night
    taboo_flags: 類別禁忌 id 清單
    custom_taboos: 自訂禁忌字串清單（食物名稱或食材）
    """
    taboo_flags = taboo_flags or []
    custom_taboos = custom_taboos or []

    result = []
    for food in FOOD_DB:
        if meal_id not in food["meals"]:
            continue
        if any(f in food["taboo_flags"] for f in taboo_flags):
            continue
        if any(ct in food["name"] for ct in custom_taboos):
            continue
        result.append(food)
    return result


def get_food_names_for_prompt(meal_id: str, taboo_flags: list[str] = None, custom_taboos: list[str] = None) -> str:
    """
    回傳給 Claude prompt 用的食物名稱字串
    """
    foods = get_foods_for_meal(meal_id, taboo_flags, custom_taboos)
    return "、".join(f["name"] for f in foods)
