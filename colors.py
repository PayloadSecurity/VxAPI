from colorama import Fore, Back, Style


class Color:

    @staticmethod
    def error(text):
        return Back.RED + str(text) + Style.RESET_ALL

    @staticmethod
    def control(text):
        return Fore.YELLOW + '\n<<< ' + str(text) + ' >>>\n' + Style.RESET_ALL

    @staticmethod
    def success(text):
        return Back.GREEN + str(text) + Style.RESET_ALL
