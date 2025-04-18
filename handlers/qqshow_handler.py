import requests
from jx3api import get_role_qqshow

def handle_qqshow_query(content: str) -> str:
    parts = content.strip().split()

    server = "梦江南"
    name = "王熙凤"

    if len(parts) >= 3:
        server = parts[1]
        name = parts[2]
    elif len(parts) == 2:
        name = parts[1]

    result = get_role_qqshow(server=server, name=name)
    if not result:
        return {
            "content": f"⚠️ 无法查询角色「{name}」在「{server}」的名片信息，请确认角色是否存在。",
            "image": None,
            "file_image": None
        }

    return {
        "content": f"🎴 角色名片：{name}@{server}",
        "image": result["showAvatar"],
        "file_image": None
    }
