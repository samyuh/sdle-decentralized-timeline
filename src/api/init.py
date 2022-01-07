import threading
from src.server.kademliaNode import KademliaNode
from src.cli import AuthMenu, MainMenu
from .authentication import Authentication

class InitAPI:
    def __init__(self, ip, port, initial):
        if initial: 
            self.node = KademliaNode(ip, port)
        else: 
            self.node = KademliaNode(ip, port, "127.0.0.1", "8000")

        self.authentication = Authentication(self.node)
        self.loop = self.node.run()

    def run(self):
        threading.Thread(target=self.loop.run_forever, daemon=True).start()

    def cli(self):
        answers = AuthMenu.menu()
        user = None
        if answers['method'] == 'register':
            user = self.authentication.register(answers['information'])
        elif answers['method'] == 'login':
            user = self.authentication.login(answers['information'])

        while True:
            answers = MainMenu().menu()
            match answers['action']:
                case 'follow':
                    user.add_follower(answers['information']['username'])
                case 'post':
                    return 0
                case 'match':
                    return 0
                case 'logout':
                    return 0