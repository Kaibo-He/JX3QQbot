import requests
from jx3api import get_role_qqshow

def handle_qqshow_query(content: str) -> str:
    parts = content.strip().split()
        
    server = "梦江南"
    name = "王熙凤"
    if len(parts) >= 3:
        server = parts[2]
    elif len(parts) == 2:
        name = parts[1]

    result = get_role_qqshow(server=server, name=name)
    if not result:
        return {
            "content": f"查询失败，可能是区服或角色名错误，或接口超时，请稍后重试。",
            "image": None,
            "file_image": None
        }

    # 下载图片内容
    try:
        image_res = requests.get(result["showAvatar"], timeout=5)
        if image_res.status_code != 200:
            raise Exception("图片下载失败")
        image_bytes = image_res.content
    except Exception as e:
        print("图片获取失败:", e)
        return {
            "content": f"角色名片：{name}@{server}\n 名片图像获取失败。",
            "image": None,
            "file_image": None
        }

    return {
    "content": f"角色名片：{name}@{server}",
    "image": result["showAvatar"],    # 直接把 URL 给 image
    "file_image": None
    }
