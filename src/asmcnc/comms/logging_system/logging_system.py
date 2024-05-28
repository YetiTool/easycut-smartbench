import inspect
import logging
import os
import sys

LOG_STRING_FORMAT = "[%(asctime)s] - [%(levelname)s] [%(module_name)s] %(message)s"
LOG_DATE_FORMAT = "%H:%M:%S %d-%m-%Y"
LOG_FOLDER_PATH = os.path.join(os.path.dirname(__file__), "logs")
if not os.path.exists(LOG_FOLDER_PATH):
    os.makedirs(LOG_FOLDER_PATH)
try:
    from colorlog import ColoredFormatter

    formatter = ColoredFormatter(
        fmt="%(log_color)s" + LOG_STRING_FORMAT,
        datefmt=LOG_DATE_FORMAT,
        log_colors={
            "DEBUG": "cyan",
            "INFO": "green",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "red,bg_black",
        },
    )
except ImportError:
    formatter = logging.Formatter(LOG_STRING_FORMAT, datefmt=LOG_DATE_FORMAT)


class ModuleLogger(logging.Logger):

    def __init__(self, name, level=logging.DEBUG):
        super(ModuleLogger, self).__init__(name, level)

    def _log(self, level, msg, args, exc_info=None, extra=None):
        if extra is None:
            extra = {}
        frame = inspect.currentframe().f_back.f_back
        module_name = inspect.getmodule(frame).__name__
        if "." in module_name:
            module_name = module_name.split(".")[-1]
        extra["module_name"] = module_name
        super(ModuleLogger, self)._log(level, msg, args, exc_info, extra)


class LoggerSingleton(object):
    _instance = None
    _logger = None

    def __new__(cls, level=logging.DEBUG, *args, **kwargs):
        """
        Creates and returns a new instance of the LoggerSingleton class if one does not already exist.
        Returns the existing instance if one does exist.

        :param level: The level to set the logger to, e.g. logging.DEBUG.
        The logger will log all messages of this level and above.
        :param args: Any positional arguments to pass to the __new__ method of the super class.
        :param kwargs: Any keyword arguments to pass to the __new__ method of the super class.
        """
        if not cls._instance:
            cls._instance = super(LoggerSingleton, cls).__new__(cls, *args, **kwargs)
            cls._instance._setup_logger(level=level)
        return cls._instance

    def _setup_logger(self, level, name="yeti_logger"):
        """
        Set up the logger.
        :param level: The level to set the logger to, e.g. logging.DEBUG.
        :param name: The name of the logger. Defaults to "yeti_logger".
        :return: None
        """
        self._logger = ModuleLogger(name, level)
        self._logger.setLevel(level)
        self._logger.addHandler(self.__get_console_handler(level))

    @staticmethod
    def __get_console_handler(level):
        """
        Get a console handler for the logger.

        :return:  A console handler for the logger.
        """
        console_handler = logging.StreamHandler(stream=sys.stdout)
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        return console_handler

    def get_logger(self):
        """
        Get the logger.
        :return: The instance of the ModuleLogger.
        """
        return self._logger


Logger = LoggerSingleton().get_logger()
Logger.info("Logger initialised")
