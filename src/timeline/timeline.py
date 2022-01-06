from __future__ import annotations
from typing import TypedDict, List, Type

import pickle
import threading
import os
from datetime import timedelta, datetime
from dateutil.relativedelta import relativedelta

# TODO: Put this in a config file later
MESSAGE_LIFESPAN = {
    "years": 0,
    "months": 0,
    "days": 0,
    "hours": 0,
    "minutes": 2,
    "seconds": 0
}
class MessageHeader(TypedDict):
    id: int
    user: str
    time: str
    seen: bool
class TimelineMessage(TypedDict):
    header: MessageHeader
    content: str

class Timeline:
    username: str
    mutex: Type[threading._RLock]

    def __init__(self, username : str) -> None:
        self.username : str = username
        self.messages : List[TimelineMessage] = []
        self.mutex : Type[threading._RLock] = threading.RLock()
        self.storage_path : str = f'./storage/{self.username}'
        self.__load_messages()

    def get_messages_from_user(self, user : str) -> List[TimelineMessage]:

        messages = []
        for message in self.messages:
            if message['header']['user'] == user: 
                messages.append(message)

        return messages

    def add_message(self, message : TimelineMessage) -> None:
        self.mutex.acquire()

        message['header']['seen'] = False

        self.messages.append(message)

        self.mutex.release()

    def prune_messages(self) -> None:
        expire_date = datetime.now() - relativedelta(years=MESSAGE_LIFESPAN['years'],
                                                    months=MESSAGE_LIFESPAN['months'],
                                                    days=MESSAGE_LIFESPAN['days'],
                                                    hours=MESSAGE_LIFESPAN['hours'],
                                                    minutes=MESSAGE_LIFESPAN['minutes'],
                                                    seconds=MESSAGE_LIFESPAN['seconds'])

        self.mutex.acquire()
        messages = []
        for message in self.messages:
            if message['header']['user'] == self.username:
                messages.append(message)
            else:
                # TODO: Decide date format
                # TODO: check if message was seen already?
                if (datetime.strptime(message['header']['time'], "%Y/%m/%d %H:%M:%S") > expire_date):
                    messages.append(message)
        
        self.messages = messages
        self.save_messages()
        self.mutex.release()

    def save_messages(self) -> None:
        self.mutex.acquire()

        with open(f'{self.storage_path}/timeline.pickle', 'wb') as storage:
            pickle.dump(self.__dict__, storage, protocol=pickle.HIGHEST_PROTOCOL)

        self.mutex.release()

    def __load_messages(self) -> None:
        self.mutex.acquire()
        try:
            os.makedirs(self.storage_path, exist_ok=True)
            with open(f'{self.storage_path}/timeline.pickle', 'rb') as storage:
                self.__dict__.update(pickle.load(storage))

        except Exception:            
            print("ERROR TIMELINE")
        self.mutex.release()

    def mark_messages_as_seen(self) -> None:
        self.mutex.acquire()

        for message in self.messages:
            message['header']['seen'] = True
        
        self.save_messages()
        self.mutex.release()

    def __repr__(self) -> str:
        self.mark_messages_as_seen()

        messages = sorted(self.messages, key=lambda msg: msg['header']['time'], reverse=True)

        messages_str = ""

        for message in self.messages:
            messages_str += f"\n{message['header']['user']} · {message['header']['time']}\n" + f"> {message['content']}\n"

        return f"{self.username}'s timeline\n{messages_str}"