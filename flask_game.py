import json
import feedparser
from linebot import LineBotApi
from linebot.models import TextSendMessage
from apscheduler.schedulers.blocking import BlockingScheduler

# 設定
RSS_URL = 'https://www.4gamers.com.tw/rss/latest-news'
SEEN_FILE = 'seen.json'
USER_ID = 'U1ae7049f1375aaaed4654403a0023929'
LINE_CHANNEL_TOKEN = 'vkCdffDpp0DmpplQOsqzvoNZ6avF4VnwfXBuuWdpsDLI1ZBJn6wcFIW4CN6IAibPE04ZwwSl9Q+fLku+56Vh79b4LyNOqEQvlJWISU16BDpREfrCydAqQZ8i4Txuy5fMfqfozwJHsp/yhipqZMSYBAdB04t89/1O/w1cDnyilFU='

line_bot_api = LineBotApi(LINE_CHANNEL_TOKEN)

# 讀取已通知過的 ID
try:
    with open(SEEN_FILE, 'r', encoding='utf-8') as f:
        seen_ids = set(json.load(f))
except (FileNotFoundError, json.JSONDecodeError):
    seen_ids = set()

def check_updates():
    global seen_ids
    feed = feedparser.parse(RSS_URL)
    new_ids = set()

    for entry in feed.entries:
        entry_id = getattr(entry, 'id', entry.link)
        if entry_id not in seen_ids and "免費" in entry.title:
            # 發送 LINE 訊息
            msg = f'新免費遊戲：{entry.title}\n{entry.link}'
            line_bot_api.push_message(USER_ID, TextSendMessage(text=msg))
        new_ids.add(entry_id)

    # 更新並儲存已見 ID
    seen_ids |= new_ids
    with open(SEEN_FILE, 'w', encoding='utf-8') as f:
        json.dump(list(seen_ids), f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    # 每 5 分鐘排程一次
    check_updates()  # ← 這行是立即先執行一次
    scheduler = BlockingScheduler()
    scheduler.add_job(check_updates, 'interval', minutes=5, id='rss_checker', replace_existing=True)
    scheduler.start()
