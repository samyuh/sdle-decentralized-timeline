import argparse
import ipaddress
import sys
import socket
from contextlib import closing

import api

def valid_ip(ip):
    try:
        ip = ipaddress.ip_address(ip)
    except ValueError:
        raise argparse.ArgumentTypeError(f'IP address is invalid: {ip}')
    return ip

def valid_port(port):
    print('aqui')
    cond = (1 <= port <= 65535)
    print('aqui2')
    print(cond)
    print(port.isdigit())
    if port.isdigit() and 1 <= port <= 65535:
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
    parser.add_argument("-i", "--ip", help="IP address", type=valid_ip, default=None)
    parser.add_argument("-p", "--port", help="Port number", type=valid_port, default=None)
    parser.add_argument("-b", "--bootstrap", help="Bootstrap on or off", type=bool, default=False)

    arguments = None

    try:
        arguments = parser.parse_args()
    except argparse.ArgumentTypeError as e:
        print(str(e))
        sys.exit(1)

    return arguments

if __name__ == "__main__":
    arguments = parse_arguments()

    print(f'IP: {arguments.ip}')
    print(f'IP: {arguments.port}')
    print(f'IP: {arguments.bootstrap}')

    if not open_port(arguments.ip, arguments.port):
        print(f'Port is occupied: {arguments.port}')
        sys.exit(1)

    api.API()