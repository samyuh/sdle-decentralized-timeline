import asyncio
from kademlia.network import Server

class KademliaNode:
    def __init__(self, ip, port, bootstrap_ip=None, bootstrap_port=None):
        self.ip = ip
        self.port = port
        self.bootstrap_ip = bootstrap_ip
        self.bootstrap_port = bootstrap_port

        self.kademliaServer = Server()
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

    def run(self):
        self.loop.run_until_complete(self.kademliaServer.listen(int(self.port)))
        
        if self.bootstrap_ip != None:
            bootstrap_node = (self.bootstrap_ip, int(self.bootstrap_port))
            self.loop.run_until_complete(self.kademliaServer.bootstrap([bootstrap_node]))
        
        return self.loop
    
    def set(self, key, value):
        return asyncio.run_coroutine_threadsafe(self.__set(key, value), self.loop).result()

    def get(self, key):
        return asyncio.run_coroutine_threadsafe(self.__get(key), self.loop).result()

    async def __set(self, key, value):
        await self.kademliaServer.set(key, value)
        return True

    async def __get(self, key):
        result = await self.kademliaServer.get(key)
        print("Get result:", result)
        return result