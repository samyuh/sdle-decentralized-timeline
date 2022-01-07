import logging
import asyncio
import json
from threading import Thread

from kademlia.network import Server
from src.server.authentication import Authentication

# TODO: read bootstrap nodes from file.ini, there might be more than one bootstrap node
BOOTSTRAP_NODES = [('127.0.0.1', 8000)]
DEBUG = False

class KademliaServer:
    def __init__(self, ip, port, initial):
        self.ip = ip
        self.port = port
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.initial = initial

        self.__start(BOOTSTRAP_NODES)
        self.__init_modules()

    def __start(self, bootstrap_nodes):
        # handler = logging.StreamHandler()
        # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        # handler.setFormatter(formatter)
        # if DEBUG:
        #     log = logging.getLogger('kademlia')
        #     log.addHandler(handler)
        #     log.setLevel(logging.DEBUG)
        #     loop.set_debug(True)
        
        self.server = Server()
        self.loop.run_until_complete(self.server.listen(interface=self.ip, port=self.port))
        if (not self.initial): self.loop.run_until_complete(self.server.bootstrap(bootstrap_nodes))

        Thread(target=self.loop.run_forever, daemon=True).start()
        
    async def server(self):
        self.server = await asyncio.start_server(
            self.handle_request,
            self.ip,
            self.port
        )

        await self.server.serve_forever()

    def __init_modules(self):
        self.authentication = Authentication(self.server)

    async def locate_user(self, username):
        user_info = await self.server.get(username)
        user_info = json.loads(user_info)

        if user_info is None:
            raise Exception("User doesn't exist")
        return (user_info['ip'], user_info['port'])

    async def locate_followers(self, followers):
        followers_info = {}
        for username in followers:
            followers_info[username] = await self.locate_user(username)

        return followers_info

    async def add_follower(self, user, followed_user):
        user_info = await self.server.get(user)
        followed_info = await self.server.get(followed_user)
        
        if user_info is not None:
            user_info = json.loads(user_info)
            user_info['followers'].append(followed_user)
        else:
            raise Exception(f"You ({followed_user}) don't exist on the server")

        if followed_info is not None:
            followed_info = json.loads(followed_info)
            followed_info['following'].append(user)
        else:
            raise Exception(f"The user {user} doesn't exist on the server")

        await self.server.set(user, json.dumps(user_info))
        await self.server.set(followed_user, json.dumps(followed_info))

    def close(self):
        self.server.stop()