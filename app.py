from flask import Flask, request, Response

app = Flask(__name__)

# Token xác minh Webhook
VERIFY_TOKEN = "e9519302e14743eeee435fd03597d4"

@app.route("/", methods=["GET"])
def verify():
    """Xác minh Webhook với Facebook"""
    token_sent = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    # In log kiểm tra token và challenge
    print(f"📌 Received token: {token_sent}")
    print(f"📌 Expected token: {VERIFY_TOKEN}")
    print(f"📌 Received challenge: {challenge}")

    if token_sent == VERIFY_TOKEN and challenge:
        return Response(response=str(challenge), status=200, mimetype="text/plain")
    
    return Response(response="Xác minh thất bại", status=403, mimetype="text/plain")

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))  
    app.run(host="0.0.0.0", port=port, debug=True)
