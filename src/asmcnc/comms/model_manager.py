import json
import os
import threading
from hashlib import md5

from kivy._event import EventDispatcher
from kivy.clock import Clock

from asmcnc.comms.router_machine import ProductCodes



class ModelManagerSingleton(EventDispatcher):
    _instance = None
    _initialized = False
    product_code = ProductCodes.UNKNOWN
    _lock = threading.Lock()

    # File paths:
    PC_FILE_PATH = os.path.join(os.getcwd(), "sb_values", "model_info.json")
    PC_MIGRATION_PATH = os.path.join(os.getcwd(), "asmcnc", "comms", "product_code_migration")
    MIGRATION_FILE_PATH = os.path.join(PC_MIGRATION_PATH, "migration.json")
    MIGRATION_RAW_FILE_PATH = os.path.join(PC_MIGRATION_PATH, "migration_raw.json")

    PLYMOUTH_SPLASH_FILE_PATH = "/usr/share/plymouth/debian-logo.png"
    SKAVA_UI_IMAGES_PATH = os.path.join(os.getcwd(), "asmcnc", "skavaUI", "img")
    YETI_SPLASH_PATH = os.path.join(SKAVA_UI_IMAGES_PATH, "yeti_splash_screen.png")
    DWT_SPLASH_PATH = os.path.join(SKAVA_UI_IMAGES_PATH, "dwt_splash_screen.png")

    def __new__(cls, machine=None):
        with cls._lock:
            if cls._instance is None:
                print("Creating new instance of ModelManagerSingleton")
                cls._instance = super(ModelManagerSingleton, cls).__new__(cls)
            return cls._instance

    def __init__(self, machine=None):
        # Always check for call with machine object:
        if machine is not None:
            self.machine = machine
            # we only need the update when we have no file yet.
            if not os.path.exists(self.PC_FILE_PATH):
                self.machine.s.bind(setting_50=self.on_setting_50)

        if self._initialized:
            return
        self._initialized = True
        # Do init here:
        self.set_machine_type(self.load_saved_product_code())
        self._process_raw_migration_file()

    def _process_raw_migration_file(self):
        """This function will only run once when a new migration_raw.json file was added."""
        if os.path.exists(self.MIGRATION_RAW_FILE_PATH):
            with open(self.MIGRATION_RAW_FILE_PATH, 'r') as f:
                d = json.load(f)
                d['Pro Plus'] = [md5(s).hexdigest() for s in d['Pro Plus']]
                d['Pro X'] = [md5(s).hexdigest() for s in d['Pro X']]
            with open(self.MIGRATION_FILE_PATH, 'w') as f:
                json.dump(d, f)

    def on_setting_50(self, instance, value):
        """is called when the serial number ($50) is first read.
        value should be XXXX.YY where YY is the product code.

        Also fixes Pro Plus and Pro X machines in the field."""
        try:
            serial_number = str(value).split('.')[0]
            pc_value = int(str(value).split('.')[1])
            self.fix_wrong_product_code(serial_number, pc_value)
            self.set_machine_type(ProductCodes(pc_value), True)
        except:
            # this should only happen when then machine has no serial number yet (first boot)
            # so we do nothing. ;)
            pass

    def fix_wrong_product_code(self, sn, old_pc):
        """Checks if the machine was produced with a wrong product code. 03 != 04,05"""
        if not os.path.exists(self.MIGRATION_FILE_PATH):
            return ProductCodes.UNKNOWN
        with open(self.MIGRATION_FILE_PATH, 'r') as f:
            data = json.load(f)
        os.remove(self.MIGRATION_FILE_PATH)
        if md5('YS6' + sn).hexdigest() in data['Pro Plus']:
            full_sn = sn + '.04'
            print('Old Pro Plus detected. Fixed SN to: {}'.format(full_sn))
            Clock.schedule_once(lambda dt: self.machine.write_dollar_setting(50, full_sn), 1)
            return ProductCodes.PRECISION_PRO_PLUS
        elif md5(sn).hexdigest() in data['Pro X']:
            full_sn = sn + '.05'
            print('Old Pro X detected. Fixed SN to: {}'.format(full_sn))
            Clock.schedule_once(lambda dt: self.machine.write_dollar_setting(50, full_sn), 1)
            return ProductCodes.PRECISION_PRO_X


    def is_machine_drywall(self):
        # () -> bool
        """
        Checks for the existence of the dwt.txt file.
        :return: True if the file exists, False otherwise.
        """
        return self.product_code is ProductCodes.DRYWALLTEC

    def set_machine_type(self, pc, save=False):
        # type: (ProductCodes, bool) ->  None
        # (bool) -> None
        """
        Sets the console to a specific product code. See ProductCodes for more info.
        Takes care of additional needed changes like splash screen.
        """
        if self.product_code == pc:
            return
        self.product_code = pc
        if save:
            self.save_product_code(pc)

        self.__set_splash_screen(pc)

    def __set_splash_screen(self, pc):
        # type: (ProductCodes) ->  None
        """
        Sets the plymouth splash screen to the appropriate one.
        """
        if pc is ProductCodes.DRYWALLTEC:
            os.system("sudo cp {} {}".format(self.DWT_SPLASH_PATH, self.PLYMOUTH_SPLASH_FILE_PATH))
        else:
            os.system("sudo cp {} {}".format(self.YETI_SPLASH_PATH, self.PLYMOUTH_SPLASH_FILE_PATH))

    def load_saved_product_code(self):
        """Returns the saved product code or UNKNOWN if nothing was saved yet."""
        if not os.path.exists(self.PC_FILE_PATH):
            return ProductCodes.UNKNOWN
        else:
            with open(self.PC_FILE_PATH, 'r') as f:
                d = json.load(f)
            for pc in ProductCodes:
                if md5(str(pc.value)).hexdigest() == d['product_code']:
                    return pc

    def save_product_code(self, pc):
        # type: (ProductCodes) -> None
        hashed_pc = md5(str(pc.value)).hexdigest()
        d = {'product_code': hashed_pc}

        with open(self.PC_FILE_PATH, 'w') as f:
            json.dump(d, f)


