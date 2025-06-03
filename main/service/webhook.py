from flask import Flask, request

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    print(request.json)
    print(request.headers)
    print(request.host_url)
    return 'Webhook received!', 200