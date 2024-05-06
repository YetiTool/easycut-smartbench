from asmcnc.comms.logging_system.logging_system import Logger
from kivy.core.window import Window

"""
Created on nov 2020
@author: Ollie
Text input # on_enter: root.sucessful_activation
"""
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.textinput import TextInput
from asmcnc.skavaUI import widget_status_bar
from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
import os
from asmcnc.core_UI import scaling_utils as utils

Builder.load_string(
    """

<WarrantyScreen3>:

	title_label : title_label
	enter_your_activation_code_label : enter_your_activation_code_label
	activation_code : activation_code
	error_message_top : error_message_top
	error_message_bottom : error_message_bottom
	next_button : next_button

	on_touch_down: root.on_touch()

	BoxLayout: 
		size_hint: (None,None)
		width: dp(1.0*app.width)
		height: dp(1.0*app.height)
		orientation: 'vertical'

		canvas:
			Color:
				rgba: hex('##e5e5e5')
			Rectangle:
				size: self.size
				pos: self.pos


		BoxLayout:
			padding: 0
			spacing: 0
			orientation: "vertical"

			# HEADER
			BoxLayout:
				padding: 0
				spacing: 0
				canvas:
					Color:
						rgba: hex('#1976d2ff')
					Rectangle:
						pos: self.pos
						size: self.size
				Label:
					id: title_label
					size_hint: (None,None)
					height: dp(0.125*app.height)
					width: dp(1.0*app.width)
					text: "SmartBench Warranty Registration"
					color: hex('#f9f9f9ff')
					# color: hex('#333333ff') #grey
					font_size: dp(0.0375*app.width)
					halign: "center"
					valign: "bottom"
					markup: True

			# BODY
			BoxLayout:
				size_hint: (None,None)
				width: dp(1.0*app.width)
				height: dp(0.620833333333*app.height)
				orientation: 'vertical'
				
				Label:
					id: enter_your_activation_code_label
					font_size: str(0.0375*app.width) + 'sp'
					# text: "[color=333333ff]Enter your activation code:[/color]"
					text_size: self.size
					valign: 'bottom'
					halign: 'center'
					markup: 'true'
					color: hex('#333333ff')

				BoxLayout:
					orientation: 'vertical'
					width: dp(1.0*app.width)
					height: dp(0.15625*app.height)
					padding:[dp(0.25)*app.width, 0]
					size_hint: (None,None)
					TextInput: 
						id: activation_code
						valign: 'middle'
						halign: 'center'
						height: dp(0.104166666667*app.height)
						width: dp(0.5*app.width) 
						size_hint: (None,None)
						text_size: self.size
						font_size: str(0.0375*app.width) + 'sp'
						markup: True
						multiline: False
						text: ''
						input_filter: 'int'
						color: hex('#333333ff')
				BoxLayout:
					orientation: 'vertical'
					width: dp(1.0*app.width)
					height: dp(0.260416666667*app.height)
					padding:[dp(0.025)*app.width, dp(0.0416666666667)*app.height]
					size_hint: (None,None)
					Label:
						id: error_message_top
						font_size: str(0.025*app.width) + 'sp'
						text: "Please check your activation code."
						text_size: self.size
						valign: 'bottom'
						halign: 'center'
						markup: 'true'
						color: hex('#e64a19ff')
						opacity: 0
					Label:
						id: error_message_bottom
						font_size: str(0.025*app.width) + 'sp'
						text: "Stuck on this screen? Contact us at https://www.yetitool.com/support"
						text_size: self.size
						valign: 'bottom'
						halign: 'center'
						markup: 'true'
						color: hex('#e64a19ff')
						opacity: 0

			# FOOTER
			BoxLayout: 
				padding:[dp(0.0125)*app.width, 0, dp(0.0125)*app.width, dp(0.0208333333333)*app.height]
				size_hint: (None, None)
				height: dp(0.254166666667*app.height)
				width: dp(1.0*app.width)
				orientation: 'horizontal'
				BoxLayout: 
					size_hint: (None, None)
					height: dp(0.254166666667*app.height)
					width: dp(0.305625*app.width)
					padding:[0, 0, dp(0.230625)*app.width, 0]
					Button:
					    font_size: str(0.01875 * app.width) + 'sp'
						size_hint: (None,None)
						height: dp(0.108333333333*app.height)
						width: dp(0.075*app.width)
						background_color: color_provider.get_rgba("invisible")
						center: self.parent.center
						pos: self.parent.pos
						on_press: root.prev_screen()
						BoxLayout:
							padding: 0
							size: self.parent.size
							pos: self.parent.pos
							Image:
								source: "./asmcnc/apps/systemTools_app/img/back_to_menu.png"
								center_x: self.parent.center_x
								y: self.parent.y
								size: self.parent.width, self.parent.height
								allow_stretch: True

				BoxLayout: 
					size_hint: (None, None)
					height: dp(0.254166666667*app.height)
					width: dp(0.36375*app.width)
					padding:[0, 0, 0, dp(0.0666666666667)*app.height]
					Button:
						id: next_button
						background_normal: "./asmcnc/skavaUI/img/next.png"
						background_down: "./asmcnc/skavaUI/img/next.png"
						border: [dp(14.5)]*4
						size_hint: (None,None)
						width: dp(0.36375*app.width)
						height: dp(0.164583333333*app.height)
						on_press: root.next_screen(False)
						text: 'Next...'
						font_size: str(0.0375*app.width) + 'sp'
						color: hex('#f9f9f9ff')
						markup: True
						center: self.parent.center
						pos: self.parent.pos
				BoxLayout: 
					size_hint: (None, None)
					height: dp(0.254166666667*app.height)
					width: dp(0.305625*app.width)
					padding:[dp(0.241875)*app.width, 0, 0, 0]


"""
)


