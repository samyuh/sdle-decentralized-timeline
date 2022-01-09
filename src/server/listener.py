from __future__ import annotations

import zmq
import json

class Listener:
    def __init__(self, user):
        self.user = user
        self.ctx = zmq.Context()
        self.socket = self.ctx.socket(zmq.PAIR)

        self.listening_ip = "127.0.0.1"
        self.listening_port = self.user.port - 1000
        self.socket.bind(f'tcp://{self.listening_ip}:{self.listening_port}')

    def recv_msg_loop(self):
        while True:
            message = self.socket.recv_string()

            msg = json.loads(message)
            print("Received message:")
            print(msg)

            # Parsing in a new thread?
            self.user.listener_action(msg['header']['type'], msg) 
