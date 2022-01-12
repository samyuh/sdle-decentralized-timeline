from __future__ import annotations
from typing import Tuple, TypedDict, TYPE_CHECKING

import os
import asyncio

from src.connection.message.message import MessageInterface, MessageType
from src.utils.logger import Logger

if TYPE_CHECKING:
    from src.connection.message.message import MessageHeader
    from src.connection.dispatcher import MessageDispatcher
    from src.api.user import User, UserData

class RequestPostMessage(TypedDict):
    header: MessageHeader

class RequestPostType(MessageInterface):
    def __init__(self, user : User, sender : MessageDispatcher) -> None:
        super().__init__(user, sender)

    def build(self, followed_user : str) -> Tuple[UserData, RequestPostMessage]:
        username = self.user.username
        random_check = str(os.urandom(32))
        signature = self.user.sign(random_check)

        message = {
            'header': {
                'user': username,
                'signature': signature,
                'followed': followed_user,
                'type': MessageType.REQUEST_POSTS.value
            },
            'content': random_check,
        }

        return message

    