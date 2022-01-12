from __future__ import annotations
from typing import List, Tuple, TypedDict, TYPE_CHECKING

import asyncio

from src.connection.message.message import MessageInterface, MessageType
from src.utils.logger import Logger

if TYPE_CHECKING:
    from src.connection.message.message import MessageHeader
    from src.connection.dispatcher import MessageDispatcher
    from src.api.user import User
    from src.api.timeline import TimelineMessage

class SendPostMessage(TypedDict):
    header: MessageHeader
    content: List[TimelineMessage]

class SendPostType(MessageInterface):
    def __init__(self, user : User, sender : MessageDispatcher) -> None:
        super().__init__(user, sender)

    def build(self, follower_user : str) -> Tuple[any, SendPostMessage]:
        username = self.user.username
        timeline = self.user.get_own_timeline()
        signature = self.user.sign(timeline)

        message = {
            'header': {
                'user': username,
                'signature': signature,
                'type': MessageType.SEND_POSTS.value,
            },
            'content': timeline
        }
        
        return message