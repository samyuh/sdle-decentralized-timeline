from typing import Tuple, Union

import asyncio
from kademlia.network import Server

from src.utils.logger import Logger

class KademliaNode:
    ip: str = None
    port: int = None
    bootstrap_node: Tuple[str, int] = None
    server: Server = Server()
    loop: asyncio.AbstractEventLoop = asyncio.new_event_loop()

    def __init__(self, ip: str, port: int, bootstrap_node: Tuple[str, int] = None) -> None:
        """
        Kademlia Node instance.  
        This is object should be created to listen on the network.

        Attributes:
            ip: IP address of the user connecting interface
            port: Open port of the user connecting interface
            bootstrap_node (optional): tuple containing IP address and port of the bootstrap node
            server: server that will be running kademlia server
            loop: loop that will be running server listener

        Args:
            ip: IP address of the user connecting interface
            port: Open port of the user connecting interface
            bootstrap_node (optional): tuple containing IP address and port of the bootstrap node
        """
        self.ip = ip
        self.port = port
        self.bootstrap_node = bootstrap_node
        self.logger = Logger()

    def run(self) -> asyncio.AbstractEventLoop:
        """
        Start listening on the given port.
        Connect to a bootstrap node, if one is given.

        Returns:
            EventLoop
        """
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(self.server.listen(self.port))
        
        if self.bootstrap_node != None:
            self.loop.run_until_complete(self.server.bootstrap([self.bootstrap_node]))
        
        return self.loop

    def set(self, key: str, value: str) -> None:
        """
        Set the given key to the given value in the network.

        Args:
            key: Value 
            value: Value to be set on predetermined key
        Returns:
            None
        """
        asyncio.run_coroutine_threadsafe(self.__set(key, value), self.loop).result()

    def get(self, key : str) -> str:
        """
        Get a key if the network has it.

        Args:
            key: Key to search through nodes in Kademlia
        Returns:
            None if nothing is found, the value of key. 
        """
        return asyncio.run_coroutine_threadsafe(self.__get(key), self.loop).result()

    def close(self) -> None:
        """
        Stop Kademlia server
        """
        asyncio.run_coroutine_threadsafe(self.__close(), self.loop).result()

    async def __set(self, key: str, value: str) -> None:
        await self.server.set(key, value)
        self.logger.log("Kademlia", "debug", f"SET {value}")

    async def __get(self, key: str) -> Union[str, None]:
        result = await self.server.get(key)
        self.logger.log("Kademlia", "deb", f"GET {result}")
        return result
    
    async def __close(self) -> None:
        self.server.stop()