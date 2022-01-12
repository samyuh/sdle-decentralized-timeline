from __future__ import annotations
from typing import Callable, Tuple, TypedDict, TYPE_CHECKING

from Crypto.PublicKey import RSA
import json
import os
import hashlib


from src.utils.logger import Logger

if TYPE_CHECKING:
    from src.server.kademlia_node import KademliaNode
    from src.api.user import UserData
    from src.cli.main import MainMenuAnswer

class ActionList(TypedDict):
    register: Callable[[dict], Tuple[KademliaNode, str, UserData]]
    login: Callable[[dict], Tuple[KademliaNode, str, UserData]]

class Authentication:
    node : KademliaNode
    action_list : ActionList
    def __init__(self, listening : Tuple[str, int], node : KademliaNode) -> None:
        self.node = node
        self.listening = listening
        self.action_list = {
            'register': self.register,
            'login': self.login,
        }

    def action(self, action : str, information : MainMenuAnswer) -> Callable[[dict], Tuple[KademliaNode, str, UserData]]:
        return self.action_list[action](information)
    
    def register(self, information : MainMenuAnswer) -> Tuple[KademliaNode, str, UserData]:
        username = information['username']
        password = information['password']
        
        try:
            user_info = self.node.get(username)
            
            if user_info is None:
                salt = os.urandom(32)
                key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
                RSA_key = RSA.generate(bits=1024)
                
                if not os.path.exists('./key'):
                    os.makedirs('./key')

                with open(f'./key/{username}.key', 'w') as storage_key:
                    storage_key.write(f"{RSA_key.n}\n{RSA_key.d}")

                print(self.listening)
                user_data = {
                    'salt': salt.hex(),
                    'hash_password': key.hex(),
                    'public_key_n': RSA_key.n,
                    'public_key_e': RSA_key.e,
                    "followers": [],
                    "following": [],
                    "ip": self.node.ip,
                    "port": self.node.port,
                    'listening_ip': self.listening[0],
                    'listening_port': self.listening[1],
                }

                self.node.set(username, json.dumps(user_data))
                user_args = (self.node, username, user_data)
            else:
                raise Exception(f'Registration failed. User {username} already exists')
        except Exception as e:
            Logger.log("Register", "error", str(e))
            return None

        Logger.log("Register", "success", "user registered successfully")
        return user_args

    def login(self, information : MainMenuAnswer) -> Tuple[KademliaNode, str, UserData]:
        username = information['username']
        password = information['password']

        user_args = None

        try: 
            user_info = self.node.get(username)

            if user_info is not None:
                user_info = json.loads(user_info)
                salt = bytes.fromhex(user_info['salt'])
                key = bytes.fromhex(user_info['hash_password'])
                new_key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)

                if key != new_key:
                    raise Exception(f"Login failed. Password is wrong!")
                
                user_args = (self.node, username, user_info)
            else:
                raise Exception(f"Login failed. User {username} doesn't exist")
                
        except Exception as e:
            Logger.log("Register", "error", str(e))
            return None

        Logger.log("Login", "success", "success")
        return user_args