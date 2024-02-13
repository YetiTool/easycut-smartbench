from kivy.core.window import Window

"""
Created on 31 March 2021
@author: Letty
"""
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock

Builder.load_string(
    """
<AlarmScreen1>:
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
		height: dp(app.get_scaled_height(480))
		width: dp(app.get_scaled_width(800))
		# Alarm header
		BoxLayout: 
			padding:[app.get_scaled_width(15), 0, app.get_scaled_width(15), 0]
			spacing: 0
			size_hint: (None, None)
			height: dp(app.get_scaled_height(50))
			width: dp(app.get_scaled_width(800))
			orientation: 'horizontal'
			Label:
				id: alarm_title
				size_hint: (None, None)
				font_size: str(get_scaled_width(30)) + 'sp'
				color: [0,0,0,1]
				markup: True
				halign: 'left'
				height: dp(app.get_scaled_height(50))
				width: dp(app.get_scaled_width(770))
				text_size: self.size
		# Red underline
		BoxLayout: 
			padding:[app.get_scaled_width(10), 0, app.get_scaled_width(10), 0]
			spacing: 0
			size_hint: (None, None)
			height: dp(app.get_scaled_height(5))
			width: dp(app.get_scaled_width(800))
			Image:
				id: red_underline
				source: "./asmcnc/skavaUI/img/red_underline.png"
				center_x: self.parent.center_x
				y: self.parent.y
				size: self.parent.width, self.parent.height
				allow_stretch: True
		# Image and text
		BoxLayout: 
			padding:[0, app.get_scaled_height(35), 0, 0]
			spacing: 0
			size_hint: (None, None)
			height: dp(app.get_scaled_height(283))
			width: dp(app.get_scaled_width(800))
			orientation: 'vertical'
			BoxLayout: 
				id: icon_container
				padding:[app.get_scaled_width(335), 0, 0, 0]
				size_hint: (None, None)
				height: dp(app.get_scaled_height(130))
				width: dp(app.get_scaled_width(800))       
				Image:
					id: icon
					center_x: self.parent.center_x
					y: self.parent.y
					size: self.parent.width, self.parent.height
					allow_stretch: True
					size_hint: (None, None)
					height: dp(app.get_scaled_height(130))
					width: dp(app.get_scaled_width(130))
			BoxLayout:
				id: description container
				padding:[app.get_scaled_width(30), 0, app.get_scaled_width(30), 0]
				spacing: 0
				size_hint: (None, None)
				height: dp(app.get_scaled_height(118))
				width: dp(app.get_scaled_width(800))
				Label:
					id: description_label
					font_size: str(get_scaled_width(20)) + 'sp'
					color: [0,0,0,1]
					markup: True
					halign: 'center'
					valign: 'middle'
					text_size: self.size
					size: self.parent.size
		# Buttons
		BoxLayout: 
			padding:[app.get_scaled_width(10), 0, app.get_scaled_width(10), app.get_scaled_height(10)]
			size_hint: (None, None)
			height: dp(app.get_scaled_height(142))
			width: dp(app.get_scaled_width(800))
			orientation: 'horizontal'
			BoxLayout: 
				size_hint: (None, None)
				height: dp(app.get_scaled_height(132))
				width: dp(app.get_scaled_width(244.5))
				padding:[0, 0, app.get_scaled_width(184.5), 0]

			BoxLayout: 
				size_hint: (None, None)
				height: dp(app.get_scaled_height(132))
				width: dp(app.get_scaled_width(291))
				padding:[0, 0, 0, app.get_scaled_height(52)]
				Button:
					id: next_button
					background_normal: "./asmcnc/skavaUI/img/next.png"
					background_down: "./asmcnc/skavaUI/img/next.png"
					border: [dp(14.5)]*4
					size_hint: (None,None)
					width: dp(app.get_scaled_width(291))
					height: dp(app.get_scaled_height(79))
					on_press: root.next_screen()
					text: 'Next...'
					font_size: str(get_scaled_width(30)) + 'sp'
					color: hex('#f9f9f9ff')
					markup: True
					center: self.parent.center
					pos: self.parent.pos
			BoxLayout: 
				size_hint: (None, None)
				height: dp(app.get_scaled_height(132))
				width: dp(app.get_scaled_width(244.5))
				padding:[app.get_scaled_width(193.5), 0, 0, 0]
"""
)


class AlarmScreen1(Screen):
    def __init__(self, **kwargs):
        super(AlarmScreen1, self).__init__(**kwargs)
        self.a = kwargs["alarm_manager"]
        self.alarm_title.text = self.a.l.get_bold("Alarm: Unexpected event!")
        self.icon.source = "./asmcnc/core_UI/sequence_alarm/img/alarm_icon.png"
        self.next_button.text = self.a.l.get_str("Next") + "..."

    def next_screen(self):
        if self.a.support_sequence:
            self.a.sm.current = "alarm_2"
        else:
            self.a.sm.get_screen("alarm_5").return_to_screen = "alarm_1"
            self.a.sm.current = "alarm_5"

    def prev_screen(self):
        self.a.sm.current = "alarm_1"

    def on_pre_enter(self):
        self.update_font_size(self.description_label)

    def update_font_size(self, value):
        text_length = self.a.l.get_text_length(value.text)
        if text_length > 330:
            value.font_size = 0.02 * Window.width
        elif text_length > 280:
            value.font_size = 0.02125 * Window.width
        elif text_length > 270:
            value.font_size = 0.0225 * Window.width
        else:
            value.font_size = 0.025 * Window.width
