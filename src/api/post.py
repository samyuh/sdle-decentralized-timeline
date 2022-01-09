import asyncio

from src.api.message import MessageType
from src.api.snowflake import Snowflake
from src.server.sender import Sender

class Publish:
    def __init__(self):
        self.sender = Sender()        

    @staticmethod
    async def send_to_user(user, message):
        sender = Sender(user['port'])
        sender.send_msg(message)
        ### Do we need to receive any output to verify if the message was delivered?
        ### Do we need to return any value?

    @staticmethod
    async def publishing(users, message):
        tasks = [Publish.send_to_user(user, message) for user in users.values()]
        await asyncio.gather(*tasks)

class MessageDispatcher:
    def __init__(self, user):
        self.action_dict = {
            MessageType.POST_MESSAGE: PostMessageType(user),
            MessageType.REQUEST_POSTS: RequestPostType(user),
            MessageType.SEND_POSTS: SendPostType(user),
        }

    def send(self, action, message):
        self.action_dict[action].send(message)
        
class PostMessageType:
    def __init__(self, user):
        self.user = user

    def send(self, message):
        username = self.user.username
        users = self.user.get_followers()

        snowflake_id = Snowflake.get_id(username, 1)
        snowflake_time = Snowflake.get_time()

        ### Creating Message
        msg = {
            'header': {
                'id': snowflake_id,
                'user': username,
                'time': snowflake_time,
                'seen': False,
                'type': MessageType.POST_MESSAGE.value,
            },
            'content' : message
        }

        try:
            asyncio.run(Publish.publishing(users, msg)) 
        except Exception as e:
            print(e)

        self.user.update_timeline(msg)

class RequestPostType:
    def __init__(self, user):
        self.user = user

    def send(self, followed_user):
        username = self.user.username
        followed_info = self.user.get_user(followed_user)

        msg = {
            'header': {
                'user': username,
                'followed' : followed_user,
                'type': MessageType.REQUEST_POSTS.value
            },
        }

        asyncio.run(Publish.send_to_user(followed_info, msg))

class SendPostType:
    def __init__(self, user):
        self.user = user

    def send(self, follower_user):
        follower_info = self.user.get_user(follower_user)
        timeline = self.user.get_own_timeline()

        msg = {
            'header': {
                'type': MessageType.SEND_POSTS.value,
            },
            'content' : timeline
        }
        
        asyncio.run(Publish.send_to_user(follower_info, msg))