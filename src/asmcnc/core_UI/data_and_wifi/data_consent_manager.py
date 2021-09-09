from kivy.uix.screenmanager import ScreenManager, Screen
import os

class DataConsentManager(object):

	def __init__(self, screen_manager, first_time_for_user = True):
		self.sm = screen_manager
		self.ftfu = first_time_for_user
		self.set_up_data_screens()

	def set_up_data_screens(self):
		pass

	def open_data_consent(self):
		pass

	def update_seen(self):
		user_has_seen_privacy_notice = (os.popen('grep "user_has_seen_privacy_notice" /home/pi/easycut-smartbench/src/config.txt').read())
		
		if not user_has_seen_privacy_notice:
			os.system("sudo sed -i -e '$auser_has_seen_privacy_notice=True' /home/pi/easycut-smartbench/src/config.txt")

		elif user_has_seen_privacy_notice.endswith('False'):
			os.system('sudo sed -i "s/user_has_seen_privacy_notice=False/user_has_seen_privacy_notice=True/" /home/pi/easycut-smartbench/src/config.txt') 
