from playwright.async_api import async_playwright

# HTML 渲染为图片
async def render_html_to_image(html: str, output_path: str):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 960, "height": 1800})
        await page.set_content(html, wait_until="networkidle")
        await page.screenshot(path=output_path, full_page=True)
        await browser.close()
        
# HTML 中 element 渲染为图片
async def render_element_to_image(url: str, class_name: str, output_path: str):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(url, wait_until="networkidle")

        # 等待该 class 出现
        await page.wait_for_selector(f".{class_name}")

        # 获取该元素并截图
        element = await page.query_selector(f".{class_name}")
        if element:
            await element.screenshot(path=output_path)
        else:
            print("未找到指定的元素。")
            
        await browser.close()
