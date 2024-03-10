import os, sys, json


def shutdown():
    with open('shutdown_handler.json', 'r') as f:
        shutdown_handler = json.load(f)
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
