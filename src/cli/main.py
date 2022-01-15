from __future__ import annotations
from typing import TypedDict, TYPE_CHECKING

from src.utils.logger import Logger
from simple_term_menu import TerminalMenu    

if TYPE_CHECKING:
    from src.api.user import UserActionInfo

class MainMenuAnswer(TypedDict):
    action: str
    information: UserActionInfo

class MainMenu:
    @staticmethod
    def menu() -> MainMenuAnswer:
        logger = Logger()
        print("-----------------")
        print("--- Main Menu ---")
        print("-----------------")
        choices=['New Post', 'Follow User', 'Unfollow User', 'View Timeline', 'View Profile', 'Get Suggestions', 'Logout']
        terminal_menu = TerminalMenu(choices, 
        menu_highlight_style=("fg_blue",),
        menu_cursor_style=("fg_blue", "bold"))
        menu_entry_index = terminal_menu.show()
        action = choices[menu_entry_index]

        result = {'action': action, 'information': {}}

        if action == 'New Post':
            logger.log("Post","info",'Post message')
            message = input('New Post: ')
            result['information']['message'] = message
        
        elif action == 'Follow User':
            logger.log("Follow","info", 'Follow user')
            username = input('User to follow: ')
            result['information']['username'] = username

        elif action == 'Unfollow User':
            logger.log("Unfollow","info",'Unfollow user')
            username = input('User to unfollow: ')
            result['information']['username'] = username

        elif action == 'View Timeline':
            logger.log("View","info",'View Timeline')

        elif action == 'View Profile':
            logger.log("Profile","info",'View Profile')

        elif action == 'Get Suggestions':
            logger.log("Suggestions","info",'Get Suggestions')
        
        elif action == 'Logout':
            logger.log("Logout","info",'Logout! See you soon on Camellia')

        return result