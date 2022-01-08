import asyncio

from src.api.message import *
from src.api.snowflake import Snowflake
class PostMessage:
    @staticmethod
    def send_message(user, message_type, content):
        if message_type == MessageType.POST_MESSAGE:
            PostMessage.publish_message(user, content)
        elif message_type == MessageType.REQUEST_POSTS:
            PostMessage.request_posts(user, content)
        elif message_type == MessageType.SEND_POSTS:
            PostMessage.send_posts(user, content)

    @staticmethod
    def publish_message(user, message):
        username = user.username
        users = user.get_followers()

        snowflake_id = Snowflake.get_id(username, 1)
        snowflake_time = Snowflake.get_time()

        ### Creating Message
        msg = {
            'header': {
                'id': snowflake_id,
                'user': username,
                'type': MessageType.POST_MESSAGE.value,
                'time': snowflake_time,
                'seen': False,
            },
            'content' : message
        }

        try:
            asyncio.run(user.publishing(users, msg)) 
        except Exception as e:
            print(e)

        user.update_timeline(msg)

    @staticmethod
    def request_posts(user, followed_user):
        msg = {
            'header': {
                'user': user.username,
                'followed' : followed_user,
                'type': MessageType.REQUEST_POSTS.value
            },
        }

        followed_info = user.get_user(followed_user)
        asyncio.run(user.send_to_user(followed_info, msg))

    @staticmethod
    def send_posts(user, follower_user):
        follower_info = user.get_user(follower_user)
        timeline = user.get_own_timeline()

        ### Creating Message
        msg = {
            'header': {
                'type': MessageType.SEND_POSTS.value,
            },
            'content' : timeline
        }
        
        asyncio.run(user.send_to_user(follower_info, msg))

