import os
import requests
from flask import Flask, request

app = Flask(__name__)

# Facebook Page Access Token
PAGE_ACCESS_TOKEN = "THAY_BẰNG_PAGE_ACCESS_TOKEN_CỦA_BẠN"
VERIFY_TOKEN = "e9519302e14743eeee435fd03597d4"  # Token dùng để xác minh Webhook

@app.route("/", methods=["GET"])
def verify():
    """Xác minh Webhook với Facebook"""
    token_sent = request.args.get("hub.verify_token")
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return "Xác minh thất bại", 403

@app.route("/", methods=["POST"])
def webhook():
    """Nhận tin nhắn từ Facebook Messenger"""
    data = request.get_json()
    if data.get("object") == "page":
        for entry in data.get("entry", []):
            for message_event in entry.get("messaging", []):
                if message_event.get("message"):
                    handle_message(message_event)
    return "OK", 200

def handle_message(event):
    """Xử lý tin nhắn và gửi phản hồi"""
    sender_id = event["sender"]["id"]
    message_text = event["message"]["text"]

    # Gửi phản hồi đơn giản (có thể thay bằng OpenAI GPT-4 sau này)
    response_text = f"Bạn vừa gửi: {message_text}"
    
    send_message(sender_id, response_text)

def send_message(recipient_id, text):
    """Gửi tin nhắn đến người dùng"""
    url = f"https://graph.facebook.com/v12.0/me/messages?access_token={PAGE_ACCESS_TOKEN}"
    payload = {
        "recipient": {"id": recipient_id},
        "message": {"text": text},
    }
    headers = {"Content-Type": "application/json"}
    requests.post(url, json=payload, headers=headers)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Sử dụng port do Render cấp
    app.run(host="0.0.0.0", port=port, debug=True)
