from src.connection.message import MessageType, PostMessageType, RequestPostType, SendPostType

import asyncio
import zmq
import json

class MessageDispatcher:
    def __init__(self, user):
        self.ctx = zmq.Context()
        self.socket = self.ctx.socket(zmq.PAIR)

        self.action_dict = {
            MessageType.POST_MESSAGE: PostMessageType(user, self),
            MessageType.REQUEST_POSTS: RequestPostType(user, self),
            MessageType.SEND_POSTS: SendPostType(user, self),
        }

    def action(self, action, message):
        message_built = self.action_dict[action].build(message)
        self.action_dict[action].send(*message_built)

        return message_built[1]

    async def publish_one(self, user, message):
        self.set_port(user['ip'], user['port'] - 1000)
        self.send_msg(message)

    async def publish_many(self, users, message):
        tasks = [self.publish_one(user, message) for user in users.values()]
        await asyncio.gather(*tasks)
    
    def set_port(self, dispatcher_ip, dispatcher_port):
        self.socket.connect(f'tcp://{dispatcher_ip}:{dispatcher_port}')

    def send_msg(self, message):
        json_message = json.dumps(message)
        self.socket.send_string(json_message)