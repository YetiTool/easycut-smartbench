from itertools import combinations
import os
import subprocess
from asmcnc.comms.logging_system.logging_system import Logger

smartbench_values_dir = "./sb_values/"
set_up_options_file_path = smartbench_values_dir + "set_up_options.txt"


def set_check_config_flag():
    os.system('sudo sed -i "s/check_config=False/check_config=True/" config.txt')


def write_set_up_options():
    file = open(set_up_options_file_path, "w+")
    file.write(str(True))
    file.close()


def set_user_to_view_privacy_notice():
    user_has_seen_privacy_notice = os.popen(
        'grep "user_has_seen_privacy_notice" /home/pi/easycut-smartbench/src/config.txt'
    ).read()
    if not user_has_seen_privacy_notice:
        os.system(
            "sudo sed -i -e '$auser_has_seen_privacy_notice=False' /home/pi/easycut-smartbench/src/config.txt"
        )
    elif "True" in user_has_seen_privacy_notice:
        os.system(
            'sudo sed -i "s/user_has_seen_privacy_notice=True/user_has_seen_privacy_notice=False/" /home/pi/easycut-smartbench/src/config.txt'
        )


def activation_code_proxy():
    activation_code_filepath = "/home/pi/smartbench_activation_code.txt"
    os.system("sudo touch " + activation_code_filepath)


def welcome_user_to_smartbench():
    show_user_welcome_app = os.popen(
        'grep "show_user_welcome_app" /home/pi/easycut-smartbench/src/config.txt'
    ).read()
    if not show_user_welcome_app:
        os.system(
            "sudo sed -i -e '$ashow_user_welcome_app=True' /home/pi/easycut-smartbench/src/config.txt"
        )
    elif "False" in show_user_welcome_app:
        os.system(
            'sudo sed -i "s/show_user_welcome_app=False/show_user_welcome_app=True/" /home/pi/easycut-smartbench/src/config.txt'
        )


def set_release_notes():
    os.system(
        'sudo sed -i "s/power_cycle_alert=False/power_cycle_alert=True/" /home/pi/easycut-smartbench/src/config.txt'
    )


def do_pro_config():
    user_has_seen_pro_plus_safety = os.popen(
        'grep "user_has_seen_pro_plus_safety" /home/pi/easycut-smartbench/src/config.txt'
    ).read()
    if "True" in user_has_seen_pro_plus_safety:
        os.system(
            'sudo sed -i "s/user_has_seen_pro_plus_safety=True/user_has_seen_pro_plus_safety=False/" /home/pi/easycut-smartbench/src/config.txt'
        )


def set_pro_safety_with_file():
    os.system("touch /home/pi/plus.txt")
    do_pro_config()


def set_pro_safety_no_file():
    os.system("rm /home/pi/plus.txt")
    do_pro_config()


function_list = [
    set_user_to_view_privacy_notice,
    activation_code_proxy,
    welcome_user_to_smartbench,
    set_release_notes,
    set_pro_safety_no_file,
]
min_r = 1
max_r = 6
for r in range(min_r, max_r):
    for sublist in list(combinations(function_list, r)):
        Logger.info(sublist)
        for i in sublist:
            i()
        set_check_config_flag()
        cmd = ["python", "main.py"]
        subprocess.Popen(cmd).wait()
