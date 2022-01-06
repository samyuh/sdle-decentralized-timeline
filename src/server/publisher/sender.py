import zmq

class Sender:
    def __init__(self, port):
        self.ctx = zmq.Context()
        self.socket = self.ctx.socket(zmq.REQ)
        connection_port = port - 1000
        self.socket.connect(f'tcp://127.0.0.1:{connection_port}')
    
    def send_msg(self, message):
        #message = "Hello world"
        self.socket.send_string(message)
        print(f"Sent Message: {message}")

        ### Receber uma reply de confirmação?
        # msg = socket.recv()
        # print(f"Received Message: {msg})