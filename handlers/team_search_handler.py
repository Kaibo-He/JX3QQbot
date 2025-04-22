# handlers/team_search_handler.py
from jinja2 import Environment, FileSystemLoader
from pathlib import Path
import os
import hashlib
import time
from datetime import datetime

from config import DEFAULT_SERVER
from api.jx3api import get_team_records
from utils.html_to_image import render_html_to_adapted_image

TEMPLATE_DIR = "templates"
OUTPUT_PATH = "/tmp/team_card.png"
CACHE_DIR = "/tmp/team_cache"
os.makedirs(CACHE_DIR, exist_ok=True)
CACHE_DURATION = 180

# 接收角色数据，生成图片
async def generate_team_card(data: dict, keyword: str) -> bytes:
    # 缓存 key
    cache_key = hashlib.md5((keyword + data["server"]).encode()).hexdigest()
    cache_path = os.path.join(CACHE_DIR, f"{cache_key}.png")
    # 缓存命中且未过期
    if os.path.exists(cache_path) and (time.time() - os.path.getmtime(cache_path) < CACHE_DURATION):
        return Path(cache_path).read_bytes()
    
    # 渲染
    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
    template = env.get_template("team_card.html")

    def format_time(ts):
        if ts == 0:
            return "-"
        return datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")
    for item in data["data"]:
        item["time"] = format_time(item["createTime"])
    context = {
        "item_list": data["data"][:25],
        "server_name": data["server"]
    }

    html = template.render(context)
    await render_html_to_adapted_image(html, cache_path, width=1500)
    
    return Path(cache_path).read_bytes()

async def handle_team_search(content: str):
    parts = content.strip().split()
    
    if len(parts) < 2:
        return {
            "content": "格式错误，如需查询团队招募请输入：\n招募/团队招募 关键词 [区服]"
        }
    keyword = parts[1]
    server = parts[2] if len(parts) >= 3 else DEFAULT_SERVER
    
    data = await get_team_records(server=server, keyword=keyword)
    if not data:
        return { "content": "查询失败，可能是区服名错误，或接口超时，请稍后重试。", "file_image": None }

    image = await generate_team_card(data, keyword)
    return {
        "content": "搜索团队招募：",
        "file_image": image
    }