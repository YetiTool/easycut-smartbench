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

	status_container : status_container
	title_label : title_label
	instructions_label : instructions_label
	cant_use_web_label : cant_use_web_label
	contact_us_at_support : contact_us_at_support
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
				
			Label:
				id: title_label
				font_size: '30sp'
				# text: "[color=333333ff]SmartBench Warranty Registration[/color]"
				text_size: self.size
				valign: 'bottom'
				halign: 'center'
				markup: 'true'
				bold: True
				color: hex('#333333ff')

			BoxLayout:
				orientation: 'vertical'
				width: dp(800)
				height: dp(200)
				padding: [20, 20, 20, 0]
				size_hint: (None,None)
				spacing: 0

				Label:
					id: instructions_label
					size_hint_y: 0.3
					font_size: '20sp'
					# text: "[color=333333ff]To submit your details and receive your activation code, go to[/color]"
					text_size: self.size
					valign: 'middle'
					halign: 'center'
					markup: True
					color: hex('#333333ff')

				BoxLayout:
					orientation: 'horizontal'
					width: dp(800)
					height: dp(132)
					# padding: [20, 0]
					size_hint: (None,None)
					spacing: 0

	                BoxLayout:
	                    padding: [10,0,0,0]
						width: dp(162)
						height: dp(132)
						size_hint: (None,None)
	                    Image:
	                        source: "./asmcnc/apps/warranty_app/img/registration-qr-code.png"
	                        center_x: self.parent.center_x
	                        y: self.parent.y
	                        size: self.parent.width, self.parent.height
	                        allow_stretch: True

					BoxLayout:
						orientation: 'vertical'
						width: dp(598)
						height: dp(132)
						padding: [0,0,0,0]
						size_hint: (None,None)

						Label:
							size_hint_y: 0.4
							font_size: '23sp'
							text: "[color=333333ff]https://www.yetitool.com/support/Register-Your-Product[/color]"
							text_size: self.size
							valign: 'middle'
							halign: 'left'
							markup: 'true'
							multiline: True
							color: hex('#333333ff')
						
						Label:
							id: cant_use_web_label
							size_hint_y: 0.3
							font_size: '20sp'
							# text: "[color=333333ff]Can't use the web form?"
							text_size: self.size
							valign: 'bottom'
							halign: 'left'
							markup: 'true'
							color: hex('#333333ff')

						Label:
							id: contact_us_at_support
							size_hint_y: 0.3
							font_size: '20sp'
							# text: "[color=333333ff]Contact us at https://www.yetitool.com/support[/color]"
							text_size: self.size
							valign: 'middle'
							halign: 'left'
							markup: 'true'
							color: hex('#333333ff')

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
	                    background_normal: "./asmcnc/skavaUI/img/next.png"
	                    background_down: "./asmcnc/skavaUI/img/next.png"
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
				padding: [10, 0, 0, 10]
				size_hint: (None,None)
				width: dp(70)
				height: dp(62)

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

""")

class WarrantyScreen2(Screen):

	def __init__(self, **kwargs):
		super(WarrantyScreen2, self).__init__(**kwargs)
		self.wm=kwargs['warranty_manager']
		self.m=kwargs['machine']
		self.l=kwargs['localization']
		
		self.status_bar_widget = widget_status_bar.StatusBar(screen_manager=self.wm.sm, machine=self.m)
		self.status_container.add_widget(self.status_bar_widget)
		self.status_bar_widget.cheeky_color = '#1976d2'

		self.update_strings()

	def next_screen(self):
		self.wm.sm.current = 'warranty_3'

	def go_back(self):
		self.wm.sm.current = 'warranty_1'
	
	def update_strings(self):
		self.title_label.text = self.l.get_str("SmartBench Warranty Registration")
		self.instructions_label.text = self.l.get_str("To submit your details and receive your activation code, go to")
		self.cant_use_web_label.text = self.l.get_str("Can't use the web form?")
		self.contact_us_at_support.text = self.l.get_str("Contact us at https://www.yetitool.com/support")
		self.next_button.text = self.l.get_str("Next") + "..."

