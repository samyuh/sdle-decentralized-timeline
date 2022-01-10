from configparser import ConfigParser
from typing import Union

import argparse
import ipaddress
import socket
from contextlib import closing

from src.utils.logger import Logger

class Validation:
    @staticmethod
    def valid_ip(ip : str) -> str:
        try:
            ipaddress.ip_address(ip)
        except ValueError:
            raise argparse.ArgumentTypeError(f'IP address is invalid: {ip}')
        return ip

    @staticmethod
    def valid_port(port : Union[int, str]) -> None:
        try:
            port = int(port)
        except:
            raise argparse.ArgumentTypeError(f'Port number should be an integer: {port}')
        if 1 <= port <= 65535:
            return port
        raise argparse.ArgumentTypeError(f'Invalid port: {port}')

    @staticmethod
    def open_port(host : str, port : int) -> bool:
        with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
            if sock.connect_ex((host, port)) == 0:
                return True
            else:
                return False
    
    @staticmethod
    def parse_arguments(config : ConfigParser) -> argparse.Namespace:
        parser = argparse.ArgumentParser()

        # Optional arguments
        parser.add_argument("-i", "--ip", help="IP address", type=Validation.valid_ip, default=config.get('BOOTSTRAP', 'IP'))
        parser.add_argument("-p", "--port", help="Port number", type=Validation.valid_port, default=config.get('BOOTSTRAP', 'PORT'))
        parser.add_argument('-init', '--initial-node', help="Is initial node", dest='initial', action='store_true')
        parser.add_argument('--no-initial', help="Is regular node", dest='initial', action='store_false')
        parser.set_defaults(initial=False)
        arguments = None

        try:
            arguments = parser.parse_args()
        except argparse.ArgumentTypeError as e:
            Logger.log("ArgParser", "error", str(e))
            exit(1)

        return arguments