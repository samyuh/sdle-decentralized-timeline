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

class PostMessage:
    def __init__(self):
        self.action_dict = {
            MessageType.POST_MESSAGE: PostMessageType(),
            MessageType.REQUEST_POSTS: RequestPostType(),
            MessageType.SEND_POSTS: SendPostType(),
        }

    def send(self, action, user, message):
        self.action_dict[action].send(user, message)
        
class PostMessageType(PostMessage):
    def __init__(self):
        pass

    def send(self, user, message):
        username = user.username
        users = user.get_followers()

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

        user.update_timeline(msg)

class RequestPostType(PostMessage):
    def __init__(self):
        pass

    def send(self, user, followed_user):
        msg = {
            'header': {
                'user': user.username,
                'followed' : followed_user,
                'type': MessageType.REQUEST_POSTS.value
            },
        }

        followed_info = user.get_user(followed_user)
        asyncio.run(Publish.send_to_user(followed_info, msg))

class SendPostType(PostMessage):
    def __init__(self):
        pass

    def send(self, user, follower_user):
        follower_info = user.get_user(follower_user)
        timeline = user.get_own_timeline()

        ### Creating Message
        msg = {
            'header': {
                'type': MessageType.SEND_POSTS.value,
            },
            'content' : timeline
        }
        
        asyncio.run(Publish.send_to_user(follower_info, msg))