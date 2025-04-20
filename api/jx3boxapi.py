import requests
import random
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

async def create_retry_session(retries=3, backoff_factor=1.0):
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
async def get_item_info(item_name: str):
    session = create_retry_session()
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Referer": "https://www.jx3box.com/",
        "Origin": "https://www.jx3box.com",
        "Authorization": "Basic Om5vZGUgY29tbW9uIHJlcXVlc3Q=",  # 网页请求中也带这个
        "X-Requested-With": "XMLHttpRequest",  # 很关键！模拟前端异步请求
    }
    
    for per in range(25, 14, -1):
        url = "https://node.jx3box.com/api/node/item/search"
        payload = {
            "keyword": item_name,
            "page": 1,
            "per": per,
            "client": "std"
        }
        print(f"🔍 尝试 per={per} 请求...")

        try:
            res = session.get(url, params=payload, headers=headers, timeout=20)
            if res.status_code != 200:
                print(f"❌ 请求失败 status={res.status_code}")
                print(res.text)
                continue  # 尝试下一个 per

            result = res.json()
            if result.get("code") != 200 or "data" not in result or "data" not in result["data"]:
                print(f"⚠️ 数据无效 code={result.get('code')}, msg={result.get('msg')}")
                continue

            data = result["data"]["data"]
            print(f"✅ 成功获取数据，per={per}, 数量={len(data)}")
            return data

        except Exception as e:
            print(f"❌ 请求异常 per={per}：{e}")
            continue  # 尝试下一个 per
    
    print("❌ 所有尝试失败，未获取到数据")
    return []

# 根据物品id获得近30日内区服交易行价格
async def get_item_auction(server: str, item_id: str):
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