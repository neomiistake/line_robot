import os
import requests
from flask import Flask, request, jsonify
from groq import Groq

app = Flask(__name__)

# 設定 LINE API Key
LINE_ACCESS_TOKEN = "vkCdffDpp0DmpplQOsqzvoNZ6avF4VnwfXBuuWdpsDLI1ZBJn6wcFIW4CN6IAibPE04ZwwSl9Q+fLku+56Vh79b4LyNOqEQvlJWISU16BDpREfrCydAqQZ8i4Txuy5fMfqfozwJHsp/yhipqZMSYBAdB04t89/1O/w1cDnyilFU="
LINE_REPLY_URL = "https://api.line.me/v2/bot/message/reply"

# 設定 Groq API Key
GROQ_API_KEY = "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"
GROQ_MODEL = "llama-3.3-70b-versatile"

# 初始化 Groq Client
client = Groq(api_key=GROQ_API_KEY)

def chat_with_groq(user_message):
    """發送訊息給 Groq API 並取得回應"""
    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[{"role": "user", "content": user_message}]
    )
    return response.choices[0].message.content

def send_line_reply(reply_token, text):
    """將 AI 回應發送回 LINE"""
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LINE_ACCESS_TOKEN}"
    }
    data = {
        "replyToken": reply_token,
        "messages": [{"type": "text", "text": text}]
    }
    requests.post(LINE_REPLY_URL, headers=headers, json=data)

@app.route("/webhook", methods=["POST"])
def webhook():
    """接收來自 LINE 的訊息並回應"""
    data = request.json
    for event in data["events"]:
        if event["type"] == "message" and event["message"]["type"] == "text":
            user_msg = event["message"]["text"]
            reply_token = event["replyToken"]  # 這裡原本遺漏了

            # 使用 Groq 取得回應
            groq_reply = chat_with_groq(user_msg)

            # 傳送回應給 LINE
            send_line_reply(reply_token, groq_reply)

    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

