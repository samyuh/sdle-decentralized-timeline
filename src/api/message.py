from __future__ import annotations
from typing import TypedDict

from enum import Enum

class MessageLifespan(TypedDict, total=False):
    years: int
    months: int
    days: int
    hours: int
    minutes: int
    seconds: int

class MessageHeader(TypedDict):
    id: int
    user: str
    time: str
    seen: bool

class TimelineMessage(TypedDict):
    header: MessageHeader
    content: str

class MessageType(Enum):
    POST_MESSAGE = 1
    REQUEST_POSTS = 2
    SEND_POSTS = 3
