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
        follower_info = self.user.get_user(follower_user)
        timeline = self.user.get_own_timeline()

        message = {
            'header': {
                'type': MessageType.SEND_POSTS.value,
            },
            'content' : timeline
        }
        
        return (follower_info, message)
    
    def send(self, follower_info, message) -> None:
        try:
            asyncio.run(self.sender.publish_one(follower_info, message))
        except Exception as e:
            Logger.log("SendPost", "error", str(e))