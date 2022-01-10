import json
from typing import Callable, Tuple, TypedDict
from src.api.user import UserData
from src.cli.main import MainMenuAnswer

from src.server.kademlia_node import KademliaNode
from src.utils.logger import Logger

class ActionList(TypedDict):
    register: Callable[[dict], Tuple[KademliaNode, str, UserData]]
    login: Callable[[dict], Tuple[KademliaNode, str, UserData]]

class Authentication:
    node : KademliaNode
    action_list : ActionList
    def __init__(self, node : KademliaNode) -> None:
        self.node = node
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
                user_data = {
                    "password": password,
                    "followers": [],
                    "following": [],
                    "ip": self.node.ip,
                    "port": self.node.port
                }

                self.node.set(username, json.dumps(user_data))
                user_args = (self.node, username, user_data)
            else:
                raise Exception(f'Registration failed. User {username} already exists')
        except Exception as e:
            Logger.log("Register", "error", str(e))
            exit(1)

        Logger.log("Register", "success", "user registered successfully")
        return user_args

    def login(self, information : MainMenuAnswer) -> Tuple[KademliaNode, str, UserData]:
        username = information['username']
        password = information['password']

        try: 
            user_info = self.node.get(username)

            if user_info is not None:
                user_info = json.loads(user_info)

                if password != user_info['password']:
                    raise Exception(f"Login failed. Password is wrong!")
                
                user_args = (self.node, username, user_info)
            else:
                raise Exception(f"Login failed. User {username} doesn't exist")
                
        except Exception as e:
            Logger.log("Register", "error", str(e))
            exit(1)

        Logger.log("Login", "success", "success")
        return user_args