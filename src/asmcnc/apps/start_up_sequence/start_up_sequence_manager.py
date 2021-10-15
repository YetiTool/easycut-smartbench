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

	screen_sequence = []
	seq_step = 0

	welcome_sm = None
	release_notes_screen = None
	data_consent_sm = None
	starting_smartbench_screen = None
	warranty_sm = None
	reboot_to_apply_settings_screen = None
	safety_screen = None

	def __init__(self, screen_manager, machine, settings, localization, job, database, config_check, version):

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

	def start_sequence(self):

		print(self.screen_sequence)

		self.seq_step = 0
		self.sm.current = self.screen_sequence[self.seq_step]

	def next_in_sequence(self):

		self.seq_step +=1

		print(self.screen_sequence[self.seq_step])

		self.sm.current = self.screen_sequence[self.seq_step]

	def prev_in_sequence(self):

		self.seq_step -=1
		self.sm.current = self.screen_sequence[self.seq_step]

	def set_up_sequence(self):

		self.prep_welcome_app()

		# self.prep_release_notes_screen()

		self.prep_data_consent_app()

		# self.prep_warranty_app()

		# self.prep_reboot_to_apply_settings_screen()

		self.prep_starting_smartbench_screen()
		self.prep_safety_screen()


	def add_screen_to_sequence(self, screen_name):
		if screen_name not in self.screen_sequence:
			self.screen_sequence.append(screen_name)



        # if self.m.trigger_setup and os.path.isfile("/home/pi/smartbench_activation_code.txt"):
        #     self.start_in_warranty_mode = True

        # else:
        #     self.start_in_warranty_mode = False

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
			self.welcome_sm = screen_manager_welcome_to_smartbench.ScreenManagerWelcomeToSmartBench(self, self.sm, self.l)


	def prep_release_notes_screen(self):
		if not self.release_notes_screen:
			self.release_notes_screen = screen_release_notes.ReleaseNotesScreen(name = 'release_notes', screen_manager = self.sm, localization = self.l, version = self.v)
			self.sm.add_widget(self.release_notes_screen)

	def prep_data_consent_app(self):
		if not self.data_consent_sm: 
			self.data_consent_sm = screen_manager_data_consent.ScreenManagerDataConsent(self, self.sm, self.l)

	def prep_warranty_app(self):
		if not self.warranty_sm:
			self.warranty_sm = screen_manager_warranty.ScreenManagerWarranty(self.sm, self.m, self.l)

	def prep_reboot_to_apply_settings_screen(self):
		if not self.reboot_to_apply_settings_screen:    		
			self.reboot_to_apply_settings_screen = screen_reboot_to_apply_settings.ApplySettingsScreen(name = 'reboot_apply_settings', screen_manager = self.sm, machine = self.m, localization = self.l)
			self.sm.add_widget(self.reboot_to_apply_settings_screen)

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

	## FUNCTIONS TO OPEN APPS AND SCREENS

	def open_welcome_app(self):
		self.current_app = 'welcome'
		self.welcome_sm.open_welcome_app()

	def open_release_notes(self):
		self.sm.current = 'release_notes'

	def open_data_consent_app(self):
		self.current_app = 'data_consent' # might change these to start up sequence
		self.data_consent_sm.open_data_consent('warranty_5', 'cnc_academy') # will probably make this CNC Academy screen instead

	def open_warranty_app(self):
		# all checks now happen in welcome screen
		self.current_app = 'warranty'
		self.warranty_sm.open_warranty_app()

	def open_starting_smartbench(self):
		self.sm.current = 'starting_smartbench'

	def open_reboot_apply_settings(self):
		self.sm.current = 'reboot_apply_settings'

	def open_safety(self):
		self.sm.current = 'safety'