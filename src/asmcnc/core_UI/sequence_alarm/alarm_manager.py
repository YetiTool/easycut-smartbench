from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen
import sys, os
import datetime

from asmcnc.core_UI.sequence_alarm.screens import screen_alarm_1, \
screen_alarm_2, screen_alarm_3, \
screen_alarm_4, screen_alarm_5
from asmcnc.comms import usb_storage

# this class is set up in serial comms, so that alarm screens are available at any time
# not going to use it as a "screen manager" as alarm screens want to be instantly available at all times
# instead just use it to access messages/alarm info across screens

ALARM_CODES_DICT = {

	"ALARM:1" : "An end-of-axis limit switch was triggered during a move.",
	"ALARM:2" : "The requested motion target exceeds the machine's travel.",
	"ALARM:3" : "Machine was reset while in motion and cannot guarantee position.",
	"ALARM:4" : "Probe fail. Probe was not in the expected state before starting probe cycle.",
	"ALARM:5" : "Probe fail. Tool did not contact the probe within the search distance.",
	"ALARM:6" : "Homing fail: SmartBench was reset during active homing cycle.",
	"ALARM:7" : "Homing fail: the stop bar was triggered during the homing cycle.",
	"ALARM:8" : "Homing fail: during the homing cycle, an axis failed to clear the limit switch when pulling off.",
	"ALARM:9" : "Homing fail: could not find the limit switch within search distance.",
	"ALARM:10": "Homing fail: on dual axis machines, could not find the second limit switch for self-squaring."
}

