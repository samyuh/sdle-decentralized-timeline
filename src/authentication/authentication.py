from src.server import User
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
        return user

    async def login(self, server, information):
        try:
            user_data = await server.login(information['username'], information['password'])
            user = User(server, information['username'], user_data)
        except Exception as e:
            print(e)
            sys.exit(1)

        return user