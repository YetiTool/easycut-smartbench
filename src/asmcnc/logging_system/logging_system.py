import logging
import os
from datetime import datetime

from colorlog import ColoredFormatter


class FileFilter(logging.Filter):
    def __init__(self, module_name):
        super(FileFilter, self).__init__()
        self.module_name = module_name

    def filter(self, record):
        return record.name == self.module_name


class FileFormatter(logging.Formatter):
    def format(self, record):
        record.message = "[{0}] {1}".format(record.filename, record.getMessage())
        return super(FileFormatter, self).format(record)


LOG_STRING_FORMAT = "[%(asctime)s] [%(name)s] - [%(levelname)s] - %(message)s"
LOG_DATE_FORMAT = "%d-%m-%Y %H:%M:%S"

LOG_FOLDER_PATH = os.path.join(os.path.dirname(__file__), "logs")

if not os.path.exists(LOG_FOLDER_PATH):
    os.makedirs(LOG_FOLDER_PATH)


class Logger(logging.Logger):
    def __init__(self, name, level=logging.DEBUG):
        super(Logger, self).__init__(name, level)
        self.addFilter(FileFilter(name))
        self.addHandler(self.get_file_handler())
        self.addHandler(self.get_console_handler())

    def get_file_handler(self):
        current_date_time = datetime.now().strftime(LOG_DATE_FORMAT)
        file_name = "{0}-logs-{1}.log".format(self.name, current_date_time)

        file_handler = logging.FileHandler(os.path.join(LOG_FOLDER_PATH, file_name))
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(
            FileFormatter(fmt=LOG_STRING_FORMAT, datefmt=LOG_DATE_FORMAT)
        )
        return file_handler

    @staticmethod
    def get_console_handler():
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(
            ColoredFormatter(
                fmt="%(log_color)s" + LOG_STRING_FORMAT,
                datefmt=LOG_DATE_FORMAT,
                log_colors={
                    "DEBUG": "cyan",
                    "INFO": "green",
                    "WARNING": "yellow",
                    "ERROR": "red",
                    "CRITICAL": "red,bg_white",
                },
            )
        )
        return console_handler
