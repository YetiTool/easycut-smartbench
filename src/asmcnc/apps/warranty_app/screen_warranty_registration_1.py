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

	canvas:
		Color:
			rgba: hex('##e5e5e5')
		Rectangle:
			size: self.size
			pos: self.pos

	BoxLayout: 
		orientation: 'vertical'

		BoxLayout:
			orientation: 'vertical'
			id: status_container 
			pos: self.pos
			size: self.pos 
			size_hint_y: 0.08

		BoxLayout:
			size_hint_y: 0.9
			orientation: 'vertical'
			size: self.parent.size
			pos: self.parent.pos

			BoxLayout:
				orientation: 'vertical'
				padding: (0,30,0,0)
				
				Label:
					font_size: '32sp'
					text: "[color=000000] SmartBench Warranty Registration [/color]"
					text_size: self.size
					width: dp(800)
					height: dp(125)
					valign: 'middle'
					halign: 'center'
					markup: 'true'
					bold: True
				Label:
					font_size: '24sp'
					text: "[color=000000] Thank you for purchasing SmartBench. [/color]"
					text_size: self.size
					width: dp(800)
					height: dp(75)
					valign: 'middle'
					halign: 'center'
					markup: 'true'

				Label:
					font_size: '24sp'
					text: "[color=000000] Please follow the next steps to complete your warranty registration process. [/color]"
					text_size: self.size
					width: dp(800)
					height: dp(75)
					valign: 'middle'
					halign: 'center'
					markup: 'true'
				
				Label:
					font_size: '24sp'
					text: "[color=000000] It will only a take a few minutes. [/color]"
					text_size: self.size
					width: dp(800)
					height: dp(75)
					valign: 'middle'
					halign: 'center'
					markup: 'true'

				BoxLayout:
					orientation: 'vertical'
					width: dp(546)
					height: dp(79)
					padding: (254,0,0,0)
					size_hint: (None,None)

					Button:
						background_color: hex('##1C00ff00')
						width: dp(291)
						height: dp(79)
						on_press: root.next_screen()
						size: self.parent.size
						pos: self.parent.pos
						

						BoxLayout:
							size: self.parent.size
							pos: self.parent.pos
							Image: 
								source: "./asmcnc/apps/warranty_app/img/next.png"
								size: self.parent.width, self.parent.height
								allow_stretch: True 
								
							

			BoxLayout:
				size_hint_y: 0.20
				size: self.size
				pos: self.size
		


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

	



