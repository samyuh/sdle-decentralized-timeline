import inquirer

class MainMenu:
    @staticmethod
    def menu():
        print('--- Main Menu ---')
        questions = [
            inquirer.List('action', message="Please choose an action", choices=['post', 'follow', 'unfollow', 'view', 'logout'],),
        ]

        answers = inquirer.prompt(questions)
        action = answers['action']

        result = {'action': action, 'information': {}}

        if action == 'post':
            print('Post message')
            message = input('New Post: ')
            result['information']['message'] = message
        
        elif action == 'follow':
            print('Follow user')
            username = input('User to follow: ')
            result['information']['username'] = username

        elif action == 'unfollow':
            print('Unfollow user')
            username = input('User to unfollow: ')
            result['information']['username'] = username
        
        elif action == 'view':
            print('View timeline')
        
        elif action == 'logout':
            print('Logout! See you soon on Kamellia!')

        return result