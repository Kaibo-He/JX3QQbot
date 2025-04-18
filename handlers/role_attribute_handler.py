import asyncio
from jinja2 import Environment, FileSystemLoader
from pathlib import Path
from playwright.async_api import async_playwright
import datetime
import os
from jx3api import get_role_attribute

TEMPLATE_DIR = "templates"
OUTPUT_PATH = "/tmp/equip_card.png"

# HTML 渲染为图片
async def render_html_to_image(html: str, output_path: str):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 960, "height": 1800})
        await page.set_content(html, wait_until="networkidle")
        await page.screenshot(path=output_path, full_page=True)
        await browser.close()

# 接收角色数据，生成卡片图
def generate_role_equip_card(data: dict) -> bytes:
    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
    template = env.get_template("equip_card.html")

    context = {
        "role_name": data.get("roleName", "未知角色"),
        "avatar_url": data.get("personAvatar", ""), 
        "kungfu_name": data.get("kungfuName", "未知心法"),
        "force_name": data.get("forceName", "未知门派"),
        "zone_name": data.get("zoneName", "未知区服"),
        "server_name": data.get("serverName", "未知区服"),
        "score": data.get("panelList", {}).get("score", 0),
        "equipList": data.get("equipList", []),
        "panelList": data.get("panelList", {"panel": []})
    }

    html = template.render(context)
    asyncio.run(render_html_to_image(html, OUTPUT_PATH))
    image_bytes = Path(OUTPUT_PATH).read_bytes()
    os.remove(OUTPUT_PATH)  # 自动删除临时文件
    return image_bytes

def handle_role_attribute_card(content: str):
    parts = content.strip().split()
    server = "梦江南"
    name = ""

    if len(parts) >= 3:
        server = parts[1]
        name = parts[2]
    elif len(parts) == 2:
        name = parts[1]

    data = get_role_attribute(server=server, name=name)
    if not data:
        return { "content": "⚠️ 无法获取角色属性信息", "file_image": None }

    image = generate_role_equip_card(data)
    return {
        "content": f"{data['roleName']} 的装备详情卡片如下：",
        "file_image": image
    }