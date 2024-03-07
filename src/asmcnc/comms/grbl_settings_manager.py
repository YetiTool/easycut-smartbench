import json
import os
import threading
from datetime import datetime

from kivy.clock import Clock

from asmcnc.core_UI import path_utils


def log(message):
    timestamp = datetime.now()
    print (timestamp.strftime('%H:%M:%S.%f')[:12] + ' ' + str(message))


class GRBLSettingsManagerSingleton(object):
    """
    This class checks GRBL dollar settings at startup and tries to fix them if possible with either saved or default
    values. Settings are categorised according to:
    https://docs.google.com/spreadsheets/d/1aQLjfAx74H8QtpxETJmtgPAJMYqiBHjGcdq0SobJoq8/edit?usp=sharing
    """
    _instance = None
    _initialized = False
    machine = None
    _lock = threading.Lock()
    _received_sn = ''

    SERIAL_ID = 50
    WRITE_DOLLAR_INTERVAL = 0.2  # needed, because serial_connection sequential stream is not thread safe!!!

    # json skeletons
    _machine_saved_data = {
        SERIAL_ID: '0000.00',  # serial number
        100: 0,  # x steps/mm
        101: 0,  # y steps/mm
        102: 0  # z steps/mm
    }

    _machine_fw_default_data = {
        SERIAL_ID: '0.03',  # serial number
        100: 56.649,  # x steps/mm
        101: 56.667,  # y steps/mm
        102: 1066.667  # z steps/mm
    }

    # File paths:
    MACHINE_DATA_FILE_PATH = path_utils.join(path_utils.sb_values_path, "machine_settings.json")

    def __new__(cls, machine=None):
        with cls._lock:
            if cls._instance is None:
                print("Creating new instance of GRBLSettingsManagerSingleton")
                cls._instance = super(GRBLSettingsManagerSingleton, cls).__new__(cls)
            return cls._instance

    def __init__(self, machine=None):
        # Always check for call with machine object:
        if self.machine is None and machine is not None:
            self.machine = machine
            self.machine.s.bind(setting_50=self.on_setting_50)
            self.machine.s.bind(setting_100=lambda instance, value: self.on_setting_steps_per_mm(instance,
                                                                                                 value,
                                                                                                 100))
            self.machine.s.bind(setting_101=lambda instance, value: self.on_setting_steps_per_mm(instance,
                                                                                                 value,
                                                                                                 101))
            self.machine.s.bind(setting_102=lambda instance, value: self.on_setting_steps_per_mm(instance,
                                                                                                 value,
                                                                                                 102))

        if self._initialized:
            return
        self._initialized = True
        # Do init here:
        self.load_machine_data_from_file()

    def load_machine_data_from_file(self):
        """
        Loads the model_data from file. Only do this once in __init__.
        """
        if os.path.exists(self.MACHINE_DATA_FILE_PATH):
            with open(self.MACHINE_DATA_FILE_PATH, 'r') as f:
                tmp = json.load(f)
            for k, v in tmp.items():
                self._machine_saved_data[int(k)] = v

    def save_machine_data_to_file(self):
        """Updates the machine_settings.json with the current data."""
        with open(self.MACHINE_DATA_FILE_PATH, 'w') as f:
            json.dump(self._machine_saved_data, f)

    def on_setting_50(self, instance, value):
        """
        Is called when the serial number ($50) is first read.
        value should be XXXX.YY where YY is the product code.

        Checks for default value and restores value from file if possible.
        """
        self._received_sn = value
        # default? EEPROM error happened -> restored defaults
        if value == self._machine_fw_default_data[self.SERIAL_ID]:
            log('Default serial number detected! Trying to restore from file...')
            # check if saved value exists:
            if self._machine_saved_data[self.SERIAL_ID] != '0000.00':
                # restore saved value:
                Clock.schedule_once(lambda dt: self.machine.write_dollar_setting(
                    self.SERIAL_ID, self._machine_saved_data[self.SERIAL_ID]), self._get_write_interval())
                log('Restored $50 (serial number) from file: {}'.format(self._machine_saved_data[self.SERIAL_ID]))
            else:
                log('Cannot restore serial number. Nothing saved yet!')
        elif self._machine_saved_data[self.SERIAL_ID] == '0000.00':  # not saved yet?
            self._machine_saved_data[self.SERIAL_ID] = value
            self.save_machine_data_to_file()
            log('First startup after update? Serial number saved to file: {}'.format(value))
        elif value != self._machine_saved_data[self.SERIAL_ID]:
            # don't update serial number
            log('Console swapped? new serial number detected: {}'.format(value))
        else:
            # serial number is neither default nor changed. nothing to do!
            pass

    def on_setting_steps_per_mm(self, instance, value, setting):
        """
        Is called when the selected setting is first read:
        - x_steps/mm ($100)
        - y_steps/mm ($101)
        - z_steps/mm ($102)

        Checks for default value and restores value from file if values are from the same machine.
        """
        descriptions = {
            100: 'x_steps/mm ($100) setting',
            101: 'y_steps/mm ($100) setting',
            102: 'z_steps/mm ($100) setting'
        }

        if value == self._machine_fw_default_data[setting]:  # default? EEPROM error happened -> restored defaults
            if self._machine_saved_data[setting] != 0:  # saved value exists?
                if self._machine_saved_data[self.SERIAL_ID] == self._received_sn:  # serial number matches?
                    # restore saved value:
                    Clock.schedule_once(lambda dt: self.machine.write_dollar_setting(setting,
                                        self._machine_saved_data[setting]),
                                        self._get_write_interval())
                    log('Restored {} from file: {}'.format(descriptions[setting], self._machine_saved_data[setting]))
                else:
                    log('Cannot restore {}. Wrong serial detected! Found: {} | Expected: {}'.
                        format(descriptions[setting], self._received_sn, self._machine_saved_data[self.SERIAL_ID]))
            else:
                log('Cannot restore {}. No backup found!'.format(descriptions[setting]))
        elif value != self._machine_saved_data[setting]:  # new values detected?
            if self._machine_saved_data[self.SERIAL_ID] == self._received_sn:  # serial number matches?
                self._machine_saved_data[setting] = value
                self.save_machine_data_to_file()
                log('Calibration run? Updated {} in file: {}'.
                    format(descriptions[setting], value))

    def _get_write_interval(self):
        """
        Returns the next write interval and increases it for the next call.
        This is needed to avoid race conditions with simultaneous write_dollar_setting calls.
        """
        ret = self.WRITE_DOLLAR_INTERVAL
        self.WRITE_DOLLAR_INTERVAL += self.WRITE_DOLLAR_INTERVAL
        return ret





