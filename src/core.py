from pathlib import Path
import threading
import pickle

from src.cli import AuthMenu, MainMenu
from src.api import Authentication, User
from src.server import KademliaNode
from zmq.eventloop.ioloop import PeriodicCallback

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

    def load_state(self, username):
        try:
            output_file = open(f"./storage/{username}.pickle", 'rb')
            user_state = pickle.load(output_file)
            self.user.timeline.messages = user_state['timeline']
            output_file.close()
        except Exception:
            # self.logger.log("PROXY", "warning", "No previous state. New state initialize") # TODO: meter no logger
            Path("./storage").mkdir(parents=True, exist_ok=True)

    def save_state(self):
        with open(f'./storage/{self.user.username}.pickle', 'wb') as handle:
            user_state = {
                'timeline' : self.user.timeline.messages
            }
            pickle.dump(user_state, handle, protocol=pickle.HIGHEST_PROTOCOL)

    def cli(self):
        self.authentication = Authentication(self.node)

        answers = AuthMenu.menu()
        self.user = User(*self.authentication.action(answers['method'], answers['information']))

        self.load_state(self.user.username)
        self.periodic_callback = PeriodicCallback(self.save_state, 1000)
        self.periodic_callback.start()

        while True:
            answers = MainMenu().menu()
            self.user.action(answers['action'], answers['information'])