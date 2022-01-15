from __future__ import annotations
from typing import Union, Tuple, Optional, TYPE_CHECKING

from asyncio.events import AbstractEventLoop
import threading

from src.cli import AuthMenu, MainMenu
from src.api import Authentication, User
from src.server import KademliaNode

if TYPE_CHECKING:
    from src.api.timeline import MessageLifespan

class Core:
    node : KademliaNode
    user : Union[User, None]
    loop : AbstractEventLoop
    timelineMessageLifespan : MessageLifespan
    def __init__(self, ip : str, port : int, listener, bootstrap_node : Tuple[str, int], timelineMessageLifespan : Optional[MessageLifespan] = {}) -> None:
        if bootstrap_node == None:
            self.node = KademliaNode(ip, port)
        else:
            self.node = KademliaNode(ip, port, bootstrap_node)

        self.timelineMessageLifespan = timelineMessageLifespan

        self.user = None   
        self.listener = listener
        self.loop = self.node.run()
        self._run_kademlia_loop()
        
    def _run_kademlia_loop(self) -> None:
        """
        Start running kademlia loop
        """
        threading.Thread(target=self.loop.run_forever, daemon=True).start()

    def cli(self) -> None:
        self.authentication = Authentication(self.listener, self.node)
        answers = AuthMenu.menu()
        
        args = self.authentication.action(answers['method'], answers['information'])

        while not args:
            answers = AuthMenu.menu()
            args = self.authentication.action(answers['method'], answers['information'])

        self.user = User(*args, timelineMessageLifespan=self.timelineMessageLifespan)
        self.user.update_timeline()

        while True:
            answers = MainMenu().menu()
            self.user.action(answers['action'], answers['information'])