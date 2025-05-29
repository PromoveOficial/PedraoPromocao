from flask import Flask, request
from pyngrok import ngrok

class WebhookService:
    def __init__(self, app: Flask):
        self.app = app
        self.ngrok_tunnel = None

    def start_ngrok(self, port: int = 5000):
        """Start ngrok tunnel."""
        self.ngrok_tunnel = ngrok.connect(port)
        print(f"Ngrok tunnel started at {self.ngrok_tunnel}")

    def stop_ngrok(self):
        """Stop ngrok tunnel."""
        if self.ngrok_tunnel:
            ngrok.disconnect(self.ngrok_tunnel.public_url)
            print("Ngrok tunnel stopped.")
            self.ngrok_tunnel = None

    def register_webhook(self, url: str):
        """Register a webhook URL."""
        @self.app.route(url, methods=['POST'])
        def webhook():
            data = request.json
            print(f"Received webhook data: {data}")
            return '', 200