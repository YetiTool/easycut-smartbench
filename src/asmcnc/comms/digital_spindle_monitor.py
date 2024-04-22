import time

from kivy.clock import Clock
from typing import Dict, List

from asmcnc.comms.logging_system.logging_system import Logger
from asmcnc.core_UI.new_popups.spindle_load_alert_popup import SpindleLoadAlertPopup

# TEST_MODE flag will make values above 0 be considered faulty readings.
TEST_MODE = False


def open_alert_popup():
    """
    Opens the alert popup.
    Call from main thread to ensure the popup is opened and rendered correctly.

    :return: None
    """
    # TODO: Add information to the popup.
    spindle_load_alert_popup = SpindleLoadAlertPopup(size_hint=(0.8, 0.8))
    spindle_load_alert_popup.open()


class DigitalSpindleMonitor(object):
    """
    A class that monitors the digital spindle load and alerts the user if a faulty reading is detected.

    Public Methods
    -------
    on_is_spindle_in_inrush_state_change(instance, value) -> None
        Callback for when the spindle inrush state changes.
    on_digital_spindle_load_raw_change(instance, value) -> None
        Callback for when the digital spindle load raw value changes.
    get_faulty_readings() -> List[Dict[str, any]]
        Returns a list of faulty readings.
    get_last_alert_time() -> time
        Returns the last alert time.
    get_threshold() -> int
        Returns the threshold.
    """

    __serial_connection = None

    __faulty_readings = []  # type: List[Dict[str, any]]
    __threshold = 20  # type: int  # Number of faulty readings before alert is triggered.
    __reset_interval = 60 * 10  # type: int  # Time in seconds before the faulty readings are reset.
    __reset_clock = None  # type: Clock

    def __init__(self, serial_connection):
        """
        :param serial_connection: SerialConnection object to bind to.
        """
        Logger.info("Starting digital spindle monitor.")

        self.__serial_connection = serial_connection
        self.__serial_connection.bind(is_spindle_in_inrush_state=self.on_is_spindle_in_inrush_state_change)

    def on_is_spindle_in_inrush_state_change(self, instance, value):
        """
        Callback for when the spindle inrush state changes.
        :param instance: SerialConnection object.
        :param value: New value of the spindle inrush state.
        :return:
        """
        Logger.debug("Spindle inrush state changed to: {}".format(value))
        if value:
            self.__serial_connection.unbind(digital_spindle_load_raw=self.on_digital_spindle_load_raw_change)
        else:
            self.__serial_connection.bind(digital_spindle_load_raw=self.on_digital_spindle_load_raw_change)

    def on_digital_spindle_load_raw_change(self, instance, value):
        """
        Callback for when the digital spindle load raw value changes.
        :param instance: SerialConnection object.
        :param value: New value of the digital spindle load raw.
        :return:
        """
        if not self.__reset_clock:
            self.__reset_clock = Clock.schedule_once(self.__reset_faulty_readings, self.__reset_interval)

        if value == -999 or (TEST_MODE and value > 0):
            self.__add_faulty_reading(value)

    def __reset_faulty_readings(self, dt):
        """
        Resets the list of faulty readings.
        :param dt: Time in seconds.
        :return: None
        """
        Logger.info("Resetting faulty readings.")
        self.__faulty_readings = []
        self.__reset_clock = None

    def __add_faulty_reading(self, value):
        """
        Adds a faulty reading to the list of faulty readings.
        :param value: The digital_spindle_load_raw value.
        :return: None
        """
        Logger.warning('Faulty spindle reading detected: {}'.format(value))

        self.__faulty_readings.append({
            'timestamp': time.time(),
            'value': value,
            'raw_status': self.__serial_connection.raw_status,
        })

        threshold_exceeded = len(self.__faulty_readings) >= self.__threshold

        if threshold_exceeded:
            self.__trigger_alert()

    def __trigger_alert(self):
        """
        When the threshold is exceeded and the alert interval is exceeded, this method is called to alert the user.
        :return: None
        """
        Logger.error("Invalid data threshold reached, alerting user.")

        Clock.schedule_once(lambda dt: open_alert_popup())
        self.__faulty_readings = []

    def get_faulty_readings(self):
        """
        Returns a list of faulty readings.
        :return: List of faulty readings.
        """
        return self.__faulty_readings

    def get_threshold(self):
        """
        Returns the threshold for the number of faulty readings before an alert is triggered.
        :return: The threshold value.
        """
        return self.__threshold
