import re
import botpy
from config_loader import get_bot_config
from botpy.message import DirectMessage
from botpy import logging

from handlers.open_server_handler import handle_open_server_query
from handlers.calendar_handler import handle_calendar_query
from handlers.qqshow_handler import handle_qqshow_query
from handlers.role_attribute_handler import handle_role_attribute_card
from handlers.team_cd_handler import handle_team_cd_query
from handlers.yizhiku_handler import get_current_quarter_result
from handlers.annouce_handler import handle_news_announce, handle_maintenance_announce, handle_skill_announce

config = get_bot_config()
_log = logging.get_logger()


class JX3BotClient(botpy.Client):
    async def on_ready(self):
        _log.info(f"机器人「{self.robot.name}」已上线")

    async def on_direct_message_create(self, message: DirectMessage):
        content = message.content.strip()
        cmd = content.strip().split()[0]
        print(f"原始消息内容: {repr(message.content)}")
        _log.info(f"命令词提取结果: {cmd}")

        if cmd in ["开服"]:
            reply = handle_open_server_query(content)
            await self.api.post_dms(
                guild_id=message.guild_id,
                content=reply,
                msg_id=message.id,
            )

        elif cmd in ["日历", "日常"]:
            reply = handle_calendar_query(content)
            await self.api.post_dms(
                guild_id=message.guild_id,
                content=reply,
                msg_id=message.id,
            )

        elif cmd in ["名片", "qq秀", "QQ秀"]:
            reply = handle_qqshow_query(content)
            if reply.get("image"):
                await self.api.post_dms(
                    guild_id=message.guild_id,
                    msg_id=message.id,
                    content=reply["content"],
                    image=reply["image"],
                )
                
        elif cmd in ["属性", "装备"]:
            reply = await handle_role_attribute_card(content)
            if reply["file_image"]:
                await self.api.post_dms(
                    guild_id=message.guild_id,
                    msg_id=message.id,
                    content=reply["content"],
                    file_image=reply["file_image"]
            )
            else:
                await self.api.post_dms(
                    guild_id=message.guild_id,
                    msg_id=message.id,
                    content=reply["content"]
                )
                
        elif cmd.lower() in ["副本", "cd"]:
            reply = handle_team_cd_query(content)
            await self.api.post_dms(
                guild_id=message.guild_id,
                msg_id=message.id,
                content=reply["content"]
            )
    
        elif cmd in ["解密", "解谜"]:
            reply = get_current_quarter_result()
            await self.api.post_dms(
                guild_id=message.guild_id,
                msg_id=message.id,
                content=reply["content"]
            )
            
        elif cmd in ["技改"]:
            reply = await handle_skill_announce()
            if reply["file_image"]:
                await self.api.post_dms(
                    guild_id=message.guild_id,
                    msg_id=message.id,
                    content=reply["content"],
                    file_image=reply["file_image"]
                )
            else:
                await self.api.post_dms(
                    guild_id=message.guild_id,
                    msg_id=message.id,
                    content=reply["content"]
                )
            
        elif cmd in ["维护"]:
            reply = await handle_maintenance_announce()
            if reply["file_image"]:
                await self.api.post_dms(
                    guild_id=message.guild_id,
                    msg_id=message.id,
                    content=reply["content"],
                    file_image=reply["file_image"]
                )
            else:
                await self.api.post_dms(
                    guild_id=message.guild_id,
                    msg_id=message.id,
                    content=reply["content"]
                )
            
        elif cmd in ["公告"]:
            reply = await handle_news_announce()
            if reply["file_image"]:
                await self.api.post_dms(
                    guild_id=message.guild_id,
                    msg_id=message.id,
                    content=reply["content"],
                    file_image=reply["file_image"]
                )
            else:
                await self.api.post_dms(
                    guild_id=message.guild_id,
                    msg_id=message.id,
                    content=reply["content"]
                )
    
        else:
            reply = "暂不支持该指令,详情请查询功能列表。"
            await self.api.post_dms(
                guild_id=message.guild_id,
                content=reply,
                msg_id=message.id,
            )

if __name__ == "__main__":
    intents = botpy.Intents(direct_message=True)
    client = JX3BotClient(intents=intents)
    client.run(appid=config["appid"], secret=config["secret"])
