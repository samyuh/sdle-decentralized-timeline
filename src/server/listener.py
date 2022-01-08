import zmq
import json
from pprint import pprint

from src.api.message import MessageType
from src.api.post import PostMessage

class Listener:
    def __init__(self, user):
        self.user = user
        self.ctx = zmq.Context()
        self.socket = self.ctx.socket(zmq.PAIR)

        self.listening_port = self.user.port - 1000
        self.socket.bind(f'tcp://127.0.0.1:{self.listening_port}')

    def recv_msg_loop(self):
        while True:
            message = self.socket.recv_string()

            msg = json.loads(message)
            print("Received message:")
            print(msg)

            if msg['header']['type'] == MessageType.POST_MESSAGE.value:
                ### Add the message to the timeline
                self.user.update_timeline(msg)
            elif msg['header']['type'] == MessageType.SEND_POSTS.value:
                for message in msg['content']:
                    self.user.update_timeline(message)
            elif msg['header']['type'] == MessageType.REQUEST_POSTS.value:
                ### Send back the list of messages from your timeline
                PostMessage.send_message(self.user, MessageType.SEND_POSTS, msg['header']['user'])
