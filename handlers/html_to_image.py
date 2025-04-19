from playwright.async_api import async_playwright

# HTML 渲染为图片
async def render_html_to_image(html: str, output_path: str, image_type: str = "png", quality: int = 100):
    async with async_playwright() as p:
        browser = await p.chromium.launch(args=["--no-sandbox"])
        page = await browser.new_page(viewport={"width": 960, "height": 1800})
        await page.set_content(html, wait_until="domcontentloaded")
        await page.wait_for_load_state("domcontentloaded")
        await page.wait_for_timeout(300)
        await page.screenshot(
            path=output_path,
            full_page=True,
            type=image_type,
            quality=quality if image_type == "jpeg" else None
        )
        await browser.close()