import asyncio

from .message import MessageType, MessageInterface

class RequestPostType(MessageInterface):
    def __init__(self, user, sender):
        self.user = user
        self.sender = sender

    def build(self, followed_user):
        username = self.user.username
        followed_info = self.user.get_user(followed_user)

        msg = {
            'header': {
                'user': username,
                'followed' : followed_user,
                'type': MessageType.REQUEST_POSTS.value
            },
        }

        return (followed_info, msg)

    def send(self, followed_info, msg):
        try:
            asyncio.run(self.publish_one(followed_info, msg))
        except Exception as e:
            print(e)