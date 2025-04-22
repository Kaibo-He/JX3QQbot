from playwright.async_api import async_playwright
import os
from pathlib import Path
import tempfile
import base64

_browser = None
_context = None

async def init_browser(width=960, height=1800):
    """全局初始化浏览器"""
    global _browser, _context
    if _browser is None:
        p = await async_playwright().start()
        _browser = await p.chromium.launch(args=["--no-sandbox"])
        _context = await _browser.new_context(viewport={"width": width, "height": height})

async def shutdown_browser():
    """关闭浏览器"""
    global _browser, _context
    if _browser:
        await _context.close()
        await _browser.close()
        _browser = None
        _context = None

# HTML 渲染为图片
async def render_html_to_image(html: str, output_path: str):
    """将 HTML 渲染为图片 """
    await init_browser()
    global _context

    with tempfile.TemporaryDirectory() as tmpdir:
        html_path = os.path.join(tmpdir, "temp.html")
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html)

        page = await _context.new_page()
        file_url = f"file://{html_path}"
        await page.goto(file_url, wait_until="load")
        await page.wait_for_function("window.ready === true", timeout=60000)
        await page.screenshot(path=output_path, full_page=True)
        await page.close()

# HTML 渲染为图片（高度自适应）
async def render_html_to_adapted_image(
    html: str,
    output_path: str,
    min_height: int = 1800,
    width: int = 960,
    to_base64: bool = False,
    quality: int = 80,
    max_size_kb: int = 2048  # 限制最大文件大小（单位 KB）
):
    await init_browser()
    await init_browser(width=width)
    global _context

    with tempfile.TemporaryDirectory() as tmpdir:
        html_path = os.path.join(tmpdir, "temp.html")
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html)

        page = await _context.new_page()
        file_url = f"file://{html_path}"
        await page.goto(file_url, wait_until="networkidle")

        content_height = await page.evaluate("document.documentElement.scrollHeight")
        final_height = max(min_height, content_height)
        await page.set_viewport_size({"width": width, "height": final_height})

        # 先截图为 PNG（无损）
        temp_png_path = os.path.join(tmpdir, "initial.png")
        await page.screenshot(path=temp_png_path, full_page=False)
        await page.close()

        file_size_kb = os.path.getsize(temp_png_path) // 1024

        # 判断是否压缩
        if file_size_kb > max_size_kb:
            # 压缩为 JPEG
            from PIL import Image
            im = Image.open(temp_png_path).convert("RGB")
            im.save(output_path, format="JPEG", quality=quality)
        else:
            # 直接复制为最终图像
            with open(temp_png_path, "rb") as src, open(output_path, "wb") as dst:
                dst.write(src.read())

    if to_base64:
        with open(output_path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode()
        return f"data:image/jpeg;base64,{encoded}"

    return output_path