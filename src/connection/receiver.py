import asyncio
from concurrent.futures import ThreadPoolExecutor

import zmq
from zmq.eventloop.ioloop import IOLoop
from zmq.eventloop.zmqstream import ZMQStream
import json
import threading

from src.connection.message import MessageType
from src.utils.logger import Logger

class MessageReceiver:
    def __init__(self, user, listening_ip : str, listening_port : int) -> None:
        self.user = user
        self.listening_ip = listening_ip
        self.listening_port = listening_port
        self.thread_pool = ThreadPoolExecutor(5)

    def start_listener(self):
        self.ctx = zmq.Context()
        self.socket = self.ctx.socket(zmq.PULL)
        self.socket.linger = 0
        self.socket.bind(f'tcp://{self.listening_ip}:{self.listening_port}')

        self.socketStream = ZMQStream(self.socket)
        self.socketStream.on_recv(self.recv_msg_loop)

        self.listener_action_list = {
            MessageType.TIMELINE_MESSAGE.value: self.user.receive_timeline_message,
            MessageType.REQUEST_TIMELINE.value: self.user.send_timeline,
            MessageType.SEND_TIMELINE.value: self.user.receive_timeline,
        }
        
        self.logger = Logger()

        self.loop = IOLoop.instance()
        threading.Thread(target=self.loop.start, daemon=True).start()

    # --------------------------
    # -- Listener Loop Action --
    # --------------------------
    def listener_action(self, action : int, message) -> None:
        if self.user.verify_signature(message['content'], message['header']['user'], message['header']['signature']):
            self.listener_action_list[action](message)

    # --------------------------
    # -- Listener Loop 
    # --------------------------
    def recv_msg_loop(self, message) -> None:
        message = message[0].decode('utf-8')
        msg = json.loads(message)
        self.logger.log("MessageReceiver", "debug", f"RECV {msg}")

        self.thread_pool.submit(self.listener_action, action=msg['header']['type'], message=msg)