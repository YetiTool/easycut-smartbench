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
		height: app.get_scaled_height(480.0)
		width: app.get_scaled_width(800.0)
		# Alarm header
		BoxLayout: 
			padding: app.get_scaled_tuple([15.0, 0.0, 15.0, 0.0])
			spacing: 0
			size_hint: (None, None)
			height: app.get_scaled_height(50.0)
			width: app.get_scaled_width(800.0)
			orientation: 'horizontal'
			Label:
				id: alarm_title
				size_hint: (None, None)
				font_size: app.get_scaled_sp('30.0sp')
				color: [0,0,0,1]
				markup: True
				halign: 'left'
				height: app.get_scaled_height(50.0)
				width: app.get_scaled_width(770.0)
				text_size: self.size
		# Red underline
		BoxLayout: 
			padding: app.get_scaled_tuple([10.0, 0.0, 10.0, 0.0])
			spacing: 0
			size_hint: (None, None)
			height: app.get_scaled_height(5.0)
			width: app.get_scaled_width(800.0)
			Image:
				id: red_underline
				source: "./asmcnc/skavaUI/img/red_underline.png"
				center_x: self.parent.center_x
				y: self.parent.y
				size: self.parent.width, self.parent.height
				allow_stretch: True
		# Image and text
		BoxLayout: 
			padding: app.get_scaled_tuple([0.0, 35.0, 0.0, 0.0])
			spacing: 0
			size_hint: (None, None)
			height: app.get_scaled_height(283.0)
			width: app.get_scaled_width(800.0)
			orientation: 'vertical'
			BoxLayout: 
				id: icon_container
				padding: app.get_scaled_tuple([190.0, 30.0, 218.5, 0.0])
				spacing: app.get_scaled_width(208.5)
				size_hint: (None, None)
				height: app.get_scaled_height(130.0)
				width: app.get_scaled_width(800.0)
				orientation: 'horizontal'    
				Image:
					id: icon_left
					allow_stretch: False
					size_hint: (None, None)
					height: app.get_scaled_height(100.0)
					width: app.get_scaled_width(120.0)
				Image:
					id: icon_right
					allow_stretch: False
					size_hint: (None, None)
					height: app.get_scaled_height(100.0)
					width: app.get_scaled_width(63.0)
			BoxLayout:
				id: description container
				padding: app.get_scaled_tuple([30.0, 0.0, 30.0, 0.0])
				spacing: 0
				size_hint: (None, None)
				height: app.get_scaled_height(118.0)
				width: app.get_scaled_width(800.0)
				Label:
					id: description_label
					font_size: app.get_scaled_sp('20.0sp')
					color: [0,0,0,1]
					markup: True
					halign: 'center'
					valign: 'middle'
					text_size: self.size
					size: self.parent.size
		# Buttons
		BoxLayout: 
			padding: app.get_scaled_tuple([10.0, 0.0, 10.0, 10.0])
			size_hint: (None, None)
			height: app.get_scaled_height(142.0)
			width: app.get_scaled_width(800.0)
			orientation: 'horizontal'
			BoxLayout: 
				size_hint: (None, None)
				height: app.get_scaled_height(132.0)
				width: app.get_scaled_width(244.5)
				padding: app.get_scaled_tuple([0.0, 0.0, 184.5, 0.0])
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
				height: app.get_scaled_height(132.0)
				width: app.get_scaled_width(291.0)
				padding: app.get_scaled_tuple([0.0, 0.0, 0.0, 52.0])
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
				height: app.get_scaled_height(132.0)
				width: app.get_scaled_width(244.5)
				padding: app.get_scaled_tuple([193.5, 0.0, 0.0, 0.0])
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
