"""
這是官方的範例

"""

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('UCk1EkAY8VGcSw/TiRpL0qdzjUwRIYLY7t7uyPUYIAaSqtvdQP9h1Xt0H6IyxIq+JWjN3QcIlEd44Tpey9k1Z+aLBvnwKHZra14egx28P1CvdzyRM0Jo5xYRHtYVIHoSEf7dMD5mWK9enZCiKcr3mQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('b3e5715b1fa93be7f7b3b21f3ce4ed86')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)