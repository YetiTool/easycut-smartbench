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
			height: dp(100)
			width: dp (800)
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
				size_hint: (None,None)
				height: dp(200)
				width: dp (800)
				padding: (0,0,0,0)
				
				Label:
					font_size: '32sp'
					text: "[color=000000] You have sucessfully completed your warranty activation [/color]"
					text_size: self.size
					valign: 'middle'
					halign: 'center'
					markup: 'true'
					bold: True
				
			BoxLayout:
				orientation: 'vertical'	
				width: dp(546)
				height: dp(120)	
				size_hint: (None,None)
				padding: (265,0,0,0)

				Button:
					background_color: hex('##1C00ff00')
					width: dp(291)
					height: dp(79)
					size_hint: (None,None)				
					pos: self.parent.pos 
					on_press: root.next_screen()
					
					
					BoxLayout:
						orientation: 'vertical'
						width: dp(291)
						height: dp(79)
						padding: (0,0,0,0)
						size_hint: (None,None)
						size: self.parent.size
						pos: self.parent.pos 

						Image: 
							source: "./asmcnc/apps/warranty_app/img/get_started.png"
							size: self.parent.width, self.parent.height
							pos: self.parent.pos
							allow_stretch: True 
			BoxLayout:
				orientation: 'vertical'
				size_hint_y: 0.08

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
							source: "./asmcnc/apps/warranty_app/img/exit.png"
							size: self.parent.width, self.parent.height
							allow_stretch: True 					

		


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
	



