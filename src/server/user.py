from src.timeline import Timeline
import asyncio

class User:
    def __init__(self, server, username, data):
        self.username = username
        self.password = data['password']
        self.server = server
        self.ip = data['ip']
        self.port = data['port']
        self.followers = data['followers']
        self.following = data['following'] # { username : last_msg_received }
        self.timeline = Timeline(username)

    async def send_message(self, user, message):
        connect = asyncio.open_connection(host=user.ip, port=user.port, loop=asyncio.get_event_loop())
        reader, writer = await connect

        print(f"sending message: {message}")
        writer.write(message.encode())
        await writer.drain()

        ### Do we need to receive any output to verify if the message was delivered?
        ### Do we need to return any value?

    async def publish_message(self, users, message):
        tasks = [self.send_message(user, message) for user in users]
        await asyncio.gather(*tasks) # a '*' to unpack the list into arguments for the gather method
        
        # Debugging
        print(tasks)
        ### Do we need to hande a return value?

    async def post(self, message):
        try: # TODO: maybe store the already obtained ips and ports, avoiding repetitive requests
            followers_info = await self.server.locate_followers(self.followers)
        except Exception as e:
            print(e)

        self.timeline.add_message(message)

        await self.publish_message(followers_info, message)

        print(f'Posted message: {message}')

    async def follow(self, username):
        if username == self.username:
            print(f'You can\'t follow yourself')
            return None
        
        elif username in self.following:
            print(f'You already follow the user {username}')
            return None

        try:
            await self.server.add_follower(self.username, username)
            self.following.append(username)
        except Exception as e:
            print(e)

    def get_suggestions(self):
        pass

    def __str__(self) -> str:
        res = f'User {self.username}:\n'
        res += f'\tPassword: {self.password}\n'
        res += f'\tFollowers:\n'
        for username in self.followers:
            res += f'\t\t> {username}'
        res += f'\tFollowing:\n'
        for username in self.following:
            res += f'\t\t> {username}'
        return res
