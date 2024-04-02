import unittest

from kivy.event import EventDispatcher
from kivy.properties import BooleanProperty, NumericProperty

from asmcnc.comms.digital_spindle_monitor import DigitalSpindleMonitor


class DigitalSpindleMonitorMockSerialConnection(EventDispatcher):
    """Skeleton class to mock serial connection object with only the properties and methods used by the digital
    spindle monitor."""
    is_spindle_in_inrush_state = BooleanProperty(True)
    digital_spindle_load_raw = NumericProperty(0, force_dispatch=True)
    spindle_on = BooleanProperty(False)

    def __init__(self):
        super(DigitalSpindleMonitorMockSerialConnection, self).__init__()


# Can only be run individually otherwise the Kivy properties will not be reset between tests.
class TestDigitalSpindleMonitor(unittest.TestCase):
    def test_on_is_spindle_in_inrush_state_change(self):
        """Test that the digital spindle monitor binds to the digital spindle load raw property when the spindle
        inrush state changes to True."""
        mock_serial_connection = DigitalSpindleMonitorMockSerialConnection()
        digital_spindle_monitor = DigitalSpindleMonitor(mock_serial_connection)

        # Set flags to allow the digital spindle monitor to log a faulty reading.
        mock_serial_connection.is_spindle_in_inrush_state = False
        mock_serial_connection.spindle_on = True

        # Check that the digital spindle monitor logs a faulty reading when the digital spindle load raw value is -999.
        mock_serial_connection.digital_spindle_load_raw = -999
        self.assertEqual(len(digital_spindle_monitor.get_faulty_readings()), 1)

        # Set is_spindle_in_inrush_state flag to True to prevent the digital spindle monitor from logging a faulty
        # reading.
        mock_serial_connection.is_spindle_in_inrush_state = True

        # Check that if digital spindle load is updated, the digital spindle monitor does not log a faulty reading.
        mock_serial_connection.digital_spindle_load_raw = -999
        self.assertEqual(len(digital_spindle_monitor.get_faulty_readings()), 1)

        # Set spindle_on flag to False to prevent the digital spindle monitor from logging a faulty reading.
        mock_serial_connection.spindle_on = False

        # Reset is_spindle_in_inrush_state flag to False to ensure spindle_on flag is checked.
        mock_serial_connection.is_spindle_in_inrush_state = False

        # Check that if spindle_on flag is False, the digital spindle monitor does not log a faulty reading.
        mock_serial_connection.digital_spindle_load_raw = -999
        self.assertEqual(len(digital_spindle_monitor.get_faulty_readings()), 1)

    def test_on_digital_spindle_load_raw_change(self):
        """Test that the digital spindle monitor detects and logs a faulty reading when the digital spindle load raw
        value is -999."""
        mock_serial_connection = DigitalSpindleMonitorMockSerialConnection()
        digital_spindle_monitor = DigitalSpindleMonitor(mock_serial_connection)

        # Set flags to allow the digital spindle monitor to log a faulty reading.
        mock_serial_connection.is_spindle_in_inrush_state = False
        mock_serial_connection.spindle_on = True

        # Send threshold number of faulty readings to trigger an alert.
        for _ in range(digital_spindle_monitor.get_threshold()):
            mock_serial_connection.digital_spindle_load_raw = -999

        # Check that the digital spindle monitor logs an alert when the threshold is exceeded.
        self.assertEqual(len(digital_spindle_monitor.get_faulty_readings()), digital_spindle_monitor.get_threshold())
        self.assertTrue(digital_spindle_monitor.get_last_alert_time() is not None)
