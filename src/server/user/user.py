from src.client.timeline import Timeline
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
        # connect = asyncio.open_connection(host=user.ip, port=user.port, loop=asyncio.get_event_loop())
        # reader, writer = await connect

        # print(f"sending message: {message}")
        # writer.write(message.encode())
        # await writer.drain()
        pass
        #sender = Sender(user.port)
        #sender.send_msg(message)

        ### Do we need to receive any output to verify if the message was delivered?
        ### Do we need to return any value?

    async def publish_message(self, users, message):
        tasks = [self.send_message(user, message) for user in users]
        #await asyncio.gather(*tasks) # a '*' to unpack the list into arguments for the gather method
        
        # Debugging
        print(tasks)

        for user in users:
            print(user)
            self.send_message(user, message)
        ### Do we need to handle a return value?

    async def post(self, message):
        try: # TODO: maybe store the already obtained ips and ports, avoiding repetitive requests
            followers_info = await self.server.locate_followers(self.followers)
        except Exception as e:
            print(e)

        #self.timeline.add_message(message)
        await self.publish_message(followers_info, message)

        print(f'Posted message: {message}')

    async def follow(self, followed_user):
        if followed_user == self.username:
            print(f"You can't follow yourself")
            return None
        elif followed_user in self.following:
            print(f'You already follow the user {followed_user}')
            return None

        try:
            await self.server.add_follower(self.username, followed_user)
            self.following.append(followed_user)
        except Exception as e:
            print(e)

    async def view_timeline(self):
        print(self.timeline)

    def update_timeline(self, message):
        self.timeline.add_message(message)

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
