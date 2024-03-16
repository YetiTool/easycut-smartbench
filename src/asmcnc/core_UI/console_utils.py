import os, sys, json


def correct_shutdown():
    correct_shutdown_flag = (os.popen('grep "correct_shutdown" config.txt').read())
    if 'False' in correct_shutdown_flag:
        return True
    else:
        if not correct_shutdown_flag:
            os.system("sudo sed -i -e '$acorrect_shutdown=False' /home/pi/easycut-smartbench/src/config.txt")
        elif 'True' in correct_shutdown_flag:
            os.system('sudo sed -i "s/correct_shutdown=True/correct_shutdown=False/" config.txt')
        return False


def shutdown():
    if sys.platform != 'win32' and sys.platform != 'darwin':
        os.system('sudo sed -i "s/correct_shutdown=False/correct_shutdown=True/" config.txt')
        os.system('sudo shutdown -h now')


def cancel_shutdown():
    if sys.platform != 'win32' and sys.platform != 'darwin':
        os.system('sudo sed -i "s/correct_shutdown=True/correct_shutdown=False/" config.txt')
        os.system('sudo shutdown -c')


def reboot():
    if sys.platform != 'win32' and sys.platform != 'darwin':
        os.system('sudo sed -i "s/correct_shutdown=False/correct_shutdown=True/" config.txt')
        os.system("sudo reboot")
