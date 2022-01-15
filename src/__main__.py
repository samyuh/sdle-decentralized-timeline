from configparser import ConfigParser

from .core import Core
from src.utils import Logger, Validation

def load_configuration() -> ConfigParser:
    configuration = ConfigParser()
    configuration.read('./config.ini')
    return configuration

if __name__ == "__main__":
    config = load_configuration()

    timelineMessageLifespan = {
        "active": bool(config.get('MESSAGE_LIFESPAN', 'ACTIVE', fallback=False)),
        "years": config.get('MESSAGE_LIFESPAN', 'YEARS', fallback=0),
        "months": config.get('MESSAGE_LIFESPAN', 'MONTHS', fallback=0),
        "days": config.get('MESSAGE_LIFESPAN', 'DAYS', fallback=0),
        "hours": config.get('MESSAGE_LIFESPAN', 'HOURS', fallback=0),
        "minutes": config.get('MESSAGE_LIFESPAN', 'MINUTES', fallback=0),
        "seconds": config.get('MESSAGE_LIFESPAN', 'SECONDS', fallback=0)
    }

    arguments = Validation.parse_arguments(config)
    if Validation.open_port(arguments.ip, arguments.port):
        Logger.log('Initialization', 'error', f'Port is occupied: {arguments.port}')
        exit(1)

    if Validation.open_port(arguments.listening_ip, arguments.listening_port):
        Logger.log('Initialization', 'error', f'Listener Port is occupied: {arguments.listening_port}')
        exit(1)

    Logger.log('Initialization', 'info', f'Kademlia IP: {arguments.ip}')
    Logger.log('Initialization', 'info', f'Kademlia Port: {arguments.port}')
    Logger.log('Initialization', 'info', f'Listener Port: {arguments.listening_ip}')
    Logger.log('Initialization', 'info', f'Listener Port: {arguments.listening_port}')

    listener = (arguments.listening_ip, int(arguments.listening_port))
    if arguments.init:
        Logger.log('Initialization', 'info', 'Init Node')
        bootstrap_node = None
    else:
        Logger.log('Initialization', 'info', f'Bootstrap IP: {arguments.bootstrap_ip}')
        Logger.log('Initialization', 'info', f'Bootstrap Port: {arguments.bootstrap_port}')
        bootstrap_node = (arguments.bootstrap_ip, int(arguments.bootstrap_port))

    api = Core(arguments.ip, int(arguments.port), listener, bootstrap_node, timelineMessageLifespan)
    api.cli()
    exit(0)
