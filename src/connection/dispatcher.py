import asyncio
import zmq
import json

from src.connection.message import MessageType, PostMessageType, RequestPostType, SendPostType

class MessageDispatcher:
    def __init__(self, user) -> None:
        self.ctx = zmq.Context()
        self.socket = self.ctx.socket(zmq.PAIR)

        self.action_dict = {
            MessageType.POST_MESSAGE: PostMessageType(user, self),
            MessageType.REQUEST_POSTS: RequestPostType(user, self),
            MessageType.SEND_POSTS: SendPostType(user, self),
        }

    def action(self, action : int, message : str):
        message_built = self.action_dict[action].build(message)
        self.action_dict[action].send(*message_built)

        return message_built[1]

    async def publish_one(self, user : dict, message : dict) -> None:
        self.set_port(user['ip'], user['port'] - 1000)
        self.send_msg(message)

    async def publish_many(self, users, message) -> None:
        tasks = [self.publish_one(user, message) for user in users.values()]
        await asyncio.gather(*tasks)
    
    def set_port(self, dispatcher_ip : str, dispatcher_port : int) -> None:
        self.socket.connect(f'tcp://{dispatcher_ip}:{dispatcher_port}')

    def send_msg(self, message) -> None:
        json_message = json.dumps(message)
        self.socket.send_string(json_message)