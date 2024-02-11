import unittest
import sys

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager

from asmcnc.keyboard.custom_keyboard import Keyboard

"""
Need to use sys.path.append to add the src folder to the path so that the imports work

I think this is a hacky way of doing it, but it works for now. 
"""

sys.path.append('./src')

from asmcnc.comms.localization import Localization
from asmcnc.comms.router_machine import RouterMachine
from asmcnc.comms.serial_connection import SerialConnection
from asmcnc.comms.yeti_grbl_protocol.protocol import protocol_v2
from asmcnc.job.job_data import JobData
from settings.settings_manager import Settings

"""
Run unit tests with: python -m unittest discover -s tests/automated_unit_tests
"""


class UnitTestBase(unittest.TestCase):
    _serial_connection = None  # type: SerialConnection
    _router_machine_module = None  # type: RouterMachine
    _localization_module = None  # type: Localization
    _protocol_module = None  # type: protocol_v2
    _screen_manager = None  # type: ScreenManager
    _settings_manager_module = None  # type: Settings
    _job_data_module = None  # type: JobData
    _keyboard_module = None  # type: Keyboard

    def setUp(self):
        self._app = App()
        self._app.width = 800
        self._app.height = 480

    def _create_serial_connection_module(
        self, machine, screen_manager, settings_manager, localization, job
    ):
        return SerialConnection(
            machine=machine,
            screen_manager=screen_manager,
            settings_manager=settings_manager,
            localization=localization,
            job=job,
        )

    def _create_router_machine_module(
        self, screen_manager, settings_manager, localization, job, win_serial_port="COM"
    ):
        return RouterMachine(
            win_serial_port=win_serial_port,
            screen_manager=screen_manager,
            settings_manager=settings_manager,
            localization=localization,
            job=job,
        )

    def _create_localization_module(self):
        return Localization()  # Refactor name to localisation?

    def _create_protocol_module(self):
        return protocol_v2()

    def _create_screen_manager(self):
        return ScreenManager()

    def _create_job_data_module(self, localization, settings_manager):
        return JobData(localization=localization, settings_manager=settings_manager)

    def _create_settings_manager_module(self, screen_manager):
        return Settings(screen_manager=screen_manager)

    def _create_keyboard(self, localization):
        return Keyboard(localization=localization)

    def _create_modules(self):
        self._localization_module = self._create_localization_module()

        self._screen_manager = self._create_screen_manager()

        self._settings_manager_module = self._create_settings_manager_module(
            self._screen_manager
        )

        self._job_data_module = self._create_job_data_module(
            self._localization_module, self._settings_manager_module
        )

        self._protocol_module = self._create_protocol_module()

        self._router_machine_module = self._create_router_machine_module(
            self._screen_manager,
            self._settings_manager_module,
            self._localization_module,
            self._job_data_module,
        )

        self._serial_connection_module = self._create_serial_connection_module(
            self._router_machine_module,
            self._screen_manager,
            self._settings_manager_module,
            self._localization_module,
            self._job_data_module,
        )

        self._keyboard_module = self._create_keyboard(
            self._localization_module
        )


if __name__ == "__main__":
    unittest.main()
