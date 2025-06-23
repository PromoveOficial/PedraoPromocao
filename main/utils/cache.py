import redis
from logging import Logger
from .component import Component

class Cache(Component):
    def __init__(self, logger: Logger | None):
        super().__init__()
        if logger is not None: 
            self.logger = logger
        
        self.KEY_QUEUE = 'queue:messages'
        self.KEY_USERS = 'users' # Concat the user number
        self.KEY_MESSAGES = 'messages' # Concat the message uuid
        
        self.redis = redis.Redis(host='localhost', port=6379, decode_responses=True)
        
    """
    Receive the users in that format:
        {
            '16315551181': 
                {
                    'name': 'test user name', 
                    'number': '16315551181', 
                    'messages': 
                        [
                            {
                                'id': 'ABGGFlA5Fpa', 
                                'type': 'text', 
                                'timestamp': 1504902988,
                                'content': 
                                    {
                                        'body': 'this is a text message'
                                    }
                            },
                            ...
                        ]
                },
            ...
        }

        and split in this two;
        
        user: 
                {
                    'name': 'test user name',
                    'queue_position': 0 # The position that Queue.add() returned
                    'messenger': 'whatsapp' # For now is just whatsapp
                    'messages': [
                        'ABGGFlA5Fpa',
                        ...
                        # The id of all messages of that instance
                    ]
                }
        ------------------------------------------------------------------------                     
    
        messages:
                {
                    'ABGGFlA5Fpa': 
                        {
                            'timestamp': 1504902988
                            'type': 'text'
                            'content': 
                                {
                                    'body': 'this is a text message'
                                } 
                        }
                    ...
                }
        ------------------------------------------------------------------------

        And then send the data for the cache in redis.
    """

    
    def add(self, users: object):
        for user_number in users:
            KEY_USER = f"{self.KEY_USERS}:{user_number}"
            user_content = users[user_number]
            messages = []
            timestamp = 0
            
            if self.redis.json().get(KEY_USER, "$") is not None:
                user_messages = self.redis.json().get(KEY_USER, "$['messages']")[0]
                messages = user_messages

            
            for message in user_content['messages']:
                if message['id'] in messages_ids:
                    break
                
                messages_ids.append(message['id'])
                
                formatted_message[message['timestamp']] = {
                    'id': message['id'],
                    'type': message['type'],
                    'content': message['content']
                }
                
                # self.logger.debug(self.redis.json().get(KEY_MESSAGE, "$"))
                
            self.redis.zadd(self.KEY_QUEUE, {user_number: timestamp})

            if self.redis.json().get(KEY_USER, "$") is None:
                user = {
                    'name': user_content['name'],
                    'queue': self.redis.zcard(self.KEY_QUEUE) - 1, # The number of elemets in the queue - 1
                    'messenger': 'whatsapp',
                    'messages': messages_ids
                }
                
                self.redis.json().set(KEY_USER, "$", user)
            else:
                self.redis.json().set(KEY_USER, "$['messages']", messages_ids)


            # self.logger.debug(f"Last in queue: {self.redis.zcard(self.KEY_QUEUE)}")
            # self.logger.debug(self.redis.json().get(KEY_USER, "$"))
            
    def get_next(self):
        next_user = self.redis.zpopmin(self.KEY_QUEUE)[0]
        KEY_USER = f"{self.KEY_USERS}:{next_user}"
        user = self.redis.json().get(KEY_USER, "$")[0]
        if user:
            self.redis.json().delete(KEY_USER, "$")
            
        messages = []
        self.logger.debug(user)