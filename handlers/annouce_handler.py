from jx3api import get_news_announce, get_maintenance_announce, get_skill_announce
from handlers.html_to_image import render_element_to_image
from pathlib import Path
import hashlib
import os
import time

CACHE_DIR = "/tmp/announce_cache"
os.makedirs(CACHE_DIR, exist_ok=True)
CACHE_DURATION = 60  # 缓存60秒
CLASS_NAME = "index-mainContainer-1IdO6"

async def _generate_announcement_image(url: str) -> bytes:
    cache_key = hashlib.md5(url.encode()).hexdigest()
    cache_path = os.path.join(CACHE_DIR, f"{cache_key}.png")

    if os.path.exists(cache_path) and (time.time() - os.path.getmtime(cache_path) < CACHE_DURATION):
        img = Path(cache_path).read_bytes()
        os.remove(cache_path)
        return img

    # 渲染
    await render_element_to_image(url, CLASS_NAME, cache_path)

    img = Path(cache_path).read_bytes()
    os.remove(cache_path)
    return img

async def handle_news_announce() -> dict:
    url = get_news_announce()
    if not url:
        return {"content": "⚠️ 获取公告失败", "file_image": None}
    img = await _generate_announcement_image(url)
    return {"content": "📢 最新公告：", "file_image": img}

async def handle_maintenance_announce() -> dict:
    url = get_maintenance_announce()
    if not url:
        return {"content": "⚠️ 获取维护信息失败", "file_image": None}
    img = await _generate_announcement_image(url)
    return {"content": "🔧 维护公告：", "file_image": img}

async def handle_skill_announce() -> dict:
    url = get_skill_announce()
    if not url:
        return {"content": "⚠️ 获取技改信息失败", "file_image": None}
    img = await _generate_announcement_image(url)
    return {"content": "📖 技改说明：", "file_image": img}