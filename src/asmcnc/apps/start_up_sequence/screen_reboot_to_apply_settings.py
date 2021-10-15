'''
Created on 15th September 2021
@author: Letty
Reboot to apply language settings
'''

from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
import sys, os
from asmcnc.skavaUI import widget_status_bar
Builder.load_string("""
<ApplySettingsScreen>:
				
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
					text_size: self.size
					valign: 'top'
					halign: 'center'
					markup: 'true'
					bold: True
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

class ApplySettingsScreen(Screen):

	def __init__(self, **kwargs):
		super(ApplySettingsScreen, self).__init__(**kwargs)
		self.wm=kwargs['warranty_manager']
		self.m=kwargs['machine']
		self.l=kwargs['localization']

		self.status_bar_widget = widget_status_bar.StatusBar(screen_manager=self.wm.sm, machine=self.m)
		self.status_container.add_widget(self.status_bar_widget)
		self.status_bar_widget.cheeky_color = '#1976d2'

		self.update_strings()

	def next_screen(self):
		# self.wm.exit_app()
		self.wm.sm.current = 'rebooting'

	def go_back(self):
		self.wm.sm.current = 'cnc_academy'

	def update_strings(self): # add to lang list!
		self.success_label.text = self.l.get_str("Reboot to finish applying your settings, and get started!")
		self.next_button.text = self.l.get_str("Reboot!")