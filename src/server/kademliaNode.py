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
    
    """ 
    This code takes soo much to update!
    Time to run: 10+ seconds somethings

    async def get(self, key):
        result = await self.server.get(key)
        print("Get result:", result)

    async def set(self, key, value):
        await self.server.set(key, value)
    """

    """
    With this one bellow:
    It is created a listner (We could create a listener using asyncio maybe?)
    Launch listener loop each time a set or get is needed
    Velocity: Instantly    
    """
    async def set(self, key, value):
        server = Server()
        await server.listen(8469)

        bootstrap_node = (self.ip, int(self.port))
        await server.bootstrap([bootstrap_node])
        await server.set(key, value)
        server.stop()

    async def get(self, key):
        server = Server()
        await server.listen(8469)

        bootstrap_node = (self.ip, int(self.port))
        await server.bootstrap([bootstrap_node])
        result = await server.get(key)
        server.stop()
        print("Get result:", result)
        return result