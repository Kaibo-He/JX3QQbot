# handlers/luck_handler.py
from jinja2 import Environment, FileSystemLoader
from pathlib import Path
import os
import hashlib
import time
from datetime import datetime

from config import DEFAULT_SERVER, LUCK_DICT
from api.jx3api import get_luck_records
from utils.html_to_image import render_html_to_adapted_image

TEMPLATE_DIR = "templates"
OUTPUT_PATH = "/tmp/luck_card.png"
CACHE_DIR = "/tmp/luck_cache"
os.makedirs(CACHE_DIR, exist_ok=True)
CACHE_DURATION = 180

# 接收角色数据，生成图片
async def generate_luck_card(data: dict) -> bytes:
    # 缓存 key
    cache_key = hashlib.md5((data[0].get("name", "") + data[0].get("event", "")).encode()).hexdigest()
    cache_path = os.path.join(CACHE_DIR, f"{cache_key}.png")
    # 缓存命中且未过期
    if os.path.exists(cache_path) and (time.time() - os.path.getmtime(cache_path) < CACHE_DURATION):
        return Path(cache_path).read_bytes()
    
    # 渲染
    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
    template = env.get_template("luck_card.html")

    total_luck = len(LUCK_DICT["绝世"]) + len(LUCK_DICT["普通"]) + len(LUCK_DICT["宠物"])
    triggered_set = set([item["event"] for item in data if item["status"] == 1])

    result = {}

    for category, events in LUCK_DICT.items():
        entry_list = []
        count = 0
        for name in events:
            triggered = name in triggered_set
            if triggered:
                count += 1
            entry_list.append({
                "name": name,
                "triggered": triggered
            })
    
        total = len(events)
        percent = round(count / total * 100, 2) if total > 0 else 0

        result[category] = {
            "list": entry_list,
            "progress": count,
            "total": total,
            "percent": percent
        }

    recent = data[:5]
    def format_time(ts):
        if ts == 0:
            return "-"
        return datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")
    for item in recent:
        item["time"] = format_time(item["time"])
    context = {
        "role_name": data[0]["name"],
        "server_name": f"{data[0]['server']}@{data[0]['zone']}",
        "total_speed": len(data),
        "total_total": total_luck,
        "stats": result,
        "recent": recent
    }

    html = template.render(context)
    await render_html_to_adapted_image(html, cache_path)
    
    return Path(cache_path).read_bytes()

async def handle_luck_card(content: str):
    parts = content.strip().split()
    
    if len(parts) < 2:
        return {
            "content": "格式错误，如需查询奇遇记录请输入：\n奇遇 角色id [区服]"
        }
    name = parts[1]
    server = parts[2] if len(parts) >= 3 else DEFAULT_SERVER
    
    data = await get_luck_records(server=server, name=name)
    if not data:
        return { "content": "查询失败，可能是区服或角色名错误，或接口超时，请稍后重试。", "file_image": None }

    image = await generate_luck_card(data)
    return {
        "content": f"奇遇记录：{name}@{server}",
        "file_image": image
    }