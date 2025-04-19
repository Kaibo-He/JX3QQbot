from jx3api import get_news_announce, get_maintenance_announce, get_skill_announce
from playwright.async_api import async_playwright

CLASS_NAME = "index-mainContainer-1IdO6"

async def _extract_text_from_element(url: str, class_name: str) -> str:
    async with async_playwright() as p:
        browser = await p.chromium.launch(args=["--no-sandbox"])
        page = await browser.new_page()
        await page.goto(url, wait_until="networkidle")
        await page.wait_for_timeout(2000)  # Vue 页面要等一下

        await page.wait_for_selector(f".{class_name}", timeout=10000)
        element = await page.query_selector(f".{class_name}")
        if not element:
            return "⚠️ 无法找到公告内容元素"

        text = await element.inner_text()
        await browser.close()
        return text.strip() or "⚠️ 公告内容为空"

async def handle_news_announce() -> dict:
    url = get_news_announce()
    if not url:
        return {"content": "⚠️ 获取公告失败", "file_image": None}
    text = await _extract_text_from_element(url, CLASS_NAME)
    return {"content": f"📢 最新公告：\n\n{text}"}

async def handle_maintenance_announce() -> dict:
    url = get_maintenance_announce()
    if not url:
        return {"content": "⚠️ 获取维护信息失败", "file_image": None}
    text = await _extract_text_from_element(url, CLASS_NAME)
    return {"content": f"🔧 维护公告：\n\n{text}"}

async def handle_skill_announce() -> dict:
    url = get_skill_announce()
    if not url:
        return {"content": "⚠️ 获取技改信息失败", "file_image": None}
    text = await _extract_text_from_element(url, CLASS_NAME)
    return {"content": f"📖 技改说明：\n\n{text}"}