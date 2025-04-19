def split_text(text: str, max_len: int = 1500) -> list[str]:
    return [text[i:i + max_len] for i in range(0, len(text), max_len)]

async def safe_post_long_text(api, guild_id, msg_id, full_text: str, prefix: str = ""):
    chunks = split_text(full_text)
    for idx, chunk in enumerate(chunks):
        content = f"{prefix}\n\n{chunk}" if idx == 0 else chunk
        try:
            await api.post_dms(
                guild_id=guild_id,
                msg_id=msg_id,
                content=content
            )
        except Exception as e:
            _log.error(f"[发送失败] 第{idx+1}段: {e}")
            await api.post_dms(
                guild_id=guild_id,
                msg_id=msg_id,
                content="⚠️ 消息发送失败，请稍后再试"
            )
            break