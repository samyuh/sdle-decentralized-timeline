from colorama import Fore, Style

class Logger(object):
    @staticmethod
    def log(origin : str, type_message : str, message : str) -> None:
        msg = f'{origin}: {message}'

        if (type_message == "info"):
            print(f"{Fore.CYAN}[ INFO ] {msg} {Style.RESET_ALL}")
        elif (type_message == "warning"):
            print(f"{Fore.YELLOW}[ WARN ] {msg} {Style.RESET_ALL}")
        elif (type_message == "error"):
            print(f"{Fore.RED}[ ERR ] {msg} {Style.RESET_ALL}")
        elif (type_message == "success"):
            print(f"{Fore.GREEN}[ SUCC ] {msg} {Style.RESET_ALL}")
