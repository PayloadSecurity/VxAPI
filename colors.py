from colorama import Fore, Back, Style


class Color:

    @staticmethod
    def error(text):
        return Back.RED + str(text) + Style.RESET_ALL

    @staticmethod
    def control(text):
        return Fore.YELLOW + '\n<<< ' + str(text) + ' >>>\n\r' + Style.RESET_ALL

    @staticmethod
    def control_without_arrows(text):
        return Fore.YELLOW + str(text) + Style.RESET_ALL

    @staticmethod
    def warning(text):
        return Back.YELLOW + '\n\n<<< Warning: ' + str(text) + ' >>>\n'  + Style.RESET_ALL

    @staticmethod
    def success(text):
        return Back.GREEN + str(text) + Style.RESET_ALL
