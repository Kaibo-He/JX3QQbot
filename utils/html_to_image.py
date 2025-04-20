from playwright.async_api import async_playwright
import os
from pathlib import Path
import tempfile
import base64

# HTML 渲染为图片（支持本地图片加载）
async def render_html_to_image(html: str, output_path: str):
    # 写入 HTML 到临时目录
    with tempfile.TemporaryDirectory() as tmpdir:
        html_path = os.path.join(tmpdir, "temp.html")
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html)

        async with async_playwright() as p:
            browser = await p.chromium.launch(args=["--no-sandbox"])
            page = await browser.new_page(viewport={"width": 960, "height": 1800})
            
            file_url = f"file://{html_path}"
            await page.goto(file_url, wait_until="networkidle")

            await page.screenshot(path=output_path, full_page=True)
            await browser.close()

# HTML 渲染为图片（高度自适应）
async def render_html_to_adapted_image(
    html: str,
    output_path: str,
    min_height: int = 1800,
    to_base64: bool = False,
    quality: int = 80
):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 960, "height": min_height})

        # 将 HTML 写入临时文件
        html_path = "/tmp/temp_render.html"
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html)
        await page.goto(f"file://{html_path}", wait_until="networkidle")

        # 获取页面实际高度
        content_height = await page.evaluate("document.documentElement.scrollHeight")
        final_height = max(min_height, content_height)
        await page.set_viewport_size({"width": 960, "height": final_height})

        # 保存为 JPG
        await page.screenshot(path=output_path, type="jpeg", quality=quality)
        await browser.close()

    # 返回 base64 字符串
    if to_base64:
        with open(output_path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode()
        return f"data:image/jpeg;base64,{encoded}"

    # 默认返回文件路径
    return output_path