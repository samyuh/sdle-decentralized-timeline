import calendar
import time
from datetime import datetime

class Snowflake:
    """
    Snowflake IDs, or snowflakes, are a form of unique identifier used in distributed computing. 
    The format was created by Twitter and is used for the IDs of tweets. 
    The format has been adopted by other companies, including Discord, and Instagram, which uses a modified version. 

    Source: https://en.wikipedia.org/wiki/Snowflake_ID
    """

    @staticmethod
    def get_id(host, sequence):
        epoch = calendar.timegm(time.gmtime())
        return f"{epoch}{host}{sequence}"

    @staticmethod
    def get_current_time():
        ### change the final format using the datetime library
        now = datetime.now()
        return now


class Header:
    def __init__(self, user, sequence):
        self.id = Snowflake.getId(user, sequence)
        self.user = user
        self.sequence = sequence

    def dump(self):
        return str(self.id) + str(self.user) + str(self.sequence)

class Message:
    def __init__(self, header, content):
        self.header = header
        self.content = content

    def dump():
        print(f"Message")