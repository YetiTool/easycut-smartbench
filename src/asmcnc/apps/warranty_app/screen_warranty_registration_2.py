'''
Created on nov 2020
@author: Ollie
'''

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.textinput import TextInput
from asmcnc.skavaUI import widget_status_bar
from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.gridlayout import GridLayout
import sys, os
Builder.load_string("""

<WarrantyScreen2>:

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
			
			Label:
				font_size: '32dp'
				text: "[color=000000] SmartBench warranty registration. [/color]"
				text_size: self.size
				valign: 'middle'
				halign: 'center'
				markup: 'true'
				bold: True
	
			BoxLayout:
				orientation: 'vertical'
				
				Label:
					font_size: '22dp'
					text: "[color=000000] To submit your details and receive your activation code, go to: [/color]"
					text_size: self.size
					valign: 'middle'
					halign: 'center'
					markup: 'true'

				BoxLayout:
					orientaion: 'vertical'

					Label:
						font_size: '26dp'
						text: "[color=000000] https://www.yetitool.com/registration [/color]"
						text_size: self.size
						valign: 'middle'
						halign: 'center'
						markup: 'true'


				
			BoxLayout:
				padding: (0,0,0,30)
				height: dp(30)
				
				Label:
					font_size: '22dp'
					text: "[color=000000] Can't use web form?                                                                                                                       https://www.yetitool.com/support or call +44 1275 217060[/color]"
					text_size: self.size
					valign: 'middle'
					halign: 'center'
					markup: 'true'

			
	
		BoxLayout:
			orientation: 'vertical'	
			width: dp(402)
			height: dp(120)	
			size_hint: (None,None)
			padding: (256,0,0,20)
			
			

			Button:
				background_color: hex('##1C00ff00')
				width: dp(291)
				height: dp(79)
				on_press: root.next_screen()
				size_hint: (None,None)				
				pos: self.parent.pos 
				

				BoxLayout:
					orientation: 'vertical'
					width: dp(291)
					height: dp(79)
					padding: (0,0,0,0)
					size_hint: (None,None)
					size: self.parent.size
					pos: self.parent.pos 
					
					Image: 
						source: "./asmcnc/apps/warranty_app_2/img/next.png"
						size: self.parent.width, self.parent.height
						pos: self.parent.pos
						allow_stretch: True 


		

		BoxLayout:
			orientation: 'vertical'
			padding: [0, 0, 0, 0]
			size_hint: (None,None)
			width: dp(69)
			height: dp(60)

			Button:
				orientation: 'horizontal'
				background_color: hex('#1C00ff00')
				size_hint: (None,None)
				width: dp(59)
				height: dp(50)


				BoxLayout:
					size_hint: (None,None)
					padding: [10, 0, 0, 10]
					width: dp(59)
					height: dp(50)


					Image:
						source: "./asmcnc/apps/warranty_app_2/img/exit.png"
						size: self.parent.width, self.parent.height
						allow_stretch: True 
		


""")

class WarrantyScreen2(Screen):

	def __init__(self, **kwargs):
		super(WarrantyScreen2, self).__init__(**kwargs)
		self.sm=kwargs['screen_manager']
		self.m=kwargs['machine']
		
		self.status_bar_widget = widget_status_bar.StatusBar(screen_manager=self.sm, machine=self.m)
		self.status_container.add_widget(self.status_bar_widget)
		self.status_bar_widget.cheeky_color = '#1976d2'

	def next_screen(self):
		self.sm.current = 'warranty_3'
	



