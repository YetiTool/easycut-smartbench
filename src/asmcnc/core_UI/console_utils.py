import os
import sys
from asmcnc.comms.grbl_settings_manager import GRBLSettingsManagerSingleton


def correct_shutdown(*args):
    correct_shutdown_flag = os.popen('grep "correct_shutdown" config.txt').read()
    if GRBLSettingsManagerSingleton().has_rig_settings():
        return True
    if "False" in correct_shutdown_flag:
        return False
    else:
        if not correct_shutdown_flag:
            os.system(
                "sudo sed -i -e '$acorrect_shutdown=False' /home/pi/easycut-smartbench/src/config.txt"
            )
        elif "True" in correct_shutdown_flag:
            os.system(
                'sudo sed -i "s/correct_shutdown=True/correct_shutdown=False/" config.txt'
            )
        return True


def shutdown(*args):
    if sys.platform != "win32" and sys.platform != "darwin":
        os.system(
            'sudo sed -i "s/correct_shutdown=False/correct_shutdown=True/" config.txt'
        )
        os.system("sudo shutdown -h")


def shutdown_now(*args):
    if sys.platform != "win32" and sys.platform != "darwin":
        os.system(
            'sudo sed -i "s/correct_shutdown=False/correct_shutdown=True/" config.txt'
        )
        os.system("sudo shutdown -h now")


def cancel_shutdown(*args):
    if sys.platform != "win32" and sys.platform != "darwin":
        os.system(
            'sudo sed -i "s/correct_shutdown=True/correct_shutdown=False/" config.txt'
        )
        os.system("sudo shutdown -c")


def reboot(*args):
    if sys.platform != "win32" and sys.platform != "darwin":
        os.system(
            'sudo sed -i "s/correct_shutdown=False/correct_shutdown=True/" config.txt'
        )
        os.system("sudo reboot")
