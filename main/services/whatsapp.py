import requests

#temporario, pelo amor de deus N DEIXA VAZAR
ACCESS_TOKEN = 'EACLKdCDWmR4BO1ttOj019ZARqpxJX3fPCjC60z0ZCHKEe0eilTjnFEmAKVhkhIgwhsyY8ZBydZAIBfBYVCu1UFQQrjPu5U0SJ9KbfZChTnvmTBPZCOQdA1Xkmo2YeNNyqIeeZAMjK6F16VQYmr4gqE6Fo5IzwTpeonlllEUOuN9I7q54l08XZAgYuMMETht9xn0xhIMmuCuHPIpfVDXX0WGq7rKhKa9okGj7c643gLYeZCls74n7WelsEVwZDZD' 

PHONE_NUMBER_ID = '673567229167004'

def sendTextMessage():
    url = f'https://graph.facebook.com/v22.0/{PHONE_NUMBER_ID}/messages'
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {ACCESS_TOKEN}"
        }
    data = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": "+5531975064142",
        "type": "text",
        "text": {
            "preview_url": True,
            "body": "mensagem de teste"

            }
        }


    response = requests.post(url, headers=headers, json=data)
    print(response.status_code)
    print(response.json())
