import os
import sys
import glob
import threading

import serial
from kivy.event import EventDispatcher

from asmcnc.comms.logging_system.logging_system import Logger

BAUD_RATE = 115200

LINUX = sys.platform == "linux2"
WINDOWS = sys.platform == "win32"
MAC = sys.platform == "darwin"

PI3 = os.uname()[-1] == "armv7l"
PI4 = os.uname()[-1] == "aarch64"


def get_ports_to_try():
    if MAC:
        return glob.glob("/dev/tty.usb*")
    elif WINDOWS:
        return ["COM3"]  # does this ever change

    # Linux (Raspberry Pi) ports
    if PI3:
        return glob.glob("/dev/ttyACM*")
    elif PI4:
        return glob.glob("/dev/ttyACM*")

    return []


class SerialManager(EventDispatcher):
    """
    SerialManager class is responsible for creating and managing the serial communication between Easycut and the
    SmartBench.
    """

    __instance = None

    def __new__(cls, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.__instance = super(SerialManager, cls).__new__(cls)
        return cls.__instance

    _enabled = True

    _serial = None
    _serial_lock = threading.Lock()

    _procedure_thread = None

    _ports_to_try = None

    def __init__(self, **kwargs):
        super(SerialManager, self).__init__(**kwargs)

        self.register_event_type("on_connection_success")
        self.register_event_type("on_connection_failure")

        self._ports_to_try = get_ports_to_try()

        self._procedure_thread = threading.Thread(target=self.do_connection_procedure)
        self._procedure_thread.start()

    def do_connection_procedure(self):
        for port in self._ports_to_try:
            self._serial = serial.Serial(port, BAUD_RATE, timeout=1)
            if self._serial.is_open:
                self.dispatch("on_connection_success", port)
                break

        if not self._serial.is_open:
            self.dispatch("on_connection_failure")

    def on_connection_success(self, port):
        Logger.info("Serial connection established on port: {}.".format(port))
        pass

    def on_connection_failure(self, *args):
        Logger.error("Serial connection failed.")
        pass


if __name__ == '__main__':
    sm = SerialManager()
