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
				
	status_container : status_container
	success_label : success_label
	next_button : next_button

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
					id: success_label
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
				padding: [dp(254.5),0,dp(254.5),0]
				size_hint: (None,None)

                BoxLayout: 
                    size_hint: (None, None)
                    height: dp(79)
                    width: dp(291)
                    
					Button:
						id: next_button
	                    background_normal: "./asmcnc/apps/warranty_app/img/next.png"
	                    background_down: "./asmcnc/apps/warranty_app/img/next.png"
	                    border: [dp(14.5)]*4
						size_hint: (None,None)
						width: dp(291)
						height: dp(79)
						on_press: root.next_screen()
						text: 'Get started!'
						font_size: '30sp'
						color: hex('#f9f9f9ff')
						markup: True
	                    center: self.parent.center
	                    pos: self.parent.pos
								
			BoxLayout:
				orientation: 'vertical'
				padding: [10, 0, 0, 10]
				size_hint: (None,None)
				width: dp(70)
				height: dp(62)

""")

class WarrantyScreen5(Screen):

	def __init__(self, **kwargs):
		super(WarrantyScreen5, self).__init__(**kwargs)
		self.wm=kwargs['warranty_manager']
		self.m=kwargs['machine']
		self.l=kwargs['localization']
		
		self.status_bar_widget = widget_status_bar.StatusBar(screen_manager=self.wm.sm, machine=self.m)
		self.status_container.add_widget(self.status_bar_widget)
		self.status_bar_widget.cheeky_color = '#1976d2'

		self.update_strings()

	def next_screen(self):
		self.wm.exit_app()

	def go_back(self):
		self.wm.sm.current = 'warranty_4'

	def update_strings(self):
		self.success_label.text = self.l.get_str("You have sucessfully completed your warranty registration.")
		self.next_button.text = self.l.get_str("Next") + "..."
