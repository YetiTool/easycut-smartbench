from kivy.core.window import Window

"""
Created on 15th September 2021
@author: Letty
Reboot to apply language settings
"""
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
import sys, os
from asmcnc.skavaUI import widget_status_bar

Builder.load_string(
    """
<ApplySettingsScreen>:

	title_label : title_label
	success_label : success_label
	next_button : next_button
	BoxLayout: 
		size_hint: (None,None)
		width: app.get_scaled_width(800.0)
		height: app.get_scaled_height(480.0)
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
				orientation: 'vertical'
				BoxLayout:
					orientation: 'vertical'
					width: app.get_scaled_width(800.0)
					height: app.get_scaled_height(200.0)
					padding: app.get_scaled_tuple([20.0, 0])
					size_hint: (None,None)
					Label:
						id: success_label
						font_size: app.get_scaled_sp('30.0sp')
						text_size: self.size
						valign: 'top'
						halign: 'center'
						markup: 'true'
						color: hex('#333333ff')
			# FOOTER
			BoxLayout: 
				padding: app.get_scaled_tuple([10.0, 0, 10.0, 10.0])
				size_hint: (None, None)
				height: app.get_scaled_height(122.0)
				width: app.get_scaled_width(800.0)
				orientation: 'horizontal'
				BoxLayout: 
					size_hint: (None, None)
					height: app.get_scaled_height(122.0)
					width: app.get_scaled_width(244.5)
					padding: app.get_scaled_tuple([0, 0, 184.5, 0])
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
					padding: app.get_scaled_tuple([0, 0, 0, 32.0])
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
					padding: app.get_scaled_tuple([193.5, 0, 0, 0])
"""
)


class ApplySettingsScreen(Screen):
    def __init__(self, **kwargs):
        super(ApplySettingsScreen, self).__init__(**kwargs)
        self.start_seq = kwargs["start_sequence"]
        self.sm = kwargs["screen_manager"]
        self.m = kwargs["machine"]
        self.l = kwargs["localization"]
        self.update_strings()

    def next_screen(self):
        self.start_seq.exit_sequence(False) # used for test
        self.sm.current = "rebooting"

    def prev_screen(self):
        self.start_seq.prev_in_sequence()

    def update_strings(self):
        self.title_label.text = self.l.get_str("Reboot!")
        self.success_label.text = self.l.get_bold(
            "Reboot to finish applying your settings, and get started!"
        )
        self.next_button.text = self.l.get_str("Reboot!")
        self.update_font_size(self.next_button)

    def update_font_size(self, value):
        text_length = self.l.get_text_length(value.text)
        if text_length > 20:
            value.font_size = 0.03125 * Window.width
        else:
            value.font_size = 0.0375 * Window.width
