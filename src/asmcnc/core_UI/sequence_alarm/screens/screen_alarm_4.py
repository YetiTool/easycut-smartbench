"""
Created on 31 March 2021
@author: Letty
"""
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock

Builder.load_string(
    """
<AlarmScreen4>:
	alarm_title : alarm_title
	icon_container : icon_container
	icon : icon
	description_label : description_label
	next_button : next_button

	canvas:
		Color: 
			rgba: [1, 1, 1, 1]
		Rectangle: 
			size: self.size
			pos: self.pos
	BoxLayout:
		orientation: 'vertical'
		padding: 0
		spacing: 0
		size_hint: (None, None)
		height: dp(1.0*app.height)
		width: dp(1.0*app.width)
		# Alarm header
		BoxLayout: 
			padding:[app.get_scaled_width(15), 0, app.get_scaled_width(15), 0]
			spacing: 0
			size_hint: (None, None)
			height: dp(0.104166666667*app.height)
			width: dp(1.0*app.width)
			orientation: 'horizontal'
			Label:
				id: alarm_title
				size_hint: (None, None)
				font_size: str(0.0375*app.width) + 'sp'
				color: [0,0,0,1]
				markup: True
				halign: 'left'
				height: dp(0.104166666667*app.height)
				width: dp(0.9625*app.width)
				text_size: self.size
		# Red underline
		BoxLayout: 
			padding:[app.get_scaled_width(10), 0, app.get_scaled_width(10), 0]
			spacing: 0
			size_hint: (None, None)
			height: dp(0.0104166666667*app.height)
			width: dp(1.0*app.width)
			Image:
				id: red_underline
				source: "./asmcnc/skavaUI/img/red_underline.png"
				center_x: self.parent.center_x
				y: self.parent.y
				size: self.parent.width, self.parent.height
				allow_stretch: True
		# Image and text
		BoxLayout: 
			padding:[0, app.get_scaled_height(35.000000000016), 0, 0]
			spacing: 0
			size_hint: (None, None)
			height: dp(0.589583333333*app.height)
			width: dp(1.0*app.width)
			orientation: 'vertical'
			BoxLayout: 
				id: icon_container
				padding:[app.get_scaled_width(335), 0, 0, 0]
				size_hint: (None, None)
				height: dp(0.270833333333*app.height)
				width: dp(1.0*app.width)       
				Image:
					id: icon
					center_x: self.parent.center_x
					y: self.parent.y
					size: self.parent.width, self.parent.height
					allow_stretch: True
					size_hint: (None, None)
					height: dp(0.270833333333*app.height)
					width: dp(0.1625*app.width)
			BoxLayout:
				id: description container
				padding:[app.get_scaled_width(30), 0, app.get_scaled_width(30), 0]
				spacing: 0
				size_hint: (None, None)
				height: dp(0.245833333333*app.height)
				width: dp(1.0*app.width)
				Label:
					id: description_label
					font_size: str(0.025*app.width) + 'sp'
					color: [0,0,0,1]
					markup: True
					halign: 'center'
					valign: 'middle'
					text_size: self.size
					size: self.parent.size
		# Buttons
		BoxLayout: 
			padding:[app.get_scaled_width(10), 0, app.get_scaled_width(10), app.get_scaled_height(9.999999999984)]
			size_hint: (None, None)
			height: dp(0.295833333333*app.height)
			width: dp(1.0*app.width)
			orientation: 'horizontal'
			BoxLayout: 
				size_hint: (None, None)
				height: dp(0.275*app.height)
				width: dp(0.305625*app.width)
				padding:[0, 0, app.get_scaled_width(184.5), 0]
				Button:
				    font_size: str(0.01875 * app.width) + 'sp'
					size_hint: (None,None)
					height: dp(0.108333333333*app.height)
					width: dp(0.075*app.width)
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
				height: dp(0.275*app.height)
				width: dp(0.36375*app.width)
				padding:[0, 0, 0, app.get_scaled_height(51.99999999984)]
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
				height: dp(0.275*app.height)
				width: dp(0.305625*app.width)
				padding:[app.get_scaled_width(193.5), 0, 0, 0]
"""
)


class AlarmScreen4(Screen):
    def __init__(self, **kwargs):
        super(AlarmScreen4, self).__init__(**kwargs)
        self.a = kwargs["alarm_manager"]
        self.alarm_title.text = self.a.l.get_bold("Alarm: Learn more...")
        self.icon.source = "./asmcnc/core_UI/sequence_alarm/img/qr-code.png"
        self.description_label.text = (
            self.a.l.get_str(
                "Learn more about the cause of the alarm by visiting our knowledge base at"
            )
            + "\n"
            + "https://www.yetitool.com/support/knowledge-base/alarm-screens"
        )
        self.next_button.text = self.a.l.get_str("Next") + "..."

    def next_screen(self):
        self.a.sm.get_screen("alarm_5").return_to_screen = "alarm_4"
        self.a.sm.current = "alarm_5"

    def prev_screen(self):
        self.a.sm.current = "alarm_3"
