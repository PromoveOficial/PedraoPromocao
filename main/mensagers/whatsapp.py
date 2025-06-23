import requests
from dotenv import load_dotenv
import os
from flask import request
from flask_restful import Resource
import redis
import logging
from ..utils.responses import *
from ..utils.cache import Cache # Linha estranha mas prometo q funciona kkkkkkkkkk
from ..utils.component import Component

class Whatsapp(Component, Resource):
    def __init__(self):
        super().__init__()

        self.KEY_QUEUE = 'queue:messages'
        self.KEY_USERS = 'users' # Concat the user number
        self.KEY_MESSAGES = 'messages'
        
        load_dotenv(override=True)

        # Get the phone number id from env
        self.PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_NUM_ID")
        # self.logger.debug('Whatsapp phone number loaded')
        
        # Setup all admin numbers
        self.ADMIN_NUMBERS = []
        i = 1
        while os.getenv(f"WHATSAPP_ADMIN_NUM{i}") is not None:
            self.ADMIN_NUMBERS.append(os.getenv(f"WHATSAPP_ADMIN_NUM{i}"))
            i += 1
        # self.logger.debug('Admin numbers loaded.')
        
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
            # self.logger.debug(request_content)
            entry = request_content['entry'][0]['changes'][0]['value']
            
            received_message = entry['messages'][0]
            MESSAGE_KEY = f"{self.KEY_MESSAGES}:{received_message['id']}"
            message = {
                'timestamp': received_message['timestamp'],
                'type': received_message['type'],
                'content': received_message[received_message['type']] 
            }
            
            user_number = entry['contacts'][0]['wa_id']
            USER_KEY = f"{self.KEY_USERS}:{user_number}"
            user = self.redis.json().get(USER_KEY, "$")
            
            if user_number in self.ADMIN_NUMBERS:
                self.logger.debug('admin mando msg.')
            
            # If use isn't in the cache create it and add to the queue
            if user is None:
                user = [{
                    'name': entry['contacts'][0]['profile']['name'],
                    'timestamp': received_message['timestamp'],
                    'mensager': 'whatsapp',
                    'messages': []
                }]
                
                self.redis.zadd(self.KEY_QUEUE, {received_message['timestamp']: user_number})
                
            user = user[0] # Redis return in a list, so to remove it we made the user 
            # in a self list and remove it from it here
            
            user['messages'].append(received_message['id'])
            
            self.redis.json().set(MESSAGE_KEY, "$", message)
            self.redis.json().set(USER_KEY, "$", user)

            # self.logger.debug(self.redis.json().get(USER_KEY, "$"))
            # self.logger.debug(self.redis.json().get(MESSAGE_KEY, "$"))
            # self.logger.debug(self.redis.zcard(self.KEY_QUEUE))
                                                          
            response = RequestComplete()
        except RequestError as e:
            response = e
        except Exception as e:
            self.logger.critical(f"[EXCEPTIONAL ERROR] {e}")
            response = ExceptionalError()
        finally:
            return response.content
    
    
    def sendTextMessage(self, message, number):
        ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
        url = f'https://graph.facebook.com/v22.0/{self.PHONE_NUMBER_ID}/messages'
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
        print(response.status_code)
        print(response.json())
