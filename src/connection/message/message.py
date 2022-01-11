from __future__ import annotations
from typing import TypedDict, TYPE_CHECKING

import abc
from enum import Enum

if TYPE_CHECKING:
    from src.api.user import User
    from src.connection.dispatcher import MessageDispatcher


class MessageType(Enum):
    POST_MESSAGE = 1
    REQUEST_POSTS = 2
    SEND_POSTS = 3

class MessageHeader(TypedDict, total=False):
    id: int
    user: str
    time: str
    seen: bool
    type: int

class MessageInterface(abc.ABC):
    user: User 
    sender: MessageDispatcher
    def __init__(self, user : User, sender : MessageDispatcher) -> None:
        self.user = user
        self.sender = sender

    @abc.abstractclassmethod
    def build(self, info):
        pass
    
    @abc.abstractclassmethod
    def send(self, message):
        pass