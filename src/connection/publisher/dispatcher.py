from src.connection.message import MessageType, PostMessageType, RequestPostType, SendPostType
from .sender import Sender

import zmq
import json

class MessageDispatcher:
    def __init__(self, user):
        sender = Sender()

        self.action_dict = {
            MessageType.POST_MESSAGE: PostMessageType(user, sender),
            MessageType.REQUEST_POSTS: RequestPostType(user, sender),
            MessageType.SEND_POSTS: SendPostType(user, sender),
        }

    def action(self, action, message):
        # Build message
        message_built = self.action_dict[action].build(message)

        # Send Message
        self.action_dict[action].send(*message_built)

        # Return message Sent
        return message_built[1]

    # def set_port(self, ip, port):

    #     self.socket.connect(f'tcp://{ip}:{port}')

    # def send_msg(self, message):
    #     json_message = json.dumps(message)
    #     self.socket.send_string(json_message)