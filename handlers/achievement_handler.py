# handlers/achievement_handler.py
from jinja2 import Environment, FileSystemLoader
from pathlib import Path
import os
import hashlib
import time

from config import DEFAULT_SERVER
from api.jx3api import get_role_achievement
from utils.html_to_image import render_html_to_image

TEMPLATE_DIR = "templates"
OUTPUT_PATH_1 = "/tmp/achievement_total.png"
OUTPUT_PATH_2 = "/tmp/achievement_map.png"
OUTPUT_PATH_1 = "/tmp/achievement_dungeon.png"
CACHE_DIR = "/tmp/achievement_cache"
os.makedirs(CACHE_DIR, exist_ok=True)
CACHE_DURATION = 60  # 缓存60秒

async def generate_achievement_total_card(data: dict) -> bytes:
    # 缓存 key
    cache_key = hashlib.md5((data.get("role_name", "") + data.get("server_name", "")) + "total".encode()).hexdigest()
    cache_path = os.path.join(CACHE_DIR, f"{cache_key}.png")
    # 缓存命中且未过期
    if os.path.exists(cache_path) and (time.time() - os.path.getmtime(cache_path) < CACHE_DURATION):
        return Path(cache_path).read_bytes()
    
    # 渲染
    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
    template = env.get_template("achievement_total.html")
    
    type_list = {}
    for item in data["data"]["total"]:
        item_info = {}
        seniority_speed = 0
        seniority_total = 0
        pieces_speed = 0
        pieces_total = 0
        for sub in data["data"]["total"][item]:
            seniority_speed += data["data"]["total"][item][sub]["seniority"]["speed"]
            seniority_total += data["data"]["total"][item][sub]["seniority"]["total"]
            pieces_speed += data["data"]["total"][item][sub]["pieces"]["speed"]
            pieces_total += data["data"]["total"][item][sub]["pieces"]["total"]
    
        item_info["seniority_speed"] = seniority_speed
        item_info["seniority_total"] = seniority_total
        item_info["pieces_speed"] = pieces_speed
        item_info["pieces_total"] = pieces_total
        item_info["percent"] = round(pieces_speed / pieces_total * 100, 2)
        type_list[item] = item_info

    context = {
        "role_name": data["roleName"],
        "server_name": f"{data['zoneName']}@{data['serverName']}",
        "total_speed": data["data"]["score"],
        "total_total": data["data"]["totalScore"],
        "total_percent": round(data['data']['score'] / data['data']['totalScore'] * 100, 2),
        "type_list": type_list
    }

    html = template.render(context)
    await render_html_to_image(html, cache_path)
    
    return Path(cache_path).read_bytes()

async def generate_achievement_map_card(data: dict) -> bytes:
    # 缓存 key
    cache_key = hashlib.md5((data.get("role_name", "") + data.get("server_name", "")) + "map".encode()).hexdigest()
    cache_path = os.path.join(CACHE_DIR, f"{cache_key}.png")
    # 缓存命中且未过期
    if os.path.exists(cache_path) and (time.time() - os.path.getmtime(cache_path) < CACHE_DURATION):
        return Path(cache_path).read_bytes()
    
    # 渲染
    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
    template = env.get_template("achievement_map.html")
    
    type_list = {}
    for item in data["data"]["maps"]:
        item_info = {}
        seniority_speed = data["data"]["maps"][item]["seniority"]["speed"]
        seniority_total = data["data"]["maps"][item]["seniority"]["total"]
        pieces_speed = data["data"]["maps"][item]["pieces"]["speed"]
        pieces_total = data["data"]["maps"][item]["pieces"]["total"]
    
        item_info["seniority_speed"] = seniority_speed
        item_info["seniority_total"] = seniority_total
        item_info["pieces_speed"] = pieces_speed
        item_info["pieces_total"] = pieces_total
        item_info["percent"] = round(pieces_speed / pieces_total * 100, 2)
        type_list[item] = item_info

    context = {
        "role_name": data["roleName"],
        "server_name": f"{data['zoneName']}@{data['serverName']}",
        "total_speed": data["data"]["score"],
        "total_total": data["data"]["totalScore"],
        "total_percent": round(data['data']['score'] / data['data']['totalScore'] * 100, 2),
        "type_list": type_list
    }

    html = template.render(context)
    await render_html_to_image(html, cache_path)
    
    return Path(cache_path).read_bytes()

async def generate_achievement_dungeons_card(data: dict) -> bytes:
    # 缓存 key
    cache_key = hashlib.md5((data.get("role_name", "") + data.get("server_name", "")) + "dungeons".encode()).hexdigest()
    cache_path = os.path.join(CACHE_DIR, f"{cache_key}.png")
    # 缓存命中且未过期
    if os.path.exists(cache_path) and (time.time() - os.path.getmtime(cache_path) < CACHE_DURATION):
        return Path(cache_path).read_bytes()
    
    # 渲染
    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
    template = env.get_template("achievement_dungeons.html")
    
    context = {
        "role_name": data["roleName"],
        "server_name": f"{data['zoneName']}@{data['serverName']}",
        "total_speed": data["data"]["score"],
        "total_total": data["data"]["totalScore"],
        "total_percent": round(data['data']['score'] / data['data']['totalScore'] * 100, 2),
        "type_list": data["data"]["dungeons"]
    }

    html = template.render(context)
    await render_html_to_image(html, cache_path)
    
    return Path(cache_path).read_bytes()

async def handle_role_attribute_card(content: str):
    parts = content.strip().split()
    
    if len(parts) < 2:
        return {
            "content": "格式错误，如需查询资历分布请输入：\n资历/资历分布 角色id [区服]"
        }
        
    if len(parts) >= 3:
        server = parts[2]
    name = parts[1]
    server = parts[2] if len(parts) >= 3 else DEFAULT_SERVER

    data = get_role_achievement(server=server, name=name)
    if not data:
        return { "content": "查询失败，可能是区服或角色名错误，或接口超时，请稍后重试。", "file_image": None }

    image1 = await generate_achievement_total_card(data)
    image2 = await generate_achievement_map_card(data)
    image3 = await generate_achievement_dungeons_card(data)
    return [
        {"content": "资历总览", "file_image": image1},
        {"content": "地图总览", "file_image": image2},
        {"content": "秘境总览", "file_image": image3},
    ]