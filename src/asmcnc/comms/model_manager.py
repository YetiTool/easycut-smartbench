import json
import os
import threading
from enum import Enum
from hashlib import md5
from asmcnc import paths
from asmcnc.comms.logging_system.logging_system import Logger
from kivy.event import EventDispatcher


class ProductCodes(Enum):
    DRYWALLTEC = 6
    PRECISION_PRO_X = 5
    PRECISION_PRO_PLUS = 4
    PRECISION_PRO = 3
    STANDARD = 2
    FIRST_VERSION = 1
    UNKNOWN = 0


class MachineType(Enum):
    SMARTBENCH = "SmartBench"
    DRYWALLTEC = "DrywallTec"
    UNKNOWN = "Unknown"


class ModelManagerSingleton(EventDispatcher):
    """
    This class takes care of all the model specific handling:
    - saves the product code (hashed) to the console if no file exists (Updating UC). Update only possible via
      factory settings. Update will handle things like splash screen image.
    - saves hw and fw version (updated on change): Will be used to determine model capabilities.
      console swap will update the file with new ZH values.
    - provides model distinction: e.g. is_machine_drywall()
    """

    _instance = None
    _initialized = False
    machine = None
    _lock = threading.Lock()
    _data = {
        "product_code": ProductCodes.UNKNOWN,
        "fw_version": "0.0.0.0",
        "hw_version": "0",
    }
    PC_FILE_PATH = os.path.join(paths.SB_VALUES_PATH, "model_info.json")
    MIGRATION_FOLDER_PATH = os.path.join(paths.COMMS_PATH, "product_code_migration")
    MIGRATION_FILE_PATH = os.path.join(MIGRATION_FOLDER_PATH, "migration.json")
    MIGRATION_RAW_FILE_PATH = os.path.join(MIGRATION_FOLDER_PATH, "migration_raw.json")
    PLYMOUTH_SPLASH_FILE_PATH = "/usr/share/plymouth/debian-logo.png"
    YETI_SPLASH_PATH = os.path.join(paths.SKAVA_UI_IMG_PATH, "yeti_splash_screen.png")
    DWT_SPLASH_PATH = os.path.join(paths.SKAVA_UI_IMG_PATH, "dwt_splash_screen.png")
    SMARTBENCH_DEFAULT_NAME = "My SmartBench"
    SMARTBENCH_DEFAULT_LOCATION = "SmartBench location"
    MODEL_NAME_LOCATIONS = {
        ProductCodes.DRYWALLTEC: {"name": "SmartCNC", "location": "SmartCNC location"}
    }

    def __new__(cls, machine=None):
        with cls._lock:
            if cls._instance is None:
                Logger.debug("Creating new instance of ModelManagerSingleton")
                cls._instance = super(ModelManagerSingleton, cls).__new__(cls)
            return cls._instance

    def __init__(self, machine=None):
        if self.machine is None and machine is not None:
            self.machine = machine
            if not os.path.exists(self.PC_FILE_PATH):
                self.machine.s.bind(setting_50=self.on_setting_50)
            self.machine.s.bind(fw_version=self.on_firmware_version)
            self.machine.s.bind(hw_version=self.on_hardware_version)
        if self._initialized:
            return
        self._initialized = True
        self.load_model_data_from_file()
        self._process_raw_migration_file()

    def _process_raw_migration_file(self):
        """This function will only run once when a new migration_raw.json file was added."""
        if os.path.exists(self.MIGRATION_RAW_FILE_PATH):
            with open(self.MIGRATION_RAW_FILE_PATH, "r") as f:
                d = json.load(f)
                d["Pro Plus"] = [md5(s).hexdigest() for s in d["Pro Plus"]]
                d["Pro X"] = [md5(s).hexdigest() for s in d["Pro X"]]
            with open(self.MIGRATION_FILE_PATH, "w") as f:
                json.dump(d, f)

    def on_firmware_version(self, instance, value):
        """Is called when the firmware_version is first read. Updates the saved firmware_version if changed."""
        if self._data["fw_version"] != value:
            Logger.warning("Save new firmware version to file: {}".format(value))
            self._data["fw_version"] = value
            self.save_model_data_to_file()

    def on_hardware_version(self, instance, value):
        """Is called when the hardware_version is first read. Updates the saved hardware_version if changed."""
        if self._data["hw_version"] != value:
            Logger.warning("Save new hardware version to file: {}".format(value))
            self._data["hw_version"] = value
            self.save_model_data_to_file()

    def on_setting_50(self, instance, value):
        """is called when the serial number ($50) is first read.
        value should be XXXX.YY where YY is the product code.

        Also fixes Pro Plus and Pro X machines in the field."""
        try:
            serial_number = str(value).split(".")[0]
        except:
            serial_number = "0000"
        try:
            pc_value = int(str(value).split(".")[1])
        except:
            pc_value = 0
        fixed_product_code = self.fix_wrong_product_code(serial_number, pc_value)
        if fixed_product_code is not ProductCodes.UNKNOWN:
            self.set_machine_type(fixed_product_code, True)
        elif self._data["product_code"] is ProductCodes.UNKNOWN:
            Logger.info("Initially saved product code to file!")
            self.set_machine_type(ProductCodes(pc_value), True)
        self.__set_default_machine_fields()

    def fix_wrong_product_code(self, sn, old_pc):
        """Checks if the machine was produced with a wrong product code. 03 != 04,05"""
        if not os.path.exists(self.MIGRATION_FILE_PATH):
            return ProductCodes.UNKNOWN
        with open(self.MIGRATION_FILE_PATH, "r") as f:
            data = json.load(f)
        os.remove(self.MIGRATION_FILE_PATH)
        if md5("YS6" + sn).hexdigest() in data["Pro Plus"]:
            full_sn = sn + ".04"
            Logger.warning("Old Pro Plus detected. Fixed SN to: {}".format(full_sn))
            self.machine.write_dollar_setting(50, full_sn)
            self._data["product_code"] = ProductCodes.PRECISION_PRO_PLUS.value
            return ProductCodes.PRECISION_PRO_PLUS
        elif md5(sn).hexdigest() in data["Pro X"]:
            full_sn = sn + ".05"
            Logger.warning("Old Pro X detected. Fixed SN to: {}".format(full_sn))
            self.machine.write_dollar_setting(50, full_sn)
            return ProductCodes.PRECISION_PRO_X
        else:
            return ProductCodes.UNKNOWN

    def is_machine_drywall(self):
        """
        Returns True if the machine is a drywalltec machine, False otherwise.
        """
        return self._data["product_code"] is ProductCodes.DRYWALLTEC

    def is_machine_sb(self):
        """
        Returns True if the machine is a SmartBench machine, False otherwise.
        """
        return self._data["product_code"] in [
            ProductCodes.PRECISION_PRO_X,
            ProductCodes.PRECISION_PRO_PLUS,
            ProductCodes.PRECISION_PRO,
            ProductCodes.STANDARD,
            ProductCodes.FIRST_VERSION,
        ]

    def get_machine_type(self):
        if self._data["product_code"] in [
            ProductCodes.PRECISION_PRO_X,
            ProductCodes.PRECISION_PRO_PLUS,
            ProductCodes.PRECISION_PRO,
            ProductCodes.STANDARD,
            ProductCodes.FIRST_VERSION,
        ]:
            return MachineType.SMARTBENCH
        elif self._data["product_code"] in [ProductCodes.DRYWALLTEC]:
            return MachineType.DRYWALLTEC
        return MachineType.UNKNOWN

    def set_machine_type(self, pc, save=False):
        """
        Sets the console to a specific product code. See ProductCodes for more info.
        Takes care of additional needed changes like splash screen.
        """
        if self._data["product_code"] == pc:
            return
        self._data["product_code"] = pc
        if save:
            self.save_product_code(pc)
        self.__set_splash_screen(pc)
        Logger.debug("Product code set to: {}".format(pc))

    def __set_splash_screen(self, pc):
        """
        Sets the plymouth splash screen to the appropriate one.
        """
        if pc is ProductCodes.DRYWALLTEC:
            os.system(
                "sudo cp {} {}".format(
                    self.DWT_SPLASH_PATH, self.PLYMOUTH_SPLASH_FILE_PATH
                )
            )
        else:
            os.system(
                "sudo cp {} {}".format(
                    self.YETI_SPLASH_PATH, self.PLYMOUTH_SPLASH_FILE_PATH
                )
            )

    def load_model_data_from_file(self):
        """
        Loads the model_data from file. Only do this once in __init__.
        """
        if os.path.exists(self.PC_FILE_PATH):
            with open(self.PC_FILE_PATH, "r") as f:
                tmp = json.load(f)
            for k, v in list(tmp.items()):
                self._data[k] = v
            for pc in ProductCodes:
                if (
                    md5(str(pc.value).encode("utf-8")).hexdigest()
                    == self._data["product_code"]
                ):
                    self._data["product_code"] = pc
                    Logger.info("Read product code from file: {}".format(pc.name))
                    break

    def save_product_code(self, pc):
        """Saves the given product code to model_info.json."""
        Logger.info("Save new product code to file: {}".format(pc))
        self._data["product_code"] = pc
        self.save_model_data_to_file()

    def get_product_code(self):
        return self._data["product_code"]

    def get_product_code_name(self):
        return self._data["product_code"].name

    def save_model_data_to_file(self):
        """Updates the model_info.json with the current data."""
        tmp = dict(self._data)
        for pc in ProductCodes:
            if pc is self._data["product_code"]:
                tmp["product_code"] = md5(str(pc.value)).hexdigest()
                break
        with open(self.PC_FILE_PATH, "w") as f:
            json.dump(tmp, f)

    def __set_default_machine_fields(self):
        """
        Sets the default machine name and location to the relevant strings.
        Either gets the value from the dictionary or uses the default values.

        Only called when the serial number is first read.
        """
        default = {
            "name": self.SMARTBENCH_DEFAULT_NAME,
            "location": self.SMARTBENCH_DEFAULT_LOCATION,
        }
        name_location = self.MODEL_NAME_LOCATIONS.get(
            self._data["product_code"], default
        )
        self.machine.write_device_label(name_location["name"])
        self.machine.write_device_location(name_location["location"])

    def fw_version_greater_or_equal(self, reference_version):
        """
        Compares the machines fw version against a reference_version.

        Returns True if fw version is at least as high as the given reference_version.

        reference_version format: 'x.y.z'
        """
        machine_fw_parts = [int(i) for i in self._data["fw_version"].split(".")[:3]]
        ref_version_parts = [int(i) for i in reference_version.split(".")[:3]]
        return machine_fw_parts >= ref_version_parts

    def is_machine_upgradeable(self):
        """Returns True if the upgrade app should be shown for the current machine."""
        if self._data["product_code"] in [
            ProductCodes.PRECISION_PRO_X,
            ProductCodes.PRECISION_PRO_PLUS,
        ]:
            return True
        elif self._data[
            "product_code"
        ] is ProductCodes.PRECISION_PRO and self.fw_version_greater_or_equal("2.2.8"):
            return True
        else:
            return False
