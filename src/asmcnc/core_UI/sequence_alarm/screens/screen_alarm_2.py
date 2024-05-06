"""
Created on 31 March 2021
@author: Letty
"""
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock

Builder.load_string(
    """
<AlarmScreen2>:
	alarm_title : alarm_title
	icon_container : icon_container
	icon_left : icon_left
	icon_right : icon_right
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
				padding:[dp(0.2375)*app.width, dp(0.0625)*app.height, dp(0.273125)*app.width, 0]
				spacing:0.260625*app.width
				size_hint: (None, None)
				height: dp(0.270833333333*app.height)
				width: dp(1.0*app.width)
				orientation: 'horizontal'    
				Image:
					id: icon_left
					allow_stretch: False
					size_hint: (None, None)
					height: dp(0.208333333333*app.height)
					width: dp(0.15*app.width)
				Image:
					id: icon_right
					allow_stretch: False
					size_hint: (None, None)
					height: dp(0.208333333333*app.height)
					width: dp(0.07875*app.width)
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
				padding:[dp(0.241875)*app.width, 0, 0, 0]
"""
)


class AlarmScreen2(Screen):
    def __init__(self, **kwargs):
        super(AlarmScreen2, self).__init__(**kwargs)
        self.a = kwargs["alarm_manager"]
        self.alarm_title.text = self.a.l.get_bold("Alarm: Record details")
        self.icon_left.source = "./asmcnc/core_UI/sequence_alarm/img/camera_dark.png"
        self.icon_right.source = (
            "./asmcnc/core_UI/sequence_alarm/img/usb_empty_dark.png"
        )
        self.description_label.text = self.a.l.get_str(
            "Record the alarm report for diagnosis and support. Take a photo of the report on the next screen, or insert a USB stick now to download it."
        )
        self.next_button.text = self.a.l.get_str("Next") + "..."

    def next_screen(self):
        self.a.sm.get_screen("alarm_3").for_support = True
        self.a.sm.current = "alarm_3"

    def prev_screen(self):
        if self.a.support_sequence:
            self.a.sm.current = "alarm_1"
        else:
            self.a.sm.get_screen("alarm_3").for_support = False
            self.a.sm.current = "alarm_3"
