# handlers/role_attribute_handler.py
from jinja2 import Environment, FileSystemLoader
from pathlib import Path
import os
import hashlib
import time

from config import DEFAULT_SERVER, KUNGFU_ICON_MAP
from api.jx3api import get_role_attribute
from utils.html_to_image import render_html_to_image

TEMPLATE_DIR = "templates"
OUTPUT_PATH = "/tmp/equip_card.png"
CACHE_DIR = "/tmp/equip_cache"
os.makedirs(CACHE_DIR, exist_ok=True)
CACHE_DURATION = 180

# 接收角色数据，生成图片
async def generate_role_equip_card(data: dict) -> bytes:
    # 缓存 key
    cache_key = hashlib.md5((data.get("roleName", "") + data.get("serverName", "")).encode()).hexdigest()
    cache_path = os.path.join(CACHE_DIR, f"{cache_key}.png")
    # 缓存命中且未过期
    if os.path.exists(cache_path) and (time.time() - os.path.getmtime(cache_path) < CACHE_DURATION):
        return Path(cache_path).read_bytes()
    
    # 渲染
    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
    template = env.get_template("equip_card.html")
    
    def normalize_kungfu_name(name: str) -> str:
        return name.split("·")[0].strip()
    
    kungfu_name_raw = data.get("kungfuName", "未知心法")
    kungfu_name = normalize_kungfu_name(kungfu_name_raw)
    kungfu_icon_url = KUNGFU_ICON_MAP.get(kungfu_name)

    context = {
        "role_name": data.get("roleName", "未知角色"),
        "kungfu_name": kungfu_name_raw,
        "kungfu_icon": kungfu_icon_url,
        "force_name": data.get("forceName", "未知门派"),
        "zone_name": data.get("zoneName", "未知区服"),
        "server_name": data.get("serverName", "未知区服"),
        "score": data.get("panelList", {}).get("score", 0),
        "equipList": data.get("equipList", []),
        "panelList": data.get("panelList", {"panel": []})
    }

    html = template.render(context)
    await render_html_to_image(html, cache_path)
    
    return Path(cache_path).read_bytes()

async def handle_role_attribute_card(content: str):
    parts = content.strip().split()
    
    if len(parts) < 2:
        return {
            "content": "格式错误，如需查询角色装备请输入：\n装备/属性 角色id [区服]"
        }
        
    if len(parts) >= 3:
        server = parts[2]
    name = parts[1]
    server = parts[2] if len(parts) >= 3 else DEFAULT_SERVER

    data = await get_role_attribute(server=server, name=name)
    if not data:
        return { "content": "查询失败，可能是区服或角色名错误，或接口超时，请稍后重试。", "file_image": None }

    image = await generate_role_equip_card(data)
    return {
        "content": f"{data['roleName']} 的装备详情如下：",
        "file_image": image
    }