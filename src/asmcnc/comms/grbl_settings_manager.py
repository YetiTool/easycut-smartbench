import json
import os
import threading
from asmcnc import paths
from asmcnc.comms.logging_system.logging_system import Logger


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
    _received_sn = ""
    SERIAL_ID = 50
    _machine_saved_data = {
        SERIAL_ID: "0000.00",
        "type": "machine",
        (51): -1,
        (100): 0,
        (101): 0,
        (102): 0,
    }
    _machine_fw_default_data = {
        SERIAL_ID: "0.03",
        (100): 56.649,
        (101): 56.667,
        (102): 1066.667,
    }
    _system_default_data = {
        (0): 10,
        (1): 255,
        (2): 4,
        (4): 0,
        (5): 1,
        (6): 0,
        (10): 3,
        (11): 0.01,
        (12): 0.002,
        (13): 0,
        (20): 1,
        (21): 1,
        (22): 1,
        (23): 3,
        (24): 600.0,
        (25): 3000.0,
        (26): 250,
        (27): 15.0,
        (30): 25000,
        (31): 0,
        (32): 0,
        (110): 8000.0,
        (111): 6000.0,
        (112): 750.0,
        (120): 130.0,
        (121): 130.0,
        (122): 200.0,
        (130): 1300.0,
    }
    _system_default_data_rig = {(2): 0, (5): 0, (120): 500.0, (121): 500.0}
    settings_to_save = [51]
    MACHINE_DATA_FILE_PATH = os.path.join(paths.SB_VALUES_PATH, "machine_settings.json")

    def __new__(cls, machine=None):
        with cls._lock:
            if cls._instance is None:
                Logger.info("Creating new instance of GRBLSettingsManagerSingleton")
                cls._instance = super(GRBLSettingsManagerSingleton, cls).__new__(cls)
            return cls._instance

    def __init__(self, machine=None):
        if self.machine is None and machine is not None:
            self.machine = machine
            self.machine.s.bind(
                setting_51=lambda instance, value: self.on_console_specific_setting(
                    instance, value, 51
                )
            )
            self.machine.s.bind(
                setting_50=lambda instance, value: self.on_setting_50(value)
            )
            self.machine.s.bind(
                setting_100=lambda instance, value: self.on_setting_steps_per_mm(
                    value, 100
                )
            )
            self.machine.s.bind(
                setting_101=lambda instance, value: self.on_setting_steps_per_mm(
                    value, 101
                )
            )
            self.machine.s.bind(
                setting_0=lambda instance, value: self.on_persistent_setting(value, 0)
            )
            self.machine.s.bind(
                setting_1=lambda instance, value: self.on_persistent_setting(value, 1)
            )
            self.machine.s.bind(
                setting_2=lambda instance, value: self.on_persistent_setting(value, 2)
            )
            self.machine.s.bind(
                setting_4=lambda instance, value: self.on_persistent_setting(value, 4)
            )
            self.machine.s.bind(
                setting_5=lambda instance, value: self.on_persistent_setting(value, 5)
            )
            self.machine.s.bind(
                setting_6=lambda instance, value: self.on_persistent_setting(value, 6)
            )
            self.machine.s.bind(
                setting_10=lambda instance, value: self.on_persistent_setting(value, 10)
            )
            self.machine.s.bind(
                setting_11=lambda instance, value: self.on_persistent_setting(value, 11)
            )
            self.machine.s.bind(
                setting_12=lambda instance, value: self.on_persistent_setting(value, 12)
            )
            self.machine.s.bind(
                setting_13=lambda instance, value: self.on_persistent_setting(value, 13)
            )
            self.machine.s.bind(
                setting_20=lambda instance, value: self.on_persistent_setting(value, 20)
            )
            self.machine.s.bind(
                setting_21=lambda instance, value: self.on_persistent_setting(value, 21)
            )
            self.machine.s.bind(
                setting_22=lambda instance, value: self.on_persistent_setting(value, 22)
            )
            self.machine.s.bind(
                setting_23=lambda instance, value: self.on_persistent_setting(value, 23)
            )
            self.machine.s.bind(
                setting_24=lambda instance, value: self.on_persistent_setting(value, 24)
            )
            self.machine.s.bind(
                setting_25=lambda instance, value: self.on_persistent_setting(value, 25)
            )
            self.machine.s.bind(
                setting_26=lambda instance, value: self.on_persistent_setting(value, 26)
            )
            self.machine.s.bind(
                setting_27=lambda instance, value: self.on_persistent_setting(value, 27)
            )
            self.machine.s.bind(
                setting_30=lambda instance, value: self.on_persistent_setting(value, 30)
            )
            self.machine.s.bind(
                setting_31=lambda instance, value: self.on_persistent_setting(value, 31)
            )
            self.machine.s.bind(
                setting_32=lambda instance, value: self.on_persistent_setting(value, 32)
            )
            self.machine.s.bind(
                setting_110=lambda instance, value: self.on_persistent_setting(
                    value, 110
                )
            )
            self.machine.s.bind(
                setting_111=lambda instance, value: self.on_persistent_setting(
                    value, 111
                )
            )
            self.machine.s.bind(
                setting_112=lambda instance, value: self.on_persistent_setting(
                    value, 112
                )
            )
            self.machine.s.bind(
                setting_120=lambda instance, value: self.on_persistent_setting(
                    value, 120
                )
            )
            self.machine.s.bind(
                setting_121=lambda instance, value: self.on_persistent_setting(
                    value, 121
                )
            )
            self.machine.s.bind(
                setting_122=lambda instance, value: self.on_persistent_setting(
                    value, 122
                )
            )
            self.machine.s.bind(
                setting_130=lambda instance, value: self.on_persistent_setting(
                    value, 130
                )
            )
        if self._initialized:
            return
        self._initialized = True
        self.load_machine_data_from_file()

    def load_machine_data_from_file(self):
        """
        Loads the model_data from file. Only do this once in __init__.
        """
        if os.path.exists(self.MACHINE_DATA_FILE_PATH):
            with open(self.MACHINE_DATA_FILE_PATH, "r") as f:
                tmp = json.load(f)
            for k, v in list(tmp.items()):
                if k == "type":
                    self._machine_saved_data[k] = v
                else:
                    self._machine_saved_data[int(k)] = v
            if self._machine_saved_data["type"] != "machine":
                Logger.debug(
                    "Running on a rig?: {}".format(self._machine_saved_data["type"])
                )
                self._system_default_data.update(self._system_default_data_rig)

    def save_machine_data_to_file(self):
        """Updates the machine_settings.json with the current data."""
        with open(self.MACHINE_DATA_FILE_PATH, "w") as f:
            json.dump(self._machine_saved_data, f)

    def on_setting_50(self, value):
        """
        Is called when the serial number ($50) is first read.
        value should be XXXX.YY where YY is the product code.

        Checks for default value and restores value from file if possible.
        """
        self._received_sn = value
        if value == self._machine_fw_default_data[self.SERIAL_ID]:
            Logger.warning(
                "Default serial number detected! Trying to restore from file..."
            )
            if self._machine_saved_data[self.SERIAL_ID] != "0000.00":
                self.machine.write_dollar_setting(
                    self.SERIAL_ID, self._machine_saved_data[self.SERIAL_ID]
                )
                Logger.warning(
                    "Restored $50 (serial number) from file: {}".format(
                        self._machine_saved_data[self.SERIAL_ID]
                    )
                )
            else:
                Logger.error("Cannot restore serial number. Nothing saved yet!")
        elif self._machine_saved_data[self.SERIAL_ID] == "0000.00":
            self._machine_saved_data[self.SERIAL_ID] = value
            self.save_machine_data_to_file()
            Logger.info(
                "First startup after update? Serial number saved to file: {}".format(
                    value
                )
            )
        elif value != self._machine_saved_data[self.SERIAL_ID]:
            Logger.warning(
                "Console swapped? new serial number detected: {}".format(value)
            )
        else:
            pass

    def on_setting_steps_per_mm(self, value, setting):
        """
        Is called when the selected setting is first read:
        - x_steps/mm ($100)
        - y_steps/mm ($101)
        - z_steps/mm ($102)

        Checks for default value and restores value from file if values are from the same machine.
        """
        descriptions = {
            (100): "x_steps/mm ($100) setting",
            (101): "y_steps/mm ($101) setting",
            (102): "z_steps/mm ($102) setting",
        }
        if value == self._machine_fw_default_data[setting]:
            if self._machine_saved_data[setting] != 0:
                if self._machine_saved_data[self.SERIAL_ID] == self._received_sn:
                    self.machine.write_dollar_setting(
                        setting, self._machine_saved_data[setting]
                    )
                    Logger.warning(
                        "Restored {} from file: {}".format(
                            descriptions[setting], self._machine_saved_data[setting]
                        )
                    )
                else:
                    Logger.error(
                        "Cannot restore {}. Wrong serial detected! Found: {} | Expected: {}".format(
                            descriptions[setting],
                            self._received_sn,
                            self._machine_saved_data[self.SERIAL_ID],
                        )
                    )
            else:
                Logger.error(
                    "Cannot restore {}. No backup found!".format(descriptions[setting])
                )
        elif value != self._machine_saved_data[setting]:
            if self._machine_saved_data[self.SERIAL_ID] == self._received_sn:
                self._machine_saved_data[setting] = value
                self.save_machine_data_to_file()
                Logger.info(
                    "Calibration run? Updated {} in file: {}".format(
                        descriptions[setting], value
                    )
                )

    def on_persistent_setting(self, value, setting):
        """
        Called when a persistent setting is read in.

        Checks for default value and restores value from file if possible.
        """
        descriptions = {
            (0): "Step pulse, microseconds ($0) setting",
            (1): "Step idle delay, milliseconds ($1) setting",
            (2): "Step port invert, mask ($2) setting",
            (4): "Step enable invert, boolean ($4) setting",
            (5): "Limit pins invert, boolean ($5) setting",
            (6): "Probe pin invert, boolean ($6) setting",
            (10): "Status report, mask ($10) setting",
            (11): "Junction deviation, mm ($11) setting",
            (12): "Arc tolerance, mm ($12) setting",
            (13): "Report inches, boolean ($13) setting",
            (20): "Soft limits, boolean ($20) setting",
            (21): "Hard limits, boolean ($21) setting",
            (22): "Homing cycle, boolean ($22) setting",
            (23): "Homing dir invert, mask ($23) setting",
            (24): "Homing feed, mm/min ($24) setting",
            (25): "Homing seek, mm/min ($25) setting",
            (26): "Homing debounce, milliseconds ($26) setting",
            (27): "Homing pull-off, mm ($27) setting",
            (30): "Max spindle speed, RPM ($30) setting",
            (31): "Min spindle speed, RPM ($31) setting",
            (32): "Laser mode, boolean ($32) setting",
            (110): "X Max rate, mm/min ($110) setting",
            (111): "Y Max rate, mm/min ($111) setting",
            (112): "Z Max rate, mm/min ($112) setting",
            (120): "X Acceleration, mm/sec^2 ($120) setting",
            (121): "Y Acceleration, mm/sec^2 ($121) setting",
            (122): "Z Acceleration, mm/sec^2 ($122) setting",
            (130): "X Max travel, mm ($130) setting",
        }
        if value != self._system_default_data[setting]:
            self.machine.write_dollar_setting(
                setting, self._system_default_data[setting]
            )
            Logger.warning(
                "Restored {} to default: {}".format(
                    descriptions[setting], self._system_default_data[setting]
                )
            )

    def has_rig_settings(self):
        return self._machine_saved_data["type"] != "machine"

    def on_console_specific_setting(self, instance, value, setting):
        """
        Called when a console specific setting is read in.

        Checks if the read in value differs from last recorded value.
        """
        descriptions = {(51): "SC2 ($51) setting"}
        if self._machine_saved_data[setting] == -1:
            self._machine_saved_data[setting] = value
            self.save_machine_data_to_file()
            Logger.info(
                "First startup after update? Setting {} saved to file: {}".format(
                    descriptions[setting], value
                )
            )
        elif value != self._machine_saved_data[setting]:
            self.machine.write_dollar_setting(
                setting, self._machine_saved_data[setting]
            )
            Logger.warning(
                "Restored {} from file: {}".format(
                    descriptions[setting], self._machine_saved_data[setting]
                )
            )

    def save_console_specific_setting(self, setting, value):
        """
        Called externally to change a setting which has not been bound to a function.
        """
        descriptions = {(51): "SC2 ($51) setting"}
        if value != self._machine_saved_data[setting]:
            self._machine_saved_data[setting] = value
            self.save_machine_data_to_file()
            Logger.info("Wrote {} to file: {}".format(descriptions[setting], value))
