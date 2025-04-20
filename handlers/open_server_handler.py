# handlers/open_server_handler.py
from config import DEFAULT_SERVER
from api.jx3api import get_server_status

async def handle_open_server_query(content: str) -> str:
    parts = content.strip().split()

    if len(parts) > 2:
        return {
            "content": "格式错误，如需查询开服状态请输入：\n开服 [区服]",
            "file_image": None
        }
    server = parts[1] if len(parts) == 2 else DEFAULT_SERVER
        
    status = await get_server_status(server)
    if not status:
        return {
            "content": f"无法获取【{server}】的开服状态，接口可能出错或区服名称不正确。",
            "file_image": None
        }
        
    msg = (
        f"【{status['server']}】（{status['zone']}）\n"
        f"状态：{status['status']}\n"
        f"最后更新时间：{status['update_time']}"
    )
    
    return {
        "content": msg,
        "file_image": None
    }
