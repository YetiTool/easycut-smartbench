from kivy.core.window import Window
"""
Created on nov 2020
@author: Ollie
"""
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.textinput import TextInput
from asmcnc.skavaUI import widget_status_bar
from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.gridlayout import GridLayout
import sys, os
from asmcnc.apps.start_up_sequence.warranty_app.screens import popup_warranty

Builder.load_string(
    """

<WarrantyScreen1>:

	title_label : title_label
	scan_qr_code : scan_qr_code
	instructions_label : instructions_label
	cant_use_web_label : cant_use_web_label
	contact_us_at_support : contact_us_at_support
	prev_screen_button : prev_screen_button
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
					text: "SmartBench Warranty Registration"
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


				Button:
				    font_size: app.get_scaled_sp('15.0sp')
					size_hint_x: None
					width: app.get_scaled_width(52.0)
					background_color: hex('##e5e5e5')
					background_normal: ''
					on_press: root.go_to_factory_settings()

				Label:
					id: scan_qr_code
					font_size: app.get_scaled_sp('30.0sp')
					text_size: self.size
					valign: 'bottom'
					halign: 'center'
					markup: 'true'
					color: hex('#333333ff')

				BoxLayout:
					orientation: 'vertical'
					width: app.get_scaled_width(800.0)
					height: app.get_scaled_height(200.0)
					padding: app.get_scaled_tuple([20.0, 20.0, 20.0, 0.0])
					size_hint: (None,None)
					spacing: 0

					Label:
						id: instructions_label
						size_hint_y: 0.3
						font_size: app.get_scaled_sp('20.0sp')
						# text: "[color=333333ff]To submit your details and receive your activation code, go to[/color]"
						text_size: self.size
						valign: 'middle'
						halign: 'center'
						markup: True
						color: hex('#333333ff')

					BoxLayout:
						orientation: 'horizontal'
						width: app.get_scaled_width(800.0)
						height: app.get_scaled_height(132.0)
						# padding: app.get_scaled_tuple([20.0, 0.0])
						size_hint: (None,None)
						spacing: 0

						BoxLayout:
							padding: app.get_scaled_tuple([10.0, 0.0, 0.0, 0.0])
							width: app.get_scaled_width(162.0)
							height: app.get_scaled_height(132.0)
							size_hint: (None,None)
							Image:
								source: "./asmcnc/apps/start_up_sequence/warranty_app/img/registration-qr-code.png"
								center_x: self.parent.center_x
								y: self.parent.y
								size: self.parent.width, self.parent.height
								allow_stretch: True

						BoxLayout:
							orientation: 'vertical'
							width: app.get_scaled_width(598.0)
							height: app.get_scaled_height(132.0)
							padding: app.get_scaled_tuple([0.0, 0.0, 0.0, 0.0])
							size_hint: (None,None)

							Label:
								size_hint_y: 0.4
								font_size: app.get_scaled_sp('22.0sp')
								text: "[color=333333ff]https://www.yetitool.com/support/Register-Your-Product[/color]"
								text_size: self.size
								valign: 'middle'
								halign: 'left'
								markup: 'true'
								multiline: True
								color: hex('#333333ff')
							
							Label:
								id: cant_use_web_label
								size_hint_y: 0.3
								font_size: app.get_scaled_sp('20.0sp')
								# text: "[color=333333ff]Can't use the web form?"
								text_size: self.size
								valign: 'bottom'
								halign: 'left'
								markup: 'true'
								color: hex('#333333ff')

							Label:
								id: contact_us_at_support
								size_hint_y: 0.3
								font_size: app.get_scaled_sp('20.0sp')
								# text: "[color=333333ff]Contact us at https://www.yetitool.com/support[/color]"
								text_size: self.size
								valign: 'middle'
								halign: 'left'
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
						id: prev_screen_button
						size_hint: (None,None)
						height: app.get_scaled_height(51.9999999998)
						width: app.get_scaled_width(60.0)
						background_color: hex('#F4433600')
						center: self.parent.center
						pos: self.parent.pos
						on_press: root.prev_screen()
						opacity: 1
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
						height: app.get_scaled_height(78.9999999998)
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
					padding: app.get_scaled_tuple([192.5, 0.0, 0.0, 0.0])

					Button:
					    font_size: app.get_scaled_sp('15.0sp')
						size_hint: (None,None)
						height: app.get_scaled_height(51.9999999998)
						width: app.get_scaled_width(52.0)
						background_color: hex('##e5e5e5')
						background_normal: ''
						on_press: root.quit_to_console()

"""
)


class WarrantyScreen1(Screen):
    def __init__(self, **kwargs):
        super(WarrantyScreen1, self).__init__(**kwargs)
        self.start_seq = kwargs["start_sequence"]
        self.m = kwargs["machine"]
        self.l = kwargs["localization"]
        self.update_strings()

    def next_screen(self):
        self.start_seq.next_in_sequence()

    def prev_screen(self):
        self.start_seq.prev_in_sequence()

    def update_strings(self):
        self.title_label.text = self.l.get_str("SmartBench Warranty Registration")
        self.scan_qr_code.text = self.l.get_bold("Scan the QR Code to start")
        self.instructions_label.text = self.l.get_str(
            "To submit your details and receive your activation code, go to"
        )
        self.cant_use_web_label.text = self.l.get_str("Can't use the web form?")
        self.contact_us_at_support.text = self.l.get_str(
            "Contact us at https://www.yetitool.com/support"
        )
        self.next_button.text = self.l.get_str("Next") + "..."
        self.update_contact_us_font_sizes()

    def update_contact_us_font_sizes(self): # Update both labels together to make it look nicer
        if self.l.get_text_length(self.contact_us_at_support.text) > 70:
            self.cant_use_web_label.font_size = 0.02125 * Window.width
            self.contact_us_at_support.font_size = 0.02125 * Window.width
        else:
            self.cant_use_web_label.font_size = 0.025 * Window.width
            self.contact_us_at_support.font_size = 0.025 * Window.width

    def go_to_factory_settings(self):
        popup_warranty.PopupFactorySettingsPassword(self.start_seq.am)

    def quit_to_console(self):
        popup_warranty.QuitToConsoleWarranty(self.start_seq.sm)
