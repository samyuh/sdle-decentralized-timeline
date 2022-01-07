import logging
import asyncio
import sys
import threading
import argparse

from utils import Logger, Validation
from configparser import ConfigParser

from kademlia.network import Server

from kademliaNode import KademliaNode

def load_configuration():
    configur = ConfigParser()
    configur.read('./config.ini')
    return configur


if __name__ == "__main__":
    config = load_configuration()

    arguments = Validation.parse_arguments(config)
    Logger.log('Unknown', 'info', f'IP: {arguments.ip}')
    Logger.log('Unknown', 'info', f'Port: {arguments.port}')
    Logger.log('Unknown', 'info', f'Init Node: {arguments.initial}')

    if Validation.open_port(arguments.ip, arguments.port):
        Logger.log('Unknown', 'error', f'Port is occupied: {arguments.port}')
        exit(1)

    node = KademliaNode(arguments.ip, arguments.port, "127.0.0.1", "8000")
    #node = KademliaNode(arguments.ip, arguments.port)
    loop = node.run()
    threading.Thread(target=loop.run_forever, daemon=True).start()

    while True:
        name = input("Enter: ")
        if name == "get":
            asyncio.run(node.get("key"))
        else:
            asyncio.run(node.set(name, "teste"))