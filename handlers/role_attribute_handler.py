from jinja2 import Environment, FileSystemLoader
from pathlib import Path
import os
import hashlib
import time
from jx3api import get_role_attribute
from handlers.html_to_image import render_html_to_image
from utils.image_base64_cache import url_to_base64_cached

TEMPLATE_DIR = "templates"
CACHE_DIR = "/tmp/equip_cache"
os.makedirs(CACHE_DIR, exist_ok=True)
CACHE_DURATION = 60  # 缓存60秒

def embed_equip_icons(equip_list):
    for equip in equip_list:
        # 装备图标
        if "icon" in equip:
            equip["icon"] = url_to_base64_cached(equip["icon"])

        # 大附魔图标
        if "commonEnchant" in equip and "icon" in equip["commonEnchant"]:
            equip["commonEnchant"]["icon"] = url_to_base64_cached(equip["commonEnchant"]["icon"])

        # 五行石图标
        if "fiveStone" in equip:
            for stone in equip["fiveStone"]:
                if "icon" in stone:
                    stone["icon"] = url_to_base64_cached(stone["icon"])
                    
# 接收角色数据，生成卡片图
async def _generate_role_equip_card(data: dict) -> bytes:
    # 缓存 key
    cache_key = hashlib.md5((data.get("roleName", "") + data.get("serverName", "")).encode()).hexdigest()
    cache_path = os.path.join(CACHE_DIR, f"{cache_key}.png")
    # 缓存命中且未过期
    if os.path.exists(cache_path) and (time.time() - os.path.getmtime(cache_path) < CACHE_DURATION):
        img = Path(cache_path).read_bytes()
        os.remove(cache_path)
        return img
    
    # 渲染
    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
    template = env.get_template("equip_card.html")
    
    equip_list = data.get("equipList", [])
    embed_equip_icons(equip_list)
    context = {
        "role_name": data.get("roleName", "未知角色"),
        "kungfu_name": data.get("kungfuName", "未知心法"),
        "force_name": data.get("forceName", "未知门派"),
        "zone_name": data.get("zoneName", "未知区服"),
        "server_name": data.get("serverName", "未知区服"),
        "score": data.get("panelList", {}).get("score", 0),
        "equipList": equip_list,
        "panelList": data.get("panelList", {"panel": []})
    }

    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
    template = env.get_template("equip_card.html")
    html = template.render(context)
    
    # 生成并保存
    await render_html_to_image(html, cache_path)
    img = Path(cache_path).read_bytes()
    os.remove(cache_path)
    return img

async def handle_role_attribute_card(content: str):
    parts = content.strip().split()
    server = "梦江南"
    name = ""

    if len(parts) >= 3:
        server = parts[1]
        name = parts[2]
    elif len(parts) == 2:
        name = parts[1]

    data = get_role_attribute(server=server, name=name)
    if not data:
        return { "content": "⚠️ 无法获取角色属性信息", "file_image": None }

    image = await _generate_role_equip_card(data)
    return {
        "content": f"{data['roleName']} 的装备详情如下：",
        "file_image": image
    }