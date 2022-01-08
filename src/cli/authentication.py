import inquirer

class AuthMenu:
    @staticmethod
    def menu():
        print('--- Authentication Menu ---')
        questions = [
            inquirer.List('authentication', message="Please sign in", choices=['register', 'login'],),
        ]

        answers = inquirer.prompt(questions)
        method = answers['authentication']
        username = input('Enter your username: ')
        password = input('Enter your password: ')
        return {'method': method, 'information': {'username': username, 'password': password}}