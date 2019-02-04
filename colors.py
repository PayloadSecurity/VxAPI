from colorama import Fore, Back, Style
import sys


class Color:

    @staticmethod
    def is_atty():
        if hasattr(sys.stderr, 'isatty') and not sys.stderr.isatty():
            return False

        if hasattr(sys.stdout, 'isatty') and not sys.stdout.isatty():
            return False

        return True

    @staticmethod
    def error(text):
        text = str(text)

        return Back.RED + text + Style.RESET_ALL if Color.is_atty() else text

    @staticmethod
    def control(text):
        text = '\n<<< ' + str(text) + ' >>>\n\r'

        return Fore.YELLOW + text + Style.RESET_ALL if Color.is_atty() else text

    @staticmethod
    def control_without_arrows(text):
        text = str(text)

        return Fore.YELLOW + text + Style.RESET_ALL if Color.is_atty() else text

    @staticmethod
    def warning(text):
        text = '\n\n<<< Warning: ' + str(text) + ' >>>\n'

        return Back.YELLOW + text + Style.RESET_ALL if Color.is_atty() else text

    @staticmethod
    def success(text):
        text = str(text)

        return Back.GREEN + text + Style.RESET_ALL if Color.is_atty() else text
