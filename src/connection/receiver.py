import zmq
import json
import threading

from src.connection.message import MessageType
from src.utils.logger import Logger

class MessageReceiver:
    def __init__(self, user, listening_ip : str, listening_port : int) -> None:
        self.user = user

        self.ctx = zmq.Context()
        self.socket = self.ctx.socket(zmq.PAIR)
        self.socket.bind(f'tcp://{listening_ip}:{listening_port}')
        threading.Thread(target=self.recv_msg_loop, daemon=True).start()

        self.listener_action_list = {
            MessageType.POST_MESSAGE.value: self.user.update_timeline,
            MessageType.SEND_POSTS.value: self.user.many_update_timeline,
            MessageType.REQUEST_POSTS.value: self.user.send_message,
        }

    # --------------------------
    # -- Listener Loop Action --
    # --------------------------
    def listener_action(self, action : int, message) -> None:
        self.listener_action_list[action](message)

    # --------------------------
    # -- Listener Loop 
    # --------------------------
    def recv_msg_loop(self) -> None:
        while True:
            message = self.socket.recv_string()

            msg = json.loads(message)
            Logger.log("MessageReceiver", "info", f"RECV {msg}")

            # Parsing in a new thread?
            self.listener_action(msg['header']['type'], msg) 
    
