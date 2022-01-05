import logging
import asyncio
import sys

from kademlia.network import Server

if len(sys.argv) != 5:
    print("Usage: python set.py <bootstrap node> <bootstrap port> <key> <value>")
    sys.exit(1)

handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
log = logging.getLogger('kademlia')
log.addHandler(handler)
log.setLevel(logging.DEBUG)

async def run():
    server = Server()
    await server.listen(interface="127.0.0.1",port=8000)
    bootstrap_node = (sys.argv[1], int(sys.argv[2]))
    await server.bootstrap([bootstrap_node])
    await server.set(sys.argv[3], sys.argv[4])
    server.stop()

asyncio.get_event_loop().run_until_complete(run())