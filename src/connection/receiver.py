import zmq
import json
import threading

from src.connection.message import MessageType
from src.utils.logger import Logger

class MessageReceiver:
    def __init__(self, user, listening_ip : str, listening_port : int) -> None:
        self.user = user
        self.ctx = zmq.Context()
        self.socket = self.ctx.socket(zmq.PULL)
        self.socket.linger = 0
        self.socket.bind(f'tcp://{listening_ip}:{listening_port}')
        threading.Thread(target=self.recv_msg_loop, daemon=True).start()

        self.listener_action_list = {
            MessageType.TIMELINE_MESSAGE.value: self.user.receive_timeline_message,
            MessageType.REQUEST_TIMELINE.value: self.user.send_timeline,
            MessageType.SEND_TIMELINE.value: self.user.receive_timeline,
        }
        
        self.Logger = Logger()

    # --------------------------
    # -- Listener Loop Action --
    # --------------------------
    def listener_action(self, action : int, message) -> None:
        if self.user.verify_signature(message['content'], message['header']['user'], message['header']['signature']):
            self.listener_action_list[action](message)

    # --------------------------
    # -- Listener Loop 
    # --------------------------
    def recv_msg_loop(self) -> None:
        while True:
            message = self.socket.recv_string()
            msg = json.loads(message)
            self.Logger.log("MessageReceiver", "info", f"RECV {msg}")

            self.listener_action(msg['header']['type'], msg)
