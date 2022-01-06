import asyncio

from src.authentication import Authentication
from src.server.kademliaServer import KademliaServer
from src.menu import AuthenticationMenu, MainMenu
from src.utils import Logger, Validation


def register_coroutine(server, answers, authentication):
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        future = asyncio.run_coroutine_threadsafe(authentication.register(server, answers['information']), loop)
        return future.result()
    except Exception as e:
        print(e)

def login_coroutine(server, answers, authentication):
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        future = asyncio.run_coroutine_threadsafe(authentication.login(server, answers['information']), loop)
        return future.result()
    except Exception as e:
        print(e)

def post_coroutine(answers, user):
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        future = asyncio.run_coroutine_threadsafe(user.post(answers['information']['message']), loop)
        return future.result()
    except Exception as e:
        print(e)

def follow_coroutine(answers, user):
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        future = asyncio.run_coroutine_threadsafe(user.follow(answers['information']['username']), loop)
        return future.result()
    except Exception as e:
        print(e)

### This method should be called like this: coroutine_prototype(user.follow(answers['information']['username'])
def coroutine_prorotype(routine):
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        future = asyncio.run_coroutine_threadsafe(routine, loop)
        return future.result()
    except Exception as e:
        print(e)

if __name__ == "__main__":
    arguments = Validation.parse_arguments()
    logger = Logger()

    logger.log('Unknown', 'info', f'IP: {arguments.ip}')
    logger.log('Unknown', 'info', f'Port: {arguments.port}')
    logger.log('Unknown', 'info', f'BS: {arguments.bootstrap}')

    if Validation.open_port(arguments.ip, arguments.port):
        logger.log('Unknown', 'error', f'Port is occupied: {arguments.port}')
        exit(1)

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
