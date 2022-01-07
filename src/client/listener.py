import zmq
import time

class Listener:
    def __init__(self, user):
        self.user = user
        self.ctx = zmq.Context()
        self.socket = self.ctx.socket(zmq.REP)
        #self.listening_port = self.user.port - 1000
        #self.socket.bind(f'tcp://127.0.0.1:{self.listening_port}')

    def recv_msg_loop(self):
        while True:
            print("here")
            message = self.socket.recv_string()
            print(f"Received string:{message}")

            ### Add the message to the timeline
            # self.user.update_timeline(message)

            ### Send back a confirmation message?
            # self.socket.send()

