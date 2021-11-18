import os

from asmcnc.apps.start_up_sequence.screens import \
screen_reboot_to_apply_settings, \
screen_release_notes, \
screen_starting_smartbench, \
screen_safety_warning

from asmcnc.apps.start_up_sequence.warranty_app import screen_manager_warranty
from asmcnc.apps.start_up_sequence.data_consent_app import screen_manager_data_consent
from asmcnc.apps.start_up_sequence.welcome_to_smartbench_app import screen_manager_welcome_to_smartbench


class StartUpSequence(object):

	screen_sequence = []
	seq_step = 0
	reboot_in_sequence = False

	welcome_sm = None
	release_notes_screen = None
	data_consent_sm = None
	starting_smartbench_screen = None
	warranty_sm = None
	reboot_to_apply_settings_screen = None
	safety_screen = None

	def __init__(self, app_manager, screen_manager, machine, settings, localization, job, database, config_check, version):

		self.am = app_manager
		self.sm = screen_manager
		self.m = machine
		self.set = settings
		self.jd = job
		self.l = localization
		self.db = database
		self.cc = config_check
		self.v = version

		self.set_up_sequence()
		self.start_sequence()

	## SCREEN SEQUENCE

	def set_up_sequence(self):

		if self.cc:

			if self.welcome_user():
				self.prep_welcome_app()

			if self.show_release_notes():
				self.prep_release_notes_screen()

			if self.show_user_data_consent():
				self.prep_data_consent_app()

			if self.show_warranty_app():
				self.prep_warranty_app()

		if self.reboot_in_sequence:		
			self.prep_reboot_to_apply_settings_screen()

		else:
			self.prep_starting_smartbench_screen()
			self.prep_safety_screen()

	## BASIC SEQUENCE NAVIGATION FUNCTIONS

	def start_sequence(self):

		self.seq_step = 0
		self.sm.current = self.screen_sequence[self.seq_step]

	def next_in_sequence(self):

		self.seq_step +=1
		self.sm.current = self.screen_sequence[self.seq_step]

	def prev_in_sequence(self):

		if self.seq_step > 0:
			self.seq_step -=1
			self.sm.current = self.screen_sequence[self.seq_step]

	def add_screen_to_sequence(self, screen_name):
		if screen_name not in self.screen_sequence:
			self.screen_sequence.append(screen_name)

	## FUNCTIONS TO CHECK WHICH SCREENS TO SHOW

	def welcome_user(self):
		flag = (os.popen('grep "show_user_welcome_app" config.txt').read())

		if ('True' in flag): 
			self.reboot_in_sequence = True
			return True
		else: return False

	def show_release_notes(self):
		pc_alert = (os.popen('grep "power_cycle_alert=True" config.txt').read())
		if "True" in pc_alert: return True
		else: return False

	def show_user_data_consent(self):
		data_consent = (os.popen('grep "user_has_seen_privacy_notice" config.txt').read())
		if ('False' in data_consent) or (not data_consent): return True
		else: return False

	def show_warranty_app(self):
		if os.path.isfile("/home/pi/smartbench_activation_code.txt"): return True
		else: return False


	## FUNCTIONS TO PREP APPS AND SCREENS

	def prep_welcome_app(self):
		if not self.welcome_sm:
			self.welcome_sm = screen_manager_welcome_to_smartbench.ScreenManagerWelcomeToSmartBench(self, self.sm, self.l)

	def prep_release_notes_screen(self):
		if not self.release_notes_screen:
			self.release_notes_screen = screen_release_notes.ReleaseNotesScreen(name = 'release_notes', start_sequence = self, screen_manager = self.sm, localization = self.l, version = self.v)
			self.sm.add_widget(self.release_notes_screen)

		if 'release_notes' not in self.screen_sequence:
			self.screen_sequence.append('release_notes')

	def prep_data_consent_app(self):
		if not self.data_consent_sm: 
			self.data_consent_sm = screen_manager_data_consent.ScreenManagerDataConsent(self, self.sm, self.l)

	def prep_warranty_app(self):
		if not self.warranty_sm:
			self.warranty_sm = screen_manager_warranty.ScreenManagerWarranty(self, self.sm, self.m, self.l)

	def prep_reboot_to_apply_settings_screen(self):
		if not self.reboot_to_apply_settings_screen:    		
			self.reboot_to_apply_settings_screen = screen_reboot_to_apply_settings.ApplySettingsScreen(name = 'reboot_apply_settings', start_sequence = self, screen_manager = self.sm, machine = self.m, localization = self.l)
			self.sm.add_widget(self.reboot_to_apply_settings_screen)

		if 'reboot_apply_settings' not in self.screen_sequence:
			self.screen_sequence.append('reboot_apply_settings')

	def prep_starting_smartbench_screen(self):
		if not self.starting_smartbench_screen:
			self.starting_smartbench_screen = screen_starting_smartbench.StartingSmartBenchScreen(name = 'starting_smartbench', start_sequence = self, screen_manager = self.sm, machine =self.m, settings = self.set, database = self.db, localization = self.l)
			self.sm.add_widget(self.starting_smartbench_screen)

		if 'starting_smartbench' not in self.screen_sequence:
			self.screen_sequence.append('starting_smartbench')

	def prep_safety_screen(self):
		if not self.safety_screen:    		
			self.safety_screen = screen_safety_warning.SafetyScreen(name = 'safety', start_sequence = self, screen_manager = self.sm, machine = self.m, localization = self.l)
			self.sm.add_widget(self.safety_screen)

		if 'safety' not in self.screen_sequence:
			self.screen_sequence.append('safety')


	## END OF SEQUENCE FUNCTIONS

	def exit_sequence(self, user_has_confirmed):

		if self.sm.current != 'alarmScreen' and self.sm.current != 'errorScreen' and self.sm.current != 'door':
			if user_has_confirmed:

				[self.destroy_screen(i) for i in self.screen_sequence]
				self.__del__()


	def update_check_config_flag(self):

		# if self.cc:
			# os.system('sudo sed -i "s/check_config=True/check_config=False/" config.txt')

		os.popen('sudo sed -i "s/check_config=True/check_config=False/" config.txt')


	def destroy_screen(self, screen_name):

		if self.sm.has_screen(screen_name):

			try:
				self.sm.remove_widget(self.sm.get_screen(screen_name))
				print (screen_name + ' deleted')

			except: pass


	def __del__(self):
		print 'End of startup sequence'



