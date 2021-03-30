'''
Created on nov 2020
@author: Letty
'''

from kivy.lang import Builder
from kivy.factory import Factory
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.spinner import Spinner, SpinnerOption
import sys, os
from asmcnc.skavaUI import widget_status_bar
from kivy.clock import Clock

Builder.load_string("""

#:import Factory kivy.factory.Factory

<LanguageSpinner@SpinnerOption>

    background_normal: ''
    background_color: [1,1,1,1]
    height: dp(50)
    color: 0,0,0,1
    halign: 'left'
    markup: 'True'
    font_size: 25

<LanguageSelectScreen>:

	status_container : status_container
	language_button : language_button
	# title_label : title_label
	# thankyou_label : thankyou_label
	# next_steps_label : next_steps_label
	# minutes_label : minutes_label
	# next_button : next_button

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
				# height: dp(200)
				height: dp(299.6)
				padding: [dp(254.5),dp(0),dp(254.5),dp(160.6)]
				size_hint: (None,None)

				BoxLayout: 
					size_hint: (None, None)
					height: dp(79)
					width: dp(291)

					Spinner:
						id: language_button
						background_normal: "./asmcnc/apps/warranty_app/img/next.png"
						background_down: "./asmcnc/apps/warranty_app/img/next.png"
						border: [dp(14.5)]*4
						size_hint: (None,None)
						width: dp(291)
						height: dp(79)
						center: self.parent.center
						pos: self.parent.pos
						text: 'Choose language'
						color: hex('#f9f9f9ff')
						markup: True
						option_cls: Factory.get("LanguageSpinner")
						on_text: root.choose_language()
						font_size: '30sp'

				# Label:
				# 	id: thankyou_label
				# 	size_hint_y: 0.25
				# 	font_size: '20sp'
				# 	# text: "[color=333333ff]Thank you for purchasing SmartBench.[/color]"
				# 	text_size: self.size
				# 	valign: 'bottom'
				# 	halign: 'center'
				# 	markup: 'true'
				# 	color: hex('#333333ff')

				# Label:
				# 	id: next_steps_label
				# 	size_hint_y: 0.5
				# 	font_size: '20sp'
				# 	# text: "[color=333333ff]Please follow the next steps to complete your warranty registration process.[/color]"
				# 	text_size: self.size
				# 	valign: 'middle'
				# 	halign: 'center'
				# 	markup: 'true'
				# 	multiline: True
				# 	color: hex('#333333ff')
				
				# Label:
				# 	id: minutes_label
				# 	size_hint_y: 0.25
				# 	font_size: '20sp'
				# 	# text: "[color=333333ff]It will only a take a few minutes.[/color]"
				# 	text_size: self.size
				# 	valign: 'top'
				# 	halign: 'center'
				# 	markup: 'true'
				# 	color: hex('#333333ff')

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
					# Button:
					# 	id: next_button
					# 	background_normal: "./asmcnc/apps/warranty_app/img/next.png"
					# 	background_down: "./asmcnc/apps/warranty_app/img/next.png"
					# 	border: [dp(14.5)]*4
					# 	size_hint: (None,None)
					# 	width: dp(291)
					# 	height: dp(79)
					# 	on_press: root.next_screen()
					# 	# text: 'Next...'
					# 	font_size: '30sp'
					# 	color: hex('#f9f9f9ff')
					# 	markup: True
					# 	center: self.parent.center
					# 	pos: self.parent.pos
								
			BoxLayout:
				orientation: 'vertical'
				padding: [dp(738), 0, dp(10), dp(10)]
				size_hint: (None,None)
				width: dp(800)
				height: dp(62)

				# Button:
				# 	size_hint: (None,None)
				# 	height: dp(52)
				# 	width: dp(52)
				# 	background_color: hex('##e5e5e5')
				# 	background_normal: ''
				# 	center: self.parent.center
				# 	pos: self.parent.pos
				# 	on_press: root.quit_to_console()

		


""")

class LanguageSelectScreen(Screen):

	def __init__(self, **kwargs):
		super(LanguageSelectScreen, self).__init__(**kwargs)
		self.wm=kwargs['warranty_manager']
		self.m=kwargs['machine']
		self.l=kwargs['localization']
		
		self.status_bar_widget = widget_status_bar.StatusBar(screen_manager=self.wm.sm, machine=self.m)
		self.status_container.add_widget(self.status_bar_widget)
		self.status_bar_widget.cheeky_color = '#1976d2'

		self.language_button.values = self.l.supported_languages

	def next_screen(self):
		self.wm.open_warranty_app()

	def choose_language(self):
		chosen_lang = self.language_button.text
		self.l.load_in_new_language(chosen_lang)
		Clock.schedule_once(lambda dt: self.next_screen(), 0.3)


