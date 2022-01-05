from ..timeline import Timeline

class User:
    def __init__(self, server, username, password):
        self.username = username
        self.password = password
        self.server = server
        self.followers = []
        self.following = {} # { username : last_msg_received }
        self.timeline = Timeline()

    def post(self, message):
        pass

    def follow(self, username):
        pass

    def get_suggestions(self):
        pass
