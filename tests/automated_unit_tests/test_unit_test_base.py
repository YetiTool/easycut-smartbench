import logging
import unittest
from .unit_test_base import UnitTestBase
"""
Run unit tests with: python -m unittest discover -s tests/automated_unit_tests
or in IDE
"""


class TestUnitTestBase(UnitTestBase):

    def setUp(self):
        super(TestUnitTestBase, self).setUp()
        self._create_modules()

    def test_create_serial_connection(self):
        self.assertIsNotNone(self._serial_connection_module)
        self.assertIsNotNone(self._serial_connection_module.alarm)

    def test_create_router_machine(self):
        self.assertIsNotNone(self._router_machine_module)

    def test_create_protocol(self):
        self.assertIsNotNone(self._protocol_module)

    def test_create_job_data(self):
        self.assertIsNotNone(self._job_data_module)

    def test_create_settings_manager(self):
        self.assertIsNotNone(self._settings_manager_module)

    def test_create_screen_manager(self):
        self.assertIsNotNone(self._screen_manager)

    def test_create_localization(self):
        self.assertIsNotNone(self._localization_module)


if __name__ == '__main__':
    unittest.main()
