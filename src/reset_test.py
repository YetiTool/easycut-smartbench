import os 

smartbench_values_dir = './sb_values/'
set_up_options_file_path = smartbench_values_dir + 'set_up_options.txt'

def set_user_to_view_privacy_notice():
    user_has_seen_privacy_notice = (os.popen('grep "user_has_seen_privacy_notice" /home/pi/easycut-smartbench/src/config.txt').read())
    
    if not user_has_seen_privacy_notice:
        os.system("sudo sed -i -e '$auser_has_seen_privacy_notice=False' /home/pi/easycut-smartbench/src/config.txt")

    elif 'True' in user_has_seen_privacy_notice:
        os.system('sudo sed -i "s/user_has_seen_privacy_notice=True/user_has_seen_privacy_notice=False/" /home/pi/easycut-smartbench/src/config.txt') 


def write_set_up_options():
	file = open(set_up_options_file_path, 'w+')
	file.write(str(True))
	file.close()


def activation_code_proxy():
	activation_code_filepath = "/home/pi/smartbench_activation_code.txt"
	os.system("sudo touch " + activation_code_filepath)

write_set_up_options()
set_user_to_view_privacy_notice()
activation_code_proxy()