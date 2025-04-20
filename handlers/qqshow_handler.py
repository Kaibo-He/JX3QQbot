# handlers.qqshow_handler.py
from config import DEFAULT_SERVER
import requests
from api.jx3api import get_role_qqshow

def handle_qqshow_query(content: str) -> str:
    parts = content.strip().split()
        
    name = "王熙凤"
    server = "梦江南"

    if len(parts) > 3:
        return {
            "content": "格式错误，如需查询角色名片请输入：\n名片/qq秀/QQ秀 角色id [区服]",
            "image":None
        }


    result = get_role_qqshow(server=server, name=name)
    if not result:
        return {
            "content": f"查询失败，可能是区服或角色名错误，或接口超时，请稍后重试。",
            "image": None
        }
    name = parts[1] if len(parts) >= 2 else "王熙凤"
    server = parts[2] if len(parts) == 3 else DEFAULT_SERVER

    # 下载图片内容
    try:
        image_res = requests.get(result["showAvatar"], timeout=5)
        if image_res.status_code != 200:
            raise Exception("图片下载失败")
    except Exception as e:
        print("图片获取失败:", e)
        return {
            "content": f"角色名片：{name}@{server}\n 名片图像获取失败。",
            "image": None,
            "file_image": None
        }

    return {
    "content": f"角色名片：{name}@{server}",
    "image": result["showAvatar"]
    }
