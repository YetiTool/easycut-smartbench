import inspect
import logging
import os

from colorlog import ColoredFormatter

LOG_STRING_FORMAT = "[%(asctime)s] - [%(levelname)s] [%(module_name)s] %(message)s"
LOG_DATE_FORMAT = "%H:%M:%S %d-%m-%Y"

LOG_FOLDER_PATH = os.path.join(os.path.dirname(__file__), "logs")

if not os.path.exists(LOG_FOLDER_PATH):
    os.makedirs(LOG_FOLDER_PATH)


class ModuleLogger(logging.Logger):
    def __init__(self, name, level=logging.DEBUG):
        super(ModuleLogger, self).__init__(name, level)

    def debug(self, msg, *args, **kwargs):
        if self.isEnabledFor(logging.DEBUG):
            self._log(logging.DEBUG, msg, args, **kwargs)

    def info(self, msg, *args, **kwargs):
        if self.isEnabledFor(logging.INFO):
            self._log(logging.INFO, msg, args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        if self.isEnabledFor(logging.WARNING):
            self._log(logging.WARNING, msg, args, **kwargs)

    def error(self, msg, *args, **kwargs):
        if self.isEnabledFor(logging.ERROR):
            self._log(logging.ERROR, msg, args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        if self.isEnabledFor(logging.CRITICAL):
            self._log(logging.CRITICAL, msg, args, **kwargs)

    def _log(self, level, msg, args, exc_info=None, extra=None):
        if extra is None:
            extra = {}

        # Get the caller's stack frame (two f_back as this class called _log) and extract its module name.
        # https://stackoverflow.com/a/3711243
        frame = inspect.currentframe().f_back.f_back
        module_name = inspect.getmodule(frame).__name__

        # Might want to change this to show more than just the last part of the module name.
        if "." in module_name:
            module_name = module_name.split(".")[-1]

        # Store the module name in the record.
        extra["module_name"] = module_name

        # Call the parent class's _log() method and pass the extra information.
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
        self._logger.addHandler(self.__get_console_handler())

    @staticmethod
    def __get_console_handler():
        """
        Get a console handler for the logger.

        :return:  A console handler for the logger.
        """
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
                    "CRITICAL": "red,bg_black",
                },
            )
        )
        return console_handler

    def get_logger(self):
        """
        Get the logger.
        :return: The instance of the ModuleLogger.
        """
        return self._logger
