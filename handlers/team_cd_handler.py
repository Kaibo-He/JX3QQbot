from jx3api import get_team_cd_data

def handle_team_cd_query(content: str) -> dict:
    parts = content.strip().split()
    
    if len(parts) < 2:
        return {
            "content": "请输入角色名。"
        }
        
    server = "梦江南"
    name = parts[1]
    if len(parts) >= 3:
        server = parts[2]

    data = get_team_cd_data(server, name)
    if not data or "data" not in data:
        return {"content": "查询失败，可能是区服或角色名错误，或接口超时，请稍后重试。"}

    msg = f"副本进度：{data['roleName']}@{data['serverName']}\n"
    
    if not data["data"]:
        return {"content": f"副本进度：{data['roleName']}@{data['serverName']}\n该角色暂无副本通关记录。"}
    
    for instance in data["data"]:
        boss_names = [b["name"] for b in instance["bossProgress"] if b["finished"]]
        bosses = "，".join(boss_names) if boss_names else "无击杀记录"
        msg += f"♦︎ {instance['mapName']}（{instance['mapType']}）：{bosses}\n"

    return {"content": msg.strip()}