import json
from typing import Callable, Dict, List, TypedDict
from typing_extensions import NotRequired
from src.connection.message.request_post import RequestPostMessage
from src.connection.message.send_post import SendPostMessage, SendPostType

from src.server.kademlia_node import KademliaNode

from .timeline import Timeline, TimelineMessage

from src.connection import MessageDispatcher, MessageReceiver
from src.connection.message import MessageType

class UserData(TypedDict):
    password: str
    followers: List[str]
    following: List[str]
    ip : str
    port : int

class UserActionInfo(TypedDict, total=False):
    username: NotRequired[str]
    message: NotRequired[str]

class User:
    node : KademliaNode
    username : str
    password : str
    ip : str
    port : int
    followers : list
    following : list
    listening_ip : str
    listening_port : int
    message_dispatcher : MessageDispatcher
    message_receiver : MessageReceiver
    action_list: Dict[str, Callable[[UserActionInfo], None]]
    timeline: Timeline

    def __init__(self, node, username : str, data : UserData) -> None:
        self.node = node
        self.username = username
        self.password = data['password']
        self.ip = data['ip']
        self.port = data['port']
        self.followers = data['followers']
        self.following = data['following']

        self.listening_ip = data['ip']
        self.listening_port = data['port'] - 1000

        # Follower Module
        # TODO FOLLOWER

        # Send Messages Module
        self.message_dispatcher = MessageDispatcher(self)

        # Listener Module
        self.message_receiver = MessageReceiver(self, self.listening_ip, self.listening_port)

        # Actions
        self.action_list = {
            'post': self.post,
            'follow': self.follow,
            'unfollow': self.unfollow,
            'view': self.view,
            'logout': self.logout
        }

        # Timeline Module
        self.timeline = Timeline(username)
        # TODO: Update timeline with posts from when the user node was offline
        # ZMQ already restores these posts O.O
        # self.update_state()

    # --------------------------
    #  Action Menu Command
    # --------------------------
    def action(self, action : str, information : UserActionInfo) -> None:
        self.action_list[action](information)
    
    def post(self, information : UserActionInfo) -> None:
        message = self.message_dispatcher.action(MessageType.POST_MESSAGE, information['message'])
        self.timeline.add_message(message)

    def follow(self, information : UserActionInfo) -> None:
        user_followed = self.add_follower(information['username'])

        if user_followed != None:
            self.message_dispatcher.action(MessageType.REQUEST_POSTS, user_followed)

    def unfollow(self, information : UserActionInfo) -> None:
        user_unfollowed = self.remove_follower(information['username'])
        
        if user_unfollowed != None:
            self.delete_posts(user_unfollowed)

    def view(self, _) -> None:
        print(self.timeline)

    def logout(self, _) -> None:
        self.node.close()
        exit(0)
        
    # --------------------------
    # -- Listener Loop Action --
    # --------------------------
    def update_timeline(self, message : TimelineMessage) -> None:
        self.timeline.add_message(message)

    def many_update_timeline(self, messages : SendPostMessage):
        for message in messages['content']:
            self.timeline.add_message(message)

    def send_message(self, message : RequestPostMessage):
        self.message_dispatcher.action(MessageType.SEND_POSTS, message['header']['user'])

    # ------------
    # - TimeLine -
    # ------------
    def get_own_timeline(self):
        return self.timeline.get_messages_from_user(self.username)

    def delete_posts(self, user_unfollowed):
        self.timeline.delete_posts(user_unfollowed)

    def update_state(self) -> None:
        for followed_user in self.following:
            self.timeline.delete_posts(followed_user)
            self.message_dispatcher.action(MessageType.REQUEST_POSTS, followed_user)

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

    def remove_follower(self, user_unfollowed : str):
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

    def get_user(self, username : str) -> UserData:
        user_info = self.node.get(username)
        if user_info is None:
            raise Exception(f'User {username} doesn\'t exist')

        user_info = json.loads(user_info)
        return user_info

    def get_followers(self) -> Dict[str, UserData]:
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
