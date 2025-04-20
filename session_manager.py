import asyncio
from datetime import datetime, timedelta

# 每个用户的会话数据结构
sessions = {}

# 配置：会话超时秒数、合法指令
SESSION_TIMEOUT = 120  # 两分钟
VALID_INPUTS = ["1", "2", "3", "4"]

# 判断是否处于有效会话中
def is_in_session(user_id: str) -> bool:
    return user_id in sessions

# 开启会话
def start_session(user_id: str, initial_context: dict):
    sessions[user_id] = {
        "step": 1,
        "context": initial_context,
        "start_time": datetime.now(),
        "last_active": datetime.now(),
    }

# 获取当前会话上下文
def get_session(user_id: str):
    return sessions.get(user_id)

# 更新活动时间
def refresh_session(user_id: str):
    if user_id in sessions:
        sessions[user_id]["last_active"] = datetime.now()

# 退出会话
def end_session(user_id: str):
    if user_id in sessions:
        del sessions[user_id]

# 清理超时会话（应在主程序定期调用或触发点中调用）
def cleanup_sessions():
    now = datetime.now()
    to_remove = [uid for uid, s in sessions.items() if now - s["last_active"] > timedelta(seconds=SESSION_TIMEOUT)]
    for uid in to_remove:
        del sessions[uid]

# 验证用户输入是否符合预期
def is_valid_input(user_input: str) -> bool:
    return user_input in VALID_INPUTS
