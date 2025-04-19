from jx3api import get_news_announce, get_maintenance_announce, get_skill_announce
from playwright.async_api import async_playwright
from jinja2 import Environment, FileSystemLoader
from pathlib import Path
import os
from html_to_image import render_html_to_image

TEMPLATE_DIR = "templates"
CACHE_DIR = "/tmp/announce_cache"
os.makedirs(CACHE_DIR, exist_ok=True)
CACHE_DURATION = 60

# 抓取网页元素文字
async def extract_text_from_element(url: str, class_name: str) -> str:
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        browser = await p.chromium.launch(args=["--no-sandbox"])
        page = await browser.new_page()
        await page.goto(url, wait_until="networkidle")
        await page.wait_for_selector(f".{class_name}", timeout=10000)
        element = await page.query_selector(f".{class_name}")
        text = await element.inner_text()
        await browser.close()
        return text.strip()
    
# 渲染公告图片
async def render_announcement_image(title: str, content: str, output_path: str) -> None:
    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
    template = env.get_template("announce_card.html")
    html = template.render(title=title, content=content)
    await render_html_to_image(html, output_path)


async def handle_news_announce() -> dict:
    url = get_news_announce()
    if not url:
        return {"content": "⚠️ 获取公告失败", "file_image": None}
    
    text = await extract_text_from_element(url, "index-mainContainer-1IdO6")

    cache_key = hashlib.md5(text.encode()).hexdigest()
    cache_path = os.path.join(CACHE_DIR, f"{cache_key}.png")

    if os.path.exists(cache_path) and time.time() - os.path.getmtime(cache_path) < CACHE_DURATION:
        img = Path(cache_path).read_bytes()
        os.remove(cache_path)
        return {"content": "📢 最新公告如下：", "file_image": img}

    await render_announcement_image("📢 最新公告", text, cache_path)
    img = Path(cache_path).read_bytes()
    os.remove(cache_path)

    return {"content": "📢 最新公告如下：", "file_image": img}

async def handle_maintenance_announce() -> dict:
    url = get_maintenance_announce()
    if not url:
        return {"content": "⚠️ 获取维护信息失败", "file_image": None}
    text = await extract_text_from_element(url, "index-mainContainer-1IdO6")

    cache_key = hashlib.md5(text.encode()).hexdigest()
    cache_path = os.path.join(CACHE_DIR, f"{cache_key}.png")

    if os.path.exists(cache_path) and time.time() - os.path.getmtime(cache_path) < CACHE_DURATION:
        img = Path(cache_path).read_bytes()
        os.remove(cache_path)
        return {"content": "🔧 维护公告如下：", "file_image": img}

    await render_announcement_image("🔧 维护公告", text, cache_path)
    img = Path(cache_path).read_bytes()
    os.remove(cache_path)

    return {"content": "🔧 维护公告如下：", "file_image": img}

async def handle_skill_announce() -> dict:
    url = get_skill_announce()
    if not url:
        return {"content": "⚠️ 获取技改信息失败", "file_image": None}
    text = await extract_text_from_element(url, "index-mainContainer-1IdO6")

    cache_key = hashlib.md5(text.encode()).hexdigest()
    cache_path = os.path.join(CACHE_DIR, f"{cache_key}.png")

    if os.path.exists(cache_path) and time.time() - os.path.getmtime(cache_path) < CACHE_DURATION:
        img = Path(cache_path).read_bytes()
        os.remove(cache_path)
        return {"content": "📖 技改说明如下：", "file_image": img}

    await render_announcement_image("📖 技改说明", text, cache_path)
    img = Path(cache_path).read_bytes()
    os.remove(cache_path)

    return {"content": "📖 技改说明如下：", "file_image": img}