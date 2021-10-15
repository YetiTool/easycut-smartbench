# -*- coding: utf-8 -*-
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.scrollview import ScrollView
from kivy.properties import StringProperty, DictProperty

from asmcnc.skavaUI import popup_info

Builder.load_string("""


<ScrollPrivacyNotice>:

    privacy_notice : privacy_notice

    RstDocument:
        id: privacy_notice
        base_font_size: 30
        underline_color: 'e5e5e5'
        colors: root.color_dict

<WiFiAndDataConsentScreen3>

	scroll_privacy_notice : scroll_privacy_notice
	user_info : user_info
	terms_checkbox : terms_checkbox
	decline_button : decline_button
	accept_button : accept_button

    BoxLayout:
        height: dp(800)
        width: dp(480)
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
                    size_hint: (None,None)
                    height: dp(60)
                    width: dp(800)
                    text: "Wi-Fi and Data Consent"
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
                height: dp(288)
                padding: [dp(15), dp(5), dp(15), dp(5)]
                spacing: 5
                orientation: 'vertical'

                BoxLayout: 
                	size_hint: (1,8)
	                canvas.before:
	                    Color:
	                        rgba: hex('#e5e5e5ff')
	                    Rectangle:
	                        pos: self.pos
	                        size: self.size
					padding: dp(1)
	            	ScrollPrivacyNotice:
	                	id: scroll_privacy_notice

                BoxLayout: 
                	size_hint: (1,1)
                	orientation: 'horizontal'
                	padding: [dp(20), dp(0)]
	                # canvas:
	                #	# Test to see box
	                #     Color:
	                #         rgba: hex('#1976d2ff')
	                #     Rectangle:
	                #         pos: self.pos
	                #         size: self.size

	                Label: 
	                	id: user_info
						size_hint: (0.7,1)
	                    # color: hex('#f9f9f9ff') # white
	                    color: hex('#333333ff') #grey
	                    font_size: dp(18)
	                    halign: "center"
	                    valign: "middle"
	                    markup: True
	                    text_size: self.size
	                    size: self.texture_size


					CheckBox:
						id: terms_checkbox
						size_hint: (0.3,1)
		                background_checkbox_normal: "./asmcnc/skavaUI/img/checkbox_inactive.png"
		                on_active: root.on_checkbox_active()

            # FOOTER
			BoxLayout: 
				padding: [10,0,10,10]
				size_hint: (None, None)
				height: dp(132)
				width: dp(800)
				orientation: 'horizontal'
				BoxLayout: 
					size_hint: (None, None)
					height: dp(122)
					width: dp(60)
					# padding: [0, 0, 184.5, 0]
					Button:
						size_hint: (None,None)
						height: dp(52)
						width: dp(60)
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
					height: dp(122)
					width: dp(660)
					padding: [dp(6),0,dp(6),dp(42)]
					spacing: dp(66)
					Button:
						id: decline_button
						background_normal: "./asmcnc/skavaUI/img/next.png"
						background_down: "./asmcnc/skavaUI/img/next.png"
						background_disabled_normal: "./asmcnc/core_UI/data_and_wifi/img/standard_button_disabled.png"
						border: [dp(14.5)]*4
						size_hint: (None,None)
						width: dp(291)
						height: dp(79)
						on_press: root.decline_terms()
						font_size: '30sp'
						color: hex('#f9f9f9ff')
						markup: True
						center: self.parent.center
						pos: self.parent.pos

					Button:
						id: accept_button
						background_normal: "./asmcnc/skavaUI/img/next.png"
						background_down: "./asmcnc/skavaUI/img/next.png"
						background_disabled_normal: "./asmcnc/core_UI/data_and_wifi/img/standard_button_disabled.png"
						border: [dp(14.5)]*4
						size_hint: (None,None)
						width: dp(291)
						height: dp(79)
						on_press: root.accept_terms()
						font_size: '30sp'
						color: hex('#f9f9f9ff')
						markup: True
						center: self.parent.center
						pos: self.parent.pos

				BoxLayout: 
					size_hint: (None, None)
					height: dp(122)
					width: dp(60)
					# padding: [193.5, 0, 0, 0]

""")

class ScrollPrivacyNotice(ScrollView):
    text = StringProperty('')

    color_dict = DictProperty({
                    'background': 'e5e5e5ff',
                    'link': '1976d2ff',
                    'paragraph': '333333ff',
                    'title': '333333ff',
                    'bullet': '333333ff'})


class WiFiAndDataConsentScreen3(Screen):

	checkbox_checked = False

	def __init__(self, **kwargs):
		super(WiFiAndDataConsentScreen3, self).__init__(**kwargs)
		self.c=kwargs['consent_manager']
		self.l = kwargs['localization']
		self.update_strings()
		self.set_checkbox_default()

		self.scroll_privacy_notice.privacy_notice.source = "./asmcnc/core_UI/data_and_wifi/privacy_notice.txt"

	def on_pre_leave(self):
		self.set_checkbox_default()

	def prev_screen(self):
		self.c.sm.current='consent_2'

	def update_strings(self):
		self.user_info.text = self.l.get_str("I have read and understood the privacy notice")
		self.decline_button.text = self.l.get_str("Decline")
		self.accept_button.text = self.l.get_str("Accept")

	def accept_terms(self):
		if self.terms_checkbox.active: 
			self.c.accept_terms_and_enable_wifi()

	def decline_terms(self):
		if self.terms_checkbox.active: 
			self.c.warn_user_before_accepting_decline()

	def on_checkbox_active(self):
		if self.terms_checkbox.active: 
			self.decline_button.disabled = False
			self.accept_button.disabled = False
		else:
			self.decline_button.disabled = True
			self.accept_button.disabled = True

	def set_checkbox_default(self):
		self.terms_checkbox.active = False
		self.decline_button.disabled = True
		self.accept_button.disabled = True