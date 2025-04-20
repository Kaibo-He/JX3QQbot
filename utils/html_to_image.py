from playwright.async_api import async_playwright

# HTML 渲染为图片
async def render_html_to_image(html: str, output_path: str):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 960, "height": 1800})
        await page.set_content(html, wait_until="networkidle")
        await page.screenshot(path=output_path, full_page=True)
        await browser.close()

# HTML 渲染为图片（高度自适应）
async def render_html_to_adapted_image(html: str, output_path: str, min_height: int = 1800):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 960, "height": min_height})
        await page.set_content(html, wait_until="networkidle")

        # 通过 JS 获取内容实际高度
        content_height = await page.evaluate("document.documentElement.scrollHeight")
        final_height = max(min_height, content_height)

        # 调整页面高度再截图
        await page.set_viewport_size({"width": 960, "height": final_height})
        await page.screenshot(path=output_path)
        await browser.close()