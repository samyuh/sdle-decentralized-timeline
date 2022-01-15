from __future__ import annotations
from typing import Tuple, TypedDict, TYPE_CHECKING

import os

from src.connection.message.message import MessageInterface, MessageType

if TYPE_CHECKING:
    from src.connection.message.message import MessageHeader
    from src.api.user import User, UserData

class RequestPostMessage(TypedDict):
    header: MessageHeader

class RequestTimeline(MessageInterface):
    def __init__(self, user : User) -> None:
        super().__init__(user)

    def build(self, timeline_owner : str) -> Tuple[UserData, RequestPostMessage]:
        username = self.user.username
        random_check = str(os.urandom(32))
        signature = self.user.sign(random_check)

        message = {
            'header': {
                'user': username,
                'signature': signature,
                'timeline_owner': timeline_owner,
                'type': MessageType.REQUEST_TIMELINE.value
            },
            'content': random_check,
        }

        return message

    