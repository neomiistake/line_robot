from flask import Flask, request, jsonify, abort
from linebot import LineBotApi
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import requests
from linebot.v3.webhook import WebhookHandler

app = Flask(__name__)

# 你的 LINE channel token 與 secret
CHANNEL_ACCESS_TOKEN = "vkCdffDpp0DmpplQOsqzvoNZ6avF4VnwfXBuuWdpsDLI1ZBJn6wcFIW4CN6IAibPE04ZwwSl9Q+fLku+56Vh79b4LyNOqEQvlJWISU16BDpREfrCydAqQZ8i4Txuy5fMfqfozwJHsp/yhipqZMSYBAdB04t89/1O/w1cDnyilFU="
CHANNEL_SECRET = "25b60fae77b43a90b46264fc8a2f896e"

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)
LINE_REPLY_URL = "https://api.line.me/v2/bot/message/reply"


@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers.get('X-Line-Signature')
    body = request.get_data(as_text=True)

    print("收到 LINE Webhook 事件:", body)  # Debugging
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Webhook 驗證失敗")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_all(event):
    print("收到事件:", event)


def handle_message(event):
    user_text = event.message.text
    print("收到使用者訊息:", user_text)  # Debugging

    reply_text = "你說了：" + user_text
    print("回應使用者:", reply_text)  # Debugging

    # 第一種回應方法：使用 SDK 的 reply_message
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_text)
    )

    # 第二種方法（如果你想額外調用外部模型）：
    payload = {
        "model": "llama3.1",  # 根據你的模型名稱調整
        "messages": [{"role": "user", "content": user_text}],
        "stream": False
    }
    try:
        # 注意：請確認這個 API 路徑是否正確（有時候可能是 /v1/chat）
        response = requests.post("http://localhost:11434/api/chat", json=payload)
        response.raise_for_status()
        print("Ollama API 回應狀態碼:", response.status_code)
        print("Ollama API 回應內容:", response.json())
        data = response.json()
        reply_text = data.get("message", "很抱歉，無法生成回覆。")
    except Exception as e:
        print("調用 Ollama API 錯誤：", e)
        reply_text = "調用 AI 模型時發生錯誤。"

    # 使用自定義回覆函式發送回應
    reply_message(event.reply_token, reply_text)

def reply_message(reply_token, text):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {CHANNEL_ACCESS_TOKEN}"
    }
    payload = {
        "replyToken": reply_token,
        "messages": [{"type": "text", "text": text}]
    }

    response = requests.post(LINE_REPLY_URL, headers=headers, json=payload)
    print("Reply status:", response.status_code, response.text)  # Debugging


if __name__ == "__main__":
    app.run(debug=True, port=5000)
