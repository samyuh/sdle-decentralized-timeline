from __future__ import annotations
from typing import Dict, Tuple, TYPE_CHECKING

import asyncio

from src.connection.message.message import MessageInterface, MessageType
from src.connection.message.snowflake import Snowflake
from src.utils.logger import Logger

if TYPE_CHECKING:
    from src.api.user import User, UserData
    from src.connection.dispatcher import MessageDispatcher
    from src.api.timeline import TimelineMessage

class PostMessageType(MessageInterface):
    def __init__(self, user : User, sender : MessageDispatcher) -> None:
        super().__init__(user, sender)

    def build(self, message : str) -> Tuple[Dict[str, UserData], TimelineMessage]:
        username = self.user.username
        users = self.user.get_followers()

        snowflake_id = Snowflake.get_id(username, 1)
        snowflake_time = Snowflake.get_time()

        signature = self.user.sign(message)
        msg = {
            'header': {
                'id': snowflake_id,
                'user': username,
                'signature': signature,
                'time': snowflake_time,
                'seen': False,
                'type': MessageType.POST_MESSAGE.value,
            },
            'content': message
        }

        return (users, msg)

    def send(self, users, message_built) -> None:
        try:
            asyncio.run(self.sender.publish_many(users, message_built)) 
        except Exception as e:
            Logger.log("PostMessage", "error", str(e))