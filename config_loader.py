from dotenv import load_dotenv
import os

load_dotenv()  # 自动从 .env 文件中加载环境变量

def get_bot_config():
    return {
        "appid": os.getenv("BOT_APPID"),
        "secret": os.getenv("BOT_SECRET"),
        "token": os.getenv("BOT_TOKEN")
    }

def get_jx3api_auth():
    return {
        "token": os.getenv("JX3_TOKEN"),
        "ticket": os.getenv("JX3_TICKET")
    }