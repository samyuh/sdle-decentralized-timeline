from __future__ import annotations
from typing import TypedDict, TYPE_CHECKING

import abc
from enum import Enum

if TYPE_CHECKING:
    from src.api.user import User

class MessageType(Enum):
    TIMELINE_MESSAGE = 1
    REQUEST_TIMELINE = 2
    SEND_TIMELINE = 3

class MessageHeader(TypedDict, total=False):
    id: int
    user: str
    time: str
    seen: bool
    type: int

class MessageInterface(abc.ABC):
    user: User 

    def __init__(self, user : User) -> None:
        self.user = user

    @abc.abstractclassmethod
    def build(self, info):
        pass