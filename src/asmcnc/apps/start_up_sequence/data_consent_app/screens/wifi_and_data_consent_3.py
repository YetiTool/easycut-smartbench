# -*- coding: utf-8 -*-
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.scrollview import ScrollView
from kivy.properties import StringProperty, DictProperty
from asmcnc.skavaUI import popup_info

Builder.load_string(
    """


<ScrollPrivacyNotice>:

	privacy_notice : privacy_notice

	RstDocument:
		id: privacy_notice
		base_font_size: app.get_scaled_width(30.0)
		underline_color: 'e5e5e5'
		colors: root.color_dict

<WiFiAndDataConsentScreen3>

	header_label : header_label
	scroll_privacy_notice : scroll_privacy_notice
	user_info : user_info
	terms_checkbox : terms_checkbox
	decline_button : decline_button
	accept_button : accept_button

	BoxLayout:
		height: app.get_scaled_height(800.000000002)
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
					text: "Wi-Fi and Data Consent"
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
				height: app.get_scaled_height(288.0)
				padding: app.get_scaled_tuple([15.0, 5.0, 15.0, 5.0])
				spacing: app.get_scaled_width(5.00000000002)
				orientation: 'vertical'

				BoxLayout: 
					size_hint: (1,8)
					canvas.before:
						Color:
							rgba: hex('#e5e5e5ff')
						Rectangle:
							pos: self.pos
							size: self.size
					padding: app.get_scaled_tuple([1.0, 1.0])
					ScrollPrivacyNotice:
						id: scroll_privacy_notice

				BoxLayout: 
					size_hint: (1,1)
					orientation: 'horizontal'
					padding: app.get_scaled_tuple([20.0, 0.0])
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
						font_size: app.get_scaled_width(18.0)
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
				padding: app.get_scaled_tuple([10.0, 0.0, 10.0, 10.0])
				size_hint: (None, None)
				height: app.get_scaled_height(132.0)
				width: app.get_scaled_width(800.0)
				orientation: 'horizontal'
				BoxLayout: 
					size_hint: (None, None)
					height: app.get_scaled_height(122.0)
					width: app.get_scaled_width(60.0)
					# padding: app.get_scaled_tuple([0.0, 0.0, 184.5, 0.0])
					Button:
					    font_size: app.get_scaled_sp('15.0sp')
						size_hint: (None,None)
						height: app.get_scaled_height(51.9999999998)
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
					width: app.get_scaled_width(660.0)
					padding: app.get_scaled_tuple([6.0, 0.0, 6.0, 42.0])
					spacing: app.get_scaled_width(66.0)
					Button:
						id: decline_button
						background_normal: "./asmcnc/skavaUI/img/next.png"
						background_down: "./asmcnc/skavaUI/img/next.png"
						background_disabled_normal: "./asmcnc/apps/start_up_sequence/data_consent_app/img/standard_button_disabled.png"
						border: app.get_scaled_tuple([14.5, 14.5, 14.5, 14.5])
						size_hint: (None,None)
						width: app.get_scaled_width(291.0)
						height: app.get_scaled_height(78.9999999998)
						on_press: root.decline_terms()
						font_size: app.get_scaled_sp('30.0sp')
						color: hex('#f9f9f9ff')
						markup: True
						center: self.parent.center
						pos: self.parent.pos

					Button:
						id: accept_button
						background_normal: "./asmcnc/skavaUI/img/next.png"
						background_down: "./asmcnc/skavaUI/img/next.png"
						background_disabled_normal: "./asmcnc/apps/start_up_sequence/data_consent_app/img/standard_button_disabled.png"
						border: app.get_scaled_tuple([14.5, 14.5, 14.5, 14.5])
						size_hint: (None,None)
						width: app.get_scaled_width(291.0)
						height: app.get_scaled_height(78.9999999998)
						on_press: root.accept_terms()
						font_size: app.get_scaled_sp('30.0sp')
						color: hex('#f9f9f9ff')
						markup: True
						center: self.parent.center
						pos: self.parent.pos

				BoxLayout: 
					size_hint: (None, None)
					height: app.get_scaled_height(122.0)
					width: app.get_scaled_width(60.0)
					# padding: app.get_scaled_tuple([193.5, 0.0, 0.0, 0.0])

"""
)


class ScrollPrivacyNotice(ScrollView):
    text = StringProperty("")
    color_dict = DictProperty(
        {
            "background": "e5e5e5ff",
            "link": "1976d2ff",
            "paragraph": "333333ff",
            "title": "333333ff",
            "bullet": "333333ff",
        }
    )


class WiFiAndDataConsentScreen3(Screen):
    checkbox_checked = False
    privacy_notice_path = (
        "./asmcnc/apps/start_up_sequence/data_consent_app/privacy_notice/"
    )

    def __init__(self, **kwargs):
        super(WiFiAndDataConsentScreen3, self).__init__(**kwargs)
        self.start_seq = kwargs["start_sequence"]
        self.c = kwargs["consent_manager"]
        self.l = kwargs["localization"]
        self.update_strings()
        self.set_checkbox_default()

    def on_pre_leave(self):
        self.set_checkbox_default()

    def prev_screen(self):
        try:
            self.start_seq.prev_in_sequence()
        except:
            self.c.sm.current = "consent_2"

    def update_strings(self):
        self.header_label.text = self.l.get_str("Wi-Fi and Data Consent")
        self.scroll_privacy_notice.privacy_notice.source = (
            self.privacy_notice_path + self.l.lang + ".rst"
        )
        self.user_info.text = self.l.get_str(
            "I have read and understood the privacy notice"
        )
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
