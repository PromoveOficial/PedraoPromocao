import os
import redis
import re
from logging import Logger
from dotenv import load_dotenv
from .scrapper import getProductInfo
import requests
import uuid

# Setup all admin numbers
load_dotenv(override=True)
ADMIN_NUMBERS = []
i = 1
while os.getenv(f"WHATSAPP_ADMIN_NUM{i}") is not None:
    ADMIN_NUMBERS.append(os.getenv(f"WHATSAPP_ADMIN_NUM{i}"))
    i += 1
    
KEY_QUEUE = 'queue:messages'
KEY_USERS = 'users' # Concat the user number
KEY_MESSAGES = 'messages'
    
PROCESSABLE_MESSAGE_TYPES = ['text']    
    
def admin_command(logger: Logger, command: str):
    adm = Administration_Options(logger)
        
    ENTRYS = {
        'next_user': ['proximo usuario', 'next', 'prox', 'desce o proximo big P'],
        'help': ['ajuda', 'help']
    }    
        
    logger.debug(f"COMANDO: {command}")   
    
    response = {} 
    
    # Consult the cache and send the first user in the     
    if command.lower() in ENTRYS['next_user']:
        response["type"] = "text"
        response["content"] = adm.get_next_client()
    elif command.lower() in ENTRYS['help']:
        response["type"] = "text"
        response["content"] = adm.help(ENTRYS)
    elif re.fullmatch(r"^https:\/\/[\w\.\/\-\#\=\&\?\+\%]+$", command):
        # logger.debug(f"URL: {command}")
        product = getProductInfo(logger, command)
        # product = "OK"
        response['type'] = 'image'
        response['content'] = {}
        response['content']['caption'] = f"Nome: {product['name']}\nPreço: {product['price']}"

        logger.debug(product)
        
        namespace = uuid.NAMESPACE_URL        
        picture_name = uuid.uuid5(namespace, product['name'])
        url_save_temporary_picture = "https://inviting-gecko-seemingly.ngrok-free.app/pedraobot/pictures"
        arguments = {
            'picture-url': product['picture_url'],
            'picture-name': picture_name
        }
        
        save_temporary_picture_request = requests.post(url_save_temporary_picture, params=arguments)
        if save_temporary_picture_request.status_code != 200:
            response['type'] = 'text'
            response['content'] = "Não foi possivel obter a imagem"
            return response
        
        response['content']['image_url'] = f'https://inviting-gecko-seemingly.ngrok-free.app/pedraobot/pictures/{picture_name}'
    else:
        response["type"] = "text"
        response["content"] = "Comando não reconhecido, para obter a lista de comandos digite 'help'"
        
    logger.debug(response)
    return response

class Administration_Options():
    def __init__(self, logger: Logger):
        self.logger = logger

        self.redis = redis.Redis(host='localhost', port=6379, decode_responses=True)

    def help(self, entrys):
        EXPLANATIONS = {
            'next_user': "Lista o próximo usuário na fila",
            'help': "Exibe essa mensagem"
        }
        formatted_lines = []
        for key, commands in entrys.items():
            line = f"{EXPLANATIONS[key]} -> {", ".join(commands)}"
            formatted_lines.append(line)

        return "\n".join(formatted_lines)
    
    def get_next_client(self):
        next_user_number = self.redis.zrange(KEY_QUEUE, 0, 0, withscores=True)[0][0]
        next_user = self.redis.json().get(f"{KEY_USERS}:{next_user_number}", "$")[0]
        
        messages = []
        for message_id in next_user['messages']:
            message_full = self.redis.json().get(f"{KEY_MESSAGES}:{message_id}", "$")[0]
            message_type = message_full['type']
            if message_type not in PROCESSABLE_MESSAGE_TYPES:
                continue
            
            if message_type == 'text':
                messages.append(message_full['content']['body'])
        
        next_user['messages'] = messages
        
        response_model = f"Cliente: {next_user['name']}\nMensagens = {next_user['messages']}\nFrom = {next_user['mensager']}"
        
        # self.logger.debug(response_model)
        return response_model
        
    def add_product(self, url):
        product = getProductInfo(self.logger, url)
        
        return "OK"