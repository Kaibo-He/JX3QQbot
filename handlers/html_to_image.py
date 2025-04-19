from playwright.async_api import async_playwright

# HTML 渲染为图片
async def render_html_to_image(html: str, output_path: str):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 960, "height": 1800})
        await page.set_content(html, wait_until="networkidle")
        await page.screenshot(path=output_path, full_page=True)
        await browser.close()
