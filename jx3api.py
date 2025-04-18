# jx3api.py
import requests
import datetime

# 开服状态
def get_server_status(server: str = "梦江南"):
    url = "https://www.jx3api.com/data/server/check"
    payload = {"server": server}

    try:
        res = requests.post(url, json=payload, timeout=5)
        if res.status_code != 200:
            return None

        result = res.json()
        if result["code"] != 200 or "data" not in result:
            return None

        data = result["data"]
        status_text = "✅ 已开服" if data["status"] == 1 else "❌ 维护中"
        update_time = datetime.datetime.fromtimestamp(data["time"]).strftime("%Y-%m-%d %H:%M:%S")

        return {
            "server": data["server"],
            "zone": data["zone"],
            "status": status_text,
            "update_time": update_time
        }

    except Exception as e:
        print("Error fetching JX3API server status:", e)
        return None

# 活动日历
def get_daily_calendar(server: str = "梦江南", num: int = 0):
    url = "https://www.jx3api.com/data/active/calendar"
    payload = {"server": server, "num": num}

    try:
        res = requests.post(url, json=payload, timeout=5)
        if res.status_code != 200:
            return None

        result = res.json()
        if result["code"] != 200 or "data" not in result:
            return None

        data = result["data"]
        return {
            "date": data["date"],
            "week": data["week"],
            "war": data["war"],
            "battle": data["battle"],
            "orecar": data["orecar"],
            "school": data["school"],
            "rescue": data["rescue"],
            "luck": data["luck"],
            "card": data["card"],
            "leader": data.get("leader", None),
            "draw": data.get("draw", None),
            "team": data.get("team", [])
        }

    except Exception as e:
        print("Error fetching calendar:", e)
        return None