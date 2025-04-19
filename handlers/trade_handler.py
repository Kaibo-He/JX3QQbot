from jinja2 import Environment, FileSystemLoader
from pathlib import Path
import os
import hashlib
import time
from jx3api import get_trade_data
from handlers.html_to_image import render_html_to_image

TEMPLATE_DIR = "templates"
OUTPUT_PATH = "/tmp/trade_card.png"
CACHE_DIR = "/tmp/trade_cache"
os.makedirs(CACHE_DIR, exist_ok=True)
CACHE_DURATION = 60  # 缓存60秒

# 接收角色数据，生成图片
async def generate_trade_card(data: dict) -> bytes:
    # 缓存 key
    cache_key = hashlib.md5((data.get("roleName", "") + data.get("serverName", "")).encode()).hexdigest()
    cache_path = os.path.join(CACHE_DIR, f"{cache_key}.png")
    # 缓存命中且未过期
    if os.path.exists(cache_path) and (time.time() - os.path.getmtime(cache_path) < CACHE_DURATION):
        return Path(cache_path).read_bytes()
    
    # 渲染
    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
    template = env.get_template("trade_card.html")

    context = {
        "server_name": "梦江南",
        "item_name": data["name"],
        "item_class": data["class"],
        "item_subclass": data["subclass"],
        "item_date": data["date"],
        "item_view": data["view"],
        "trade_list": data["data"]
        }

    html = template.render(context)
    
    # 生成并保存
    await render_html_to_image(html, cache_path)
    img = Path(cache_path).read_bytes()
    os.remove(cache_path)
    return img

async def handle_trade_card(content: str):
    parts = content.strip().split()
    
    if len(parts) < 2:
        return {
            "content": "请输入外观名称。"
        }
        
    server = "梦江南"
    name = parts[1]
    if len(parts) >= 3:
        server = parts[2]

    data = get_trade_data(server=server, name=name)
    if not data:
        return { "content": "查询失败，可能是外观名称无法匹配，或接口超时，请稍后重试。", "file_image": None }

    image = await generate_trade_card(data)
    return {
        "content": f"{data['name']} 物价详情如下：",
        "file_image": image
    }