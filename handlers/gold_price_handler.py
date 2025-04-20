# handlers/gold_price_handler.py
from api.jx3api import get_gold_price

async def handle_gold_price(content: str) -> str:
    parts = content.strip().split()
    server = "梦江南"  # 默认区服

    if len(parts) < 2:
        pass
    elif len(parts) == 2:
        server = parts[1]
    elif len(parts) > 2:
        return "格式错误，如需查询金币价格请输入：\n金价/金币/买金 [区服]"

    data = await get_gold_price(server)
    if data:
        return (
            f"金币价格查询 | {server}\n"
            f"时间：{data['date']}\n"
            f"帖吧：{int(float(data['tieba']))}\n"
            f"万宝楼：{int(float(data['wanbaolou']))}"
        )
    else:
        return f"无法获取【{server}】的金币价格，接口可能出错或区服名称不正确。"
