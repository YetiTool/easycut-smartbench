from kivy.uix.screenmanager import ScreenManager, Screen
import os
from asmcnc.core_UI.data_and_wifi.screens import wifi_and_data_consent_1, wifi_and_data_consent_2, popup_data_wifi_warning

class DataConsentManager(object):

	return_to_screen = 'safety'
	back_to_screen = 'build_info'

	def __init__(self, screen_manager, localization):
		self.sm = screen_manager
		self.l = localization
		self.set_up_data_screens()

	def set_up_data_screens(self):
		if not self.sm.has_screen('consent_1'):
			consent_1_screen = wifi_and_data_consent_1.WiFiAndDataConsentScreen1(name='consent_1', consent_manager = self)
			self.sm.add_widget(consent_1_screen)

		if not self.sm.has_screen('consent_2'):
			consent_2_screen = wifi_and_data_consent_2.WiFiAndDataConsentScreen2(name='consent_2', consent_manager = self)
			self.sm.add_widget(consent_2_screen)

	def open_data_consent(self, screen_to_go_back_to, screen_to_exit_to):
		self.return_to_screen = screen_to_exit_to
		self.back_to_screen = screen_to_go_back_to
		self.set_up_data_screens()
		self.sm.current = 'consent_1'

	def back_to_previous_screen(self):
		self.sm.current = self.back_to_screen
		if self.back_to_screen != 'build_info':
			self.remove_consent_screens()

	def accept_terms_and_enable_wifi(self):
		os.system('sudo rfkill unblock wifi')
		self.exit_data_consent_app()

	def warn_user_before_accepting_decline(self):
		popup_data_wifi_warning.PopupDataAndWiFiDisableWarning(self, self.l)

	def decline_terms_and_disable_wifi(self):
		os.system('sudo rfkill block wifi')
		self.exit_data_consent_app()

	def exit_data_consent_app(self):
		self.update_seen()
		self.sm.current = self.return_to_screen
		self.remove_consent_screens()
		self.remove_entry_screens_if_necessary()

	def remove_consent_screens(self):
		self.destroy_screen('consent_1')
		self.destroy_screen('consent_2')

	def remove_entry_screens_if_necessary(self):
		# Get rid of entry screens as well if necessary
		self.destroy_screen('warranty_5')
		self.destroy_screen('release_notes')

	def destroy_screen(self, screen_name):
		if self.sm.has_screen(screen_name):
			self.sm.remove_widget(self.sm.get_screen(screen_name))
			print (screen_name + ' deleted')

	def update_seen(self):
		user_has_seen_privacy_notice = (os.popen('grep "user_has_seen_privacy_notice" /home/pi/easycut-smartbench/src/config.txt').read())
		
		if not user_has_seen_privacy_notice:
			os.system("sudo sed -i -e '$auser_has_seen_privacy_notice=True' /home/pi/easycut-smartbench/src/config.txt")

		elif user_has_seen_privacy_notice.endswith('False'):
			os.system('sudo sed -i "s/user_has_seen_privacy_notice=False/user_has_seen_privacy_notice=True/" /home/pi/easycut-smartbench/src/config.txt')
