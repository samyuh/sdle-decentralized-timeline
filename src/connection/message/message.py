from __future__ import annotations

import abc
from typing import TypedDict
from enum import Enum

class MessageHeader(TypedDict):
    id: int
    user: str
    time: str
    seen: bool

class MessageType(Enum):
    POST_MESSAGE = 1
    REQUEST_POSTS = 2
    SEND_POSTS = 3

class MessageInterface(abc.ABC):
    def __init__(self, user, sender):
        self.user = user
        self.sender = sender
    
    @abc.abstractclassmethod
    def build(self, info):
        pass
    
    @abc.abstractclassmethod
    def send(self, message):
        pass