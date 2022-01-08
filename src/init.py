import threading

from src.server.kademlia_node import KademliaNode
from src.cli import AuthMenu, MainMenu
from src.api.authentication import Authentication
from src.api.post import PostMessage
from src.api.message import *

class InitAPI:
    def __init__(self, ip, port, initial):
        if initial: 
            self.node = KademliaNode(ip, port)
        else: 
            self.node = KademliaNode(ip, port, ("127.0.0.1", 8000))

        self.authentication = Authentication(self.node)
        self.loop = self.node.run()

    def run(self):
        """
        Start running kademlia loop
        """
        threading.Thread(target=self.loop.run_forever, daemon=True).start()

    def close(self):
        pass

    def cli(self):
        ### TODO: Comand pattern here!
        answers = AuthMenu.menu()
        user = None
        if answers['method'] == 'register':
            user = self.authentication.register(answers['information'])
        elif answers['method'] == 'login':
            user = self.authentication.login(answers['information'])

        while True:
            answers = MainMenu().menu()

            if answers['action'] == 'follow':
                user_followed = user.add_follower(answers['information']['username'])
                if user_followed != None: 
                    PostMessage.send_message(user, MessageType.REQUEST_POSTS, user_followed)
            elif answers['action'] == 'post':
                PostMessage.send_message(user, MessageType.POST_MESSAGE, answers['information']['message'])
            elif answers['action'] == 'view':
                user.view_timeline()
            elif answers['action'] == 'logout':
                self.node.close()
                return 0