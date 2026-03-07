import requests
from tenacity import retry, stop_after_attempt, wait_fixed

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Research Opportunity Aggregator)"
}

@retry(stop=stop_after_attempt(3), wait=wait_fixed(5))
def get_request(url):
    r = requests.get(url, headers=HEADERS, timeout=30)
    r.raise_for_status()
    return r