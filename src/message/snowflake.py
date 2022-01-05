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

        

    