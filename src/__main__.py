import argparse
import ipaddress
import sys
import socket
from contextlib import closing
import asyncio

from src.authentication import Authentication
from src.server.kademliaServer import KademliaServer
from src.menu import AuthenticationMenu, MainMenu
from src.utils import Logger

def valid_ip(ip):
    try:
        ipaddress.ip_address(ip)
    except ValueError:
        raise argparse.ArgumentTypeError(f'IP address is invalid: {ip}')
    return ip

def valid_port(port):
    try:
        port = int(port)
    except:
        raise argparse.ArgumentTypeError(f'Port number should be an integer: {port}')
    if 1 <= port <= 65535:
        return port
    raise argparse.ArgumentTypeError(f'Invalid port: {port}')

def open_port(host, port):
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        if sock.connect_ex((host, port)) == 0:
            return True
        else:
            return False

def parse_arguments():
    parser = argparse.ArgumentParser()

    # Optional arguments
    parser.add_argument("-i", "--ip", help="IP address", type=valid_ip, default='127.0.0.1')
    parser.add_argument("-p", "--port", help="Port number", type=valid_port, default=8000)
    parser.add_argument('-b', '--bootstrap', help="Is bootstrap node", dest='bootstrap', action='store_true')
    parser.add_argument('--no-bootstrap', help="Is regular node", dest='bootstrap', action='store_false')
    parser.set_defaults(bootstrap=False)

    arguments = None

    try:
        arguments = parser.parse_args()
    except argparse.ArgumentTypeError as e:
        print(str(e))
        sys.exit(1)

    return arguments

def register_coroutine(server, answers, authentication):
    try:
        loop = asyncio.get_event_loop()
        future = asyncio.run_coroutine_threadsafe(authentication.register(server, answers['information']), loop)
        return future.result()
    except Exception as e:
        print(e)

def login_coroutine(server, answers, authentication):
    try:
        loop = asyncio.get_event_loop()
        future = asyncio.run_coroutine_threadsafe(authentication.login(server, answers['information']), loop)
        return future.result()
    except Exception as e:
        print(e)

def post_coroutine(answers, user):
    try:
        loop = asyncio.get_event_loop()
        future = asyncio.run_coroutine_threadsafe(user.post(answers['information']['message']), loop)
        return future.result()
    except Exception as e:
        print(e)

def follow_coroutine(answers, user):
    try:
        loop = asyncio.get_event_loop()
        future = asyncio.run_coroutine_threadsafe(user.follow(answers['information']['username']), loop)
        return future.result()
    except Exception as e:
        print(e)

### This method should be called like this: coroutine_prototype(user.follow(answers['information']['username'])
def coroutine_prorotype(routine):
    try:
        loop = asyncio.get_event_loop()
        future = asyncio.run_coroutine_threadsafe(routine, loop)
        return future.result()
    except Exception as e:
        print(e)

if __name__ == "__main__":
    arguments = parse_arguments()
    logger = Logger()

    logger.log('Unknown', 'info', f'IP: {arguments.ip}')
    logger.log('Unknown', 'info', f'Port: {arguments.port}')
    logger.log('Unknown', 'info', f'BS: {arguments.bootstrap}')

    if open_port(arguments.ip, arguments.port):
        logger.log('Unknown', 'error', f'Port is occupied: {arguments.port}')
        sys.exit(1)

    server = KademliaServer(arguments.ip, arguments.port, arguments.bootstrap)

    authentication = Authentication()
    answers = AuthenticationMenu.menu()
    user = None

    if answers['method'] == 'register':
        user = register_coroutine(server, answers, authentication)
    elif answers['method'] == 'login':
        user = login_coroutine(server, answers, authentication)
        
    print(user)

    answers = MainMenu().menu()
    if answers['action'] == 'post':
        post_coroutine(server, answers, user)
    if answers['action'] == 'follow':
        follow_coroutine(server, answers, user)

    # msg_header = Header(host, user, sequence)
    # msg = Message(msg_header, "Send Message")
    # return msg
