import logging
import asyncio
import json
from threading import Thread

from kademlia.network import Server

BOOTSTRAP_NODES = [('127.0.0.1', 8001)] # TODO: read bootstrap nodes from file.ini, there might be more than one bootstrap node
DEBUG = False

class KademliaServer:
    def __init__(self, ip, port, bootstrap):
        self.ip = ip
        self.port = port
        self.loop = None
        self.bootstrap = bootstrap
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
        if DEBUG: loop.set_debug(True)

        loop.run_until_complete(self.server.listen(interface=self.ip, port=self.port))
        if (not self.bootstrap): loop.run_until_complete(self.server.bootstrap(bootstrap_nodes))

        Thread(target=loop.run_forever, daemon=True).start()

    async def register(self, username, password):
        user_info = await self.server.get(username)

        if user_info is None:
            ### fill with the necessary data or create and object that contains all the info instead of a dictionary
            user_data = {
                "password": password,
                "followers": [],
                "following": [],
                "ip": self.ip,
                "port": self.port
            }
            ### Should the response from set be analysed?
            await self.server.set(username, json.dumps(user_data))

            return user_data
        else:
            raise Exception(f'Registration failed. User {username} already exists')
            

    async def login(self, username):
        user_info = await self.server.get(username)

        if user_info is not None:
            return json.loads(user_info)
        else:
            raise Exception(f"Login failed. User {username} doesn't exist")

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

    async def add_follower(self, follower, followed):
        follower_info = await self.server.get(follower)
        followed_info = await self.server.get(followed)

        if follower_info is not None:
            follower_info['following'].append(followed)
        else:
            raise Exception(f"You ({follower}) don't exist on the server")

        if followed_info is not None:
            followed_info['followers'].append(follower)
        else:
            raise Exception(f"The user {followed} doesn't exist on the server")

        await self.server.set(follower, json.dumps(follower_info))
        await self.server.set(followed, json.dumps(followed_info))

    def close(self):
        self.server.stop()