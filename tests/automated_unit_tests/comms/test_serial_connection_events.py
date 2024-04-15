import sys

from asmcnc.skavaUI.screen_check_job import CheckingScreen
from asmcnc.skavaUI.screen_go import GoScreen
from asmcnc.skavaUI.widget_gcode_monitor import GCodeMonitor
from automated_unit_tests.unit_test_base import UnitTestBase


sys.path.append('./src')

try:
    import unittest
    import pytest
    from mock import Mock, MagicMock
    from mock.mock import call, ANY, patch

except:
    print("Can't import mocking packages, are you on a dev machine?")

from asmcnc.comms import router_machine
from asmcnc.comms import localization

'''
######################################
RUN FROM easycut-smartbench FOLDER WITH: 
python -m pytest tests/automated_unit_tests/comms/test_serial_connection_events.py
'''


class TestSerialConnectionEvents(UnitTestBase):
    def setUp(self):
        super(TestSerialConnectionEvents, self).setUp()

        # Create modules
        self._create_modules()

    @patch.object(GoScreen, 'update_overload_peak')
    def test_update_overload_peak(self, mock_update_overload_peak):
        """
        Fire the on_update_overload_peak event by serial_connection
        and check if the GoScreen receives and handles it.
        """
        GoScreen(name='go',
                 screen_manager=self._screen_manager,
                 machine=self._router_machine_module,
                 job=self._job_data_module,
                 app_manager=None,
                 database=Mock(),
                 localization=self._localization_module,
                 yetipilot=Mock())
        self._router_machine_module.s.dispatch('on_update_overload_peak', 20)
        mock_update_overload_peak.assert_called_with(ANY, 20)

    @patch.object(GCodeMonitor, 'update_monitor_text_buffer')
    def test_update_monitor_text_buffer(self, mock_update_monitor_text_buffer):
        """
        Fire the on_serial_monitor_update event by serial_connection
        and check if the GCodeMonitor widget receives and handles it.
        """
        GCodeMonitor(screen_manager=self._screen_manager,
                     machine=self._router_machine_module,
                     localization=self._localization_module)
        self._router_machine_module.s.dispatch('on_serial_monitor_update', 'dir', 'myContent')
        mock_update_monitor_text_buffer.assert_called_with('dir', 'myContent')

    @patch.object(GoScreen, 'total_runtime_seconds')
    def test_reset_runtime_counter(self,mock_total_runtime_seconds):
        """
        Fire the on_reset_runtime event by serial_connection
        and check if the GoScreen receives and handles it.
        """
        go_screen = GoScreen(name='go',
                 screen_manager=self._screen_manager,
                 machine=self._router_machine_module,
                 job=self._job_data_module,
                 app_manager=None,
                 database=Mock(),
                 localization=self._localization_module,
                 yetipilot=Mock())
        go_screen.total_runtime_seconds = 1
        self._router_machine_module.s.dispatch('on_reset_runtime')
        self.assertEqual(go_screen.total_runtime_seconds, 0)

    def test_check_finished_event(self):
        """
        Fires on_check_job_finished event from serial_connection
        and checks if CheckingScreen receives and handles it.
        """
        check_job_screen = CheckingScreen(name='check_job',
                                                    screen_manager=self._screen_manager,
                                                    machine=self._router_machine_module,
                                                    job=self._job_data_module,
                                                    localization=self._localization_module)


        test_data = ['line1', 'line2', 'line3', 'line4']
        self._router_machine_module.s.response_log = test_data
        self._router_machine_module.s.dispatch('on_check_job_finished', self._router_machine_module.s.response_log)
        self.assertEqual(check_job_screen.error_log, test_data)
