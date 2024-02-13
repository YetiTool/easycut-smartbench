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
		padding:dp(0)
		spacing: 0
		size_hint: (None, None)
		height: dp(app.get_scaled_height(480))
		width: dp(app.get_scaled_width(800))
		# Alarm header
		BoxLayout: 
			padding:(dp(app.get_scaled_width(15)),dp(0),dp(app.get_scaled_width(15)),dp(0))
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
			padding:(dp(app.get_scaled_width(10)),dp(0),dp(app.get_scaled_width(10)),dp(0))
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
			padding:(dp(0),dp(app.get_scaled_height(35)),dp(0),dp(0))
			spacing: 0
			size_hint: (None, None)
			height: dp(app.get_scaled_height(283))
			width: dp(app.get_scaled_width(800))
			orientation: 'vertical'
			BoxLayout: 
				id: icon_container
				padding:(dp(app.get_scaled_width(190)),dp(app.get_scaled_height(30)),dp(app.get_scaled_width(190)),dp(0))
				spacing:0.260625*app.width
				size_hint: (None, None)
				height: dp(app.get_scaled_height(130))
				width: dp(app.get_scaled_width(800))
				orientation: 'horizontal'    
				Image:
					id: icon_left
					allow_stretch: False
					size_hint: (None, None)
					height: dp(app.get_scaled_height(100))
					width: dp(app.get_scaled_width(120))
				Image:
					id: icon_right
					allow_stretch: False
					size_hint: (None, None)
					height: dp(app.get_scaled_height(100))
					width: dp(app.get_scaled_width(63))
			BoxLayout:
				id: description container
				padding:(dp(app.get_scaled_width(30)),dp(0),dp(app.get_scaled_width(30)),dp(0))
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
			padding:(dp(app.get_scaled_width(10)),dp(0),dp(app.get_scaled_width(10)),dp(app.get_scaled_height(10)))
			size_hint: (None, None)
			height: dp(app.get_scaled_height(142))
			width: dp(app.get_scaled_width(800))
			orientation: 'horizontal'
			BoxLayout: 
				size_hint: (None, None)
				height: dp(app.get_scaled_height(132))
				width: dp(app.get_scaled_width(244.5))
				padding:(dp(0),dp(0),dp(app.get_scaled_width(184.5)),dp(0))
				Button:
				    font_size: str(get_scaled_width(15)) + 'sp'
					size_hint: (None,None)
					height: dp(app.get_scaled_height(52))
					width: dp(app.get_scaled_width(60))
					background_color: hex('#F4433600')
					center: self.parent.center
					pos: self.parent.pos
					on_press: root.prev_screen()
					BoxLayout:
						padding:dp(0)
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
				height: dp(app.get_scaled_height(132))
				width: dp(app.get_scaled_width(291))
				padding:(dp(0),dp(0),dp(0),dp(app.get_scaled_height(52)))
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
				padding:(dp(app.get_scaled_width(193.5)),dp(0),dp(0),dp(0))
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
