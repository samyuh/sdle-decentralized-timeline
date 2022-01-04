from ..timeline import Timeline

class User:
    def __init__(self, username, password, ip, port):
        self.username = username
        self.password = password
        self.ip = ip
        self.port = port
        self.followers = []
        self.following = {} # { username : last_msg_received }
        self.timeline = Timeline()

    def post(self, message):
        pass

    def follow(self, username):
        pass

    def get_suggestions(self):
        pass
