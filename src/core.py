from asyncio.events import AbstractEventLoop
import threading
from typing import Union

from src.cli import AuthMenu, MainMenu
from src.api import Authentication, User
from src.server import KademliaNode

class Core:
    node : KademliaNode
    user : Union[User, None]
    loop : AbstractEventLoop
    
    def __init__(self, ip : str, port : int, init) -> None:
        if init: 
            self.node = KademliaNode(ip, port)
        else:
            self.node = KademliaNode(ip, port, ("127.0.0.1", 8000))

        self.user = None
        self.loop = self.node.run()
        self._run_kademlia_loop()
        
    def _run_kademlia_loop(self) -> None:
        """
        Start running kademlia loop
        """
        threading.Thread(target=self.loop.run_forever, daemon=True).start()

    def cli(self) -> None:
        self.authentication = Authentication(self.node)

        answers = AuthMenu.menu()
        self.user = User(*self.authentication.action(answers['method'], answers['information']))
        
        if answers['method'] == 'login':
            self.user.update_state()

        while True:
            answers = MainMenu().menu()
            self.user.action(answers['action'], answers['information'])