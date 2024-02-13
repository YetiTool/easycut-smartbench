"""
Created on nov 2020
@author: Ollie
"""
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

	BoxLayout: 
		size_hint: (None,None)
		width: dp(app.get_scaled_width(800))
		height: dp(app.get_scaled_height(480))
		orientation: 'vertical'

		canvas:
			Color:
				rgba: hex('##e5e5e5')
			Rectangle:
				size: self.size
				pos: self.pos

		BoxLayout:
			padding:dp(0)
			spacing: 0
			orientation: "vertical"

			# HEADER
			BoxLayout:
				padding:dp(0)
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
					height: dp(app.get_scaled_height(60))
					width: dp(app.get_scaled_width(800))
					text: "SmartBench Warranty Registration"
					color: hex('#f9f9f9ff')
					# color: hex('#333333ff') #grey
					font_size: dp(app.get_scaled_width(30))
					halign: "center"
					valign: "bottom"
					markup: True
				   
			# BODY
			BoxLayout:
				size_hint: (None,None)
				width: dp(app.get_scaled_width(800))
				height: dp(app.get_scaled_height(298))
				orientation: 'vertical'
				
				Label:
					id: your_serial_number_label
					font_size: str(get_scaled_width(30)) + 'sp'
					# text: "[color=333333ff]Your serial number is[/color]"
					text_size: self.size
					valign: 'bottom'
					halign: 'center'
					markup: 'true'
					color: hex('#333333ff')

				BoxLayout:
					orientation: 'vertical'
					width: dp(app.get_scaled_width(800))
					height: dp(app.get_scaled_height(200))
					padding:(dp(app.get_scaled_width(20)),dp(app.get_scaled_height(20)))
					size_hint: (None,None)
					Label:
						id: serial_number_label
						size_hint_y: 1
						font_size: str(get_scaled_width(30)) + 'sp'
						text_size: self.size
						valign: 'middle'
						halign: 'center'
						markup: 'true'
						color: hex('#333333ff')

			# FOOTER
			BoxLayout: 
				padding:(dp(app.get_scaled_width(10)),dp(0),dp(app.get_scaled_width(10)),dp(app.get_scaled_height(10)))
				size_hint: (None, None)
				height: dp(app.get_scaled_height(122))
				width: dp(app.get_scaled_width(800))
				orientation: 'horizontal'
				BoxLayout: 
					size_hint: (None, None)
					height: dp(app.get_scaled_height(122))
					width: dp(app.get_scaled_width(244.5))
					padding:(dp(0),dp(0),dp(app.get_scaled_width(184.5)),dp(0))
					Button:
					    font_size: str(get_scaled_width(15)) + 'sp'
						size_hint: (None,None)
						height: dp(app.get_scaled_height(52))
						width: dp(app.get_scaled_width(60))
						background_color: hex('#F4433600')
						center: self.parent.center
						pos: self.parent.pos
						on_press: root.prev_screen()
						BoxLayout:
							padding:dp(0)
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
					height: dp(app.get_scaled_height(122))
					width: dp(app.get_scaled_width(291))
					padding:(dp(0),dp(0),dp(0),dp(app.get_scaled_height(32)))
					Button:
						id: next_button
						background_normal: "./asmcnc/skavaUI/img/next.png"
						background_down: "./asmcnc/skavaUI/img/next.png"
						border: [dp(14.5)]*4
						size_hint: (None,None)
						width: dp(app.get_scaled_width(291))
						height: dp(app.get_scaled_height(79))
						on_press: root.next_screen()
						text: 'Next...'
						font_size: str(get_scaled_width(30)) + 'sp'
						color: hex('#f9f9f9ff')
						markup: True
						center: self.parent.center
						pos: self.parent.pos
				BoxLayout: 
					size_hint: (None, None)
					height: dp(app.get_scaled_height(122))
					width: dp(app.get_scaled_width(244.5))
					padding:(dp(app.get_scaled_width(193.5)),dp(0),dp(0),dp(0))
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
            print("Could not get serial number! Please contact YetiTool support!")
        return str(serial_number_from_file)

    def next_screen(self):
        self.start_seq.next_in_sequence()

    def prev_screen(self):
        self.start_seq.prev_in_sequence()

    def update_strings(self):
        self.title_label.text = self.l.get_str("SmartBench Warranty Registration")
        self.your_serial_number_label.text = self.l.get_bold("Your serial number is")
        self.next_button.text = self.l.get_str("Next") + "..."
