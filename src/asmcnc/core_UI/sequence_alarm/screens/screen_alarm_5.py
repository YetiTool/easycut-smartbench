from kivy.core.window import Window

"""
Created on 31 March 2021
@author: Letty
"""
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from asmcnc.core_UI.scaling_utils import get_scaled_width

Builder.load_string(
    """
<AlarmScreen5>:
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
			padding:[dp(0.01875)*app.width, 0, dp(0.01875)*app.width, 0]
			spacing: 0
			size_hint: (None, None)
			height: dp(0.104166666667*app.height)
			width: dp(1.0*app.width)
			orientation: 'horizontal'
			Label:
				id: alarm_title
				size_hint: (None, None)
				font_size: str(0.0375*app.width) + 'sp'
				color: color_provider.get_rgba("black")
				markup: True
				halign: 'left'
				height: dp(0.104166666667*app.height)
				width: dp(0.9625*app.width)
				text_size: self.size
		# Red underline
		BoxLayout: 
			padding:[dp(0.0125)*app.width, 0, dp(0.0125)*app.width, 0]
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
			padding:[0, dp(0.0729166666667)*app.height, 0, 0]
			spacing: 0
			size_hint: (None, None)
			height: dp(0.589583333333*app.height)
			width: dp(1.0*app.width)
			orientation: 'vertical'
			BoxLayout: 
				id: icon_container
				padding:[dp(0.41875)*app.width, 0, 0, 0]
				size_hint: (None, None)
				height: dp(0.270833333333*app.height)
				width: dp(1.0*app.width)       
				Image:
					id: icon
					source: "./asmcnc/core_UI/sequence_alarm/img/alarm_icon.png"
					center_x: self.parent.center_x
					y: self.parent.y
					size: self.parent.width, self.parent.height
					allow_stretch: True
					size_hint: (None, None)
					height: dp(0.270833333333*app.height)
					width: dp(0.1625*app.width)
			BoxLayout:
				id: description container
				padding:[dp(0.0375)*app.width, 0, dp(0.0375)*app.width, 0]
				spacing: 0
				size_hint: (None, None)
				height: dp(0.245833333333*app.height)
				width: dp(1.0*app.width)
				Label:
					id: description_label
					font_size: str(0.025*app.width) + 'sp'
					color: color_provider.get_rgba("black")
					markup: True
					halign: 'center'
					valign: 'middle'
					text_size: self.size
					size: self.parent.size
		# Buttons
		BoxLayout: 
			padding:[dp(0.0125)*app.width, 0, dp(0.0125)*app.width, dp(0.0208333333333)*app.height]
			size_hint: (None, None)
			height: dp(0.295833333333*app.height)
			width: dp(1.0*app.width)
			orientation: 'horizontal'
			BoxLayout: 
				size_hint: (None, None)
				height: dp(0.275*app.height)
				width: dp(0.305625*app.width)
				padding:[0, 0, dp(0.230625)*app.width, 0]
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
				padding:[0, 0, 0, dp(0.108333333333)*app.height]
				Button:
					id: next_button
					background_normal: "./asmcnc/skavaUI/img/next.png"
					background_down: "./asmcnc/skavaUI/img/next.png"
					border: [dp(14.5)]*4
					size_hint: (None,None)
					width: dp(0.36375*app.width)
					height: dp(0.164583333333*app.height)
					on_press: root.more_info()
					font_size: root.default_font_size
					color: hex('#f9f9f9ff')
					markup: True
					center: self.parent.center
					pos: self.parent.pos
					opacity: 0

			BoxLayout: 
				size_hint: (None, None)
				height: dp(0.275*app.height)
				width: dp(0.305625*app.width)
				padding:[dp(0.241875)*app.width, 0, 0, 0]
				Button:
				    font_size: str(0.01875 * app.width) + 'sp'
					size_hint: (None,None)
					height: dp(0.125*app.height)
					width: dp(0.06375*app.width)
					background_color: hex('#F4433600')
					center: self.parent.center
					pos: self.parent.pos
					on_press: root.next_screen()
					BoxLayout:
						padding: 0
						size: self.parent.size
						pos: self.parent.pos
						Image:
							source: "./asmcnc/apps/systemTools_app/img/back_to_lobby.png"
							center_x: self.parent.center_x
							y: self.parent.y
							size: self.parent.width, self.parent.height
							allow_stretch: True 
"""
)


class AlarmScreen5(Screen):
    return_to_screen = "alarm_1"
    default_font_size = get_scaled_width(30)

    def __init__(self, **kwargs):
        super(AlarmScreen5, self).__init__(**kwargs)
        self.a = kwargs["alarm_manager"]
        self.alarm_title.text = self.a.l.get_bold("Alarm: Job cancelled.")
        self.icon.source = "./asmcnc/core_UI/sequence_alarm/img/alarm_icon.png"
        self.description_label.text = self.a.l.get_str(
            "For safety reasons, SmartBench will now cancel the job."
        )
        self.next_button.text = self.a.l.get_str("More info")
        self.update_font_size(self.next_button)

    def on_pre_enter(self):
        if self.a.support_sequence:
            self.next_button.opacity = 0
            self.next_button.disabled = True
        elif self.return_to_screen == "alarm_1":
            self.next_button.opacity = 1
            self.next_button.disabled = False
        else:
            self.next_button.opacity = 0
            self.next_button.disabled = True

    def next_screen(self):
        self.a.exit_sequence()

    def prev_screen(self):
        if self.a.support_sequence:
            self.a.sm.current = "alarm_4"
        else:
            self.a.sm.current = self.return_to_screen

    def more_info(self):
        self.a.sm.get_screen("alarm_3").for_support = False
        self.a.sm.current = "alarm_3"

    def update_font_size(self, value):
        text_length = self.a.l.get_text_length(value.text)
        if text_length < 12:
            value.font_size = self.default_font_size
        elif text_length > 15:
            value.font_size = self.default_font_size - 0.0025 * Window.width
        if text_length > 20:
            value.font_size = self.default_font_size - 0.005 * Window.width
        if text_length > 22:
            value.font_size = self.default_font_size - 0.00625 * Window.width
