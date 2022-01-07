from src.server.user import User
import asyncio
import sys
import json

class Authentication:
    def __init__(self, server):
        self.server = server
    
    # Registration
    async def register(self, information):
        try:
            username = information['username']
            password = information['password']
            print("before")
            user_info = await self.server.get(username)
            print("after")
            if user_info is None:
                user_data = {
                    "password": password,
                    "followers": [],
                    "following": [],
                    "ip": 10, #self.server.ip,
                    "port": 20, #self.server.port
                }

                # TODO: ASYNC SEPARATED THREAD or program will be blocked much time!
                await self.server.set(username, json.dumps(user_data))
                user = User(self.server, information['username'], user_data)
            else:
                raise Exception(f'Registration failed. User {username} already exists')

        except Exception as e:
            print(e)
            sys.exit(1)
        print('Register successful!')
        return user

    # Login
    async def login(self, information):
        try:
            username = information['username']
            password = information['password']
            print("here")
            user_info = await self.server.get(username)
            print(user_info)
            print("here")
            if user_info is not None:
                print(type(user_info))
                user_info = json.loads(user_info)
                if password != user_info['password']:
                    raise Exception(f"Login failed. Password is wrong!")
                user = User(self.server, username, user_info)
            else:
                raise Exception(f"Login failed. User {username} doesn't exist")
                
        except Exception as e:
            print(e)
            sys.exit(1)
        print('Login successful!')
        return user

    def register_coroutine(self, answers):
        try:
            print("here")
            asyncio.run(self.register(answers))
            print("here 2")
        except Exception as e:
            print(e)

    def login_coroutine(self,answers):
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            return loop.run_until_complete(self.login(answers['information']))
        except Exception as e:
            print(e)