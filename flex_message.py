# flex_message.py

STEP_COLORS = {1:"#1D9E75",2:"#2176AE",3:"#B5451B",4:"#6B4226",5:"#3D5A80",6:"#5C4033",7:"#4A4A6A"}
STEP_EMOJIS = {1:"🍽",2:"🍜",3:"👅",4:"💰",5:"🚶",6:"📍",7:"✏️"}

def build_quiz_card(step: int, question: str, options: list) -> dict:
    color = STEP_COLORS.get(step, "#444444")
    emoji = STEP_EMOJIS.get(step, "❓")
    total = 7
    dots = []
    for i in range(1, total+1):
        dots.append({"type":"box","layout":"vertical","width":"26px","height":"7px",
                     "cornerRadius":"3px","backgroundColor": color if i<=step else "#DDDDDD","contents":[]})
        if i < total:
            dots.append({"type":"box","layout":"vertical","width":"5px","height":"7px","contents":[]})
    btn_contents = []
    for opt in options:
        btn_contents.append({
            "type":"button",
            "action":{"type":"message","label":opt["label"],"text":opt["text"]},
            "style":"secondary","height":"sm","margin":"sm"
        })
    return {
        "type":"flex","altText":f"第{step}/{total}題：{question}",
        "contents":{
            "type":"bubble","size":"mega",
            "header":{
                "type":"box","layout":"vertical","backgroundColor":color,"paddingAll":"18px",
                "contents":[
                    {"type":"box","layout":"horizontal","contents":[
                        {"type":"text","text":f"{emoji}  第 {step} 題 / 共 {total} 題",
                         "size":"sm","color":"#FFFFFF","weight":"bold","flex":1},
                        {"type":"text","text":f"{step}/{total}","size":"sm","color":"#FFFFFF80","align":"end"}
                    ]},
                    {"type":"box","layout":"horizontal","margin":"md","contents":dots}
                ]
            },
            "body":{
                "type":"box","layout":"vertical","paddingAll":"20px",
                "contents":[
                    {"type":"text","text":question,"size":"xl","weight":"bold",
                     "color":"#1A1A1A","wrap":True},
                    {"type":"box","layout":"vertical","margin":"lg","contents":btn_contents}
                ]
            }
        }
    }

def build_recommendation_carousel(recommendations: list) -> dict:
    bubbles = [_build_bubble(r) for r in recommendations[:10]]
    return {"type":"flex","altText":f"為你找到 {len(bubbles)} 間推薦！",
            "contents":{"type":"carousel","contents":bubbles}}

def build_random_category_message(category: str) -> dict:
    return {
        "type":"flex","altText":f"隨機推薦：{category}",
        "contents":{
            "type":"bubble","size":"kilo",
            "body":{
                "type":"box","layout":"vertical","spacing":"md","paddingAll":"20px",
                "contents":[
                    {"type":"box","layout":"horizontal","contents":[
                        {"type":"box","layout":"vertical","backgroundColor":"#534AB7",
                         "cornerRadius":"20px","paddingAll":"10px","width":"44px","height":"44px",
                         "justifyContent":"center",
                         "contents":[{"type":"text","text":"🎲","align":"center","size":"lg"}]},
                        {"type":"box","layout":"vertical","paddingStart":"12px","justifyContent":"center",
                         "contents":[
                             {"type":"text","text":"隨機推薦","size":"xs","color":"#888888"},
                             {"type":"text","text":category,"size":"xxl","weight":"bold","color":"#1A1A1A"}
                         ]}
                    ]},
                    {"type":"separator","margin":"md","color":"#EEEEEE"},
                    {"type":"text","text":"就吃這個！不要再想了 😄","size":"sm","color":"#555555","wrap":True,"margin":"md"}
                ]
            },
            "footer":{
                "type":"box","layout":"vertical","paddingAll":"16px",
                "contents":[
                    {"type":"button","action":{"type":"message","label":"📍 找這類附近店家","text":f"__FIND__{category}"},
                     "style":"primary","color":"#534AB7","height":"sm"},
                    {"type":"button","action":{"type":"message","label":"🎲 再隨機一次","text":"__RANDOM_CAT__"},
                     "height":"sm","margin":"sm"}
                ]
            }
        }
    }

def build_random_place_message(place: dict) -> dict:
    return {"type":"flex","altText":f"隨機餐廳：{place.get('name','')}",
            "contents":_build_bubble(place,show_reason=False,title_prefix="🎯 就去這間！")}

def build_quiz_question(step: int, question: str, options: list) -> dict:
    """alias kept for backward compat"""
    return build_quiz_card(step, question, options)

def _info_row(label, value):
    return {"type":"box","layout":"horizontal","margin":"md","contents":[
        {"type":"text","text":label,"size":"xs","color":"#999999","flex":2,"weight":"bold"},
        {"type":"text","text":value or "—","size":"xs","color":"#444444","wrap":True,"flex":8}
    ]}

def _build_bubble(r: dict, show_reason=True, title_prefix="") -> dict:
    name     = r.get("name","")
    category = r.get("category","")
    reason   = r.get("reason","")
    maps_url = r.get("maps_url","")
    address  = r.get("formatted_address") or r.get("address") or r.get("vicinity") or "—"
    rating   = r.get("rating")
    dist     = r.get("distance_m")
    parking  = r.get("parking_note") or r.get("parking") or "未知"

    meta = "　".join(filter(None,[f"⭐ {rating}" if rating else "", f"📍 {dist}m" if dist else ""]))

    header = [
        {"type":"box","layout":"horizontal","contents":[
            {"type":"box","layout":"vertical","backgroundColor":"#1D9E75","cornerRadius":"6px",
             "paddingStart":"10px","paddingEnd":"10px","paddingTop":"4px","paddingBottom":"4px",
             "contents":[{"type":"text","text":category or "餐廳","size":"xs","color":"#FFFFFF","weight":"bold"}]}
        ]},
        {"type":"text","text":((title_prefix+" "+name).strip() if title_prefix else name),
         "size":"xl","weight":"bold","color":"#1A1A1A","wrap":True,"margin":"sm"},
    ]
    if meta:
        header.append({"type":"text","text":meta,"size":"sm","color":"#888888","margin":"sm"})

    body = []
    if show_reason and reason:
        body.append({"type":"text","text":f"💬 {reason}","size":"sm","color":"#444444","wrap":True})
    body.append(_info_row("地址", address))
    body.append(_info_row("停車", parking))

    footer = []
    if maps_url:
        footer.append({"type":"button","action":{"type":"uri","label":"🗺 Google Maps 導航","uri":maps_url},
                       "style":"primary","color":"#1D9E75","height":"sm"})
    footer.append({"type":"button","action":{"type":"message","label":"換一個推薦","text":"__REROLL__"},
                   "height":"sm","margin":"sm"})

    return {
        "type":"bubble",
        "body":{"type":"box","layout":"vertical","paddingAll":"20px","spacing":"none","contents":[
            {"type":"box","layout":"vertical","spacing":"none","contents":header},
            {"type":"separator","margin":"lg","color":"#EEEEEE"},
            {"type":"box","layout":"vertical","margin":"lg","spacing":"none","contents":body}
        ]},
        "footer":{"type":"box","layout":"vertical","paddingAll":"16px","contents":footer}
    }
