from configparser import ConfigParser

from src.api.init import InitAPI
from src.utils import Logger, Validation

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

    api = InitAPI(arguments.ip, arguments.port, arguments.initial)
    api.run()

    if True: api.cli()
    else: pass # WebAPP
    