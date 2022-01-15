from typing import Tuple
import time
import ntplib

from src.utils import Logger

class Snowflake:
    """
    Snowflake IDs, or snowflakes, are a form of unique identifier used in distributed computing.
    The format was created by Twitter and is used for the IDs of tweets.
    The format has been adopted by other companies, including Discord, and Instagram, which uses a modified version.

    Source: https://en.wikipedia.org/wiki/Snowflake_ID
    """
    def __init__(self): 
        self.servers = ['0.pool.ntp.org',
                    '1.pool.ntp.org',
                    '2.pool.ntp.org',
                    '3.pool.ntp.org']

        self.__set_drift()
        self.logger = Logger()

    def __set_drift(self):
        self.clock_drift = self.__get_ntp_time() - (int(time.time()))

    def __get_ntp_time(self) -> int:
        client = ntplib.NTPClient()
        for server in self.servers:
            try:    
                resp = client.request(server)
                return int(resp.tx_time)
            except Exception:
                self.logger.log("Snowflake", "error", f"Could not fetch time from NTP server ({server}).")

        return int(time.time())

    def get_id(self, host : str, sequence : int) -> Tuple[str,int]:
        epoch = int(time.time()) + self.clock_drift
        return f"{epoch}{host}{sequence}", epoch
