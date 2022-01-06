from .snowflake import Snowflake

class Header:
    def __init__(self, user, sequence):
        self.id = Snowflake.getId(user, sequence)
        self.user = user
        self.sequence = sequence

    def dump(self):
        return str(self.id) + str(self.user) + str(self.sequence)