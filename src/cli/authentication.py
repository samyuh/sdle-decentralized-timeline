from typing import TypedDict

from simple_term_menu import TerminalMenu  

class AuthMenuUserInfo(TypedDict):
    username: str
    password: str

class AuthMenuAnswer(TypedDict):
    method: str
    information: AuthMenuUserInfo

class AuthMenu:
    @staticmethod
    def menu() -> AuthMenuAnswer:
        print("\n")
        print("---------------------------")
        print('--- Authentication Menu ---')
        print("---------------------------")
        
 
        choices=['register', 'login']
        terminal_menu = TerminalMenu(choices, 
            menu_highlight_style=("fg_blue",),
            menu_cursor_style=("fg_blue", "bold"),
            title="Authentication")
        menu_entry_index = terminal_menu.show()
        action = choices[menu_entry_index]

        username = input('Enter your username: ')
        password = input('Enter your password: ')
        return {'method': action, 'information': {'username': username, 'password': password}}