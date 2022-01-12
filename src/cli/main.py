from __future__ import annotations
from typing import TypedDict, TYPE_CHECKING

import inquirer
from src.utils.logger import Logger


if TYPE_CHECKING:
    from src.api.user import UserActionInfo

class MainMenuAnswer(TypedDict):
    action: str
    information: UserActionInfo

class MainMenu:
    @staticmethod
    def menu() -> MainMenuAnswer:
        print('\n--- Main Menu ---')
        questions = [
            inquirer.List('action', message="Please choose an action", choices=['post', 'follow', 'unfollow', 'view', 'logout'],),
        ]

        answers = inquirer.prompt(questions)
        action = answers['action']

        result = {'action': action, 'information': {}}

        if action == 'post':
            Logger.log("Post","info",'Post message')
            message = input('New Post: ')
            result['information']['message'] = message
        
        elif action == 'follow':
            Logger.log("Follow","info",'Follow user')
            username = input('User to follow: ')
            result['information']['username'] = username

        elif action == 'unfollow':
            Logger.log("Unfollow","info",'Unfollow user')
            username = input('User to unfollow: ')
            result['information']['username'] = username
        
        elif action == 'view':
            Logger.log("View","info",'View Timeline')
        
        elif action == 'logout':
            Logger.log("Logout","info",'Logout! See you soon on Kamellia')

        return result