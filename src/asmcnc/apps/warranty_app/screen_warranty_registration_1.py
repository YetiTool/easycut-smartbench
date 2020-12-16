'''
Created on nov 2020
@author: Ollie
'''

from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
import sys, os
from asmcnc.skavaUI import widget_status_bar
Builder.load_string("""

<WarrantyScreen1>:

	status_container:status_container 

	BoxLayout: 
		size_hint: (None,None)
		width: dp(800)
		height: dp(480)
		orientation: 'vertical'

		canvas:
			Color:
				rgba: hex('##e5e5e5')
			Rectangle:
				size: self.size
				pos: self.pos

		BoxLayout:
			id: status_container 
			size_hint_y: 0.08

		BoxLayout:
			size_hint_y: 0.92
			orientation: 'vertical'
				
			Label:
				font_size: '32sp'
				text: "[color=000000] SmartBench Warranty Registration [/color]"
				text_size: self.size
				valign: 'bottom'
				halign: 'center'
				markup: 'true'
				bold: True

			BoxLayout:
				orientation: 'vertical'
				width: dp(800)
				height: dp(200)
				padding: 20
				size_hint: (None,None)
				Label:
					size_hint_y: 0.25
					font_size: '24sp'
					text: "[color=000000] Thank you for purchasing SmartBench. [/color]"
					text_size: self.size
					valign: 'middle'
					halign: 'center'
					markup: 'true'

				Label:
					size_hint_y: 0.5
					font_size: '24sp'
					text: "[color=000000] Please follow the next steps to complete your warranty registration process. [/color]"
					text_size: self.size
					valign: 'middle'
					halign: 'center'
					markup: 'true'
					multiline: True
				
				Label:
					size_hint_y: 0.25
					font_size: '24sp'
					text: "[color=000000] It will only a take a few minutes. [/color]"
					text_size: self.size
					valign: 'middle'
					halign: 'center'
					markup: 'true'

			BoxLayout:
				orientation: 'vertical'
				width: dp(800)
				height: dp(80)
				padding: [dp(254.5),0,dp(254.5),dp(1)]
				size_hint: (None,None)

				Button:
					background_normal: ''
					size_hint: (None,None)
					width: dp(291)
					height: dp(79)
					on_press: root.next_screen()

					BoxLayout:
						size: self.parent.size
						pos: self.parent.pos
						Image: 
							source: "./asmcnc/apps/warranty_app/img/next.png"
							size: self.parent.width, self.parent.height
							allow_stretch: True
								
			BoxLayout:
				orientation: 'vertical'
				padding: [10, 0, 0, 10]
				size_hint: (None,None)
				width: dp(69)
				height: dp(60)

				Button:
					background_normal: ''
					size_hint: (None,None)
					width: dp(59)
					height: dp(50)

					BoxLayout:
						size: self.parent.size
						pos: self.parent.pos

						Image:
							source: "./asmcnc/apps/warranty_app/img/exit.png"
							size: self.parent.width, self.parent.height
							allow_stretch: True 
							size: self.parent.size
							pos: self.parent.pos

		


""")

class WarrantyScreen1(Screen):

	def __init__(self, **kwargs):
		super(WarrantyScreen1, self).__init__(**kwargs)
		self.sm=kwargs['screen_manager']
		self.m=kwargs['machine']
		
		self.status_bar_widget = widget_status_bar.StatusBar(screen_manager=self.sm, machine=self.m)
		self.status_container.add_widget(self.status_bar_widget)
		self.status_bar_widget.cheeky_color = '#1976d2'

	def next_screen(self):
		self.sm.current = 'warranty_2'

	



