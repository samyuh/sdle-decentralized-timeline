from __future__ import annotations
from typing import List, Type, Optional, TypedDict, TYPE_CHECKING

import pickle
import threading
import time
from datetime import datetime
from dateutil.relativedelta import relativedelta
from pathlib import Path
from src.utils.logger import Logger

if TYPE_CHECKING:
    from src.connection.message import MessageHeader

class MessageLifespan(TypedDict, total=False):
    years: int
    months: int
    days: int
    hours: int
    minutes: int
    seconds: int

class TimelineMessage(TypedDict):
    header: MessageHeader
    content: str

class Timeline:
    username: str
    messages: List[TimelineMessage]
    mutex: Type[threading._RLock]
    message_lifespan: MessageLifespan
    prune_old_messages: bool

    def __init__(self, username: str, message_lifespan: Optional[MessageLifespan] = {}) -> None:
        self.username: str = username
        self.messages: List[TimelineMessage] = []
        
        self.message_lifespan = { "years": 0, "months": 0, "days": 0, "hours": 0, "minutes": 0, "seconds": 0 }
        self.prune_old_messages = False
        if message_lifespan:
            self.prune_old_messages = message_lifespan.get('active', False)
            self.message_lifespan['years'] = message_lifespan.get('years', 0)
            self.message_lifespan['months'] = message_lifespan.get('months', 0)
            self.message_lifespan['days'] = message_lifespan.get('days', 0)
            self.message_lifespan['hours'] = message_lifespan.get('hours', 0)
            self.message_lifespan['minutes'] = message_lifespan.get('minutes', 0)
            self.message_lifespan['seconds'] = message_lifespan.get('seconds', 0)

        self.mutex : Type[threading._RLock] = threading.RLock()
        self.storage_path : str = './storage'

        self.__load_messages()

        thread = threading.Thread(target = self.save_messages_periodically, daemon=True)
        thread.start()

    def get_messages_from_user(self, user : str) -> List[TimelineMessage]:
        messages = []
        for message in self.messages:
            if message['header']['user'] == user: 
                messages.append(message)

        return messages

    def delete_posts(self, user : str) -> List[TimelineMessage]:
        messages = []
        for message in self.messages:
            if message['header']['user'] != user: 
                messages.append(message)

        self.messages = messages

    def add_message(self, message : TimelineMessage) -> None:
        self.mutex.acquire()

        newMessage = message.copy()
        newMessage['header']['seen'] = False

        self.messages.append(newMessage)
        self.mutex.release()

    # TODO: callback message
    def prune_messages(self) -> None:
        if not self.prune_old_messages: return

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
                # TODO: check if message was seen already? No fim
                if (message['header']['time'] > time.mktime(expire_date.timetuple())):
                    messages.append(message)
        
        self.messages = messages
        self.save_messages()
        self.mutex.release()

    def save_messages_periodically(self):
        self.save_messages()
        threading.Timer(1,self.save_messages_periodically).start()

    def save_messages(self) -> None:
        self.mutex.acquire()
        with open(f'{self.storage_path}/{self.username}.pickle', 'wb') as storage:
            timeline_state = {
                'timeline' : self.messages
            }
            pickle.dump(timeline_state, storage, protocol=pickle.HIGHEST_PROTOCOL)

        self.mutex.release()

    def __load_messages(self) -> None:
        self.mutex.acquire()

        try:
            output_file = open(f"{self.storage_path}/{self.username}.pickle", 'rb')
            timeline_state = pickle.load(output_file)
            self.messages = timeline_state['timeline']
            output_file.close()
        except Exception:
            Logger.log("Timeline", "warning", "No previous state. New state initialized")
            Path("./storage").mkdir(parents=True, exist_ok=True)
        
        self.mutex.release()

    def mark_messages_as_seen(self) -> None:
        self.mutex.acquire()

        for message in self.messages:
            message['header']['seen'] = True
        
        # self.save_messages()
        self.mutex.release()

    def __repr__(self) -> str:
        self.mark_messages_as_seen()
        messages = sorted(self.messages, key=lambda msg: msg['header']['time'], reverse=True)
        messages_str = ""
        for message in messages:
            date = datetime.fromtimestamp(message['header']['time']).strftime('%d-%m-%Y %H:%M:%S')
            messages_str += f"\n{message['header']['user']} \u00b7 {date}\n" + f"> {message['content']}\n"

        return f"{self.username}'s timeline\n{messages_str}"