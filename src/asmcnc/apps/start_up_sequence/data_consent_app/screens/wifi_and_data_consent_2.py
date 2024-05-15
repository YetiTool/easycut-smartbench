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
                height: app.get_scaled_height(298.0)
                padding: app.get_scaled_tuple([20.0, 10.0, 20.0, 0])
                spacing: 0
                orientation: 'horizontal'
                Label: 
                	id: user_info
					size_hint: (1,1)
                    # color: hex('#f9f9f9ff') # white
                    color: hex('#333333ff') #grey
                    font_size: app.get_scaled_width(18.0)
                    halign: "left"
                    valign: "top"
                    markup: True
                    text_size: self.size
                    size: self.texture_size

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
