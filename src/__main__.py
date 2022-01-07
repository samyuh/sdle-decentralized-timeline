import asyncio
from src.server.kademliaServer import KademliaServer
from src.client.listener import Listener
from src.cli import AuthenticationMenu, MainMenu
from src.utils import Logger, Validation
from configparser import ConfigParser
import threading

def post_coroutine(answers, user):
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        return loop.run_until_complete(user.post(answers['information']['message']))
    except Exception as e:
        print(e)

def follow_coroutine(answers, user):
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        return loop.run_until_complete(user.follow(answers['information']['username']))
    except Exception as e:
        print(e)

def timeline_coroutine(user):
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        return loop.run_until_complete(user.view_timeline())
    except Exception as e:
        print(e)

def logout_coroutine(server):
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        return loop.run_until_complete(server.close())
    except Exception as e:
        print(e)

def load_configuration():
    configur = ConfigParser()
    configur.read('./src/config.ini')
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

    server = KademliaServer(arguments.ip, arguments.port, arguments.initial)
    answers = AuthenticationMenu.menu()
    user = None

    if answers['method'] == 'register':
        user = server.authentication.register_coroutine(answers)
    elif answers['method'] == 'login':
        user = server.authentication.login_coroutine(answers)
        
    listener = Listener(user)
    threading.Thread(target=listener.recv_msg_loop, daemon=True).start()
    while True:
        answers = MainMenu().menu()
        match answers['action']:
            case 'post':
                post_coroutine(answers, user)
            case 'follow':
                follow_coroutine(answers, user)
            case 'match':
                timeline_coroutine(user)
            case 'logout':
                logout_coroutine(server)
                
    # msg_header = Header(host, user, sequence)
    # msg = Message(msg_header, "Send Message")
    # return msg
