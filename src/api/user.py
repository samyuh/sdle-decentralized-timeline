from __future__ import annotations
from typing import Callable, Dict, List, TypedDict, Optional, TYPE_CHECKING

import json
import random
from hashlib import sha512

from src.api.timeline import Timeline
from src.connection.dispatcher import MessageDispatcher
from src.connection.message.message import MessageType
from src.connection.receiver import MessageReceiver
from src.utils.logger import Logger
import threading
if TYPE_CHECKING:
    from src.server.kademlia_node import KademliaNode
    from src.api.timeline import TimelineMessage, MessageLifespan
    from src.connection.message.send_timeline import SendPostMessage

class UserPrivateData(TypedDict):
    salt: int
    hash_password: str
    public_key_n: int
    public_key_e: int

class UserConnectionsData(TypedDict):
    ip : str
    port : int
    listening_ip : str
    listening_port : int

class UserActionInfo(TypedDict, total=False):
    username: str
    message: str

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

    def __init__(self, node, username, private: UserPrivateData, connection: UserConnectionsData, timelineMessageLifespan : Optional[MessageLifespan] = {}):
        self.node = node
        self.username = username

        # Private Fields
        self.hash_password = private['hash_password']
        self.salt = private['salt']
        self.public_key_n = private['public_key_n']
        self.public_key_e = private['public_key_e']
        self.__read_private_keys()

        # Connection Fields
        self.listening_ip = connection['listening_ip']
        self.listening_port = connection['listening_port']
        
        # Send Messages Module
        self.message_dispatcher = MessageDispatcher(self)

        # Listener Module
        self.message_receiver = MessageReceiver(self, self.listening_ip, self.listening_port)
        self.message_receiver.start_listener()
        #threading.Thread(target=self.message_receiver.start_listener, daemon=True).start()
        self.timeouts = {}

        # Actions
        self.action_list = {
            'New Post': self.post,
            'Follow User': self.follow,
            'Unfollow User': self.unfollow,
            'Get Suggestions': self.suggestions,
            'View Timeline': self.view,
            'View Profile': self.profile,
            'Logout': self.logout
        }

        # Timeline Module
        self.timeline = Timeline(username, message_lifespan=timelineMessageLifespan)


    # --------------------------
    #  Action Menu Command
    # --------------------------
    def action(self, action : str, information : UserActionInfo) -> None:
        self.action_list[action](information)
    
    def post(self, information : UserActionInfo) -> None:
        message = self.message_dispatcher.action(MessageType.TIMELINE_MESSAGE, information['message'])

        self.timeline.add_message(message)

    def follow(self, information : UserActionInfo) -> None:
        user_followed = self.add_follower(information['username'])

        if user_followed != None:
            self.update_timeline_follower(user_followed)

    def unfollow(self, information : UserActionInfo) -> None:
        user_unfollowed = self.remove_follower(information['username'])
        
        if user_unfollowed != None:
            self.timeline.delete_posts(user_unfollowed)

    def view(self, _) -> None:
        print(self.timeline)

    def profile(self, _) -> None:
        print(f"\t{self.username}'s profile\n")
        print(self)

    def suggestions(self, _):
        suggestions = set([])
        user_followers = self.get_user(self.username, 'public')['followers']

        for follower in user_followers:
            follower_info = self.get_user(follower, 'public')
            print(follower_info)
            suggestions.update(follower_info['followers'])

        suggestions = tuple(suggestions)

        if len(suggestions) > 5:
            suggestions = random.sample(suggestions, 5)
        
        if len(suggestions) > 0:
            print('Recommended Users:\n')
            for user in suggestions:
                print(f'\t> {user}')
        else:
            print('No Recommendations\n')

    def logout(self, _) -> None:
        self.node.close()
        exit(0)

    # --------------------------
    # -- Listener Loop Action --
    # --------------------------
    def receive_timeline_message(self, message : TimelineMessage) -> None:
        self.timeline.add_message(message)

    def send_timeline(self, message):
        self.message_dispatcher.action(MessageType.SEND_TIMELINE, message['header']['user'], message['header']['timeline_owner'])

    def receive_timeline(self, messages : SendPostMessage):
        timeline_owner = messages['header']['timeline_owner']
        
        self.timeouts[timeline_owner].cancel()

        valid_messages = []
        
        ### Verify if all messages are from the sender user
        for message in messages['content']:
            if timeline_owner == message['header']['user']:
                valid_messages.append(message)

        ### Delete all previous messages we had from that user from the timeline
        self.timeline.delete_posts(timeline_owner) # TODO: verify key signature

        ### Add the received messages to our timeline
        for message in valid_messages:
            self.timeline.add_message(message)
        
    # ------------
    # Signature
    # ------------
    def __read_private_keys(self):
        with open(f'./key/{self.username}.key', 'r') as storage_key:
            self.__private_key_n = str(storage_key.readline())
            self.__private_key_d =  str(storage_key.readline())

    def sign(self, message):
        hash = int.from_bytes(sha512(str(message).encode('utf-8')).digest(), byteorder='big')
        signature = pow(hash, int(self.__private_key_d), int(self.__private_key_n))
        return signature

    def verify_signature(self, message, user, signature):
        user_original = self.get_user(user, 'private')
        hash = int.from_bytes(sha512(str(message).encode('utf-8')).digest(), byteorder='big')
        hashFromSignature = pow(signature, int(user_original['public_key_e']), int(user_original['public_key_n']))

        signature_valid = (hash == hashFromSignature)
        Logger.log("success", "success", f"Valid signature: {signature_valid}")
        return signature_valid

    # ------------
    # - TimeLine -
    # ------------
    def get_number_posts(self):
        return len(self.timeline.get_messages_from_user(self.username))
        
    def get_timeline(self, username):
        return self.timeline.get_messages_from_user(username)
    
    def update_timeline_follower(self, username : str):
        self.message_dispatcher.action(MessageType.REQUEST_TIMELINE, username, username)

        follower_list = self.get_user(username, 'public')['followers']
        if self.username in follower_list:
            follower_list.remove(self.username)

        self.timeouts[username] = threading.Timer(1, self.__ask_next, args=[follower_list, username])
        self.timeouts[username].start()

    def __ask_next(self, follower_list, timeline_owner):
        if follower_list:
            request_user = follower_list.pop()

            print(follower_list)
            print(timeline_owner)

            self.message_dispatcher.action(MessageType.REQUEST_TIMELINE, request_user, timeline_owner)
            self.timeouts[timeline_owner] = threading.Timer(5, self.__ask_next, args=[follower_list, timeline_owner])
            self.timeouts[timeline_owner].start()
        else:
            Logger.log("UpdateTimeline", "error", f"Could not fetch {timeline_owner}'s timeline")

    def update_timeline(self) -> None:
        user_info = self.get_user(self.username, 'public')
        following = user_info['following']
        followers = user_info['followers']

        for followed_user in following:
            self.update_timeline_follower(followed_user)

        for follower in followers:
            self.message_dispatcher.action(MessageType.SEND_TIMELINE, follower, self.username)

    # -------------
    # - Followers -
    # -------------
    def add_follower(self, username_followed):
        user_following = self.get_user(self.username, 'public')['following']

        if username_followed == self.username:
            Logger.log("Add Follower", "info", 'You can\'t follow yourself')
            return None
        elif username_followed in user_following:
            Logger.log("Add Follower", "info", f'You already follow the user {username_followed}')
            return None

        ### Update following list of the current user
        try:
            user_info = self.get_user(self.username, 'public')
            user_info['following'].append(username_followed)
        except Exception as e:
            Logger.log("Add Follower", "error", str(e))
            return None

        ### Update follower list on followed
        try:
            user_followed_info = self.get_user(username_followed, 'public')
            user_followed_info['followers'].append(self.username)
        except Exception as e:
            Logger.log("Add Follower", "error", str(e))
            return None

        self.node.set(self.username + ':public', json.dumps(user_info))
        self.node.set(username_followed + ':public', json.dumps(user_followed_info))

        return username_followed

    def remove_follower(self, user_unfollowed : str):
        user_following = self.get_user(self.username, 'public')['following']

        if user_unfollowed not in user_following:
            Logger.log("Remove Follower", "info", f'You don\'t follow the user {user_unfollowed}')
            return None

        try:
            user_info = self.get_user(self.username, 'public')
            user_info['following'].remove(user_unfollowed)
        except Exception as e:
            Logger.log("Remove Follower", "error", str(e))
            return None

        try:
            user_unfollowed_info = self.get_user(user_unfollowed, 'public')
            if self.username in user_unfollowed_info['followers']:
                user_unfollowed_info['followers'].remove(self.username)
        except Exception as e:
            Logger.log("Remove Follower", "error", str(e))
            return None

        self.node.set(self.username + ':public', json.dumps(user_info))
        self.node.set(user_unfollowed + ':public', json.dumps(user_unfollowed_info))
        return user_unfollowed

    def get_user(self, username : str, scope : str):
        """
        Return information of a user
        """
        user_info = self.node.get(username + ':' + scope)
        if user_info is None:
            raise Exception(f'User {username} doesn\'t exist')

        user_info = json.loads(user_info)
        return user_info

    def get_followers_information(self, scope):
        """
        Return information of the followers
        """
        user_followers = self.get_user(self.username, 'public')['followers']

        followers_info = []
        for username in user_followers:
            followers_info.append(self.get_user(username, scope))

        return followers_info
    
    # -----------
    # - Special -
    # -----------
    def __str__(self) -> str:
        user_public = self.get_user(self.username, 'public')

        followers = user_public['followers']
        following = user_public['following']
        total_posts = len(self.timeline.get_messages_from_user(self.username))
        res = f'Number of posts: {total_posts}\n'
        res += f'Followers ({len(followers)})'
        res += ':\n' if followers else '\n'
        for username in followers:
            res += f'\t> {username}\n'
        res += f'Following ({len(following)})'
        res += ':\n' if following else '\n'
        for username in following:
            res += f'\t> {username}\n'
        return res
