# main.py
import inspect
import botpy
from config_loader import get_bot_config
from botpy.message import DirectMessage
from botpy import logging

from handlers.command_map import command_map

config = get_bot_config()
_log = logging.get_logger()

class JX3BotClient(botpy.Client):
    async def on_ready(self):
        _log.info(f"机器人「{self.robot.name}」已上线")

    async def on_direct_message_create(self, message: DirectMessage):
        _log.info(f"📩 收到私信: {message.content}")
        content = message.content.strip()
        cmd = content.strip().split()[0]
        
        handler = command_map.get(cmd)
        if handler:   
            
            if inspect.iscoroutinefunction(handler):
                reply = await handler(content)
            else:
                reply = handler(content)
            
            if isinstance(reply, dict):
                await self.api.post_dms(
                    guild_id=message.guild_id,
                    msg_id=message.id,
                    content=reply.get("content", ""),
                    file_image=reply.get("file_image"),
                    image=reply.get("image")
                )
            elif isinstance(reply, list):
                for r in reply:
                    await self.api.post_dms(
                        guild_id=message.guild_id,
                        msg_id=message.id,
                        content=r.get("content", ""),
                        file_image=reply.get("file_image"),
                        image=reply.get("image")
                    )
            elif isinstance(reply, str):
                await self.api.post_dms(
                    guild_id=message.guild_id,
                    msg_id=message.id,
                    content=reply
                )
        else:
            reply = "暂不支持该指令,详情请查询功能列表。"
            await self.api.post_dms(
                guild_id=message.guild_id,
                content=reply,
                msg_id=message.id,
            )


if __name__ == "__main__":
    intents = botpy.Intents(direct_message=True, public_guild_messages=True)
    client = JX3BotClient(intents=intents)
    client.run(appid=config["appid"], secret=config["secret"])
