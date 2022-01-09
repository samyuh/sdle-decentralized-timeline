import asyncio

from .message import MessageType, MessageInterface
from .snowflake import Snowflake

class PostMessageType(MessageInterface):
    def __init__(self, user, sender):
        self.user = user
        self.sender = sender

    def build(self, message):
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

        self.user.update_timeline(msg) # TODO: do this in other place?
        return (users, msg)

    def send(self, users, message_built):
        try:
            asyncio.run(self.publish_many(users, message_built)) 
        except Exception as e:
            print(e)