import argparse
import ipaddress
import sys
import socket
from contextlib import closing

from authentication import Authentication
import authentication
from kadmeliaServer import KadServer

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
    parser.add_argument("-i", "--ip", help="IP address", type=valid_ip, default=None)
    parser.add_argument("-p", "--port", help="Port number", type=valid_port, default=None)
    parser.add_argument('-b', '--bootstrap', dest='bootstrap', action='store_true')
    parser.add_argument('--no-bootstrap', dest='bootstrap', action='store_false')
    parser.set_defaults(bootstrap=False)

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
    print(f'Port: {arguments.port}')
    print(f'BS: {arguments.bootstrap}')

    if open_port(arguments.ip, arguments.port):
        print(f'Port is occupied: {arguments.port}')
        sys.exit(1)

    server = KadServer(arguments.ip, arguments.port)

    authentication = Authentication()
    authentication.menu()