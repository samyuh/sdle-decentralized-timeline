import Snowflake

class Header:
    def __init__(self, host, user, sequence):
        self.id = Snowflake.getId(header.host,sequence)
        self.host = host
        self.user = user
        self.sequence = sequence

    def dump(self):
        return str(self.id) + str(self.host) + str(self.user) + str(self.sequence)