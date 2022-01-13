from __future__ import annotations
from typing import Dict, Tuple, TYPE_CHECKING

from src.connection.message.message import MessageInterface, MessageType
from src.connection.message.snowflake import Snowflake
from src.utils.logger import Logger

if TYPE_CHECKING:
    from src.api.user import User, UserData
    from src.api.timeline import TimelineMessage

class SendTimelineMessage(MessageInterface):
    def __init__(self, user : User) -> None:
        super().__init__(user)

    def build(self, message : str) -> Tuple[Dict[str, UserData], TimelineMessage]:
        username = self.user.username
        snowflake_id, snowflake_time = Snowflake.get_id(username, 1)
        
        signature = self.user.sign(message)
        msg = {
            'header': {
                'id': snowflake_id,
                'user': username,
                'signature': signature,
                'time': snowflake_time,
                'seen': False,
                'type': MessageType.TIMELINE_MESSAGE.value,
            },
            'content': message
        }

        return msg

    