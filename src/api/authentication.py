import sys
import json

class Authentication:
    def __init__(self, node):
        self.node = node
        self.action_list = {
            'register': self.register,
            'login': self.login,
        }

    def action(self, action, information):
        return self.action_list[action](information)
    
    def register(self, information):
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
            print(e)
            sys.exit(1)
        print('Register successful!')
        return user_args

    def login(self, information):
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
            print(e)
            sys.exit(1)
        print('Login successful!')
        return user_args