import os

from src.asmcnc.comms.router_machine import ProductCodes

ROOT_DIR = os.path.dirname(os.path.dirname(os.getcwd()))
DWT_FILE_PATH = os.path.join(ROOT_DIR, "dwt.txt")

PLYMOUTH_SPLASH_FILE_PATH = "/usr/share/plymouth/debian-logo.png"

SKAVA_UI_IMAGES_PATH = os.path.join(os.getcwd(), "asmcnc", "skavaUI", "img")
YETI_SPLASH_PATH = os.path.join(SKAVA_UI_IMAGES_PATH, "yeti_splash_screen.png")
DWT_SPLASH_PATH = os.path.join(SKAVA_UI_IMAGES_PATH, "dwt_splash_screen.png")


def is_machine_drywall():
    # () -> bool
    """
    Checks for the existence of the dwt.txt file.
    :return: True if the file exists, False otherwise.
    """
    return os.path.exists(DWT_FILE_PATH)


def set_machine_type(pc):
    # type: (ProductCodes) ->  None
    # (bool) -> None
    """
    Creates the dwt.txt file.
    """
    if pc is ProductCodes.DRYWALLTEC:
        if not os.path.exists(DWT_FILE_PATH):
            open(DWT_FILE_PATH, "w").close()
    else:
        if os.path.exists(DWT_FILE_PATH):
            os.remove(DWT_FILE_PATH)

    __set_splash_screen(pc)


def __set_splash_screen(pc):
    # type: (ProductCodes) ->  None
    """
    Sets the plymouth splash screen to the appropriate one.
    """
    if pc is ProductCodes.DRYWALLTEC:
        os.system("sudo cp {} {}".format(DWT_SPLASH_PATH, PLYMOUTH_SPLASH_FILE_PATH))
    else:
        os.system("sudo cp {} {}".format(YETI_SPLASH_PATH, PLYMOUTH_SPLASH_FILE_PATH))

