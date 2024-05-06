# -*- coding: utf-8 -*-
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from asmcnc.skavaUI import popup_info

Builder.load_string(
    """

<WiFiAndDataConsentScreen2>

	header_label : header_label
	user_info : user_info
	next_button : next_button

    BoxLayout:
        height: dp(1.66666666667*app.height)
        width: dp(0.6*app.width)
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
                    height: dp(0.125*app.height)
                    width: dp(1.0*app.width)
                    text: "Wi-Fi and Data Consent"
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
                padding:[dp(0.025)*app.width, dp(0.0208333333333)*app.height, dp(0.025)*app.width, 0]
                spacing: 0
                orientation: 'horizontal'
                Label: 
                	id: user_info
					size_hint: (1,1)
                    # color: hex('#f9f9f9ff') # white
                    color: hex('#333333ff') #grey
                    font_size: dp(0.0225*app.width)
                    halign: "left"
                    valign: "top"
                    markup: True
                    text_size: self.size
                    size: self.texture_size

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
						on_press: root.next_screen()
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


class WiFiAndDataConsentScreen2(Screen):
    def __init__(self, **kwargs):
        super(WiFiAndDataConsentScreen2, self).__init__(**kwargs)
        self.start_seq = kwargs["start_sequence"]
        self.c = kwargs["consent_manager"]
        self.l = kwargs["localization"]
        self.update_strings()

    def next_screen(self):
        try:
            self.start_seq.next_in_sequence()
        except:
            self.c.sm.current = "consent_3"

    def prev_screen(self):
        try:
            self.start_seq.prev_in_sequence()
        except:
            self.c.sm.current = "consent_1"

    def update_strings(self):
        self.header_label.text = self.l.get_str("Wi-Fi and Data Consent")
        self.user_info.text = (
            self.l.get_str(
                "If you do not want Yeti Tool to collect machine data from your SmartBench, you can decline the data policy on the next screen."
            )
            + "\n\n"
            + self.l.get_bold(
                "This will disable Wi-Fi to prevent SmartBench sending data to Yeti Tool."
            )
            + "\n\n"
            + self.l.get_str("You will need Wi-Fi to:")
            + "\n\n"
            + "[b]\xe2\x80\xa2[/b] "
            + self.l.get_str("Automatically receive software updates")
            + "\n"
            + "[b]\xe2\x80\xa2[/b] "
            + self.l.get_str("Remotely transfer files (e.g. with SmartTransfer)")
            + "\n"
            + "[b]\xe2\x80\xa2[/b] "
            + self.l.get_str(
                "Remotely manage and monitor SmartBench (e.g. with SmartManager)"
            )
            + "\n\n"
            + self.l.get_str(
                "You can come back to this data policy at any time, and enable or disable Wi-Fi."
            )
        )
        self.next_button.text = self.l.get_str("Next") + "..."
