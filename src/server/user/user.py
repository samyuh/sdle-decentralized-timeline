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
        #self.timeline = Timeline(username)

    

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
