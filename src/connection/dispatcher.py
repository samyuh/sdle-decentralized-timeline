import asyncio
import zmq
import json
from src.utils import Logger

from src.connection.message import MessageType, PostMessageType, RequestPostType, SendPostType

class MessageDispatcher:
    def __init__(self, user) -> None:
        self.ctx = zmq.Context()
        self.socket = self.ctx.socket(zmq.PUSH)
        self.socket.linger = 0
        self.user = user

        self.action_dict = {
            MessageType.POST_MESSAGE: self.sendPostMessage,
            MessageType.REQUEST_POSTS: self.sendRequestPost,
            MessageType.SEND_POSTS: self.sendPosts,
        }

    def action(self, action : int, arg : str):
        message_built = self.action_dict[action](self.user, arg)
        return message_built
    
    def sendPostMessage(self, user, message):
        print("HERE 1")
        message_built = PostMessageType(user, self).build(message)

        #users = self.user.get_followers()
        connections_info = self.user.get_followers('connections')
        try:
            print("here: " + str(connections_info))
            asyncio.run(self.publish_many(connections_info, message_built))
        except Exception as e:
            Logger.log("SendPost", "error", str(e))
            exit(-1)

        return message_built

    def sendRequestPost(self, user, followed_username):
        print("HERE 2")
        message_built = RequestPostType(user, self).build(followed_username)

        connection_info = self.user.get_user(followed_username, 'connections')
        try:
            asyncio.run(self.publish_one(connection_info, message_built))
        except Exception as e:
            Logger.log("RequestPost", "error", str(e))
            exit(-1)
        
        return message_built

    def sendPosts(self, user, follower_user):
        message_built = SendPostType(user, self).build(follower_user)
        connection_info = self.user.get_user(follower_user, 'connections')
        try:
            asyncio.run(self.publish_one(connection_info, message_built))
        except Exception as e:
            Logger.log("SendPost RequestPost", "error", str(e))
            exit(-1)
        
        return message_built

    async def publish_one(self, user : dict, message : dict) -> None:
        self.set_port(user['listening_ip'], user['listening_port'])
        self.send_msg(message)

    async def publish_many(self, users, message) -> None:
        tasks = [self.publish_one(user, message) for user in users.values()]
        print(tasks)
        await asyncio.gather(*tasks)
    
    def set_port(self, dispatcher_ip : str, dispatcher_port : int) -> None:
        self.socket.connect(f'tcp://{dispatcher_ip}:{dispatcher_port}')

    def send_msg(self, message) -> None:
        json_message = json.dumps(message)
        self.socket.send_string(json_message)