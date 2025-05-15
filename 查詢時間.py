import requests
from bs4 import BeautifulSoup
import json

def get_publish_time(article_url):
    res = requests.get(article_url)
    soup = BeautifulSoup(res.text, 'html.parser')

    ld_json = soup.find("script", type="application/ld+json")
    if ld_json:
        data = json.loads(ld_json.string)
        if "datePublished" in data:
            return data["datePublished"]

    return None

# 測試
url = "https://www.4gamers.com.tw/news/detail/71809/nubs-arena-launch-on-steam-and-free-to-claim-for-24-hours"
print(get_publish_time(url))
