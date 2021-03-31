'''
Created on 31 March 2021
@author: Letty
'''
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock

# ALARM_CODES = {

#     "ALARM:1" : "The machine's position was likely lost. Re-homing is highly recommended.",
#     "ALARM:2" : "The requested motion target exceeds the machine's travel.",
#     "ALARM:3" : "Machine was reset while in motion and cannot guarantee position. Lost steps are likely. Re-homing is recommended.",
#     "ALARM:4" : "Probe fail. Probe was not in the expected state before starting probe cycle.",
#     "ALARM:5" : "Probe fail. Probe did not contact the workpiece within the programmed travel.",
#     "ALARM:6" : "Homing fail. Reset during active homing cycle.",
#     "ALARM:7" : "Homing fail. Safety switch was activated during the homing cycle.",
#     "ALARM:8" : "Homing fail. Cycle failed to clear limit switch when pulling off.",
#     "ALARM:9" : "Homing fail. Could not find limit switch within search distance.",

# }

# Kivy UI builder:
Builder.load_string("""

<AlarmScreen1>:

	alarm_title : alarm_title
	icon_container : icon_container
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
				text: '[b]Alarm![/b]'
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
				padding: [335,0,0,0]
				size_hint: (None, None)
				height: dp(130)
				width: dp(800)       
				Image:
					id: icon
					source: "./asmcnc/core_UI/sequence_alarm/img/alarm_icon.png"
					center_x: self.parent.center_x
					y: self.parent.y
					size: self.parent.width, self.parent.height
					allow_stretch: True
					size_hint: (None, None)
					height: dp(130)
					width: dp(130)


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
					on_press: root.go_back()
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
				Button:
					size_hint: (None,None)
					height: dp(60)
					width: dp(51)
					background_color: hex('#F4433600')
					center: self.parent.center
					pos: self.parent.pos
					on_press: root.exit_app()
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
""")

class AlarmScreen1(Screen):

	# this is the screen's description
	# alarm_description = StringProperty()

	
	def __init__(self, **kwargs):
		super(AlarmScreen1, self).__init__(**kwargs)
		self.sm=kwargs['screen_manager']
		self.m=kwargs['machine']