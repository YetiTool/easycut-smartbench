"""
Created on nov 2020
@author: Ollie
"""
from asmcnc.comms.logging_system.logging_system import Logger
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
import sys, os
from asmcnc.skavaUI import widget_status_bar

Builder.load_string(
    """

<WarrantyScreen2>:

	title_label : title_label
	your_serial_number_label : your_serial_number_label
	serial_number_label : serial_number_label
	next_button : next_button
	prev_screen_button:prev_screen_button

	BoxLayout: 
		size_hint: (None,None)
		width: dp(1.0*app.width)
		height: dp(1.0*app.height)
		orientation: 'vertical'

		canvas:
			Color:
				rgba: color_provider.get_rgba("light_grey")
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
						rgba: color_provider.get_rgba("blue")
					Rectangle:
						pos: self.pos
						size: self.size
				Label:
					id: title_label
					size_hint: (None,None)
					height: dp(0.125*app.height)
					width: dp(1.0*app.width)
					text: "SmartBench Warranty Registration"
					color: color_provider.get_rgba("near_white")
					# color: color_provider.get_rgba("dark_grey") #grey
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
					id: your_serial_number_label
					font_size: str(0.0375*app.width) + 'sp'
					# text: "[color=333333ff]Your serial number is[/color]"
					text_size: self.size
					valign: 'bottom'
					halign: 'center'
					markup: 'true'
					color: color_provider.get_rgba("dark_grey")

				BoxLayout:
					orientation: 'vertical'
					width: dp(1.0*app.width)
					height: dp(0.416666666667*app.height)
					padding:[dp(0.025)*app.width, dp(0.0416666666667)*app.height]
					size_hint: (None,None)
					Label:
						id: serial_number_label
						size_hint_y: 1
						font_size: str(0.0375*app.width) + 'sp'
						text_size: self.size
						valign: 'middle'
						halign: 'center'
						markup: 'true'
						color: color_provider.get_rgba("dark_grey")

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
					    id: prev_screen_button
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
						on_press: root.next_screen()
						text: 'Next...'
						font_size: str(0.0375*app.width) + 'sp'
						color: color_provider.get_rgba("near_white")
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


class WarrantyScreen2(Screen):
    def __init__(self, **kwargs):
        super(WarrantyScreen2, self).__init__(**kwargs)
        self.start_seq = kwargs["start_sequence"]
        self.m = kwargs["machine"]
        self.l = kwargs["localization"]
        self.serial_number_label.text = self.get_serial_number()
        self.update_strings()

    def get_serial_number(self):
        serial_number_filepath = "/home/pi/smartbench_serial_number.txt"
        serial_number_from_file = ""
        try:
            file = open(serial_number_filepath, "r")
            serial_number_from_file = str(file.read())
            file.close()
        except:
            Logger.info("Could not get serial number! Please contact YetiTool support!")
        return str(serial_number_from_file)

    def next_screen(self):
        self.start_seq.next_in_sequence()

    def prev_screen(self):
        self.start_seq.prev_in_sequence()

    def update_strings(self):
        self.title_label.text = self.l.get_str("SmartBench Warranty Registration")
        self.your_serial_number_label.text = self.l.get_bold("Your serial number is")
        self.next_button.text = self.l.get_str("Next") + "..."
