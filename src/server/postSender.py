import zmq

class Sender:
    def __init__(self, port):
        self.ctx = zmq.Context()
        self.socket = self.ctx.socket(zmq.PAIR)

        self.connection_port = port - 1000
        self.socket.connect(f'tcp://127.0.0.1:{self.connection_port}')
    
    def send_msg(self, message):
        self.socket.send_string(message)
        print(f"Sent Message: {message}")