import requests
import datetime
from config_loader import get_jx3api_auth
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

# 开服状态
async def get_server_status(server: str = "梦江南"):
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
async def get_daily_calendar(server: str = "梦江南", num: int = 0):
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

# 角色名片
async def get_role_qqshow(server: str, name: str):
    url = "https://www.jx3api.com/data/show/card"
    auth = get_jx3api_auth()

    payload = {
        "server": server,
        "name": name,
        "token": auth["token"]
    }

    try:
        res = requests.post(url, json=payload, timeout=5)
        if res.status_code != 200:
            return None

        result = res.json()
        if result.get("code") != 200 or not result.get("data"):
            return None

        return result["data"]

    except Exception as e:
        print("Error fetching card:", e)
        return None
    
# 角色装备
async def get_role_attribute(server: str, name: str):
    url = "https://www.jx3api.com/data/role/attribute"
    auth = get_jx3api_auth()
    
    payload = {
        "server": server,
        "name": name,
        "ticket": auth["ticket"],
        "token": auth["token"]
    }
    
    try:
        session = requests.Session()
        retry_strategy = Retry(total=2, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("https://", adapter)

        res = session.post(url, json=payload, timeout=20)
        if res.status_code != 200:
            return None

        result = res.json()
        if result.get("code") != 200 or "data" not in result:
            return None

        return result["data"]
    except Exception as e:
        print("Error fetching role attribute:", e)
        return None
    
# 副本CD
async def get_team_cd_data(server: str, name: str):
    url = "https://www.jx3api.com/data/role/teamCdList"
    auth = get_jx3api_auth()

    payload = {
        "server": server,
        "name": name,
        "ticket": auth["ticket"],
        "token": auth["token"]
    }

    try:
        res = requests.post(url, json=payload, timeout=10)
        if res.status_code != 200:
            return None
        result = res.json()
        if result.get("code") != 200 or "data" not in result:
            return None
        return result["data"]
    except Exception as e:
        print("副本CD请求失败:", e)
        return None
    
# 黑市物价
async def get_trade_data(server: str, name: str):
    url = "https://www.jx3api.com/data/trade/records"
    auth = get_jx3api_auth()
    
    payload = {
        "server": server,
        "name": name,
        "token": auth["token"]
    }
    
    try:
        session = requests.Session()
        retry_strategy = Retry(total=2, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("https://", adapter)

        res = session.post(url, json=payload, timeout=20)
        if res.status_code != 200:
            return None

        result = res.json()
        if result.get("code") != 200 or "data" not in result:
            return None

        return result["data"]
    except Exception as e:
        print("Error fetching trade date:", e)
        return None
    
# 金币价格
async def get_gold_price(server: str):
    url = "https://www.jx3api.com/data/trade/demon"
    auth = get_jx3api_auth()
    
    payload = {
        "server": server,
        "token": auth["token"]
    }
    
    try:
        res = requests.post(url, json=payload, timeout=5)
        if res.status_code != 200:
            return None

        result = res.json()
        if result["code"] != 200 or "data" not in result:
            return None

        data = result["data"][0]
        return {
            "date": data["date"],
            "tieba": data["tieba"],
            "wanbaolou": data["wanbaolou"]
        }

    except Exception as e:
        print("Error fetching calendar:", e)
        return None
    
# 资历分布
async def get_role_achievement(server: str, name: str):
    url = "https://www.jx3api.com/data/tuilan/achievement"
    auth = get_jx3api_auth()
    
    payload = {
        "server": server,
        "name": name,
        "class": 1,
        "ticket": auth["ticket"],
        "token": auth["token"]
    }
    
    try:
        session = requests.Session()
        retry_strategy = Retry(total=2, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("https://", adapter)

        res = session.post(url, json=payload, timeout=20)
        if res.status_code != 200:
            return None

        result = res.json()
        if result.get("code") != 200 or "data" not in result:
            return None

        return result["data"]
    except Exception as e:
        print("Error fetching role attribute:", e)
        return None
    
# 奇遇记录
async def get_luck_records(server: str, name: str):
    url = "https://www.jx3api.com/data/luck/adventure"
    auth = get_jx3api_auth()
    
    payload = {
        "server": server,
        "name": name,
        "ticket": auth["ticket"],
        "token": auth["token"]
    }
    
    try:
        session = requests.Session()
        retry_strategy = Retry(total=2, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("https://", adapter)

        res = session.post(url, json=payload, timeout=20)
        if res.status_code != 200:
            return None

        result = res.json()
        if result.get("code") != 200 or "data" not in result:
            return None

        return result["data"]
    except Exception as e:
        print("Error fetching role attribute:", e)
        return None
    
# 团队招募
async def get_team_records(server: str, keyword: str):
    url = "https://www.jx3api.com/data/member/recruit"
    auth = get_jx3api_auth()
    
    payload = {
        "server": server,
        "keyword": keyword,
        "token": auth["token"]
    }
    
    try:
        session = requests.Session()
        retry_strategy = Retry(total=2, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("https://", adapter)

        res = session.post(url, json=payload, timeout=20)
        if res.status_code != 200:
            return None

        result = res.json()
        if result.get("code") != 200 or "data" not in result:
            return None

        return result["data"]
    except Exception as e:
        print("Error fetching role attribute:", e)
        return None
