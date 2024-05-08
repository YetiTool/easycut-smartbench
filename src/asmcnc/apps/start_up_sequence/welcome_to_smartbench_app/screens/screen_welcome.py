"""
Created on nov 2020
@author: Letty
"""
from kivy.lang import Builder
from kivy.factory import Factory
from kivy.uix.screenmanager import ScreenManager, Screen
import sys, os
from kivy.clock import Clock

Builder.load_string(
    """


<WelcomeTextScreen>:

	header_label : header_label
	thankyou_label : thankyou_label
	next_steps_label : next_steps_label
	minutes_label : minutes_label

	next_button : next_button

	BoxLayout:
		height: app.get_scaled_height(800.0)
		width: app.get_scaled_width(480.0)
		canvas.before:
			Color: 
				rgba: hex('#e5e5e5ff')
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
					id: header_label
					size_hint: (None,None)
					height: app.get_scaled_height(60.0)
					width: app.get_scaled_width(800.0)
					color: hex('#f9f9f9ff')
					# color: hex('#333333ff') #grey
					font_size: app.get_scaled_width(30.0)
					halign: "center"
					valign: "bottom"
					markup: True
				   
			# BODY
			BoxLayout:
				size_hint: (None,None)
				width: app.get_scaled_width(800.0)
				height: app.get_scaled_height(298.0)
				padding: app.get_scaled_tuple([30.0, 10.0])
				spacing: app.get_scaled_width(10.0)
				orientation: 'vertical'

				Label:
					id: thankyou_label
					size_hint_y: 0.25
					font_size: app.get_scaled_sp('20.0sp')
					text_size: self.size
					valign: 'bottom'
					halign: 'center'
					markup: 'true'
					color: hex('#333333ff')

				Label:
					id: next_steps_label
					size_hint_y: 0.5
					font_size: app.get_scaled_sp('20.0sp')
					text_size: self.size
					valign: 'middle'
					halign: 'center'
					markup: 'true'
					multiline: True
					color: hex('#333333ff')
				
				Label:
					id: minutes_label
					size_hint_y: 0.25
					font_size: app.get_scaled_sp('20.0sp')
					text_size: self.size
					valign: 'top'
					halign: 'center'
					markup: 'true'
					color: hex('#333333ff')


			# FOOTER
			BoxLayout: 
				padding: app.get_scaled_tuple([10.0, 0.0, 10.0, 10.0])
				size_hint: (None, None)
				height: app.get_scaled_height(122.0)
				width: app.get_scaled_width(800.0)
				orientation: 'horizontal'
				BoxLayout: 
					size_hint: (None, None)
					height: app.get_scaled_height(122.0)
					width: app.get_scaled_width(244.5)
					padding: app.get_scaled_tuple([0.0, 0.0, 184.5, 0.0])
					Button:
					    font_size: app.get_scaled_sp('15.0sp')
						size_hint: (None,None)
						height: app.get_scaled_height(52.0)
						width: app.get_scaled_width(60.0)
						background_color: hex('#F4433600')
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
					height: app.get_scaled_height(122.0)
					width: app.get_scaled_width(291.0)
					padding: app.get_scaled_tuple([0.0, 0.0, 0.0, 32.0])
					Button:
						id: next_button
						background_normal: "./asmcnc/skavaUI/img/next.png"
						background_down: "./asmcnc/skavaUI/img/next.png"
						border: app.get_scaled_tuple([14.5, 14.5, 14.5, 14.5])
						size_hint: (None,None)
						width: app.get_scaled_width(291.0)
						height: app.get_scaled_height(79.0)
						on_press: root.next_screen()
						text: 'Next...'
						font_size: app.get_scaled_sp('30.0sp')
						color: hex('#f9f9f9ff')
						markup: True
						center: self.parent.center
						pos: self.parent.pos
				BoxLayout: 
					size_hint: (None, None)
					height: app.get_scaled_height(122.0)
					width: app.get_scaled_width(244.5)
					padding: app.get_scaled_tuple([193.5, 0.0, 0.0, 0.0])



"""
)


class WelcomeTextScreen(Screen):
    def __init__(self, **kwargs):
        super(WelcomeTextScreen, self).__init__(**kwargs)
        self.start_seq = kwargs["start_sequence"]
        self.sm = kwargs["screen_manager"]
        self.l = kwargs["localization"]
        self.update_strings()

    def next_screen(self):
        self.update_seen()
        self.start_seq.next_in_sequence()

    def prev_screen(self):
        self.start_seq.prev_in_sequence()

    def update_strings(self):
        self.header_label.text = self.l.get_str("Welcome to SmartBench")
        self.thankyou_label.text = self.l.get_str(
            "Thank you for purchasing SmartBench."
        )
        self.next_steps_label.text = self.l.get_str(
            "Please follow the next steps to set up your Console, and complete your warranty registration process."
        )
        self.minutes_label.text = self.l.get_str("It will only a take a few minutes.")
        self.next_button.text = self.l.get_str("Next") + "..."

    def update_seen(self):
        show_user_welcome_app = os.popen(
            'grep "show_user_welcome_app" /home/pi/easycut-smartbench/src/config.txt'
        ).read()
        if not show_user_welcome_app:
            os.system(
                "sudo sed -i -e '$ashow_user_welcome_app=False' /home/pi/easycut-smartbench/src/config.txt"
            )
        elif "True" in show_user_welcome_app:
            os.system(
                'sudo sed -i "s/show_user_welcome_app=True/show_user_welcome_app=False/" /home/pi/easycut-smartbench/src/config.txt'
            )
