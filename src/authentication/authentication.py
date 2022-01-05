from src.user import User

class Authentication:
    def __init__(self):
        pass

    async def register(self, server, information):
        try:
            state = await server.register(information['username'])
            user = User(server, information['username'], information['password'])
        except Exception as e:
            print(e)

        return True

    async def login(self, server, information):
        try:
            state = server.setUser(information['username'])
            user = User(server, information['username'], information['password'])
        except Exception as e:
            print(e)

        return True