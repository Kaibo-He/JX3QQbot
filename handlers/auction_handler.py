from jinja2 import Environment, FileSystemLoader
from pathlib import Path
import os
import hashlib
import time
import datetime
from handlers.html_to_image import render_html_to_image
from jx3boxapi import get_item_info, get_item_auction

TEMPLATE_DIR = "templates"
OUTPUT_PATH = "/tmp/auction_card.png"
CACHE_DIR = "/tmp/auction_cache"
os.makedirs(CACHE_DIR, exist_ok=True)
CACHE_DURATION = 60  # 缓存60秒

# 根据物品数据，生成图片
async def generate_auction_card(server: str, keyword: str) -> bytes:
    # 缓存 key
    cache_key = hashlib.md5((keyword + server).encode()).hexdigest()
    cache_path = os.path.join(CACHE_DIR, f"{cache_key}.png")
    # 缓存命中且未过期
    if os.path.exists(cache_path) and (time.time() - os.path.getmtime(cache_path) < CACHE_DURATION):
        img = Path(cache_path).read_bytes()
        os.remove(cache_path)
        return img
    
    # 渲染
    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
    template = env.get_template("auction_card.html")

    item_list = get_item_info(keyword)
    
    if not item_list:
        print("❌ 未获取到物品列表，请检查关键词或 API 是否正常返回。")
        return
    
    filtered_item_list = []
    # 获取物品icon,名称染色,交易行信息
    for item in item_list:
        auction_list = get_item_auction(server, item["id"])
        
        if not auction_list:
            continue
        
        max_price = max(auction_list, key=lambda x: x["price"])["price"]
        min_price = min(auction_list, key=lambda x: x["price"])["price"]
        new_price_item = max(auction_list, key=lambda x: x["timestamp"])
        new_price = new_price_item["price"]
        new_price_time = datetime.datetime.fromtimestamp(new_price_item["timestamp"]).strftime("%Y-%m-%d")
        
        item_data = {
            "name": item["Name"],
            "id": item["id"],
            "icon": f"https://icon.jx3box.com/icon/{item['IconID']}.png",
            "color": f"item-{item['Quality']}",
            "high": price_to_gold(max_price),
            "low": price_to_gold(min_price),
            "new": price_to_gold(new_price),
            "time": new_price_time
        }
        filtered_item_list.append(item_data)
        
        if len(filtered_item_list) >= 15:
            break
        
    context = {
        "server_name": server,
        "item_list": filtered_item_list
        }

    html = template.render(context)
    
    # 生成并保存
    await render_html_to_image(html, cache_path)
    img = Path(cache_path).read_bytes()
    os.remove(cache_path)
    return img

async def handle_auction_card(content: str):
    parts = content.strip().split()
    
    if len(parts) < 2:
        return {
            "content": "请输入物品名称。",
            "file_image": None
        }
        
    server = "梦江南"
    keyword = parts[1]
    if len(parts) >= 3:
        server = parts[2]
    
    print(f"📦 搜索关键词: {keyword}")

    image = await generate_auction_card(server, keyword)
    return {
        "content": f"交易行检索：{keyword}",
        "file_image": image
    }
        
