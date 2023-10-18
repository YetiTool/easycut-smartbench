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
		width: dp(800)
		height: dp(480)
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
					height: dp(60)
					width: dp(800)
					text: "SmartBench Warranty Registration"
					color: hex('#f9f9f9ff')
					# color: hex('#333333ff') #grey
					font_size: dp(30)
					halign: "center"
					valign: "bottom"
					markup: True
				   
			# BODY
			BoxLayout:
				size_hint: (None,None)
				width: dp(800)
				height: dp(298)
				orientation: 'vertical'


				Button:
					size_hint_x: None
					width: dp(52)
					background_color: hex('##e5e5e5')
					background_normal: ''
					on_press: root.go_to_factory_settings()

				Label:
					id: scan_qr_code
					font_size: '30sp'
					text_size: self.size
					valign: 'bottom'
					halign: 'center'
					markup: 'true'
					color: hex('#333333ff')

				BoxLayout:
					orientation: 'vertical'
					width: dp(800)
					height: dp(200)
					padding: [20, 20, 20, 0]
					size_hint: (None,None)
					spacing: 0

					Label:
						id: instructions_label
						size_hint_y: 0.3
						font_size: '20sp'
						# text: "[color=333333ff]To submit your details and receive your activation code, go to[/color]"
						text_size: self.size
						valign: 'middle'
						halign: 'center'
						markup: True
						color: hex('#333333ff')

					BoxLayout:
						orientation: 'horizontal'
						width: dp(800)
						height: dp(132)
						# padding: [20, 0]
						size_hint: (None,None)
						spacing: 0

						BoxLayout:
							padding: [10,0,0,0]
							width: dp(162)
							height: dp(132)
							size_hint: (None,None)
							Image:
								source: "./asmcnc/apps/start_up_sequence/warranty_app/img/registration-qr-code.png"
								center_x: self.parent.center_x
								y: self.parent.y
								size: self.parent.width, self.parent.height
								allow_stretch: True

						BoxLayout:
							orientation: 'vertical'
							width: dp(598)
							height: dp(132)
							padding: [0,0,0,0]
							size_hint: (None,None)

							Label:
								size_hint_y: 0.4
								font_size: '22sp'
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
								font_size: '20sp'
								# text: "[color=333333ff]Can't use the web form?"
								text_size: self.size
								valign: 'bottom'
								halign: 'left'
								markup: 'true'
								color: hex('#333333ff')

							Label:
								id: contact_us_at_support
								size_hint_y: 0.3
								font_size: '20sp'
								# text: "[color=333333ff]Contact us at https://www.yetitool.com/support[/color]"
								text_size: self.size
								valign: 'middle'
								halign: 'left'
								markup: 'true'
								color: hex('#333333ff')

			# FOOTER
			BoxLayout: 
				padding: [10,0,10,10]
				size_hint: (None, None)
				height: dp(122)
				width: dp(800)
				orientation: 'horizontal'

				BoxLayout: 
					size_hint: (None, None)
					height: dp(122)
					width: dp(244.5)
					padding: [0, 0, 184.5, 0]
					Button:
						id: prev_screen_button
						size_hint: (None,None)
						height: dp(52)
						width: dp(60)
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
					height: dp(122)
					width: dp(291)
					padding: [0,0,0,32]
					Button:
						id: next_button
						background_normal: "./asmcnc/skavaUI/img/next.png"
						background_down: "./asmcnc/skavaUI/img/next.png"
						border: [dp(14.5)]*4
						size_hint: (None,None)
						width: dp(291)
						height: dp(79)
						on_press: root.next_screen()
						text: 'Next...'
						font_size: '30sp'
						color: hex('#f9f9f9ff')
						markup: True
						center: self.parent.center
						pos: self.parent.pos

				BoxLayout: 
					size_hint: (None, None)
					height: dp(122)
					width: dp(244.5)
					padding: [dp(192.5), 0, 0, 0]

					Button:
						size_hint: (None,None)
						height: dp(52)
						width: dp(52)
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

    def update_contact_us_font_sizes(
        self,
    ):  # Update both labels together to make it look nicer
        if len(self.contact_us_at_support.text) > 70:
            self.cant_use_web_label.font_size = 17
            self.contact_us_at_support.font_size = 17
        else:
            self.cant_use_web_label.font_size = 20
            self.contact_us_at_support.font_size = 20

    def go_to_factory_settings(self):
        popup_warranty.PopupFactorySettingsPassword(self.start_seq.am)

    def quit_to_console(self):
        popup_warranty.QuitToConsoleWarranty(self.start_seq.sm)
