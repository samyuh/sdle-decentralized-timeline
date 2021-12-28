import asyncio
from kademlia.network import Server

asyncio.set_event_loop(asyncio.new_event_loop())

async def run():
    loop = asyncio.get_event_loop()
    loop.set_debug(True)

    # Create a node and start listening on port 5678
    node = Server()

    await node.listen(5678)

    loop.run_until_complete(node.listen(8468))

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        node.stop()
        loop.close()

    # Bootstrap the node by connecting to other known nodes, in this case
    # replace 123.123.123.123 with the IP of another node and optionally
    # give as many ip/port combos as you can for other nodes.
    # await node.bootstrap([("127.0.0.1", 5678)])

    # set a value for the key "my-key" on the network
    await node.set("my-key", "my awesome value")

    # get the value associated with "my-key" from the network
    result = await node.get("my-key")
    print(result)


if __name__ == '__main__':
    asyncio.run(run())