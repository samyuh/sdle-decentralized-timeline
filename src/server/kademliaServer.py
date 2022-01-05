import logging
import asyncio
from threading import Thread

from kademlia.network import Server

BOOTSTRAP_NODES = [('127.0.0.1', 8001)] # TODO: read bootstrap nodes from file.ini, there might be more than one bootstrap node
DEBUG = False

class KademliaServer:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.loop = None
        
        self.start(BOOTSTRAP_NODES)

    def start(self, bootstrap_nodes):
        
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)

        if DEBUG:
            log = logging.getLogger('kademlia')
            log.addHandler(handler)
            log.setLevel(logging.DEBUG)

        self.server = Server()

        loop = asyncio.get_event_loop()
        # loop.set_debug(True)

        loop.run_until_complete(self.server.listen(interface=self.ip, port=self.port))
        loop.run_until_complete(self.server.bootstrap(bootstrap_nodes))

        Thread(target=loop.run_forever, daemon=True).start()

    async def register(self, username):
        user = await self.server.get(username)

        if user is None:
            ### fill with the necessary data or create and object that contains all the info instead of a dictionary
            user_data = {
                "followers": [],
                "following": [],
                "ip": self.ip,
                "port":self.port
            }
            ### Should the response from set be analysed?
            await self.server.set(username, user_data)
        else:
            ### Should an exception be raised instead?
            print(f"User already exists")

    def close(self):
        self.server.stop()