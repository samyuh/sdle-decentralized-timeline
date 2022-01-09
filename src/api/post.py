import asyncio

from src.api.message import MessageType
from src.api.snowflake import Snowflake
from src.server.sender import Sender

# MESSAGE DISPATCHER
class MessageDispatcher:
    def __init__(self, user):
        self.action_dict = {
            MessageType.POST_MESSAGE: PostMessageType(user),
            MessageType.REQUEST_POSTS: RequestPostType(user),
            MessageType.SEND_POSTS: SendPostType(user),
        }

    def action(self, action, message):
        # Build message
        message_built = self.action_dict[action].build(message)

        # Send Message
        # Integrate with Publish
        self.action_dict[action].send(*message_built)


# MESSAGE BUILDER   
class MessageInterface:
    def __init__(self, user):
        self.user = user
    
    def build(self, info):
        pass

    def send(self, message):
        pass

    async def publish_one(self, user, message):
        sender = Sender(user['port'])
        sender.send_msg(message)

    async def publish_many(self, users, message):
        tasks = [self.publish_one(user, message) for user in users.values()]
        await asyncio.gather(*tasks)

class PostMessageType(MessageInterface):
    def __init__(self, user):
        self.user = user

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

class RequestPostType(MessageInterface):
    def __init__(self, user):
        self.user = user

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

class SendPostType(MessageInterface):
    def __init__(self, user):
        self.user = user

    def build(self, follower_user):
        follower_info = self.user.get_user(follower_user)
        timeline = self.user.get_own_timeline()

        msg = {
            'header': {
                'type': MessageType.SEND_POSTS.value,
            },
            'content' : timeline
        }
        
        return (follower_info, msg)
    
    def send(self, follower_info, msg):
        try:
            asyncio.run(self.publish_one(follower_info, msg))
        except Exception as e:
            print(e)