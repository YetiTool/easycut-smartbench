# -*- coding: utf-8 -*-
import os, sys

from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock

from asmcnc.skavaUI import popup_info

Builder.load_string("""

<WiFiAndDataConsentScreen1>

	user_info : user_info

    BoxLayout:
        height: dp(800)
        width: dp(480)
        canvas.before:
            Color: 
                rgba: hex('#f9f9f9ff')
            Rectangle: 
                size: self.size
                pos: self.pos

        BoxLayout:
            padding: 0
            spacing: 0
            orientation: "vertical"

            # HEADER
            BoxLayout:
                padding: 0
                spacing: 0
                canvas:
                    Color:
                        rgba: hex('#1976d2ff')
                    Rectangle:
                        pos: self.pos
                        size: self.size
                Label:
                    size_hint: (None,None)
                    height: dp(60)
                    width: dp(800)
                    text: "Wi-Fi and Data Consent"
                    color: hex('#f9f9f9ff')
                    # color: hex('#333333ff') #grey
                    font_size: dp(30)
                    halign: "center"
                    valign: "bottom"
                    markup: True
                   
            # BODY
            BoxLayout:
                size_hint: (None,None)
                width: dp(800)
                height: dp(298)
                padding: [dp(20), dp(0), dp(20), dp(0)]
                spacing: 0
                orientation: 'horizontal'
                Label: 
                	id: user_info
					size_hint: (1,1)
                    # color: hex('#f9f9f9ff') # white
                    color: hex('#333333ff') #grey
                    font_size: dp(18)
                    halign: "left"
                    valign: "middle"
                    markup: True
                    text_size: self.size
                    size: self.texture_size

            # FOOTER
			BoxLayout: 
				padding: [10,0,10,10]
				size_hint: (None, None)
				height: dp(122)
				width: dp(800)
				orientation: 'horizontal'
				BoxLayout: 
					size_hint: (None, None)
					height: dp(132)
					width: dp(244.5)
					padding: [0, 0, 184.5, 0]
					# Button:
					# 	size_hint: (None,None)
					# 	height: dp(52)
					# 	width: dp(60)
					# 	background_color: hex('#F4433600')
					# 	center: self.parent.center
					# 	pos: self.parent.pos
					# 	on_press: root.prev_screen()
					# 	BoxLayout:
					# 		padding: 0
					# 		size: self.parent.size
					# 		pos: self.parent.pos
					# 		Image:
					# 			source: "./asmcnc/apps/systemTools_app/img/back_to_menu.png"
					# 			center_x: self.parent.center_x
					# 			y: self.parent.y
					# 			size: self.parent.width, self.parent.height
					# 			allow_stretch: True
				BoxLayout: 
					size_hint: (None, None)
					height: dp(122)
					width: dp(291)
					padding: [0,0,0,32]
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
					size_hint: (None, None)
					height: dp(122)
					width: dp(244.5)
					padding: [193.5, 0, 0, 0]

""")

class WiFiAndDataConsentScreen1(Screen):

	def __init__(self, **kwargs):
		super(WiFiAndDataConsentScreen1, self).__init__(**kwargs)
		self.sm=kwargs['screen_manager']
		self.update_strings()

	def get_str(self, words):
		return words

	def get_bold(self, words):
		return '[b]' + words + '[/b]'

	def next_screen(self):
		self.sm.current = 'wifi2'

	def update_strings(self):
		self.user_info.text = (
		self.get_bold("To enable Wi-Fi, you need to accept our data collection policy.") + \
		"\n\n" + \
		self.get_str("When Wi-Fi is enabled, we will only send SmartBench’s data anonymously. This allows us to enable smart features, and improve our services.") + \
		"\n\n" + \
		self.get_str("You will need Wi-Fi if you want to:") + \
		"\n\n" + \
		"[b]•[/b] " + self.get_str("Automatically receive software updates") + \
		"\n" + \
		"[b]•[/b] " + self.get_str("Use SmartTransfer (remotely transfer files)") + \
		"\n" + \
		"[b]•[/b] " + self.get_str("Use SmartManager (remotely manage and monitor SmartBenches)") + \
		"\n\n" + \
		self.get_str("You can disable Wi-Fi at any time.")
		)
