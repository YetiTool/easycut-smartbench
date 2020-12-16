'''
Created on nov 2020
@author: Ollie
Text input # on_enter: root.sucessful_activation
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

<WarrantyScreen4>:

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
				height: dp(100)
				width: dp(800)
				padding: (0,30,0,0)
				
				Label:
					font_size: '32sp'
					text: "[color=000000] Please enter your activation code [/color]"
					text_size: self.size
					valign: 'middle'
					halign: 'center'
					markup: 'true'
					bold: True

				BoxLayout:
					orientation: 'vertical'
					padding: (325,60,0,180)
					height: dp(290)
					width: dp(500) 
					size_hint: (None,None)
				
					TextInput: 
						id: activationcode
						valign: 'middle'
						halign: 'center'
						height: dp(50)
						width: dp(200) 
						text_size: self.size
						font_size: '20sp'
						markup: True
						multiline: False
						text: ''
						# on_enter: root.next_screen()
						
					

			BoxLayout:
				size_hint_y: 0.20
				size: self.size
				pos: self.size

				BoxLayout:
					orientation: 'vertical'
					padding: [200, 0, 0, 10]
					size_hint: (None,None)
					width: dp(59)
					height: dp(50)

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

class WarrantyScreen4(Screen):

	activationcode = ObjectProperty()

	def __init__(self, **kwargs):
		super(WarrantyScreen4, self).__init__(**kwargs)
		self.sm=kwargs['screen_manager']
		self.m=kwargs['machine']
		
		self.status_bar_widget = widget_status_bar.StatusBar(screen_manager=self.sm, machine=self.m)
		self.status_container.add_widget(self.status_bar_widget)
		self.status_bar_widget.cheeky_color = '#1976d2'
	
	def next_screen(self):
		self.sm.current = 'warranty_5'
