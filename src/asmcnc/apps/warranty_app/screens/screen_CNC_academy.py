'''
Created 15th September 2021
@author: Letty
'''

from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
import sys, os
from asmcnc.skavaUI import widget_status_bar
Builder.load_string("""
<CNCAcademyScreen>:
				
	status_container : status_container
	cnc_academy_info : cnc_academy_info
	qr_code_container : qr_code_container
	qr_code_image : qr_code_image
	cnc_academy_logo_container : cnc_academy_logo_container
	cnc_academy_logo : cnc_academy_logo
	url_label : url_label
	next_button : next_button

	BoxLayout: 
		size_hint: (None,None)
		width: dp(800)
		height: dp(480)
		orientation: 'vertical'
		canvas:
			Color:
				rgba: hex('#e5e5e5')
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
				padding: [30, 0]
				Label:
					id: cnc_academy_info
					font_size: '30sp'
					text_size: self.size
					valign: 'bottom'
					halign: 'center'
					markup: 'true'
					bold: True
					color: hex('#333333ff')
					size: self.texture_size
			BoxLayout:
				orientation: 'horizontal'
				width: dp(800)
				height: dp(200)
				padding: [20, 20, 20, 0]
				size_hint: (None,None)
				spacing: 0
                BoxLayout:
                	id: qr_code_container
                    padding: [10,0,0,0]
					# width: dp(162)
					# height: dp(180)
					# size_hint: (None,None)
					size_hint_x: 0.21
                    Image:
                    	id: qr_code_image
                        source: "./asmcnc/apps/warranty_app/img/academy-qr-code.png"
                        center_x: self.parent.center_x
                        y: self.parent.y
                        size: self.parent.width, self.parent.height
                        allow_stretch: True
				BoxLayout:
					orientation: 'vertical'
					size_hint_x: 0.79
					BoxLayout:
						id: cnc_academy_logo_container
						size_hint_y: 0.75
						padding: [10, 2, 10, 0]

	                    Image:
	                    	id: cnc_academy_logo
	                        source: "./asmcnc/apps/warranty_app/img/cnc_academy_logo.png"
	                        center_x: self.parent.center_x
	                        y: self.parent.y
	                        # size: self.parent.width, self.parent.height
	                        allow_stretch: False
					Label:
						id: url_label
						size_hint_y: 0.25
						font_size: '25sp'
						text_size: self.size
						valign: 'top'
						halign: 'center'
						markup: 'true'
						multiline: True
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
	                    background_normal: "./asmcnc/apps/warranty_app/img/next.png"
	                    background_down: "./asmcnc/apps/warranty_app/img/next.png"
	                    border: [dp(14.5)]*4
						size_hint: (None,None)
						width: dp(291)
						height: dp(79)
						on_press: root.next_screen()
						# text: 'Get started!'
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

class CNCAcademyScreen(Screen):

	def __init__(self, **kwargs):
		super(CNCAcademyScreen, self).__init__(**kwargs)
		self.wm=kwargs['warranty_manager']
		self.m=kwargs['machine']
		self.l=kwargs['localization']

		self.status_bar_widget = widget_status_bar.StatusBar(screen_manager=self.wm.sm, machine=self.m)
		self.status_container.add_widget(self.status_bar_widget)
		self.status_bar_widget.cheeky_color = '#1976d2'

		self.update_strings()


	def next_screen(self):
		self.wm.sm.current = 'reboot_to_apply_settings'

	def go_back(self):
		self.wm.open_data_consent_app()

	def update_strings(self):
		self.cnc_academy_info.text = self.l.get_str("Visit Yeti Tool CNC Academy for video tutorials on how to get started.")
		self.url_label.text = "https://academy.yetitool.com"
		self.next_button.text = self.l.get_str("Next") + "..."
