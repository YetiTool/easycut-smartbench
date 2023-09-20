import os

smartbench_values_dir = "./sb_values/"
set_up_options_file_path = smartbench_values_dir + "set_up_options.txt"


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


def write_set_up_options():
    file = open(set_up_options_file_path, "w+")
    file.write(str(True))
    file.close()


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


def set_check_config_flag():
    os.system('sudo sed -i "s/check_config=False/check_config=True/" config.txt')


write_set_up_options()
set_user_to_view_privacy_notice()
activation_code_proxy()
welcome_user_to_smartbench()
os.system(
    'sudo sed -i "s/power_cycle_alert=False/power_cycle_alert=True/" /home/pi/easycut-smartbench/src/config.txt'
)
set_check_config_flag()
