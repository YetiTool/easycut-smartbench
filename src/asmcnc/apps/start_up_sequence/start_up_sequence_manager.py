import os

from asmcnc.apps.start_up_sequence import \
screen_reboot_to_apply_settings, \
screen_release_notes, \
screen_starting_smartbench, \
screen_safety_warning

from asmcnc.apps.start_up_sequence.warranty_app import screen_manager_warranty
from asmcnc.apps.start_up_sequence.data_consent_app import screen_manager_data_consent
from asmcnc.apps.start_up_sequence.welcome_to_smartbench_app import screen_manager_welcome_to_smartbench


class StartUpSequence(object):

	welcome_sm = None
	release_notes_screen = None

	def __init__(self, screen_manager, machine, settings, localization, job, database, config_check, version):

		self.sm = screen_manager
		self.m = machine
		self.set = settings
		self.jd = job
		self.l = localization
		self.db = database
		self.cc = config_check
		self.v = version

		self.prep_welcome_app()
		self.start_welcome_app()

		# self.prep_release_notes_screen()
		# self.open_release_notes()

	def check_and_launch_update_screen():

		# Check whether machine needs to be power cycled (currently only after a software update)
		pc_alert = (os.popen('grep "power_cycle_alert=True" /home/pi/easycut-smartbench/src/config.txt').read())
		if pc_alert.startswith('power_cycle_alert=True'):
			os.system('sudo sed -i "s/power_cycle_alert=True/power_cycle_alert=False/" /home/pi/easycut-smartbench/src/config.txt') 


	def update_check_config_flag():

		os.system('sudo sed -i "s/check_config=True/check_config=False/" /home/pi/easycut-smartbench/src/config.txt')


	## FUNCTIONS TO PREP APPS AND SCREENS


	def prep_welcome_app(self):
		if not self.welcome_sm:
			self.welcome_sm = screen_manager_welcome_to_smartbench.ScreenManagerWelcomeToSmartBench(self.sm, self.l)


	def prep_release_notes_screen(self):
		if not self.release_notes_screen:
			self.release_notes_screen = screen_release_notes.ReleaseNotesScreen(name = 'release_notes', screen_manager = self.sm, localization = self.l, version = self.v)
			self.sm.add_widget(self.release_notes_screen)

	def prep_data_consent_app(self):
		if not self.data_consent_sm: 
			self.data_consent_sm = screen_manager_data_consent.ScreenManagerDataConsent(self.sm, self.l)

	def prep_starting_smartbench_screen(self):
		if not self.starting_smartbench_screen:
			self.starting_smartbench_screen = screen_starting_smartbench.StartingSmartBenchScreen(name = 'starting_smartbench', screen_manager = sm, machine =m, settings = sett, database = db, app_manager = am, localization = l)
			self.sm.add_widget(self.starting_smartbench_screen)

	def prep_warranty_app(self):
		if not warranty_sm:
			self.warranty_sm = screen_manager_warranty.ScreenManagerWarranty(self.sm, self.m, self.l)

	def prep_reboot_to_apply_settings_screen(self):
		if not self.reboot_to_apply_settings_screen:    		
			self.reboot_to_apply_settings_screen = screen_reboot_to_apply_settings.ApplySettingsScreen(name = 'reboot_apply_settings', screen_manager = sm, machine =m, localization = l)
			self.sm.add_widget(self.reboot_to_apply_settings_screen)

	def prep_safety_screen(self):
		if not self.safety_screen:    		
			self.safety_screen = screen_safety_warning.SafetyScreen(name = 'safety', screen_manager = sm, machine =m, localization = l)
			self.sm.add_widget(self.safety_screen)

	## FUNCTIONS TO OPEN APPS AND SCREENS

	def start_welcome_app(self):
		self.current_app = 'welcome'
		self.welcome_sm.open_welcome_app()

	def open_release_notes(self):
		self.sm.current = 'release_notes'

	def start_data_consent_app(self):
		self.current_app = 'data_consent' # might change these to start up sequence
		self.data_consent_sm.open_data_consent('warranty_5', 'cnc_academy') # will probably make this CNC Academy screen instead

	def open_starting_smartbench(self):
		self.sm.current = 'starting_smartbench'

	def start_warranty_app(self):
		# all checks now happen in welcome screen
		self.current_app = 'warranty'
		self.warranty_sm.open_language_select_screen()

	def open_reboot_apply_settings(self):
		self.sm.current = 'reboot_apply_settings'

	def open_safety(self):
		self.sm.current = 'safety'