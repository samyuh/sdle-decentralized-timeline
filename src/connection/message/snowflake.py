from typing import Tuple

import calendar
import time
import ntplib
from datetime import datetime





class Snowflake:
    """
    Snowflake IDs, or snowflakes, are a form of unique identifier used in distributed computing. 
    The format was created by Twitter and is used for the IDs of tweets. 
    The format has been adopted by other companies, including Discord, and Instagram, which uses a modified version. 

    Source: https://en.wikipedia.org/wiki/Snowflake_ID
    """
    @staticmethod
    def get_id(host : str, sequence : int) -> Tuple[str,int]:
        
        epoch = Snowflake.get_time()
        return f"{epoch}{host}{sequence}", epoch

    @staticmethod
    def get_time() -> int:
        client = ntplib.NTPClient()
        server = '0.pool.ntp.org'
        resp = client.request(server, version=3)
        
        return int(resp.tx_time)
    
    
