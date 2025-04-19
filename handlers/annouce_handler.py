from jx3api import get_news_announce, get_maintenance_announce, get_skill_announce

async def handle_news_announce() -> dict:
    url = get_news_announce()
    if not url:
        return {"content": "⚠️ 获取公告失败", "file_image": None}
    return {"title": "📢 最新公告：", "content": url}

async def handle_maintenance_announce() -> dict:
    url = get_maintenance_announce()
    if not url:
        return {"content": "⚠️ 获取维护信息失败", "file_image": None}
    return {"title": "🔧 维护公告：", "content": url}

async def handle_skill_announce() -> dict:
    url = get_skill_announce()
    if not url:
        return {"content": "⚠️ 获取技改信息失败", "file_image": None}
    return {"title": "📖 技改说明：", "content": url}