class WarrantyScreen3(Screen):
    activationcode = ObjectProperty()
    activation_code_filepath = "/home/pi/smartbench_activation_code.txt"
    activation_code_from_file = 0
    check_activation_event = None
    default_font_size = str(utils.get_scaled_width(20)) + 'sp'

    def __init__(self, **kwargs):
        super(WarrantyScreen3, self).__init__(**kwargs)
        self.start_seq = kwargs["start_sequence"]
        self.m = kwargs["machine"]
        self.l = kwargs["localization"]
        self.kb = kwargs["keyboard"]
        self.update_strings()
        self.text_inputs = [self.activation_code]

    def on_pre_enter(self):
        self.read_in_activation_code()

    def on_enter(self):
        self.check_activation_event = Clock.schedule_interval(
            lambda dt: self.next_screen(), 2
        )
        self.kb.setup_text_inputs(self.text_inputs)

    def on_touch(self):
        for text_input in self.text_inputs:
            text_input.focus = False

    def read_in_activation_code(self):
        try:
            file = open(self.activation_code_filepath, "r")
            self.activation_code_from_file = int(str(file.read()))
            file.close()
            if self.activation_code_from_file == "":
                self.backup_generate_activation_code()
        except:
			# self.error_message_top.opacity = 1
			# self.error_message_top.text = 'Checking activation code...'
            self.backup_generate_activation_code()

    def backup_generate_activation_code(self):
        self.activation_code_from_file = self.generate_activation_code(
            self.start_seq.sm.get_screen("warranty_2").serial_number_label.text
        )
        self.error_message_bottom.opacity = 1

    def check_activation_code(self):
        if self.activation_code.text != "":
            if int(self.activation_code.text) == self.activation_code_from_file:
                if os.path.isfile(self.activation_code_filepath):
                    os.remove(self.activation_code_filepath)
                return True
            else:
                return False
        else:
            return False

    def next_screen(self, auto=True):
        if self.check_activation_code():
            if self.check_activation_event != None:
                Clock.unschedule(self.check_activation_event)
            self.activation_code.focus = False
            try:
                self.start_seq.next_in_sequence()
            except:
                if self.check_activation_event != None:
                    Clock.unschedule(self.check_activation_event)
        elif auto == True:
            pass
        else:
            self.error_message_top.opacity = 1
            self.error_message_bottom.opacity = 1

    def prev_screen(self):
        self.start_seq.prev_in_sequence()

    def on_leave(self):
        if self.check_activation_event != None:
            Clock.unschedule(self.check_activation_event)

    def generate_activation_code(self, serial_number):
        ActiveTempNoOnly = int("".join(filter(str.isdigit, serial_number)))
        Logger.info(str(ActiveTempNoOnly) + "\n")
        ActiveTempStart = str(ActiveTempNoOnly * 76289103623 + 20)
        Logger.info(ActiveTempStart + "\n")
        ActiveTempStartReduce = ActiveTempStart[0:15]
        Logger.info(ActiveTempStartReduce + "\n")
        Activation_Code_1 = int(ActiveTempStartReduce[0]) * 171350
        Activation_Code_2 = int(ActiveTempStartReduce[3]) * 152740
        Activation_Code_3 = int(ActiveTempStartReduce[5]) * 213431
        Activation_Code_4 = int(ActiveTempStartReduce[7]) * 548340
        Activation_Code_5 = int(ActiveTempStartReduce[11]) * 115270
        Activation_Code_6 = int(ActiveTempStartReduce[2]) * 4670334
        Activation_Code_7 = int(ActiveTempStartReduce[7]) * 789190
        Activation_Code_8 = int(ActiveTempStartReduce[6]) * 237358903
        Activation_Code_9 = int(ActiveTempStartReduce[6]) * 937350
        Activation_Code_10 = int(ActiveTempStartReduce[6]) * 105430
        Activation_Code_11 = int(ActiveTempStartReduce[6]) * 637820
        Activation_Code_12 = int(ActiveTempStartReduce[6]) * 67253489
        Activation_Code_13 = int(ActiveTempStartReduce[6]) * 53262890
        Activation_Code_14 = int(ActiveTempStartReduce[6]) * 89201233
        Final_Activation_Code = (
            Activation_Code_1
            + Activation_Code_2
            + Activation_Code_3
            + Activation_Code_4
            + Activation_Code_5
            + Activation_Code_6
            + Activation_Code_7
            + Activation_Code_8
            + Activation_Code_9
            + Activation_Code_10
            + Activation_Code_11
            + Activation_Code_12
            + Activation_Code_13
            + Activation_Code_14
        )
        Logger.info(str(Final_Activation_Code) + "\n")
        return Final_Activation_Code

    def update_strings(self):
        self.title_label.text = self.l.get_str("SmartBench Warranty Registration")
        self.enter_your_activation_code_label.text = self.l.get_bold(
            "Enter your activation code:"
        )
        self.error_message_top.text = self.l.get_str(
            "Please check your activation code."
        )
        self.error_message_bottom.text = self.l.get_str(
            "Stuck on this screen? Contact us at https://www.yetitool.com/support"
        )
        self.next_button.text = self.l.get_str("Next") + "..."
        self.update_font_size(self.error_message_bottom)

    def update_font_size(self, value):
        text_length = self.l.get_text_length(value.text)
        if text_length < 85:
            value.font_size = self.default_font_size
        elif text_length < 100:
            value.font_size = str(0.0225 * Window.width) + "sp"
        else:
            value.font_size = str(0.02 * Window.width) + "sp"
