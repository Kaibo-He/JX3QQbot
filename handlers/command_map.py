# handlers/command_map.py
from handlers.open_server_handler import handle_open_server_query
from handlers.calendar_handler import handle_calendar_query
from handlers.qqshow_handler import handle_qqshow_query
from handlers.role_attribute_handler import handle_role_attribute_card
from handlers.team_cd_handler import handle_team_cd_query
from handlers.yizhiku_handler import get_current_quarter_result
from handlers.auction_handler import handle_auction_card
from handlers.trade_handler import handle_trade_card
from handlers.gold_price_handler import handle_gold_price
from handlers.achievement_handler import handle_role_achievement

command_map = {
    "开服": handle_open_server_query,
    "日历": handle_calendar_query,
    "日常": handle_calendar_query,
    "名片": handle_qqshow_query,
    "qq秀": handle_qqshow_query,
    "QQ秀": handle_qqshow_query,
    "属性": handle_role_attribute_card,
    "装备": handle_role_attribute_card,
    "副本": handle_team_cd_query,
    "cd": handle_team_cd_query,
    "交易行": handle_auction_card,
    "拍卖行": handle_auction_card,
    "物价": handle_trade_card,
    "外观": handle_trade_card,
    "金价": handle_gold_price,
    "金币": handle_gold_price,
    "买金": handle_gold_price,
    "解密": get_current_quarter_result,
    "解谜": get_current_quarter_result,
    "资历": handle_role_achievement
}
