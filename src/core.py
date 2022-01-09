import threading

from src.cli import AuthMenu, MainMenu
from src.api import Authentication, PostMessage, MessageType
from src.server import KademliaNode, Listener

class Core:
    def __init__(self, ip, port, initial):
        if initial: 
            self.node = KademliaNode(ip, port)
        else: 
            self.node = KademliaNode(ip, port, ("127.0.0.1", 8000))

        self.user = None
        self.loop = self.node.run()
        self._run_kademlia_loop()
        
    def _run_kademlia_loop(self):
        """
        Start running kademlia loop
        """
        threading.Thread(target=self.loop.run_forever, daemon=True).start()

    def _run_listener(self):
        """
        Start post listener
        """
        self.listener = Listener(self.user)
        threading.Thread(target=self.listener.recv_msg_loop, daemon=True).start()

    def cli(self):
        self.authentication = Authentication(self.node)

        ### TODO: Comand pattern here!
        answers = AuthMenu.menu()
        if answers['method'] == 'register':
            self.user = self.authentication.register(answers['information'])
        elif answers['method'] == 'login':
            self.user = self.authentication.login(answers['information'])

        if self.user != None:
            self._run_listener()
        else:
            print("Error while creating a user")
            exit(1)

        while True:
            answers = MainMenu().menu()
            
            self.user.action(answers['action'], answers['information'])