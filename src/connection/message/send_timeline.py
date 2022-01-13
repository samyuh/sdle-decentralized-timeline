from __future__ import annotations
from typing import List, Tuple, TypedDict, TYPE_CHECKING

from src.connection.message.message import MessageInterface, MessageType

if TYPE_CHECKING:
    from src.connection.message.message import MessageHeader
    from src.api.user import User
    from src.api.timeline import TimelineMessage

class SendPostMessage(TypedDict):
    header: MessageHeader
    content: List[TimelineMessage]

class SendTimeline(MessageInterface):
    def __init__(self, user : User):
        super().__init__(user)

    def build(self, timeline_owner : str) -> Tuple[any, SendPostMessage]:
        username = self.user.username
        timeline = self.user.get_timeline(timeline_owner)
        signature = self.user.sign(timeline)

        message = {
            'header': {
                'user': username,
                'timeline_owner': timeline_owner,
                'signature': signature,
                'type': MessageType.SEND_TIMELINE.value,
            },
            'content': timeline
        }
        
        return message