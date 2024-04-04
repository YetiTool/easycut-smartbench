import time

from typing import Dict, List

from asmcnc.comms.logging_system.logging_system import Logger
from asmcnc.core_UI.new_popups.spindle_load_alert_popup import SpindleLoadAlertPopup


class DigitalSpindleMonitor(object):
    __serial_connection = None

    __faulty_readings = []  # type: List[Dict[str, any]]
    __threshold = 20  # type: int
    __last_alert_time = None  # type: time
    __alert_interval = 60  # type: int  # seconds

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
        Logger.debug('Spindle inrush state changed to: {}'.format(value))
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
        # TODO: Implement other checks for faulty readings.
        if value < 0:
            self.__faulty_readings.append({
                'timestamp': time.time(),
                'value': value,
            })  # TODO: Capture more information about the faulty reading.
            Logger.warning('Faulty reading detected: {}'.format(value))

            threshold_exceeded = len(self.__faulty_readings) >= self.__threshold
            alert_interval_exceeded = (self.__last_alert_time is None
                                       or time.time() - self.__last_alert_time > self.__alert_interval)

            if threshold_exceeded and alert_interval_exceeded:
                Logger.error("Threshold exceeded and alert interval exceeded. Alerting user.")
                self.__last_alert_time = time.time()
                self.__open_alert_popup()

    def __open_alert_popup(self):
        """
        Opens the alert popup.
        :return: None
        """
        # TODO: Add information to the popup.
        spindle_load_alert_popup = SpindleLoadAlertPopup(size_hint=(0.8, 0.8))
        spindle_load_alert_popup.open()

    def get_faulty_readings(self):
        """
        Returns a list of faulty readings.
        :return:
        """
        return self.__faulty_readings

    def get_last_alert_time(self):
        """
        Returns the last alert time.
        :return:
        """
        return self.__last_alert_time

    def get_threshold(self):
        """
        Returns the threshold.
        :return:
        """
        return self.__threshold
