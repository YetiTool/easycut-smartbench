import sys


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

#test_utils.create_app()


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
