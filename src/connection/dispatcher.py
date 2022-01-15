import asyncio
import zmq
import json
from src.utils import Logger

from src.connection.message import MessageType, Snowflake
from src.connection.message import SendTimelineMessage, RequestTimeline, SendTimeline

class MessageDispatcher:
    def __init__(self, user) -> None:
        self.user = user

        self.action_dict = {
            MessageType.TIMELINE_MESSAGE: self.sendTimelineMessage,
            MessageType.REQUEST_TIMELINE: self.requestTimeline,
            MessageType.SEND_TIMELINE: self.sendTimeline,
        }
        
        self.logger = Logger()

        self.snowflake = Snowflake()

    def action(self, action : int, arg : str, arg1=None):
        message_built = self.action_dict[action](self.user, arg, arg1)
        return message_built
    
    #
    # Commands
    #
    def sendTimelineMessage(self, user, message, _):
        message_built = SendTimelineMessage(user).build(message, self.snowflake)
        connections_info = self.user.get_followers_information('connections')

        try:
            asyncio.run(self.publish_many(connections_info, message_built))
        except Exception as e:
            self.logger.log("SendTimelineMessage", "error", str(e))
            exit(-1)

        return message_built

    def requestTimeline(self, user, request_to_user, timeline_owner):
        message_built = RequestTimeline(user).build(timeline_owner)
        connection_info = self.user.get_user(request_to_user, 'connections')
        try:
            asyncio.run(self.publish_one(connection_info, message_built))
        except Exception as e:
            self.logger.log("RequestTimeline", "error", str(e))
            exit(-1)
        
        return message_built

    def sendTimeline(self, user, origin_user, timeline_owner):
        message_built = SendTimeline(user).build(timeline_owner)
        connection_info = self.user.get_user(origin_user, 'connections')
        try:
            asyncio.run(self.publish_one(connection_info, message_built))
        except Exception as e:
            self.logger.log("SendTimeline", "error", str(e))
            exit(-1)
        
        return message_built

    #
    # Publisher Functions
    #
    async def publish_one(self, user : dict, message : dict) -> None:
        self.set_port(user['listening_ip'], user['listening_port'])
        self.send_msg(message)

    async def publish_many(self, users, message) -> None:
        tasks = [self.publish_one(user, message) for user in users]
        await asyncio.gather(*tasks)
    
    def set_port(self, dispatcher_ip : str, dispatcher_port : int) -> None:
        self.ctx = zmq.Context()
        self.socket = self.ctx.socket(zmq.PUSH)
        self.socket.connect(f'tcp://{dispatcher_ip}:{dispatcher_port}')
        

    def send_msg(self, message) -> None:
        json_message = json.dumps(message)
        self.socket.send_string(json_message)

        self.socket.linger = 1000
        self.socket.close()