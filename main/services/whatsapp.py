import requests
from dotenv import load_dotenv
import os

load_dotenv()

PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_NUM_ID")
ADMIN_NUM = os.getenv("WHATSAPP_ADMIN_NUM1")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")

def admin_numbers():
    return ADMIN_NUM

def sendTextMessage(mensagem, number):
    url = f'https://graph.facebook.com/v22.0/{PHONE_NUMBER_ID}/messages'
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {ACCESS_TOKEN}"
        }
    data = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": f"+{number}",
        "type": "text",
        "text": {
            "preview_url": True,
            "body": "mensagem de teste"

            }
        }


    response = requests.post(url, headers=headers, json=data)
    print(response.status_code)
    print(response.json())
