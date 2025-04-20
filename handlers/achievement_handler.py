from session_manager import is_in_session, start_session, get_session, refresh_session, end_session, is_valid_input

async def handle_role_achievement(content: str, user_id=None):
    # 启动新会话
    if not is_in_session(user_id):
        start_session(user_id, {"type": "achievement"})
        return "🎖️ 请选择二级功能：\n1. 回复 a\n2. 回复 b\n3. 回复 c\n4. 退出"

    session = get_session(user_id)
    refresh_session(user_id)
    input_text = content.strip()

    # 检查是否有效输入
    if not is_valid_input(input_text):
        return "❌ 无效选项，请输入 1-4 之一。"

    if input_text == "1":
        return "✅ 回复 a\n\n🎖️ 请选择二级功能：\n1. 回复 a\n2. 回复 b\n3. 回复 c\n4. 退出"
    elif input_text == "2":
        return "✅ 回复 b\n\n🎖️ 请选择二级功能：\n1. 回复 a\n2. 回复 b\n3. 回复 c\n4. 退出"
    elif input_text == "3":
        return "✅ 回复 c\n\n🎖️ 请选择二级功能：\n1. 回复 a\n2. 回复 b\n3. 回复 c\n4. 退出"
    elif input_text == "4":
        end_session(user_id)
        return "✅ 已退出「资历」会话。"