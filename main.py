# main.py
import os
import botpy
from config_loader import get_bot_config
from botpy.message import DirectMessage
from botpy import logging

from handlers.open_server_handler import handle_open_server_query
from handlers.calendar_handler import handle_calendar_query
from handlers.qqshow_handler import handle_qqshow_query

config = get_bot_config()
_log = logging.get_logger()


class JX3BotClient(botpy.Client):
    async def on_ready(self):
        _log.info(f"机器人「{self.robot.name}」已上线")

    async def on_direct_message_create(self, message: DirectMessage):
        content = message.content.strip()

        if content.startswith("开服"):
            reply = handle_open_server_query(content)
            await self.api.post_dms(
                guild_id=message.guild_id,
                content=reply,
                msg_id=message.id,
            )

        elif "日历" in content or "日常" in content:
            reply = handle_calendar_query(content)
            await self.api.post_dms(
                guild_id=message.guild_id,
                content=reply,
                msg_id=message.id,
            )

        elif content.startswith("名片") or content.startswith("qq秀") or content.startswith("QQ秀"):
            reply = handle_qqshow_query(content)
            if reply.get("image"):
                await self.api.post_dms(
                    guild_id=message.guild_id,
                    msg_id=message.id,
                    content=reply["content"],
                    image=reply["image"],
                )
                
        elif content.startswith("属性") or content.startswith("装备"):
            reply = handle_role_attribute_card(content)
            if reply["file_image"]:
                await self.api.post_dms(
                    guild_id=message.guild_id,
                    msg_id=message.id,
                    content=reply["content"],
                    image=reply["file_image"]
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
