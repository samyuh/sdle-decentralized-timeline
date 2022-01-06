from __future__ import annotations
from typing import TypedDict, List, Type, Optional

import pickle
import threading
import os
from datetime import timedelta, datetime
from dateutil.relativedelta import relativedelta

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

class Timeline:
    username: str
    mutex: Type[threading._RLock]
    message_lifespan: MessageLifespan

    def __init__(self, username : str, message_lifespan : Optional[MessageLifespan] = {}) -> None:
        self.username : str = username
        self.messages : List[TimelineMessage] = []
        
        self.message_lifespan = { "years": 0, "months": 0, "days": 0, "hours": 0, "minutes": 0, "seconds": 0 }
        if message_lifespan:
            self.message_lifespan['years'] = message_lifespan.get('years', 0)
            self.message_lifespan['months'] = message_lifespan.get('months', 0)
            self.message_lifespan['days'] = message_lifespan.get('days', 0)
            self.message_lifespan['hours'] = message_lifespan.get('hours', 0)
            self.message_lifespan['minutes'] = message_lifespan.get('minutes', 0)
            self.message_lifespan['seconds'] = message_lifespan.get('seconds', 0)

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

        newMessage = message.copy()
        newMessage['header']['seen'] = False

        self.messages.append(newMessage)

        self.mutex.release()

    def prune_messages(self) -> None:
        expire_date = datetime.now() - relativedelta(years=self.message_lifespan['years'],
                                                    months=self.message_lifespan['months'],
                                                    days=self.message_lifespan['days'],
                                                    hours=self.message_lifespan['hours'],
                                                    minutes=self.message_lifespan['minutes'],
                                                    seconds=self.message_lifespan['seconds'])

        self.mutex.acquire()
        messages = []
        for message in self.messages:
            if message['header']['user'] == self.username:
                messages.append(message)
            else:
                # TODO: Date format decided: UNIX time
                # TODO: check if message was seen already? No fim
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