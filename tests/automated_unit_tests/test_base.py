import unittest

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from mock.mock import Mock

from asmcnc.comms.localization import Localization
from asmcnc.comms.serial_connection import SerialConnection


def _create_screen_manager():
    return ScreenManager()


class UnitTestBase(unittest.TestCase):
    def setUp(self):
        self.__app = App()
        self.__app.width = 800
        self.__app.height = 480

        self.__screen_manager = _create_screen_manager()

    def tearDown(self):
        self.__app.stop()

    def test_create_serial_connection(self):
        serial_connection = SerialConnection(
            machine=Mock(),
            screen_manager=self.__screen_manager,
            settings_manager=Mock(),
            localization=Localization(),
            job=Mock(),
        )

        assert serial_connection is not None
        assert serial_connection.alarm is not None


if __name__ == '__main__':
    unittest.main()
