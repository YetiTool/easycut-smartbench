import os

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


def set_machine_drywall(is_drywall):
    # (bool) -> None
    """
    Creates the dwt.txt file.
    """
    if is_drywall:
        if not os.path.exists(DWT_FILE_PATH):
            open(DWT_FILE_PATH, "w").close()
    else:
        if os.path.exists(DWT_FILE_PATH):
            os.remove(DWT_FILE_PATH)

    __set_splash_screen()


def __set_splash_screen():
    # () -> None
    """
    Sets the plymouth splash screen to the appropriate one.
    """
    new_splash = DWT_SPLASH_PATH if is_machine_drywall() else YETI_SPLASH_PATH
    os.system("sudo cp {} {}".format(new_splash, PLYMOUTH_SPLASH_FILE_PATH))