class AlarmSequenceManager(object):

	# get these for each alarm call, from sm and serial comms respectively
	return_to_screen = ''
	alarm_code = ''
	alarm_description = ''

	# is full support sequence needed?
	support_sequence = False

	# retrieve these for the alarm report
	trigger_description = ''
	status_cache = ''

	report_string= 'Loading report...'

	report_setup_event = None

	def __init__(self, screen_manager, settings_manager, machine):

		self.sm = screen_manager
		self.set = settings_manager
		self.m = machine
		self.usb_stick = usb_storage.USB_storage(self.sm)

		self.set_up_alarm_screens()


	def set_up_alarm_screens(self):

		alarm_1_screen = screen_alarm_1.AlarmScreen1(name='alarm_1', alarm_manager = self)
		alarm_2_screen = screen_alarm_2.AlarmScreen2(name='alarm_2', alarm_manager = self)
		alarm_3_screen = screen_alarm_3.AlarmScreen3(name='alarm_3', alarm_manager = self)
		alarm_4_screen = screen_alarm_4.AlarmScreen4(name='alarm_4', alarm_manager = self)
		alarm_5_screen = screen_alarm_5.AlarmScreen5(name='alarm_5', alarm_manager = self)

		self.sm.add_widget(alarm_1_screen)
		self.sm.add_widget(alarm_2_screen)
		self.sm.add_widget(alarm_3_screen)
		self.sm.add_widget(alarm_4_screen)
		self.sm.add_widget(alarm_5_screen)


	def alert_user(self, message):

		if not self.is_alarm_sequence_already_running():
			if self.is_error_screen_already_up():
				self.return_to_screen = self.sm.get_screen('errorScreen').return_to_screen
			else:
				self.return_to_screen = self.sm.current

			self.alarm_code = message
			self.alarm_description = ALARM_CODES_DICT.get(message, "")
			self.sm.get_screen('alarm_1').description_label.text = self.alarm_description
			self.determine_screen_sequence()

			try: 
				self.get_first_screen()

			except:
				print("Kivy fail caught")
				Clock.schedule_once(lambda dt: self.get_first_screen(), 0.1)

			self.handle_alarm_state()

	def get_first_screen(self):
		self.sm.current = 'alarm_1'

		if ((self.alarm_code).endswith('1') or (self.alarm_code).endswith('8')):

			self.sm.get_screen('alarm_1').description_label.text = (
				self.alarm_description + \
				"\n" + \
				"Getting details..."
				)


	def determine_screen_sequence(self):
		if ((self.alarm_code).endswith('4') or (self.alarm_code).endswith('5') or (self.alarm_code).endswith('6') or (self.alarm_code).endswith('7')):
			self.support_sequence = False
		else:
			self.support_sequence = True


	def exit_sequence(self):
		
		self.m.resume_from_alarm()

		if self.return_to_screen == 'go':
			self.sm.get_screen('go').is_job_started_already = False
			self.sm.get_screen('go').temp_suppress_prompts = True
		
		if self.sm.has_screen(self.return_to_screen):
			self.sm.current = self.return_to_screen

		else: 
			self.sm.current = 'lobby'

		self.reset_variables()


	def handle_alarm_state(self):
		Clock.schedule_once(lambda dt: self.m.reset_from_alarm(), 0.8)
		self.m.set_state('Alarm')
		self.m.led_restore()
		Clock.schedule_once(lambda dt: self.update_screens(), 1)


	def is_alarm_sequence_already_running(self):

		if self.sm.current == 'alarm_1':
			return True

		if self.sm.current == 'alarm_2':
			return True

		if self.sm.current == 'alarm_3':
			return True

		if self.sm.current == 'alarm_4':
			return True

		if self.sm.current == 'alarm_5':
			return True


	def is_error_screen_already_up(self):

		if self.sm.current == 'errorScreen':
			return True


	def get_suspected_trigger(self):
		limit_code = "Unexpected limit reached: "
		limit_list = []

		if self.m.s.limit_x:
			limit_list.append('X home')

		if self.m.s.limit_X: 
			limit_list.append('X max')

		if self.m.s.limit_y: 
			limit_list.append('Y home')

		if self.m.s.limit_Y: 
			limit_list.append('Y max')

		if self.m.s.limit_z: 
			limit_list.append('Z home')

		if limit_list == []:
			limit_list.append('Unknown')

		self.trigger_description = limit_code + (', ').join(limit_list)


	def get_status_info(self):

		status_list = self.sm.get_screen('home').gcode_monitor_widget.status_report_buffer
		n = len(status_list)
		self.status_cache = ('\n').join(self.sm.get_screen('home').gcode_monitor_widget.status_report_buffer[n-2:n])


	def get_version_data(self):

		self.sw_version = self.set.sw_version
		self.fw_version = str((str(self.m.s.fw_version)).split('; HW')[0])
		self.hw_version = self.m.s.hw_version
		try: self.machine_serial_number = 'YS6' + str(self.m.serial_number())[0:4]
		except: self.machine_serial_number = '-'


	def update_screens(self):

		self.get_version_data()
		if ((self.alarm_code).endswith('1') or (self.alarm_code).endswith('8')):
			self.get_suspected_trigger()

		if self.trigger_description != '':
			self.sm.get_screen('alarm_1').description_label.text = (
					self.alarm_description + \
					"\n" +
					self.trigger_description
				)
		self.report_setup_event = Clock.schedule_once(lambda dt: self.setup_report(), 0.2)



	def reset_variables(self):

		if self.report_setup_event != None: Clock.unschedule(self.report_setup_event)

		self.return_to_screen = ""
		self.alarm_code = ""
		self.alarm_description = ""
		self.trigger_description = ""
		self.status_cache = ""
		self.report_string= 'Loading report...'
		self.sm.get_screen('alarm_3').description_label.text = self.report_string

	def download_alarm_report(self):

		self.usb_stick.enable()
		count = 0

		def get_report(count):
			if self.usb_stick.is_usb_mounted_flag == True:
				self.write_report_to_file()
				self.usb_stick.disable()

			elif count > 30:
				if self.usb_stick.is_available(): self.usb_stick.disable()

			else:
				count +=1
				Clock.schedule_once(lambda dt: get_report(count), 0.2)

		Clock.schedule_once(lambda dt: get_report(count), 0.2)


	def setup_report(self):

		self.get_status_info()

		try: 
			# If variables get reset then this will fail
			alarm_number = str((self.alarm_code.split(':'))[1])
		except:
			alarm_number = ""


		self.report_string = (

			"[b]" + "Alarm report" + "[/b]" + \
			"\n\n" + \
			"Software version:" + " " + self.sw_version + "\n" + \
			"Firmware version:" + " " + self.fw_version + "\n" + \
			"Hardware version:" + " " + self.hw_version + "\n" + \
			"Serial number:" + " " + self.machine_serial_number + \
			"\n\n" + \
			"Alarm code:" + " " + alarm_number + \
			"\n" + \
			"Alarm description: " + " " + self.alarm_description + \
			"\n" + \
			self.trigger_description + \
			"\n\n" + \
			"Status cache:" + " " + \
			"\n" + \
			self.status_cache
			)

		self.sm.get_screen('alarm_3').description_label.text = self.report_string


	def write_report_to_file(self):

		report_file_path = "/home/pi/alarm_report_" + str(datetime.date.today()) + ".txt"

		try:
			with open(report_file_path, 'w+') as file:
				file.write(self.report_string)

			os.system("sudo cp --no-preserve=mode,ownership " + report_file_path + " /media/usb/ && rm " + report_file_path)
			print("Alarm report written to file")
			return True

		except:
			print("Unable to write alarm report to file")
			return False
