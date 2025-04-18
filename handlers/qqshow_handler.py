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
            "image_bytes": None
        }

    # 下载图片并返回二进制内容
    try:
        image_res = requests.get(result["showAvatar"])
        if image_res.status_code != 200:
            raise Exception("Image download failed")

        return {
            "content": f"🎴 角色名片：{name}@{server}",
            "image_bytes": image_res.content
        }

    except Exception as e:
        print("图片获取失败：", e)
        return {
            "content": f"已获取角色名片信息，但图片下载失败：{result['showAvatar']}",
            "image_bytes": None
        }
