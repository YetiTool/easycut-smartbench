from kivy.uix.screenmanager import ScreenManager, Screen
import os
from asmcnc.apps.start_up_sequence.data_consent_app.screens import wifi_and_data_consent_1, wifi_and_data_consent_2, wifi_and_data_consent_3
from asmcnc.core_UI.popups import BasicPopup, PopupType
from asmcnc.comms.logging_system.logging_system import Logger
from asmcnc.core_UI.utils import color_provider

class ScreenManagerDataConsent(object):

	return_to_screen = 'build_info'
	back_to_screen = 'build_info'

	def __init__(self, start_sequence, screen_manager, localization):
		self.start_seq = start_sequence
		self.sm = screen_manager
		self.l = localization
		self.set_up_data_screens()

	def set_up_data_screens(self):
		if not self.sm.has_screen('consent_1'):
			consent_1_screen = wifi_and_data_consent_1.WiFiAndDataConsentScreen1(name='consent_1', start_sequence = self.start_seq, consent_manager = self, localization = self.l)
			self.sm.add_widget(consent_1_screen)

		if not self.sm.has_screen('consent_2'):
			consent_2_screen = wifi_and_data_consent_2.WiFiAndDataConsentScreen2(name='consent_2', start_sequence = self.start_seq, consent_manager = self, localization = self.l)
			self.sm.add_widget(consent_2_screen)

		if not self.sm.has_screen('consent_3'):
			consent_3_screen = wifi_and_data_consent_3.WiFiAndDataConsentScreen3(name='consent_3', start_sequence = self.start_seq, consent_manager = self, localization = self.l)
			self.sm.add_widget(consent_3_screen)

		try:
			self.start_seq.add_screen_to_sequence('consent_1')
			self.start_seq.add_screen_to_sequence('consent_2')
			self.start_seq.add_screen_to_sequence('consent_3')

			if not self.start_seq.screen_sequence.index('consent_1'):
				self.sm.get_screen('consent_1').prev_screen_button.opacity = 0

		except:
			pass

	def open_data_consent(self, screen_to_go_back_to, screen_to_exit_to):
		self.return_to_screen = screen_to_exit_to
		self.back_to_screen = screen_to_go_back_to
		self.set_up_data_screens()
		self.sm.current = 'consent_1'

	def back_to_previous_screen(self):

		try:
			self.start_seq.prev_in_sequence()

		except:
			self.sm.current = self.back_to_screen
			if self.back_to_screen == 'build_info':
				self.remove_consent_screens()

	def accept_terms_and_enable_wifi(self):
		os.system('sudo rfkill unblock wifi')
		self.exit_data_consent_app()

	def warn_user_before_accepting_decline(self):
		BasicPopup(
			sm=self.sm,
			l=self.l,
			popup_type=PopupType.ERROR,
			popup_width=500,
			popup_height=400,
			title=self.l.get_str('Warning!') + " " + self.l.get_str("Are you sure?"),
			main_string=(
			self.l.get_bold("Are you sure you want to decline the data policy? This will disable the Console Wi-Fi.") + \
			"\n\n" + \
			self.l.get_str("You can change your data preferences in the System Tools app at any time.")
			),
			button_one_text=self.l.get_bold('No, go back'),
			button_one_callback=None,
			button_one_background_color=color_provider.get_rgba("green"),
			button_two_text=self.l.get_bold("Yes, disable Wi-Fi"),
			button_two_callback=self.decline_terms_and_disable_wifi,
			button_two_background_color=[230 / 255., 74 / 255., 25 / 255., 1.],
			main_label_size_hint_y=1.3,
			main_label_padding=(0,0),
			main_layout_padding=(10,20,10,20),
			main_layout_spacing=10,
			main_label_size_delta=120,
			button_layout_padding=(20,0,20,0),
			button_layout_spacing=10,
		).open()

	def decline_terms_and_disable_wifi(self):
		os.system('sudo rfkill block wifi')
		self.exit_data_consent_app()

	def exit_data_consent_app(self):
		self.update_seen()

		try:
			self.start_seq.next_in_sequence()

		except:
			self.sm.current = self.return_to_screen
			if self.back_to_screen == 'build_info':
				self.remove_consent_screens()
				self.remove_entry_screens_if_necessary()

	def remove_consent_screens(self):
		self.destroy_screen('consent_1')
		self.destroy_screen('consent_2')
		self.destroy_screen('consent_3')

	def remove_entry_screens_if_necessary(self):
		self.destroy_screen('release_notes')

	def destroy_screen(self, screen_name):
		if self.sm.has_screen(screen_name):
			self.sm.remove_widget(self.sm.get_screen(screen_name))
			Logger.info(screen_name + ' deleted')

	def update_seen(self):
		user_has_seen_privacy_notice = (os.popen('grep "user_has_seen_privacy_notice" /home/pi/easycut-smartbench/src/config.txt').read())
		
		if not user_has_seen_privacy_notice:
			os.system("sudo sed -i -e '$auser_has_seen_privacy_notice=True' /home/pi/easycut-smartbench/src/config.txt")

		elif 'False' in user_has_seen_privacy_notice:
			os.system('sudo sed -i "s/user_has_seen_privacy_notice=False/user_has_seen_privacy_notice=True/" /home/pi/easycut-smartbench/src/config.txt')
