import base64
import inspect
import json
import logging
import os
import socket
import sys

LOG_STRING_FORMAT = "[%(asctime)s] - [%(levelname)s] [%(module_name)s] %(message)s"
LOG_DATE_FORMAT = "%H:%M:%S %d-%m-%Y"

LOG_FOLDER_PATH = os.path.join(os.path.dirname(__file__), "logs")
LOG_FILE_PATH = os.path.join(LOG_FOLDER_PATH, "run.log")

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


def serialize_log_file(log_file_path, serial_number):
    """
    Serialize the log file to base64 and remove any instances of the serial number.
    :param log_file_path:
    :param serial_number:
    :return:
    """
    with open(log_file_path, "rb") as log_file:
        log_file_contents = log_file.read()

        # Ensure that the serial number is not included in the crash report for GDPR compliance.
        log_file_contents = log_file_contents.replace(serial_number.encode(), b"SERIAL_NUMBER")

    encoded_data = base64.b64encode(log_file_contents)
    return encoded_data


def send_logs_to_server(log_file_path, serial_number):
    """
    Send log file to server, with serial numbers removed. Recommend running this function on a separate
    thread to not lock up Kivy.
    :param log_file_path: absolute path to the log file.
    :param serial_number: the machine's serial number, to be removed to comply with GDPR.
    :return:
    """
    try:
        import pika

        encoded_data = serialize_log_file(log_file_path, serial_number)

        connection = pika.BlockingConnection(
            pika.ConnectionParameters('sm-receiver.yetitool.com', 5672, '/',
                                      pika.PlainCredentials(
                                          'console',
                                          '2RsZWRceL3BPSE6xZ6ay9xRFdKq3WvQb')
                                      )
        )
        channel = connection.channel()

        channel.queue_declare(queue="crash_reports", durable=True)

        hostname = socket.gethostname().split(".")[0]

        message = {
            "hostname": hostname,
            "log_data": encoded_data,
        }

        channel.basic_publish(exchange="", routing_key="crash_reports", body=json.dumps(message))

        Logger.info("Sent crash report, hostname: {}.".format(socket.gethostname()))
        return True
    except:
        Logger.exception("Failed to send crash report.")


class ModuleLogger(logging.Logger):
    def __init__(self, name, level=logging.DEBUG):
        super(ModuleLogger, self).__init__(name, level)

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
    _level = None

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
            cls._instance.__setup_logger(level=level)
        return cls._instance

    def __setup_logger(self, level, name="yeti_logger"):
        """
        Set up the logger.
        :param level: The level to set the logger to, e.g. logging.DEBUG.
        :param name: The name of the logger. Defaults to "yeti_logger".
        :return: None
        """
        self._logger = ModuleLogger(name, level)
        self._level = level
        self._logger.setLevel(level)
        self.__file_handler = self.__get_file_handler()
        self.__console_handler = self.__get_console_handler()
        self._logger.addHandler(self.__console_handler)
        self._logger.addHandler(self.__file_handler)

    def __get_console_handler(self):
        """
        Get a console handler for the logger.

        :return:  A console handler for the logger.
        """
        console_handler = logging.StreamHandler(stream=sys.stdout)
        console_handler.setLevel(self._level)
        console_handler.setFormatter(formatter)
        return console_handler

    def __get_file_handler(self):
        """
        Get a file handler for the logger.

        :return:  A file handler for the logger.
        """
        if os.path.exists(LOG_FILE_PATH):
            os.remove(LOG_FILE_PATH)

        file_handler = logging.FileHandler(LOG_FILE_PATH)
        file_handler.setLevel(self._level)
        file_handler.setFormatter(formatter)
        return file_handler

    def get_logger(self):
        """
        Get the logger.
        :return: The instance of the ModuleLogger.
        """
        return self._logger


Logger = LoggerSingleton().get_logger()
Logger.info("Logger initialised")
