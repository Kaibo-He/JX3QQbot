# handlers/calendar_handler.py
from config import DEFAULT_SERVER
from api.jx3api import get_daily_calendar

async def handle_calendar_query(content: str) -> str:
    parts = content.strip().split()
    server = "梦江南"

    if len(parts) > 2:
        return {
            "content": "格式错误，如需查询活动日历请输入：\n日历/日常 [区服]",
            "file_image": None
        }
    server = parts[1] if len(parts) == 2 else DEFAULT_SERVER

    calendar = await get_daily_calendar(server=server)
    if not calendar:
        return {
            "content": f"{server}】的日历查询失败，可能是接口出错或区服名不正确~",
            "file_image": None
        }
        
    msg = f"当前时间：{calendar['date']}（星期{calendar['week']}） | 区服：{server}\n\n"

    # 日常任务
    msg += "【日常任务】\n"
    msg += f"┌ 秘境大战：{calendar['war']}\n"
    msg += f"├ 战场任务：{calendar['battle']}\n"
    msg += f"├ 宗门事件：{calendar['school']}\n"
    msg += f"├ 驰援任务：{calendar['rescue']}\n"
    msg += f"└ 阵营任务：{calendar['orecar']}\n\n"

    # 额外活动
    msg += "【额外活动】\n"
    msg += f"├ 福源宠物：{'；'.join(calendar['luck'])}\n"
    has_leader = calendar.get("leader")
    has_draw = calendar.get("draw")
    if has_leader:
        msg += f"├ 世界首领：{'；'.join(has_leader)}\n"
    if has_draw:
        msg += f"└ 美人画像：{has_draw}\n"
    if not has_leader and not has_draw:
        msg = msg.rstrip("├\n") + "└ 今日无额外活动\n"

    # 家园副本
    msg += "\n【家园声望·加倍道具】\n"
    msg += "；".join(calendar['card']) + "\n"

    # 武林通鉴任务
    team = calendar.get("team", [])
    msg += "\n【武林通鉴】\n"
    if len(team) >= 1:
        msg += f"├ 公共任务：{team[0]}\n"
    if len(team) >= 2:
        msg += f"├ 秘境任务：{team[1]}\n"
    if len(team) >= 3:
        msg += f"└ 团队秘境：{team[2]}\n"

    return {
        "content": msg.strip(),
        "file_image": None
    }
