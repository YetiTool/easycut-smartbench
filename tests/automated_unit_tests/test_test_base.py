import unittest

from tests.automated_unit_tests.test_base import UnitTestBase


class TestTestBase(UnitTestBase):
    def setUp(self):
        super(TestTestBase, self).setUp()

        # Create modules
        self._create_modules()

    def test_create_serial_connection(self):
        # Check that the serial connection is not None
        self.assertIsNotNone(self._serial_connection_module)

        # Check that the alarm is not None
        self.assertIsNotNone(self._serial_connection_module.alarm)

    def test_create_router_machine(self):
        # Check that the router machine is not None
        self.assertIsNotNone(self._router_machine_module)

    def test_create_protocol(self):
        # Check that the protocol is not None
        self.assertIsNotNone(self._protocol_module)

    def test_create_job_data(self):
        # Check that the job data is not None
        self.assertIsNotNone(self._job_data_module)

    def test_create_settings_manager(self):
        # Check that the settings manager is not None
        self.assertIsNotNone(self._settings_manager_module)

    def test_create_screen_manager(self):
        # Check that the screen manager is not None
        self.assertIsNotNone(self._screen_manager)

    def test_create_localization(self):
        # Check that the localization is not None
        self.assertIsNotNone(self._localization_module)


if __name__ == '__main__':
    unittest.main()
