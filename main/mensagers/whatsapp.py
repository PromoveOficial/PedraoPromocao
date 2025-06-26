import requests
from dotenv import load_dotenv
import os
from flask import request
from flask_restful import Resource
import redis
from ..utils.responses import *
from ..utils.component import Component
from ..administration.admin_options import ADMIN_NUMBERS, admin_command

KEY_QUEUE = 'queue:messages'
KEY_USERS = 'users' # Concat the user number
KEY_MESSAGES = 'messages'

KEY_ENTRYS_PROCESSED = 'entrys'

ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_NUM_ID")


class Whatsapp(Component, Resource):
    def __init__(self):
        super().__init__()
        # self.logger.debug('Whatsapp phone number loaded')
        
        self.redis = redis.Redis(host='localhost', port=6379, decode_responses=True)

    def get(self):
        # Verification proccess for whatsapp webhook
        if  ( 
            request.args.get('hub.mode') == 'subscribe' and
            request.args.get('hub.verify_token') == os.environ.get('VERIFY_TOKEN')
        ):  
            self.logger.info("Webhook verified")
            return int(request.args.get('hub.challenge')), 200

    def post(self):
        try:
            if request.headers.get('Content-Type') != 'application/json':
                raise MethodNotAllowed()
            
            """
                Format data to that format:
                {
                        '16315551181': {
                            'name': 'test user name', 
                            'number': '16315551181', 
                            'messages': 
                                [
                                    {
                                        'id': 'ABGGFlA5Fpa', 
                                        'type': 'text', 
                                        'content': 
                                            {
                                                'body': 'this is a text message'
                                            }, 
                                            'timestamp': 1504902988
                                    },
                                    ...
                                ]
                        },
                        ...
                }
            """
            request_content = request.json
            entry = request_content['entry'][0]['changes'][0]['value']
                        
            espected_object = {'messaging_product', 'metadata', 'contacts', 'messages'}
            if not espected_object.issubset(entry.keys()):
                response = RequestComplete()
                return 
            
            received_message = entry['messages'][0]
            MESSAGE_KEY = f"{KEY_MESSAGES}:{received_message['id']}"
            message = {
                'timestamp': received_message['timestamp'],
                'type': received_message['type'],
                'content': received_message[received_message['type']] 
            }
            
            
            if self.redis.json().get(MESSAGE_KEY, "$") is not None:
                response = RequestComplete()
                return
            
            user_number = entry['contacts'][0]['wa_id']
            USER_KEY = f"{KEY_USERS}:{user_number}"
            user = self.redis.json().get(USER_KEY, "$")
            
            # self.logger.debug(f"{user_number}: {message['content']}")
                        
            if user_number in ADMIN_NUMBERS:
                message_text = message['content']['body']
                self.logger.debug(f"ADMIN: {entry['contacts'][0]['profile']['name']}")
                response = admin_command(self.logger, message_text)
                self.logger.debug(response)
                if response['type'] == 'text':
                    self.sendTextMessage(response['content'], user_number)
                elif response['type'] == 'image':
                    self.sendImageMessage(response['content']['caption'], response['content']['image_url'], user_number)
                
                # self.logger.debug(received_message['id'])
                self.confirm_read(received_message['id'])
                
                response = RequestComplete()
                return
                
            # If use isn't in the cache create it and add to the queue
            if user is None:
                user = [{
                    'name': entry['contacts'][0]['profile']['name'],
                    'timestamp': received_message['timestamp'],
                    'mensager': 'whatsapp',
                    'messages': []
                }]
                
                self.redis.zadd(KEY_QUEUE, {user_number: received_message['timestamp']})
                
            user = user[0] # Redis return in a list, so to remove it we made the user 
            # in a self list and remove it from it here
            
            user['messages'].append(received_message['id'])
            
            self.redis.json().set(MESSAGE_KEY, "$", message)
            self.redis.json().set(USER_KEY, "$", user)
            
            self.confirm_read(received_message['id'])

            # self.logger.debug(self.redis.json().get(USER_KEY, "$"))
            # self.logger.debug(self.redis.json().get(MESSAGE_KEY, "$"))
            # self.logger.debug(self.redis.zcard(KEY_QUEUE))
                                                          
            response = RequestComplete()
        except RequestError as e:
            response = e
        except Exception as e:
            self.logger.critical(f"[EXCEPTIONAL ERROR] {e}")
            response = ExceptionalError()
        finally:
            return response.content
    
    
    def confirm_read(self, messsage_id):
        url = f'https://graph.facebook.com/v22.0/{PHONE_NUMBER_ID}/messages'
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {ACCESS_TOKEN}"
            }
        data = { 
            "messaging_product": "whatsapp", 
            "status": "read", 
            "message_id": f"{messsage_id}" 
        }
        
        response = requests.post(url, headers=headers, json=data)
        self.logger.debug(f"{messsage_id}: {response.json()}")
        
    def sendTextMessage(self, message, number):
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
                "body": f"{message}"
                }
            }
        response = requests.post(url, headers=headers, json=data)
        # self.logger.debug(response.status_code)
        # self.logger.debug(response.json())

    def sendImageMessage(self, caption, image_url, number):
        url = f'https://graph.facebook.com/v22.0/{PHONE_NUMBER_ID}/messages'
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {ACCESS_TOKEN}"
        }
        data = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": f"{number}",
            "type": "image",
            "image": {
                "link": f"{image_url}",
                "caption": f"{caption}"
            }
        }
        
        response = requests.post(url, headers=headers, json=data)
        self.logger.debug(response.json())
