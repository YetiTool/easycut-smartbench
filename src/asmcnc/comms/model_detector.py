import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.getcwd()))
DWT_FILE_PATH = os.path.join(ROOT_DIR, "dwt.txt")


def is_machine_drywall():
    # () -> bool
    """
    Checks for the existence of the dwt.txt file.
    :return: True if the file exists, False otherwise.
    """
    return os.path.exists(DWT_FILE_PATH)
