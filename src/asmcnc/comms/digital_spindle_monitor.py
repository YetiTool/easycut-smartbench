import collections
import json
import time

from kivy.app import App
from kivy.clock import Clock

from asmcnc.comms.logging_system.logging_system import Logger
from asmcnc.core_UI.new_popups.spindle_load_alert_popup import SpindleLoadAlertPopup

# TEST_MODE flag will make values above 0 be considered faulty readings.
TEST_MODE = True


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

    __faulty_reading_count = 0  # type: int  # Number of faulty readings.
    __faulty_reading_trigger = 20  # type: int  # Number of faulty readings before alert is triggered.

    __reset_interval = 60 * 10  # type: int  # Time in seconds before the faulty readings are reset.
    __reset_clock = None  # type: Clock

    __spindle_data_stack = collections.deque(maxlen=500)  # type: collections.deque  # List of the last 500 readings.

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
            self.__reset_clock = Clock.schedule_once(self.__reset_faulty_reading_counter, self.__reset_interval)

        self.__spindle_data_stack.append({
            "time": time.time(),
            "spindle": {
                "load": value,
                "temperature": self.__serial_connection.digital_spindle_temperature,
                "kill_time": self.__serial_connection.digital_spindle_kill_time,
                "voltage": self.__serial_connection.digital_spindle_mains_voltage,
            },
            "grbl": {
                "feed_rate": self.__serial_connection.feed_rate,
                "spindle_speed": self.__serial_connection.spindle_speed,
            }
        })

        if self.__serial_connection.spindle_health_check:
            return

        if value == -999 or (TEST_MODE and value > 0):
            self.__add_faulty_reading(value)

    def __reset_faulty_reading_counter(self, dt):
        """
        Resets the faulty reading counter.
        :param dt: kivy clock time.
        :return: None
        """
        Logger.info("Resetting faulty reading counter.")
        self.__faulty_reading_count = 0
        self.__reset_clock = None

    def __add_faulty_reading(self, value):
        """
        Adds a faulty reading to the list of faulty readings.
        :param value: The digital_spindle_load_raw value.
        :return: None
        """
        Logger.warning('Faulty spindle reading detected: {}'.format(value))

        self.__faulty_reading_count += 1

        threshold_exceeded = self.__faulty_reading_count >= self.__faulty_reading_trigger

        if threshold_exceeded:
            self.__trigger_alert()

    def export_diagnostics_file(self):
        """
        Exports the faulty readings to a diagnostics file.
        :return: None
        """
        Logger.info("Exporting diagnostics file.")

        skeleton = {
            "spindle_free_load": self.__serial_connection.spindle_freeload,
            "spindle_data_stack": list(self.__spindle_data_stack),
        }

        with open("diagnostics.json", "w") as f:
            json.dump(skeleton, f)

    def __trigger_alert(self):
        """
        When the threshold is exceeded and the alert interval is exceeded, this method is called to alert the user.
        :return: None
        """
        Logger.error("Invalid data threshold reached, alerting user.")

        machine = App.get_running_app().machine

        if self.__serial_connection.m_state == "Run":
            machine.stop_for_a_stream_pause(reason_for_pause="SPINDLE_LOAD_ALERT")
        else:
            machine.turn_off_spindle()  # Turn off spindle (likely on from spindle button)

        self.export_diagnostics_file()
        Clock.schedule_once(lambda dt: open_alert_popup())
        self.__faulty_reading_count = 0

    def get_faulty_readings(self):
        """
        Returns a list of faulty readings.
        :return: List of faulty readings.
        """
        return self.__faulty_reading_count

    def get_threshold(self):
        """
        Returns the threshold for the number of faulty readings before an alert is triggered.
        :return: The threshold value.
        """
        return self.__faulty_reading_trigger
