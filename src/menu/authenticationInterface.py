import inquirer

class AuthenticationMenu:
    @staticmethod
    def menu():
        print('--- Authentication ---')
        questions = [
            inquirer.List('authentication', message="Please sign in", choices=['register', 'login'],),
        ]

        answers = inquirer.prompt(questions)
        method = answers['authentication']

        if method == 'register':
            print('Escolheste register')
        elif method == 'login':
            print('Escolheste login')

        username = input('Enter your username')
        return {'method':method, 'information': {'username': username}}