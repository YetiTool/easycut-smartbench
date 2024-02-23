import json
import os
import threading
from hashlib import md5

from kivy._event import EventDispatcher

from src.asmcnc.comms.router_machine import ProductCodes



class ModelManagerSingleton(EventDispatcher):
    _instance = None
    _initialized = False
    _lock = threading.Lock()

    # File paths:
    ROOT_DIR = os.path.dirname(os.path.dirname(os.getcwd()))
    DWT_FILE_PATH = os.path.join(ROOT_DIR, "dwt.txt")
    PC_FILE_PATH = os.path.join(os.path.dirname(os.getcwd()), "src", "sb_values", "model_info.json")

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
                self.machine.bind(setting_50=self.on_setting_50)

        if self._initialized:
            return
        self._initialized = True
        # Do init here:
        self.product_code = ProductCodes.UNKNOWN
        self.set_machine_type(self.load_saved_product_code())

    def on_setting_50(self, instance, value):
        """is called when the serial number ($50) is first read.
        value should be XXXX.YY where YY is the product code."""
        try:
            pc_value = int(str(value).split('.')[1])
            self.set_machine_type(ProductCodes(pc_value), True)
        except:
            # this should only happen when then machine has no serial number yet (first boot)
            # so we do nothing. ;)
            pass

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
        Creates the dwt.txt file.
        """
        if self.product_code == pc:
            return
        self.product_code = pc
        if save:
            self.save_product_code(pc)

        if pc is ProductCodes.DRYWALLTEC:
            if not os.path.exists(self.DWT_FILE_PATH):
                open(self.DWT_FILE_PATH, "w").close()
        else:
            if os.path.exists(self.DWT_FILE_PATH):
                os.remove(self.DWT_FILE_PATH)

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


