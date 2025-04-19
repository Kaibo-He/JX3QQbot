# handlers/open_server_handler.py
from jx3api import get_server_status

def handle_open_server_query(content: str) -> str:
    parts = content.strip().split()
    server = "梦江南"  # 默认区服

    if len(parts) < 2:
        pass
    elif len(parts) == 2:
        server = parts[1]
    elif len(parts) > 2:
        return "格式错误，如需查询开服状态请输入：\n开服 [区服]"

    status = get_server_status(server)
    if status:
        return (
            f"【{status['server']}】（{status['zone']}）\n"
            f"状态：{status['status']}\n"
            f"最后更新时间：{status['update_time']}"
        )
    else:
        return f"无法获取【{server}】的开服状态，接口可能出错或区服名称不正确。"
