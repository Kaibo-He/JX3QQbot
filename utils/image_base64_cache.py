import base64
import requests

_base64_cache = {}

def url_to_base64_cached(url: str) -> str:
    if url in _base64_cache:
        return _base64_cache[url]
    resp = requests.get(url)
    resp.raise_for_status()
    mime = resp.headers.get("Content-Type", "image/png")
    encoded = base64.b64encode(resp.content).decode("utf-8")
    result = f"data:{mime};base64,{encoded}"
    _base64_cache[url] = result
    return result