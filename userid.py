from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

line_bot_api = LineBotApi('vkCdffDpp0DmpplQOsqzvoNZ6avF4VnwfXBuuWdpsDLI1ZBJn6wcFIW4CN6IAibPE04ZwwSl9Q+fLku+56Vh79b4LyNOqEQvlJWISU16BDpREfrCydAqQZ8i4Txuy5fMfqfozwJHsp/yhipqZMSYBAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('25b60fae77b43a90b46264fc8a2f896e')

@app.route("/webhook", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_id = event.source.user_id
    print(f'你的 LINE userId 是：{user_id}')
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=f'你的 userId 是：{user_id}')
    )

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
