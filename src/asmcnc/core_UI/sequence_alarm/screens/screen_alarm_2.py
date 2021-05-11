'''
Created on 31 March 2021
@author: Letty
'''
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock


# Kivy UI builder:
Builder.load_string("""
<AlarmScreen2>:
	alarm_title : alarm_title
	icon_container : icon_container
	icon_left : icon_left
	icon_right : icon_right
	description_label : description_label
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
		height: dp(480)
		width: dp(800)
		# Alarm header
		BoxLayout: 
			padding: [15,0,15,0]
			spacing: 0
			size_hint: (None, None)
			height: dp(50)
			width: dp(800)
			orientation: 'horizontal'
			Label:
				id: alarm_title
				size_hint: (None, None)
				font_size: '30sp'
				color: [0,0,0,1]
				markup: True
				halign: 'left'
				height: dp(50)
				width: dp(770)
				text_size: self.size
		# Red underline
		BoxLayout: 
			padding: [10,0,10,0]
			spacing: 0
			size_hint: (None, None)
			height: dp(5)
			width: dp(800)
			Image:
				id: red_underline
				source: "./asmcnc/skavaUI/img/red_underline.png"
				center_x: self.parent.center_x
				y: self.parent.y
				size: self.parent.width, self.parent.height
				allow_stretch: True
		# Image and text
		BoxLayout: 
			padding: [0,35,0,0]
			spacing: 0
			size_hint: (None, None)
			height: dp(283)
			width: dp(800)
			orientation: 'vertical'
			BoxLayout: 
				id: icon_container
				padding: [190,30,218.5,0]
				spacing: 208.5
				size_hint: (None, None)
				height: dp(130)
				width: dp(800)
				orientation: 'horizontal'    
				Image:
					id: icon_left
					allow_stretch: False
					size_hint: (None, None)
					height: dp(100)
					width: dp(120)
				Image:
					id: icon_right
					allow_stretch: False
					size_hint: (None, None)
					height: dp(100)
					width: dp(63)
			BoxLayout:
				id: description container
				padding: [30,0,30,0]
				spacing: 0
				size_hint: (None, None)
				height: dp(118)
				width: dp(800)
				Label:
					id: description_label
					font_size: '20sp'
					color: [0,0,0,1]
					markup: True
					halign: 'center'
					valign: 'middle'
					text_size: self.size
					size: self.parent.size
		# Buttons
		BoxLayout: 
			padding: [10,0,10,10]
			size_hint: (None, None)
			height: dp(142)
			width: dp(800)
			orientation: 'horizontal'
			BoxLayout: 
				size_hint: (None, None)
				height: dp(132)
				width: dp(244.5)
				padding: [0, 0, 184.5, 0]
				Button:
					size_hint: (None,None)
					height: dp(52)
					width: dp(60)
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
				height: dp(132)
				width: dp(291)
				padding: [0,0,0,52]
				Button:
					background_normal: "./asmcnc/apps/warranty_app/img/next.png"
					background_down: "./asmcnc/apps/warranty_app/img/next.png"
					border: [dp(14.5)]*4
					size_hint: (None,None)
					width: dp(291)
					height: dp(79)
					on_press: root.next_screen()
					text: 'Next...'
					font_size: '30sp'
					color: hex('#f9f9f9ff')
					markup: True
					center: self.parent.center
					pos: self.parent.pos
			BoxLayout: 
				size_hint: (None, None)
				height: dp(132)
				width: dp(244.5)
				padding: [193.5, 0, 0, 0]
""")

class AlarmScreen2(Screen):
	
	def __init__(self, **kwargs):
		super(AlarmScreen2, self).__init__(**kwargs)
		self.a=kwargs['alarm_manager']

		self.alarm_title.text = "[b]" + "Alarm: Record details" + "[/b]"
		self.icon_left.source = "./asmcnc/core_UI/sequence_alarm/img/camera_dark.png"
		self.icon_right.source = "./asmcnc/core_UI/sequence_alarm/img/usb_empty_dark.png"
		self.description_label.text = "Record the alarm report for diagnosis and support. Take a photo of the report on the next screen, or insert a USB stick now to download it."

	def next_screen(self):
		self.a.sm.get_screen('alarm_3').for_support = True
		self.a.sm.current = 'alarm_3'

	def prev_screen(self):
		if self.a.support_sequence:
			self.a.sm.current = 'alarm_1'
		else:
			self.a.sm.get_screen('alarm_3').for_support = False
			self.a.sm.current = 'alarm_3'
