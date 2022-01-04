import Snowflake

class Header:
    def __init__(self, host, sequence):
        self.id = Snowflake.getId(header.host, header.sequence)
        self.host = host
        self.sequence = sequence