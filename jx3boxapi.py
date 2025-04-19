import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def create_retry_session(retries=3, backoff_factor=1.0):
    session = requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=[500, 502, 503, 504],
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session

# 根据关键词获取物品列表
def get_item_info(item_name: str):
    session = create_retry_session()
    url = "https://node.jx3box.com/api/node/item/search"
    payload = {
        "keyword": item_name,
        "page": 1,
        "per": 20
    }

    try:
        res = session.post(url, json=payload, timeout=20)
        if res.status_code != 200:
            return None

        result = res.json()
        if result["code"] != 200 or "data" not in result:
            return None

        data = result["data"]["data"]
        return data

    except Exception as e:
        print("Error fetching JX3BoxAPI item searching:", e)
        return None

# 根据物品id获得近30日内区服交易行价格
def get_item_auction(server: str, item_id: str):
    url = "https://next2.jx3box.com/api/auction/"
    payload = {
        "server": server,
        "item_id": item_id,
        "aggregate_type": "daily"
    }
    headers = {
        "Authorization": "Basic Om5leHQgY29tbW9uIHJlcXVlc3Q=",
        "Content-Type": "application/json",
        "Origin": "https://www.jx3box.com",
        "Referer": "https://www.jx3box.com"
    }

    try:
        res = requests.post(url, json=payload, headers=headers, timeout=10)
        if res.status_code != 200:
            return None

        result = res.json()
        
        return result

    except Exception as e:
        print("Error fetch auction data:", e)
        return None