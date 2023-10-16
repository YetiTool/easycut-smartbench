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
		height: dp(1.0*app.height)
		width: dp(1.0*app.width)
		# Alarm header
		BoxLayout: 
			padding: [0.01875*app.width,0,0.01875*app.width,0]
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
			padding: [0.0125*app.width,0,0.0125*app.width,0]
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
			padding: [0,0.0729166666667*app.height,0,0]
			spacing: 0
			size_hint: (None, None)
			height: dp(0.589583333333*app.height)
			width: dp(1.0*app.width)
			orientation: 'vertical'
			BoxLayout: 
				id: icon_container
				padding: [0.41875*app.width,0,0,0]
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
				padding: [0.0375*app.width,0,0.0375*app.width,0]
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
			padding: [0.0125*app.width,0,0.0125*app.width,0.0208333333333*app.height]
			size_hint: (None, None)
			height: dp(0.295833333333*app.height)
			width: dp(1.0*app.width)
			orientation: 'horizontal'
			BoxLayout: 
				size_hint: (None, None)
				height: dp(0.275*app.height)
				width: dp(0.305625*app.width)
				padding: [0, 0,0.230625*app.width, 0]

			BoxLayout: 
				size_hint: (None, None)
				height: dp(0.275*app.height)
				width: dp(0.36375*app.width)
				padding: [0,0,0,0.108333333333*app.height]
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
				padding: [0.241875*app.width, 0, 0, 0]
"""
    )


class AlarmScreen1(Screen):

    def __init__(self, **kwargs):
        super(AlarmScreen1, self).__init__(**kwargs)
        self.a = kwargs['alarm_manager']
        self.alarm_title.text = self.a.l.get_bold('Alarm: Unexpected event!')
        self.icon.source = './asmcnc/core_UI/sequence_alarm/img/alarm_icon.png'
        self.next_button.text = self.a.l.get_str('Next') + '...'

    def next_screen(self):
        if self.a.support_sequence:
            self.a.sm.current = 'alarm_2'
        else:
            self.a.sm.get_screen('alarm_5').return_to_screen = 'alarm_1'
            self.a.sm.current = 'alarm_5'

    def prev_screen(self):
        self.a.sm.current = 'alarm_1'

    def on_pre_enter(self):
        self.update_font_size(self.description_label)

    def update_font_size(self, value):
        text_length = self.a.l.get_text_length(value.text)
        if text_length > 330:
            value.font_size = 16
        elif text_length > 280:
            value.font_size = 17
        elif text_length > 270:
            value.font_size = 18
        else:
            value.font_size = 20
