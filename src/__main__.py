from configparser import ConfigParser

from .core import Core
from src.utils import Logger, Validation

def load_configuration() -> ConfigParser:
    configuration = ConfigParser()
    configuration.read('./config.ini')
    return configuration

if __name__ == "__main__":
    config = load_configuration()

    arguments = Validation.parse_arguments(config)
    Logger.log('Unknown', 'info', f'Kademlia IP: {arguments.ip}')
    Logger.log('Unknown', 'info', f'Kademlia Port: {arguments.port}')
    if arguments.init:
        Logger.log('Unknown', 'info', f'Init Node')
    else:
        Logger.log('Unknown', 'info', f'Bootstrap IP: {arguments.bootstrap_ip}')
        Logger.log('Unknown', 'info', f'Bootstrap Port: {arguments.bootstrap_port}')


    if Validation.open_port(arguments.ip, arguments.port):
        Logger.log('Unknown', 'error', f'Port is occupied: {arguments.port}')
        exit(1)

    api = Core(arguments.ip, int(arguments.port), arguments.init)

    api.cli()

    exit(0)
    