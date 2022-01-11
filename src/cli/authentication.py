from typing import TypedDict

import inquirer

class AuthMenuUserInfo(TypedDict):
    username: str
    password: str

class AuthMenuAnswer(TypedDict):
    method: str
    information: AuthMenuUserInfo

class AuthMenu:
    @staticmethod
    def menu() -> AuthMenuAnswer:
        print('\n--- Authentication Menu ---')
        questions = [
            inquirer.List('authentication', message="Please sign in", choices=['register', 'login'],),
        ]

        answers = inquirer.prompt(questions)
        method = answers['authentication']
        username = input('Enter your username: ')
        password = input('Enter your password: ')
        return {'method': method, 'information': {'username': username, 'password': password}}