import json
import threading

from src.api.timeline import Timeline

from src.api.message import MessageType
from src.api.post import MessageDispatcher

from src.server.listener import Listener

class User:
    def __init__(self, node, username, data):
        self.node = node
        self.username = username
        self.password = data['password']
        self.ip = data['ip']
        self.port = data['port']
        self.followers = data['followers']
        self.following = data['following']

        # Follower Module
        # TODO FOLLOWER

        # Timeline Module
        self.timeline = Timeline(username)

        # Send Messages Module
        self.message_dispatcher = MessageDispatcher(self)

        # Listener Module
        self.listener = Listener(self)
        threading.Thread(target=self.listener.recv_msg_loop, daemon=True).start()

        self.listener_action_list = {
            MessageType.POST_MESSAGE.value: self.update_timeline,
            MessageType.SEND_POSTS.value: self.many_update_timeline,
            MessageType.REQUEST_POSTS.value: self.send_message,
        }

        # Actions
        self.action_list = {
            'post': self.post,
            'follow': self.follow,
            'unfollow': self.unfollow,
            'view': self.view,
            'logout': self.logout
        }

    # --------------------------
    #  Action Menu Command
    # --------------------------
    def action(self, action, information):
        self.action_list[action](information)
    
    def post(self, information):
        self.message_dispatcher.action(MessageType.POST_MESSAGE, information['message'])

    def follow(self, information):
        user_followed = self.add_follower(information['username'])
        if user_followed != None:
            self.message_dispatcher.action(MessageType.REQUEST_POSTS, user_followed)

    def unfollow(self, information):
        user_unfollowed = self.remove_follower(information['username'])
        if user_unfollowed != None:
            self.delete_posts(user_unfollowed)

    def view(self, _):
        print(self.timeline)

    def logout(self, _):
        self.node.close()
        exit(0)
        
    # --------------------------
    # -- Listener Loop Action --
    # --------------------------
    def listener_action(self, action, message):
        self.listener_action_list[action](message)

    def update_timeline(self, message):
        self.timeline.add_message(message)

    def many_update_timeline(self, messages):
        for message in messages['content']: 
            self.timeline.add_message(message)

    def send_message(self, message):
        self.message_dispatcher.action(MessageType.SEND_POSTS, message['header']['user'])

    # ------------
    # - TimeLine -
    # ------------
    def get_own_timeline(self):
        return self.timeline.get_messages_from_user(self.username)

    def delete_posts(self, user_unfollowed):
        self.timeline.delete_posts(user_unfollowed)

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
