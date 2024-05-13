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
		base_font_size: dp(0.0375)*app.width
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
		height: dp(1.66666666667*app.height)
		width: dp(0.6*app.width)
		canvas.before:
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
					id: header_label
					size_hint: (None,None)
					height: dp(0.125*app.height)
					width: dp(1.0*app.width)
					text: "Wi-Fi and Data Consent"
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
				height: dp(0.6*app.height)
				padding:[dp(0.01875)*app.width, dp(0.0104166666667)*app.height, dp(0.01875)*app.width, dp(0.0104166666667)*app.height]
				spacing:0.0104166666667*app.height
				orientation: 'vertical'

				BoxLayout: 
					size_hint: (1,8)
					canvas.before:
						Color:
							rgba: color_provider.get_rgba("light_grey")
						Rectangle:
							pos: self.pos
							size: self.size
					padding:[dp(0.00125)*app.width, dp(0.00208333333333)*app.height]
					ScrollPrivacyNotice:
						id: scroll_privacy_notice

				BoxLayout: 
					size_hint: (1,1)
					orientation: 'horizontal'
					padding:[dp(0.025)*app.width, 0]
					# canvas:
					#	# Test to see box
					#     Color:
					#         rgba: color_provider.get_rgba("blue")
					#     Rectangle:
					#         pos: self.pos
					#         size: self.size

					Label: 
						id: user_info
						size_hint: (0.7,1)
						# color: color_provider.get_rgba("near_white") # white
						color: color_provider.get_rgba("dark_grey") #grey
						font_size: dp(0.0225*app.width)
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
				padding:[dp(0.0125)*app.width, 0, dp(0.0125)*app.width, dp(0.0208333333333)*app.height]
				size_hint: (None, None)
				height: dp(0.275*app.height)
				width: dp(1.0*app.width)
				orientation: 'horizontal'
				BoxLayout: 
					size_hint: (None, None)
					height: dp(0.254166666667*app.height)
					width: dp(0.075*app.width)
					# padding: [0, 0, 184.5, 0]
					Button:
					    font_size: str(0.01875 * app.width) + 'sp'
						size_hint: (None,None)
						height: dp(0.108333333333*app.height)
						width: dp(0.075*app.width)
						background_color: color_provider.get_rgba("transparent")
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
					width: dp(0.825*app.width)
					padding:[dp(0.0075)*app.width, 0, dp(0.0075)*app.width, dp(0.0875)*app.height]
					spacing:dp(0.0825)*app.width
					Button:
						id: decline_button
						background_normal: "./asmcnc/skavaUI/img/next.png"
						background_down: "./asmcnc/skavaUI/img/next.png"
						background_disabled_normal: "./asmcnc/apps/start_up_sequence/data_consent_app/img/standard_button_disabled.png"
						border: [dp(14.5)]*4
						size_hint: (None,None)
						width: dp(0.36375*app.width)
						height: dp(0.164583333333*app.height)
						on_press: root.decline_terms()
						font_size: str(0.0375*app.width) + 'sp'
						color: color_provider.get_rgba("near_white")
						markup: True
						center: self.parent.center
						pos: self.parent.pos

					Button:
						id: accept_button
						background_normal: "./asmcnc/skavaUI/img/next.png"
						background_down: "./asmcnc/skavaUI/img/next.png"
						background_disabled_normal: "./asmcnc/apps/start_up_sequence/data_consent_app/img/standard_button_disabled.png"
						border: [dp(14.5)]*4
						size_hint: (None,None)
						width: dp(0.36375*app.width)
						height: dp(0.164583333333*app.height)
						on_press: root.accept_terms()
						font_size: str(0.0375*app.width) + 'sp'
						color: color_provider.get_rgba("near_white")
						markup: True
						center: self.parent.center
						pos: self.parent.pos

				BoxLayout: 
					size_hint: (None, None)
					height: dp(0.254166666667*app.height)
					width: dp(0.075*app.width)
					# padding: [193.5, 0, 0, 0]

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
