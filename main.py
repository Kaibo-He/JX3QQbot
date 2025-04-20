# main.py
import inspect
import botpy
from config_loader import get_bot_config
from botpy.message import DirectMessage
from botpy import logging

from handlers.command_map import command_map
from session_manager import is_in_session, cleanup_sessions
from handlers.achievement_handler import handle_role_achievement 

config = get_bot_config()
_log = logging.get_logger()

class JX3BotClient(botpy.Client):
    async def on_ready(self):
        _log.info(f"机器人「{self.robot.name}」已上线")

    async def on_direct_message_create(self, message: DirectMessage):
        _log.info(f"📩 收到私信: {message.content}")
        content = message.content.strip()
        cmd = content.strip().split()[0]
        user_id = message.author.id
        
        # 优先检查是否处于会话中
        if is_in_session(user_id):
            reply = await handle_role_achievement(content, user_id=user_id)
            await self.api.post_dms(
                guild_id=message.guild_id,
                msg_id=message.id,
                content=reply
            )
            return
        
        handler = command_map.get(cmd)
        if handler:   
            
            if cmd == "资历":
                reply = await handler(content, user_id=user_id)
            elif inspect.iscoroutinefunction(handler):
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
