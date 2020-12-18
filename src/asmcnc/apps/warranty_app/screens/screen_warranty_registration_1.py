'''
Created on nov 2020
@author: Ollie
'''

from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
import sys, os
from asmcnc.skavaUI import widget_status_bar
from asmcnc.apps.warranty_app.screens import popup_warranty

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
				font_size: '30sp'
				text: "[color=333333ff]SmartBench Warranty Registration[/color]"
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
					font_size: '20sp'
					text: "[color=333333ff]Thank you for purchasing SmartBench.[/color]"
					text_size: self.size
					valign: 'bottom'
					halign: 'center'
					markup: 'true'

				Label:
					size_hint_y: 0.5
					font_size: '20sp'
					text: "[color=333333ff]Please follow the next steps to complete your warranty registration process.[/color]"
					text_size: self.size
					valign: 'middle'
					halign: 'center'
					markup: 'true'
					multiline: True
				
				Label:
					size_hint_y: 0.25
					font_size: '20sp'
					text: "[color=333333ff]It will only a take a few minutes.[/color]"
					text_size: self.size
					valign: 'top'
					halign: 'center'
					markup: 'true'

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
				orientation: 'vertical'
				padding: [dp(738), 0, dp(10), dp(10)]
				size_hint: (None,None)
				width: dp(800)
				height: dp(62)

                Button:
                    size_hint: (None,None)
                    height: dp(52)
                    width: dp(52)
                    background_color: hex('##e5e5e5')
                    background_normal: ''
                    center: self.parent.center
                    pos: self.parent.pos
                    on_press: root.quit_to_console()
                    # BoxLayout:
                    #     padding: 0
                    #     size: self.parent.size
                    #     pos: self.parent.pos
                        # Image:
                        #     source: "./asmcnc/apps/warranty_app/img/quit_to_console.png"
                        #     center_x: self.parent.center_x
                        #     y: self.parent.y
                        #     size: self.parent.width, self.parent.height
                        #     allow_stretch: True

		


""")

class WarrantyScreen1(Screen):

	def __init__(self, **kwargs):
		super(WarrantyScreen1, self).__init__(**kwargs)
		self.wm=kwargs['warranty_manager']
		self.m=kwargs['machine']
		
		self.status_bar_widget = widget_status_bar.StatusBar(screen_manager=self.wm.sm, machine=self.m)
		self.status_container.add_widget(self.status_bar_widget)
		self.status_bar_widget.cheeky_color = '#1976d2'

	def next_screen(self):
		self.wm.sm.current = 'warranty_2'

	def quit_to_console(self):
		popup_warranty.QuitToConsoleWarranty(self.wm.sm)
	



