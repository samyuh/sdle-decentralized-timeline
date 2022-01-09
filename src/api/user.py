import json
from src.api.timeline import Timeline

from src.api.post import PostMessage

class User:
    def __init__(self, node, username, data):
        self.node = node
        self.username = username
        self.password = data['password']
        self.ip = data['ip']
        self.port = data['port']
        self.followers = data['followers']
        self.following = data['following']

        self.timeline = Timeline(username)
        self.post = PostMessage(self)
        self.action_list = {}

    # --------------------------
    # -- Listener Loop Action --
    # --------------------------
    def update_timeline(self, message):
        self.timeline.add_message(message)

    def send_message(self, action, message):
        self.post.send(action, message)

    # ------------
    # - TimeLine -
    # ------------
    def view_timeline(self):
        print(self.timeline)

    def get_own_timeline(self):
        return self.timeline.get_messages_from_user(self.username)

    def delete_posts(self, user_unfollowed):
        self.timeline.delete_posts(user_unfollowed)

    # def get_suggestions(self):
    #     pass

    # -------------
    # - Followers -
    # -------------
    def add_follower(self, user_followed):
        if user_followed == self.username:
            print(f'You can\'t follow yourself')
            return None
        elif user_followed in self.following:
            print(f'You already follow the user {user_followed}')
            return None

        ### Update following list of the current user
        try:
            user_info = self.get_user(self.username)
            user_info['following'].append(user_followed)
            self.following = user_info['following']
        except Exception as e:
            print(f'Error: {e}')
            return None

        ### Update follower list on followed
        try:
            user_followed_info = self.get_user(user_followed)
            user_followed_info['followers'].append(self.username)
        except Exception as e:
            print(f'Error: {e}')
            return None

        self.node.set(self.username, json.dumps(user_info))
        self.node.set(user_followed, json.dumps(user_followed_info))

        return user_followed

    def remove_follower(self, user_unfollowed):
        if user_unfollowed not in self.following:
            print(f'You don\'t follow the user {user_unfollowed}')
            return None

        try:
            user_info = self.get_user(self.username)
            user_info['following'].remove(user_unfollowed)
            self.following = user_info['following']
        except Exception as e:
            print(f'Error: {e}')
            return None

        try:
            user_unfollowed_info = self.get_user(user_unfollowed)
            user_unfollowed_info['followers'].remove(self.username)
        except Exception as e:
            print(f'Error: {e}')
            return None

        self.node.set(self.username, json.dumps(user_info))
        self.node.set(user_unfollowed, json.dumps(user_unfollowed_info))
        return user_unfollowed

    def get_user(self, username):
        user_info = self.node.get(username)
        if user_info is None:
            raise Exception(f'User {username} doesn\'t exist')

        user_info = json.loads(user_info)
        return user_info

    def get_followers(self):
        self.followers = json.loads(self.node.get(self.username))['followers']

        followers_info = {}
        for username in self.followers:
            followers_info[username] = self.get_user(username)

        return followers_info
    
    # -----------
    # - Special -
    # -----------
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