def price_to_gold(price: float) -> dict:
    zhuan_img = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABkAAAASCAYAAACuLnWgAAAACXBIWXMAAAsTAAALEwEAmpwYAAAGymlUWHRYTUw6Y29tLmFkb2JlLnhtcAAAAAAAPD94cGFja2V0IGJlZ2luPSLvu78iIGlkPSJXNU0wTXBDZWhpSHpyZVN6TlRjemtjOWQiPz4gPHg6eG1wbWV0YSB4bWxuczp4PSJhZG9iZTpuczptZXRhLyIgeDp4bXB0az0iQWRvYmUgWE1QIENvcmUgNS42LWMxNDIgNzkuMTYwOTI0LCAyMDE3LzA3LzEzLTAxOjA2OjM5ICAgICAgICAiPiA8cmRmOlJERiB4bWxuczpyZGY9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkvMDIvMjItcmRmLXN5bnRheC1ucyMiPiA8cmRmOkRlc2NyaXB0aW9uIHJkZjphYm91dD0iIiB4bWxuczp4bXA9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC8iIHhtbG5zOmRjPSJodHRwOi8vcHVybC5vcmcvZGMvZWxlbWVudHMvMS4xLyIgeG1sbnM6cGhvdG9zaG9wPSJodHRwOi8vbnMuYWRvYmUuY29tL3Bob3Rvc2hvcC8xLjAvIiB4bWxuczp4bXBNTT0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL21tLyIgeG1sbnM6c3RFdnQ9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9zVHlwZS9SZXNvdXJjZUV2ZW50IyIgeG1wOkNyZWF0b3JUb29sPSJBZG9iZSBQaG90b3Nob3AgQ0MgMjAxOCAoV2luZG93cykiIHhtcDpDcmVhdGVEYXRlPSIyMDIxLTA2LTI3VDExOjI0OjU0KzA4OjAwIiB4bXA6TW9kaWZ5RGF0ZT0iMjAyMS0wNy0wN1QwNjoxMjo1MyswODowMCIgeG1wOk1ldGFkYXRhRGF0ZT0iMjAyMS0wNy0wN1QwNjoxMjo1MyswODowMCIgZGM6Zm9ybWF0PSJpbWFnZS9wbmciIHBob3Rvc2hvcDpDb2xvck1vZGU9IjMiIHBob3Rvc2hvcDpJQ0NQcm9maWxlPSJzUkdCIElFQzYxOTY2LTIuMSIgeG1wTU06SW5zdGFuY2VJRD0ieG1wLmlpZDo5ZGRiZTFmMi01MTA0LWQ0NDItYWQ5NS1iOTcyMTE2YTA3NmEiIHhtcE1NOkRvY3VtZW50SUQ9ImFkb2JlOmRvY2lkOnBob3Rvc2hvcDpmMzJiMGQxYy00N2Q5LWY1NGItODMzYS1hNjEwZjRiMzQ0NDQiIHhtcE1NOk9yaWdpbmFsRG9jdW1lbnRJRD0ieG1wLmRpZDpjOTE4MWRlOC1lN2NjLWRhNDUtYjFhMS03OWM1ZDkxNTdiNjUiPiA8eG1wTU06SGlzdG9yeT4gPHJkZjpTZXE+IDxyZGY6bGkgc3RFdnQ6YWN0aW9uPSJjcmVhdGVkIiBzdEV2dDppbnN0YW5jZUlEPSJ4bXAuaWlkOmM5MTgxZGU4LWU3Y2MtZGE0NS1iMWExLTc5YzVkOTE1N2I2NSIgc3RFdnQ6d2hlbj0iMjAyMS0wNi0yN1QxMToyNDo1NCswODowMCIgc3RFdnQ6c29mdHdhcmVBZ2VudD0iQWRvYmUgUGhvdG9zaG9wIENDIDIwMTggKFdpbmRvd3MpIi8+IDxyZGY6bGkgc3RFdnQ6YWN0aW9uPSJzYXZlZCIgc3RFdnQ6aW5zdGFuY2VJRD0ieG1wLmlpZDoxMjdjOWVkYS1hM2ZmLWZiNDUtYTViMS1mMGZmYzdjNDdhNGEiIHN0RXZ0OndoZW49IjIwMjEtMDctMDdUMDY6MTE6NTYrMDg6MDAiIHN0RXZ0OnNvZnR3YXJlQWdlbnQ9IkFkb2JlIFBob3Rvc2hvcCBDQyAyMDE4IChXaW5kb3dzKSIgc3RFdnQ6Y2hhbmdlZD0iLyIvPiA8cmRmOmxpIHN0RXZ0OmFjdGlvbj0ic2F2ZWQiIHN0RXZ0Omluc3RhbmNlSUQ9InhtcC5paWQ6OWRkYmUxZjItNTEwNC1kNDQyLWFkOTUtYjk3MjExNmEwNzZhIiBzdEV2dDp3aGVuPSIyMDIxLTA3LTA3VDA2OjEyOjUzKzA4OjAwIiBzdEV2dDpzb2Z0d2FyZUFnZW50PSJBZG9iZSBQaG90b3Nob3AgQ0MgMjAxOCAoV2luZG93cykiIHN0RXZ0OmNoYW5nZWQ9Ii8iLz4gPC9yZGY6U2VxPiA8L3htcE1NOkhpc3Rvcnk+IDwvcmRmOkRlc2NyaXB0aW9uPiA8L3JkZjpSREY+IDwveDp4bXBtZXRhPiA8P3hwYWNrZXQgZW5kPSJyIj8+vCyjFAAAAfBJREFUOMut1E8og3EYwPH3KBzmpvydg2haRKRWUnawiLmsJqU4qOXiTaa3Wasdl4NiViS1HIRprLlYSrTSDnLYCYfFDtSKww5aj+f55bd+r/x53/Grb/udnk/P27tXAgBJ7PNJxpX+bb/Ti03mnjaapF/O53ls5ncIvEH5tm9+UbH33iJQoPCeSMZjXf+CECBbO1YxwE0KuAGLIGeLMfUTpAnJ3ow1LNlrjjHAO8CrDI/XDkhFLOwelFthqr3s4Spus5aMiEB0pZsNp2LLRobBmwsQ+BbSijCAshkkNlxECFBBJzFHSQhtwCEazuOICmozvgTnXA5diGI3AC+bViCXCcDGoplFd7jvhUzCxKL71dEMTFmMz8GFgXFdyJanswjRYOriYEKFJDfrWJALFCH87dGKHIqQbJWKEMW3oPY9BgYQhJtQXm2vcFqp59D5roMhIiRuwTfRjdC5uTitxn/3CQZnOyOIlLGyaRnyWRnCnmYW3e/SMVCcFrDVSrC37pZ1fVY4FJo3qSAazEtFh9hwHiJruhAO4eAoDeeQMigVAbrTcGGTUd0IHXxEVSJEg1UJjwofXUVJCJ38a75SGW4NYbDlm2C5R80w1oibVEv500h4uqRP/VdQ2D8bouECkhGBPyMcuowG+jDnR31aPpDvt7XVCXcJR68AAAAASUVORK5CYII="
    jin_img = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABkAAAASCAYAAACuLnWgAAAACXBIWXMAAAsTAAALEwEAmpwYAAAF+2lUWHRYTUw6Y29tLmFkb2JlLnhtcAAAAAAAPD94cGFja2V0IGJlZ2luPSLvu78iIGlkPSJXNU0wTXBDZWhpSHpyZVN6TlRjemtjOWQiPz4gPHg6eG1wbWV0YSB4bWxuczp4PSJhZG9iZTpuczptZXRhLyIgeDp4bXB0az0iQWRvYmUgWE1QIENvcmUgNS42LWMxNDIgNzkuMTYwOTI0LCAyMDE3LzA3LzEzLTAxOjA2OjM5ICAgICAgICAiPiA8cmRmOlJERiB4bWxuczpyZGY9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkvMDIvMjItcmRmLXN5bnRheC1ucyMiPiA8cmRmOkRlc2NyaXB0aW9uIHJkZjphYm91dD0iIiB4bWxuczp4bXA9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC8iIHhtbG5zOmRjPSJodHRwOi8vcHVybC5vcmcvZGMvZWxlbWVudHMvMS4xLyIgeG1sbnM6cGhvdG9zaG9wPSJodHRwOi8vbnMuYWRvYmUuY29tL3Bob3Rvc2hvcC8xLjAvIiB4bWxuczp4bXBNTT0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL21tLyIgeG1sbnM6c3RFdnQ9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9zVHlwZS9SZXNvdXJjZUV2ZW50IyIgeG1wOkNyZWF0b3JUb29sPSJBZG9iZSBQaG90b3Nob3AgQ0MgMjAxOCAoV2luZG93cykiIHhtcDpDcmVhdGVEYXRlPSIyMDIxLTA2LTI3VDExOjI0OjU0KzA4OjAwIiB4bXA6TW9kaWZ5RGF0ZT0iMjAyMS0wNy0wN1QwNjoxMjo0MCswODowMCIgeG1wOk1ldGFkYXRhRGF0ZT0iMjAyMS0wNy0wN1QwNjoxMjo0MCswODowMCIgZGM6Zm9ybWF0PSJpbWFnZS9wbmciIHBob3Rvc2hvcDpDb2xvck1vZGU9IjMiIHBob3Rvc2hvcDpJQ0NQcm9maWxlPSJHSU1QIGJ1aWx0LWluIHNSR0IiIHhtcE1NOkluc3RhbmNlSUQ9InhtcC5paWQ6MGJkMzdhNWEtMDhjZC0yOTRjLWFlNmUtOGMzZjQ5MzA5YTBkIiB4bXBNTTpEb2N1bWVudElEPSJhZG9iZTpkb2NpZDpwaG90b3Nob3A6M2E1Y2YwZjMtZmNiNy1hNjRjLTk2ZWMtMzBkZDViMDU1MmVmIiB4bXBNTTpPcmlnaW5hbERvY3VtZW50SUQ9InhtcC5kaWQ6Y2E3OTYzMmQtZGU5My00ZTQ0LTgwNDYtY2JmMzE5ZWZjNjBkIj4gPHhtcE1NOkhpc3Rvcnk+IDxyZGY6U2VxPiA8cmRmOmxpIHN0RXZ0OmFjdGlvbj0iY3JlYXRlZCIgc3RFdnQ6aW5zdGFuY2VJRD0ieG1wLmlpZDpjYTc5NjMyZC1kZTkzLTRlNDQtODA0Ni1jYmYzMTllZmM2MGQiIHN0RXZ0OndoZW49IjIwMjEtMDYtMjdUMTE6MjQ6NTQrMDg6MDAiIHN0RXZ0OnNvZnR3YXJlQWdlbnQ9IkFkb2JlIFBob3Rvc2hvcCBDQyAyMDE4IChXaW5kb3dzKSIvPiA8cmRmOmxpIHN0RXZ0OmFjdGlvbj0ic2F2ZWQiIHN0RXZ0Omluc3RhbmNlSUQ9InhtcC5paWQ6MGJkMzdhNWEtMDhjZC0yOTRjLWFlNmUtOGMzZjQ5MzA5YTBkIiBzdEV2dDp3aGVuPSIyMDIxLTA3LTA3VDA2OjEyOjQwKzA4OjAwIiBzdEV2dDpzb2Z0d2FyZUFnZW50PSJBZG9iZSBQaG90b3Nob3AgQ0MgMjAxOCAoV2luZG93cykiIHN0RXZ0OmNoYW5nZWQ9Ii8iLz4gPC9yZGY6U2VxPiA8L3htcE1NOkhpc3Rvcnk+IDwvcmRmOkRlc2NyaXB0aW9uPiA8L3JkZjpSREY+IDwveDp4bXBtZXRhPiA8P3hwYWNrZXQgZW5kPSJyIj8+qj+jhgAAAfZJREFUOMvdlE1IG0EYhqdiJC6KkShGRDSoMai0/gTtWrBUAoGooAsWFDyIChahCOLBi4q/lxRLlZSKvQR7CURBiKiQQ88FD3rwLD30mKPHr/NOduIsbIwXDzrw8C0beJ99h8kwImJPDXt5EnMVOQuZxmwWf1/BWQy2u38DJ2MBTjl+siGn5M1rv3s9+NZDgAfucprM8F4j3EAHX0OU+qbT6qSPuEigt2ZY+OgTfB6upx6/68RWwgU3kSWdUrGwBQSDfzdzAkikCCTWdAu/ljqEyFaid9X8TOwblNgJCi7PZwXJ/TDdXkXpLp0SpGIGxTf76PunVtoY8tDerJ8OV3RBMso/LGrQ8nQ35dqud5AgODLjzYog+XM6L0SYqgDIcFXyvrPmKJdE420o/TciwmUjKcEEkEjQCsFoszHiEc9owbPKHjpdGlqoIhkOEUCwZct4OJBN0OKh05U5qk5WHdsZpPT1AmHGt0MWYvxwRMa8WZYnGgTJrQ4xHQWOqrwSUzQhRZfx8awAz2c/DCGSMlXgKnGOyYyckoJXmT8SlxRDNDrgE8EWLuYsIkXwRf3QfNtVrIqmPnhpazqQbQKJ2iQUqBQCTumjJWojLHeJo8Xn0U70RheB/rZ72mq1Y34b1NldQ3kldlcXgJDPZhOHCXu05Nlf9f8B/yrBMSqLm+8AAAAASUVORK5CYII="
    yin_img = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABkAAAASCAYAAACuLnWgAAAACXBIWXMAAAsTAAALEwEAmpwYAAAF+2lUWHRYTUw6Y29tLmFkb2JlLnhtcAAAAAAAPD94cGFja2V0IGJlZ2luPSLvu78iIGlkPSJXNU0wTXBDZWhpSHpyZVN6TlRjemtjOWQiPz4gPHg6eG1wbWV0YSB4bWxuczp4PSJhZG9iZTpuczptZXRhLyIgeDp4bXB0az0iQWRvYmUgWE1QIENvcmUgNS42LWMxNDIgNzkuMTYwOTI0LCAyMDE3LzA3LzEzLTAxOjA2OjM5ICAgICAgICAiPiA8cmRmOlJERiB4bWxuczpyZGY9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkvMDIvMjItcmRmLXN5bnRheC1ucyMiPiA8cmRmOkRlc2NyaXB0aW9uIHJkZjphYm91dD0iIiB4bWxuczp4bXA9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC8iIHhtbG5zOmRjPSJodHRwOi8vcHVybC5vcmcvZGMvZWxlbWVudHMvMS4xLyIgeG1sbnM6cGhvdG9zaG9wPSJodHRwOi8vbnMuYWRvYmUuY29tL3Bob3Rvc2hvcC8xLjAvIiB4bWxuczp4bXBNTT0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL21tLyIgeG1sbnM6c3RFdnQ9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9zVHlwZS9SZXNvdXJjZUV2ZW50IyIgeG1wOkNyZWF0b3JUb29sPSJBZG9iZSBQaG90b3Nob3AgQ0MgMjAxOCAoV2luZG93cykiIHhtcDpDcmVhdGVEYXRlPSIyMDIxLTA2LTI3VDExOjI0OjU0KzA4OjAwIiB4bXA6TW9kaWZ5RGF0ZT0iMjAyMS0wNy0wN1QwNjoxMzoyNiswODowMCIgeG1wOk1ldGFkYXRhRGF0ZT0iMjAyMS0wNy0wN1QwNjoxMzoyNiswODowMCIgZGM6Zm9ybWF0PSJpbWFnZS9wbmciIHBob3Rvc2hvcDpDb2xvck1vZGU9IjMiIHBob3Rvc2hvcDpJQ0NQcm9maWxlPSJHSU1QIGJ1aWx0LWluIHNSR0IiIHhtcE1NOkluc3RhbmNlSUQ9InhtcC5paWQ6MzE2ZTgxYzQtMDQ2MC02ZDRhLWI0ZTAtMDgzYzEzZDhjNTgwIiB4bXBNTTpEb2N1bWVudElEPSJhZG9iZTpkb2NpZDpwaG90b3Nob3A6ODdmZGNhODktZTgyZC1hMjQ4LWIxZTUtNTlkMTVjN2U4YTFlIiB4bXBNTTpPcmlnaW5hbERvY3VtZW50SUQ9InhtcC5kaWQ6ZjFlMjE3ZDktYWEzOC1lZjQ1LWE1YmItNjZlOTIwYWZkOTk3Ij4gPHhtcE1NOkhpc3Rvcnk+IDxyZGY6U2VxPiA8cmRmOmxpIHN0RXZ0OmFjdGlvbj0iY3JlYXRlZCIgc3RFdnQ6aW5zdGFuY2VJRD0ieG1wLmlpZDpmMWUyMTdkOS1hYTM4LWVmNDUtYTViYi02NmU5MjBhZmQ5OTciIHN0RXZ0OndoZW49IjIwMjEtMDYtMjdUMTE6MjQ6NTQrMDg6MDAiIHN0RXZ0OnNvZnR3YXJlQWdlbnQ9IkFkb2JlIFBob3Rvc2hvcCBDQyAyMDE4IChXaW5kb3dzKSIvPiA8cmRmOmxpIHN0RXZ0OmFjdGlvbj0ic2F2ZWQiIHN0RXZ0Omluc3RhbmNlSUQ9InhtcC5paWQ6MzE2ZTgxYzQtMDQ2MC02ZDRhLWI0ZTAtMDgzYzEzZDhjNTgwIiBzdEV2dDp3aGVuPSIyMDIxLTA3LTA3VDA2OjEzOjI2KzA4OjAwIiBzdEV2dDpzb2Z0d2FyZUFnZW50PSJBZG9iZSBQaG90b3Nob3AgQ0MgMjAxOCAoV2luZG93cykiIHN0RXZ0OmNoYW5nZWQ9Ii8iLz4gPC9yZGY6U2VxPiA8L3htcE1NOkhpc3Rvcnk+IDwvcmRmOkRlc2NyaXB0aW9uPiA8L3JkZjpSREY+IDwveDp4bXBtZXRhPiA8P3hwYWNrZXQgZW5kPSJyIj8+WEI/qAAAAdRJREFUOMvdlL9LQlEUx99g8SQHx6KIhLCEsB9IUQhSOEQUgg3lIP0gIZJKiCB60A8wghDJECmQfgwVQTUEtoTU0g8amgI3Gx0a/BNO59w6r2doWtDShQ/3DeeeD997370SAEh/jfT/JMWG0SCXIVZklZB0kkHl69BJcl6JrJPNSH+3vT1D2NosI1hejVTQPOR2Pu9trwCB32DvsjJXBNa/To66gWZkPK8EG+8o8z5InEcF8ZiSQ+YlKWDRQsCrkjgKQTysqJAsfxJZmo1tBYF5uDkWXJxEIJ1KQjabFtxen0J8U4ElbO739Ik5sh6Aw92QSrfdVlBipObp1J2QUHOSxLcUVcKCubE+ISDeBcEcCZ6Zp+DBuwZ69khCUHMSsYwFzGfzoEgzNz0qBDSjpLyghNKgSEg4BctIwvB28ZYR2hTUq9gvXBHdUCB5eaiysjgDobWAwO9zC1y9Dpif9qpQIntHE8g6qawUCY1maqwVnR2FBSzRCihtYGqYBA3coKTLiAtyRE/3ZyqUSCugVFjv0K4v+caTyOno2CcZJyG0EhQ8WupNg7xNP5aIA9LLtaaaSl9ro2kZAaazxXJgrquewBJ9vnW/ers+RpUG/XeF//OpfwM0X9GDO5SBFgAAAABJRU5ErkJggg=="
    tong_img = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABkAAAASCAYAAACuLnWgAAAACXBIWXMAAAsTAAALEwEAmpwYAAAF+2lUWHRYTUw6Y29tLmFkb2JlLnhtcAAAAAAAPD94cGFja2V0IGJlZ2luPSLvu78iIGlkPSJXNU0wTXBDZWhpSHpyZVN6TlRjemtjOWQiPz4gPHg6eG1wbWV0YSB4bWxuczp4PSJhZG9iZTpuczptZXRhLyIgeDp4bXB0az0iQWRvYmUgWE1QIENvcmUgNS42LWMxNDIgNzkuMTYwOTI0LCAyMDE3LzA3LzEzLTAxOjA2OjM5ICAgICAgICAiPiA8cmRmOlJERiB4bWxuczpyZGY9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkvMDIvMjItcmRmLXN5bnRheC1ucyMiPiA8cmRmOkRlc2NyaXB0aW9uIHJkZjphYm91dD0iIiB4bWxuczp4bXA9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC8iIHhtbG5zOmRjPSJodHRwOi8vcHVybC5vcmcvZGMvZWxlbWVudHMvMS4xLyIgeG1sbnM6cGhvdG9zaG9wPSJodHRwOi8vbnMuYWRvYmUuY29tL3Bob3Rvc2hvcC8xLjAvIiB4bWxuczp4bXBNTT0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL21tLyIgeG1sbnM6c3RFdnQ9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9zVHlwZS9SZXNvdXJjZUV2ZW50IyIgeG1wOkNyZWF0b3JUb29sPSJBZG9iZSBQaG90b3Nob3AgQ0MgMjAxOCAoV2luZG93cykiIHhtcDpDcmVhdGVEYXRlPSIyMDIxLTA2LTI3VDExOjI0OjU0KzA4OjAwIiB4bXA6TW9kaWZ5RGF0ZT0iMjAyMS0wNy0wN1QwNjoxNDoxMSswODowMCIgeG1wOk1ldGFkYXRhRGF0ZT0iMjAyMS0wNy0wN1QwNjoxNDoxMSswODowMCIgZGM6Zm9ybWF0PSJpbWFnZS9wbmciIHBob3Rvc2hvcDpDb2xvck1vZGU9IjMiIHBob3Rvc2hvcDpJQ0NQcm9maWxlPSJHSU1QIGJ1aWx0LWluIHNSR0IiIHhtcE1NOkluc3RhbmNlSUQ9InhtcC5paWQ6NWYzZWUxOWMtZDZjOC03NjQ2LWEzM2YtYmI1NWViNWRkNWNiIiB4bXBNTTpEb2N1bWVudElEPSJhZG9iZTpkb2NpZDpwaG90b3Nob3A6YmQzNjFmMmEtOThjMi1hNjQ4LThkZWUtNzcyZGQ5NDdkODI5IiB4bXBNTTpPcmlnaW5hbERvY3VtZW50SUQ9InhtcC5kaWQ6ZGVlNmJiOGMtYmNhOS01MjQ5LThhYjEtNzU2N2M0MTk2NmRlIj4gPHhtcE1NOkhpc3Rvcnk+IDxyZGY6U2VxPiA8cmRmOmxpIHN0RXZ0OmFjdGlvbj0iY3JlYXRlZCIgc3RFdnQ6aW5zdGFuY2VJRD0ieG1wLmlpZDpkZWU2YmI4Yy1iY2E5LTUyNDktOGFiMS03NTY3YzQxOTY2ZGUiIHN0RXZ0OndoZW49IjIwMjEtMDYtMjdUMTE6MjQ6NTQrMDg6MDAiIHN0RXZ0OnNvZnR3YXJlQWdlbnQ9IkFkb2JlIFBob3Rvc2hvcCBDQyAyMDE4IChXaW5kb3dzKSIvPiA8cmRmOmxpIHN0RXZ0OmFjdGlvbj0ic2F2ZWQiIHN0RXZ0Omluc3RhbmNlSUQ9InhtcC5paWQ6NWYzZWUxOWMtZDZjOC03NjQ2LWEzM2YtYmI1NWViNWRkNWNiIiBzdEV2dDp3aGVuPSIyMDIxLTA3LTA3VDA2OjE0OjExKzA4OjAwIiBzdEV2dDpzb2Z0d2FyZUFnZW50PSJBZG9iZSBQaG90b3Nob3AgQ0MgMjAxOCAoV2luZG93cykiIHN0RXZ0OmNoYW5nZWQ9Ii8iLz4gPC9yZGY6U2VxPiA8L3htcE1NOkhpc3Rvcnk+IDwvcmRmOkRlc2NyaXB0aW9uPiA8L3JkZjpSREY+IDwveDp4bXBtZXRhPiA8P3hwYWNrZXQgZW5kPSJyIj8+Bz8DqwAAAgVJREFUOMu1lc1L40AUwIfS7KZxcSPUEkQ0fqBlDdJoL5WKEFmrUhHiSUEUZBGsn3jx4yIKKlr0oHgqyLK4B2HPC16FveyuRz36D3jxL3i+N3biiBUTxYEfLySZ98tL5k0YALD35umJEkNlrBxpMaLKDLKFp4aQWuRDqfsDSyi5aSg/UgkN+tO6hx3XoMZQv+Mt1lskGgomKbnbp3NkCTHSZ0A6oUOxsuASNczm3O4GkDncz3q4mSYYyVZyUnGVcANJUNCcTMTgz3kO8hsZDh1fXi0+YnWh4ZEIp1b5kqDgM7Kd33E8iYhyJUThyOYiIdMjoVm/ki6qgiSywAgz/ooEOk6l5LLIrlZvqJoXJbrKVrI9Mch9q4PC8ShcXOdhaqwVUiYDs1I5wevDGP86+MEXF2zYO8zwSDj3i6DNj6TwnASvtdPrIJGQFH66sLaeliWdfiS7JCGeq8Su125liaioKIn7kfS2NpdxCSWXJZREgEKeWEgoWqZGkqifJRzBTv5PjTaAouUlC05OHR5z0y0e+QNc2ps2jA+bXsQHdIM0Ywd1MklkEU+M/Dqb4FBiQdLS/ykhpgXqeKwmJyQCuZL+r7osANyCnNfsXZG6KJuXJZRYppTgVbswji9NhvY71YgfPPmAVa+B8UmdV8Oh6Ju3+uL4SLJYhTKGzOHxYPF/wvz8T+4ACwlDiF9TSoMAAAAASUVORK5CYII="
    zhuan = int(price / 100 / 100 / 10000)
    jin = int(price / 100 / 100 % 10000)
    yin = int(price / 100 % 100)
    tong = int(price % 100)
    
    parts = []
    if zhuan:
        parts.append(f"{zhuan}<img src='{zhuan_img}'>")
    if jin:
        parts.append(f"{jin}<img src='{jin_img}'>")
    if yin:
        parts.append(f"{yin}<img src='{yin_img}'>")
    if tong:
        parts.append(f"{tong}<img src='{tong_img}'>")

    return "".join(parts[:2])