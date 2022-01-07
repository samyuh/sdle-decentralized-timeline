import zmq
import time
import json
from pprint import pprint

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
            pprint(msg)

            ### Add the message to the timeline
            self.user.update_timeline(msg)

