'''
Created on nov 2020
@author: Ollie
'''

from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
import sys, os
from asmcnc.skavaUI import widget_status_bar
Builder.load_string("""

<WarrantyScreen5>:
				
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

			BoxLayout:
				orientation: 'vertical'
				width: dp(800)
				height: dp(200)
				padding: [dp(20), 0]
				size_hint: (None,None)

				Label:
					font_size: '30sp'
					text: "[color=333333ff]You have sucessfully completed your warranty registration.[/color]"
					text_size: self.size
					valign: 'top'
					halign: 'center'
					markup: 'true'
					bold: True


			BoxLayout:
				orientation: 'vertical'
				width: dp(800)
				height: dp(80)
				padding: [dp(254.5),0,dp(254.5),dp(1)]
				size_hint: (None,None)

                BoxLayout: 
                    size_hint: (None, None)
                    height: dp(79)
                    width: dp(291)
                    
					Button:
	                    background_normal: "./asmcnc/apps/warranty_app/img/next.png"
	                    background_down: "./asmcnc/apps/warranty_app/img/next.png"
	                    border: [dp(14.5)]*4
						size_hint: (None,None)
						width: dp(291)
						height: dp(79)
						on_press: root.next_screen()
						text: 'Get started!'
						font_size: '20sp'
						color: hex('#f9f9f9ff')
						markup: True
	                    center: self.parent.center
	                    pos: self.parent.pos
								
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
					on_press: root.go_back()

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

class WarrantyScreen5(Screen):

	def __init__(self, **kwargs):
		super(WarrantyScreen5, self).__init__(**kwargs)
		self.sm=kwargs['screen_manager']
		self.m=kwargs['machine']
		
		self.status_bar_widget = widget_status_bar.StatusBar(screen_manager=self.sm, machine=self.m)
		self.status_container.add_widget(self.status_bar_widget)
		self.status_bar_widget.cheeky_color = '#1976d2'

	def next_screen(self):
		self.sm.current = 'safety'

	def go_back(self):
		self.sm.current = 'warranty_4'



