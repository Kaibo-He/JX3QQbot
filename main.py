# main.py
import os
import botpy
from botpy.ext.cog_yaml import read
from botpy.message import DirectMessage
from botpy import logging

from handlers.open_server_handler import handle_open_server_query
from handlers.calendar_handler import handle_calendar_query

config = read(os.path.join(os.path.dirname(__file__), "config.yaml"))
_log = logging.get_logger()


class JX3BotClient(botpy.Client):
    async def on_ready(self):
        _log.info(f"机器人「{self.robot.name}」已上线")

    async def on_direct_message_create(self, message: DirectMessage):
        content = message.content.strip()

        if content.startswith("开服"):
            reply = handle_open_server_query(content)
        elif "日历" in content or "日常" in content:
            reply = handle_calendar_query(content)
        else:
            reply = "暂不支持该指令~ 可输入 开服 / 日历 查看相关信息"

        await self.api.post_dms(
            guild_id=message.guild_id,
            content=reply,
            msg_id=message.id,
        )


if __name__ == "__main__":
    intents = botpy.Intents(direct_message=True)
    client = JX3BotClient(intents=intents)
    client.run(appid=config["appid"], secret=config["secret"])
