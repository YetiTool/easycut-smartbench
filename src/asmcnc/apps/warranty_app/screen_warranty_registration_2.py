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
					size_hint_y: 0.3
					font_size: '20sp'
					text: "[color=333333ff]To submit your details and receive your activation code, go to[/color]"
					text_size: self.size
					valign: 'middle'
					halign: 'center'
					markup: 'true'

				Label:
					size_hint_y: 0.3
					font_size: '26sp'
					text: "[color=333333ff]https://www.yetitool.com/registration[/color]"
					text_size: self.size
					valign: 'top'
					halign: 'center'
					markup: 'true'
					multiline: True
				
				Label:
					size_hint_y: 0.2
					font_size: '20sp'
					text: "[color=333333ff]Can't use web form?"
					text_size: self.size
					valign: 'middle'
					halign: 'center'
					markup: 'true'

				Label:
					size_hint_y: 0.2
					font_size: '20sp'
					text: "[color=333333ff]Contact us at https://www.yetitool.com/support[/color]"
					text_size: self.size
					valign: 'top'
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

	def go_back(self):
		self.sm.current = 'warranty_1'
	



