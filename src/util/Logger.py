from logging import *
from colorama import init, Fore, Style
from util.Resource import get_log_path

# Initialize colorama
init(autoreset=True)

log_path = get_log_path()

class ColoredFormatter(Formatter):
    COLORS = {
        "DEBUG": Fore.CYAN,
        "INFO": Fore.GREEN,
        "WARNING": Fore.YELLOW,
        "ERROR": Fore.RED,
        "CRITICAL": Fore.RED + Style.BRIGHT,
    }

    def format(self, record):
        levelname = record.levelname
        color = self.COLORS.get(levelname, Fore.RESET)
        record.levelname = color + levelname + Fore.RESET
        return super().format(record)

class Log(Logger):
    def __new__(cls, **kwargs):
        logger = getLogger('Void')
        logger.setLevel(DEBUG)

        formatter = ColoredFormatter('[%(asctime)s.%(msecs)03d][%(levelname)s]\t%(message)s')
        formatter.datefmt = '%H:%M:%S'

        fileHandler = FileHandler(log_path, 'w')
        fileHandler.setFormatter(formatter)
        fileHandler.setLevel(DEBUG)

        consoleHandler = StreamHandler()
        consoleHandler.setFormatter(formatter)
        consoleHandler.setLevel(DEBUG)

        logger.addHandler(fileHandler)
        logger.addHandler(consoleHandler)

        return logger


logger = Log()
