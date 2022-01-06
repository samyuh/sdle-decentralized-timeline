from src.server.user import User
import asyncio
import sys

class Authentication:
    def __init__(self):
        pass
    
    async def register(self, server, information):
        try:
            user_data = await server.register(information['username'], information['password'])
            user = User(server, information['username'], user_data)
        except Exception as e:
            print(e)
            sys.exit(1)
        print('Register successful!')
        return user

    async def login(self, server, information):
        try:
            user_data = await server.login(information['username'], information['password'])
            user = User(server, information['username'], user_data)
        except Exception as e:
            print(e)
            sys.exit(1)
        print('Login successful!')
        return user

    def register_coroutine(self, server, answers):
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            return loop.run_until_complete(self.register(server, answers['information']))
        except Exception as e:
            print(e)

    def login_coroutine(self, server, answers):
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            return loop.run_until_complete(self.login(server, answers['information']))
        except Exception as e:
            print(e)