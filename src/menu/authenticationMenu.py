import inquirer

class AuthenticationMenu:
    @staticmethod
    def menu():
        print('--- Authentication Menu ---')
        questions = [
            inquirer.List('authentication', message="Please sign in", choices=['register', 'login'],),
        ]

        answers = inquirer.prompt(questions)
        method = answers['authentication']

        # TODO: para o register, fazer dupla verificação da password?
        if method == 'register':
            print('Escolheste register')
        elif method == 'login':
            print('Escolheste login')

        # TODO: guardar hash da password
        username = input('Enter your username: ')
        password = input('Enter your password: ')
        return {'method': method, 'information': {'username': username, 'password': password}}