from flask import Flask, request
import requests
import json
from openai_main import ask_ollama  # 這是你的 Ollama 啟動程式
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

# 讀取 LINE Bot 設定 (請確認你的 `config.json` 有這些設定)
with open("config.json", "r") as f:
    config = json.load(f)
LINE_CHANNEL_ACCESS_TOKEN = config["LINE_CHANNEL_ACCESS_TOKEN"]
LINE_CHANNEL_SECRET = config["LINE_CHANNEL_SECRET"]

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        return "Invalid signature", 400

    return "OK"

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_text = event.message.text  # 取得使用者輸入
    ollama_response = ask_ollama(user_text)  # 發送給 Ollama 進行處理
    reply = TextSendMessage(text=ollama_response)
    line_bot_api.reply_message(event.reply_token, reply)

if __name__ == "__main__":
    app.run(port=5000, debug=True)
