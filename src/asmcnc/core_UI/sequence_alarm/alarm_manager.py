from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen
import sys, os
from asmcnc.skavaUI import popup_info

from asmcnc.core_UI.sequence_alarm.screens import screen_alarm_1, \
screen_alarm_2, screen_alarm_3, \
screen_alarm_4, screen_alarm_5


# this class is set up in serial comms, so that alarm screens are available at any time
# not going to use it as a "screen manager" as alarm screens want to be instantly available at all times
# instead just use it to access messages/alarm info across screens

ALARM_CODES = {

    "ALARM:1" : "Unexpected limit reached. The machine's position was likely lost. Re-homing is highly recommended.",
    "ALARM:2" : "The requested motion target exceeds the machine's travel.",
    "ALARM:3" : "Machine was reset while in motion and cannot guarantee position. Lost steps are likely. Re-homing is recommended.",
    "ALARM:4" : "Probe fail. Probe was not in the expected state before starting probe cycle.",
    "ALARM:5" : "Probe fail. Probe did not contact the workpiece within the programmed travel.",
    "ALARM:6" : "Homing fail. Reset during active homing cycle.",
    "ALARM:7" : "Homing fail. Safety switch was activated during the homing cycle.",
    "ALARM:8" : "Homing fail. Cycle failed to clear limit switch when pulling off.",
    "ALARM:9" : "Homing fail. Could not find limit switch within search distance.",

}

class AlarmSequenceManager(object):

	# get these for each alarm call, from sm and serial comms respectively
	return_to_screen = ''
	alarm_code = ''
	alarm_description = ''

	# retrieve these for the alarm report
	trigger_description = ''
	status_cache = ''

    def __init__(self, screen_manager, settings_manager, machine):

        self.sm = screen_manager
        self.set = settings_manager
        self.m = machine

        self.set_up_alarm_screens()


	def set_up_alarm_screens(self):

		alarm_1_screen = screen_alarm_1.AlarmScreen3(name='alarm_1', alarm_manager = self)
		alarm_2_screen = screen_alarm_2.AlarmScreen3(name='alarm_2', alarm_manager = self)
		alarm_3_screen = screen_alarm_3.AlarmScreen3(name='alarm_3', alarm_manager = self)
		alarm_4_screen = screen_alarm_4.AlarmScreen3(name='alarm_4', alarm_manager = self)
		alarm_5_screen = screen_alarm_5.AlarmScreen3(name='alarm_5', alarm_manager = self)

		sm.add_widget(alarm_1_screen)
		sm.add_widget(alarm_2_screen)
		sm.add_widget(alarm_3_screen)
		sm.add_widget(alarm_4_screen)
		sm.add_widget(alarm_5_screen)


	def alert_user(message):

		if not self.alarm.is_alarm_sequence_already_running():
			if is_error_screen_already_up():
				self.return_to_screen = self.sm.get_screen('errorScreen').return_to_screen
			else:
				self.return_to_screen = self.sm.current

			self.alarm_code = message
			self.sm.current = 'alarm_1'


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
		pass


    def get_version_data(self):
    	self.sw_version = self.set.sw_version
        self.fw_version = str((str(self.m.s.fw_version)).split('; HW')[0])
        self.hw_version = self.m.s.hw_version
        try: self.machine_serial_number_label.text = 'YS6' + str(self.m.serial_number())[0:4]
        except: self.machine_serial_number_label.text = '-'


	def get_status_info(self):
		pass

