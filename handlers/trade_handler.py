# handlers/trade_handler.py
from jinja2 import Environment, FileSystemLoader
from pathlib import Path
import os
import hashlib
import time

from config import DEFAULT_SERVER
from api.jx3api import get_trade_data
from utils.html_to_image import render_html_to_image

TEMPLATE_DIR = "templates"
OUTPUT_PATH = "/tmp/trade_card.png"
CACHE_DIR = "/tmp/trade_cache"
os.makedirs(CACHE_DIR, exist_ok=True)
CACHE_DURATION = 60  # 缓存60秒

# 接收角色数据，生成图片
async def generate_trade_card(data: dict) -> bytes:
    # 缓存 key
    cache_key = hashlib.md5((data.get("name", "") + data.get("alias", "")).encode()).hexdigest()
    cache_path = os.path.join(CACHE_DIR, f"{cache_key}.png")
    # 缓存命中且未过期
    if os.path.exists(cache_path) and (time.time() - os.path.getmtime(cache_path) < CACHE_DURATION):
        return Path(cache_path).read_bytes()
    
    # 渲染
    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
    template = env.get_template("trade_card.html")

    context = {
        "server_name": data["data"][5][0]["server"],
        "item_name": data["name"],
        "item_alias": data["alias"],
        "item_class": data["class"],
        "item_subclass": data["subclass"],
        "item_date": data["date"],
        "item_view": data["view"],
        "trade_list": data["data"]
        }

    html = template.render(context)
    await render_html_to_image(html, cache_path)
    
    return Path(cache_path).read_bytes()

async def handle_trade_card(content: str):
    parts = content.strip().split()
    
    if len(parts) < 2:
        return {
            "content": "格式错误，如需查询外观物价请输入：\n物价/外观 外观名称 [区服]"
        }
    name = parts[1]
    server = parts[2] if len(parts) >= 3 else DEFAULT_SERVER
    
    data = get_trade_data(server=server, name=name)
    if not data:
        return { "content": "查询失败，可能是外观名称无法匹配，或接口超时，请稍后重试。", "file_image": None }

    image = await generate_trade_card(data)
    return {
        "content": f"{data['name']} 物价详情如下：",
        "file_image": image
    }