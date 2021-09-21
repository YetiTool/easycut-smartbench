'''
Created on nov 2020
@author: Letty
'''

from kivy.lang import Builder
from kivy.factory import Factory
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.spinner import Spinner, SpinnerOption
from kivy.uix.dropdown import DropDown
from kivy.uix.scrollview import ScrollView
import sys, os
from asmcnc.skavaUI import widget_status_bar
from kivy.clock import Clock

Builder.load_string("""

#:import Factory kivy.factory.Factory

# <LanguageDropDown@DropDown>
#     bar_color: hex('#1976d2ff')
#     bar_inactive_color: hex('#333333a0')
#     bar_width: dp(20)
#     bar_margin: dp(2)

# <LanguageSpinner@SpinnerOption>

#     background_normal: ''
#     background_color: hex('#f9f9f9ff')
#     height: dp(45)
#     color: hex('#333333ff')
#     halign: 'left'
#     markup: 'True'
#     font_size: 25

<LanguageSelectScreen>:

	status_container : status_container
	# language_button : language_button
	# loading_label : loading_label

	row_1_col_1 : row_1_col_1
	row_1_col_2 : row_1_col_2
	row_1_col_3 : row_1_col_3
	row_2_col_1 : row_2_col_1
	row_2_col_2 : row_2_col_2
	row_2_col_3 : row_2_col_3
	row_3_col_1 : row_3_col_1
	# row_3_col_2 : row_3_col_2
	# row_3_col_3 : row_3_col_3

	row_1_col_1_image : row_1_col_1_image
	row_1_col_2_image : row_1_col_2_image
	row_1_col_3_image : row_1_col_3_image
	row_2_col_1_image : row_2_col_1_image
	row_2_col_2_image : row_2_col_2_image
	row_2_col_3_image : row_2_col_3_image
	row_3_col_1_image : row_3_col_1_image
	# row_3_col_2_image : row_3_col_2_image
	# row_3_col_3_image : row_3_col_3_image

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

			# BoxLayout:
			# 	orientation: 'vertical'
			# 	width: dp(800)
			# 	# height: dp(200)
			# 	height: dp(299.6)
			# 	padding: [dp(254.5),dp(0),dp(254.5),0] # dp(160.6)
			# 	spacing: 80
			# 	size_hint: (None,None)

			# 	BoxLayout: 
			# 		size_hint: (None, None)
			# 		height: dp(79)
			# 		width: dp(291)

			# 		Spinner:
			# 			id: language_button
			# 			background_normal: "./asmcnc/apps/warranty_app/img/next.png"
			# 			background_down: "./asmcnc/apps/warranty_app/img/next.png"
			# 			border: [dp(14.5)]*4
			# 			size_hint: (None,None)
			# 			width: dp(291)
			# 			height: dp(79)
			# 			center: self.parent.center
			# 			pos: self.parent.pos
			# 			text: 'Choose language'
			# 			color: hex('#f9f9f9ff')
			# 			markup: True
			# 			option_cls: Factory.get("LanguageSpinner")
			# 			on_text: root.choose_language()
			# 			font_size: '30sp'
			# 			dropdown_cls: Factory.get("LanguageDropDown")

			# 	Label:
			# 		id: loading_label
			# 		size_hint: (None, None)
			# 		height: dp(60)
			# 		width: dp(291)
			# 		font_size: '20sp'
			# 		text_size: self.size
			# 		valign: 'top'
			# 		halign: 'center'
			# 		markup: 'true'
			# 		color: hex('#333333ff')
			# 		text: ""

			# BoxLayout:
			# 	orientation: 'vertical'
			# 	width: dp(800)
			# 	height: dp(80)
			# 	padding: [dp(254.5),0,dp(254.5),0]
			# 	size_hint: (None,None)
			# 	BoxLayout: 
			# 		size_hint: (None, None)
			# 		height: dp(79)
			# 		width: dp(291)
								
			# BoxLayout:
			# 	orientation: 'vertical'
			# 	padding: [dp(738), 0, dp(10), dp(10)]
			# 	size_hint: (None,None)
			# 	width: dp(800)
			# 	height: dp(62)

			BoxLayout:
				padding: [dp(21), dp(10)]

	            GridLayout:
	                pos: self.parent.pos
	                cols: 9
	                rows: 3
	                cols_minimum: {0: dp(15), 1: dp(56), 2: dp(170), 3: dp(15), 4: dp(56), 5: dp(170), 6: dp(15), 7: dp(56), 8: dp(170)}
	                spacing: 5


	                # ROW 1

					CheckBox: 
						group: "language_radio_buttons" 
						on_press: root.chosen_lang = row_1_col_1.text
						color: hex('#1976d2ff')

	                Image: 
	                	id: row_1_col_1_image
	                	allow_stretch: True

	                Label: 
	                	id: row_1_col_1
	                	valign: "middle"
						font_size: '20sp'
						text_size: self.size
						markup: True
						halign: "left"
						color: hex('#333333ff')


					CheckBox: 
						group: "language_radio_buttons" 
						on_press: root.chosen_lang = row_1_col_2.text

	                Image: 
	                	id: row_1_col_2_image
	                	allow_stretch: True

	                Label: 
	                	id: row_1_col_2
	                	text: "Italian (IT)"
	                	valign: "middle"
						font_size: '20sp'
						text_size: self.size
						markup: True
						halign: "left"
						color: hex('#333333ff')


					CheckBox: 
						group: "language_radio_buttons" 
						on_press: root.chosen_lang = row_1_col_3.text

	                Image: 
	                	id: row_1_col_3_image
	                	allow_stretch: True

	                Label: 
	                	id: row_1_col_3
	                	text: "Suomalainen (FI)"
	                	valign: "middle"
						font_size: '20sp'
						text_size: self.size
						markup: True
						halign: "left"
						color: hex('#333333ff')


					# ROW 2

					CheckBox: 
						group: "language_radio_buttons" 
						on_press: root.chosen_lang = row_2_col_1.text

	                Image: 
	                	id: row_2_col_1_image
	                	allow_stretch: True

	                Label: 
	                	id: row_2_col_1
	                	text: "Suomalainen (FI)"
	                	valign: "middle"
						font_size: '20sp'
						text_size: self.size
						markup: True
						halign: "left"
						color: hex('#333333ff')


					CheckBox: 
						group: "language_radio_buttons" 
						on_press: root.chosen_lang = row_2_col_2.text

	                Image: 
	                	id: row_2_col_2_image
	                	allow_stretch: True

	                Label: 
	                	id: row_2_col_2
	                	text: "Suomalainen (FI)"
	                	valign: "middle"
						font_size: '20sp'
						text_size: self.size
						markup: True
						halign: "left"
						color: hex('#333333ff')


					CheckBox: 
						group: "language_radio_buttons" 
						on_press: root.chosen_lang = row_2_col_3.text

	                Image: 
	                	id: row_2_col_3_image
	                	allow_stretch: True

	                Label: 
	                	id: row_2_col_3
	                	text: "Suomalainen (FI)"
	                	valign: "middle"
						font_size: '20sp'
						text_size: self.size
						markup: True
						halign: "left"
						color: hex('#333333ff')


					# ROW 3

					CheckBox: 
						group: "language_radio_buttons" 
						on_press: root.chosen_lang = row_3_col_1.text

	                Image: 
	                	id: row_3_col_1_image
	                	allow_stretch: True

	                Label: 
	                	id: row_3_col_1
	                	text: "Suomalainen (FI)"
	                	valign: "middle"
						font_size: '20sp'
						text_size: self.size
						markup: True
						halign: "left"
						color: hex('#333333ff')

					BoxLayout: 
					BoxLayout: 
					BoxLayout: 
					BoxLayout: 
					BoxLayout: 
					BoxLayout: 



					# CheckBox: 
					# 	group: "language_radio_buttons" 
					# 	on_press: root.chosen_lang = row_3_col_2.text

	    #             Image: 
	    #             	id: row_3_col_2_image
	    				# allow_stretch: True

	    #             Label: 
	    #             	id: row_3_col_2
	    #             	text: "Suomalainen (FI)"
	    #             	valign: "middle"
					# 	font_size: '20sp'
					# 	text_size: self.size
					# 	markup: True
					# 	halign: "left"
						# color: hex('#333333ff')


					# CheckBox: 
					# 	group: "language_radio_buttons" 
					# 	on_press: root.chosen_lang = row_3_col_3.text

	    #             Image: 
	    #             	id: row_3_col_3_image
	    				# allow_stretch: True

	    #             Label: 
	    #             	id: row_3_col_3
	    #             	text: "Suomalainen (FI)"
	    #             	valign: "middle"
					# 	font_size: '20sp'
					# 	text_size: self.size
					# 	markup: True
					# 	halign: "left"
						# color: hex('#333333ff')

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
						on_press: root.choose_language()
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

                # Button:
                #     size_hint: (None,None)
                #     height: dp(52)
                #     width: dp(60)
                #     background_color: hex('#F4433600')
                #     center: self.parent.center
                #     pos: self.parent.pos
                #     on_press: root.go_back()
                #     BoxLayout:
                #         padding: 0
                #         size: self.parent.size
                #         pos: self.parent.pos
                #         Image:
                #             source: "./asmcnc/apps/systemTools_app/img/back_to_menu.png"
                #             center_x: self.parent.center_x
                #             y: self.parent.y
                #             size: self.parent.width, self.parent.height
                #             allow_stretch: True



""")

class LanguageSelectScreen(Screen):

	chosen_lang = ''

	def __init__(self, **kwargs):
		super(LanguageSelectScreen, self).__init__(**kwargs)
		self.wm=kwargs['warranty_manager']
		self.m=kwargs['machine']
		self.l=kwargs['localization']
		
		self.status_bar_widget = widget_status_bar.StatusBar(screen_manager=self.wm.sm, machine=self.m)
		self.status_container.add_widget(self.status_bar_widget)
		self.status_bar_widget.cheeky_color = '#1976d2'

		self.row_1_col_1.text = self.l.supported_languages[4]
		self.row_1_col_2.text = self.l.supported_languages[4]
		self.row_1_col_3.text = self.l.supported_languages[4]
		self.row_2_col_1.text = self.l.supported_languages[4]
		self.row_2_col_2.text = self.l.supported_languages[4]
		self.row_2_col_3.text = self.l.supported_languages[4]
		self.row_3_col_1.text = self.l.supported_languages[4]
		# self.row_3_col_2.text = self.l.supported_languages[7]
		# self.row_3_col_3.text = self.l.supported_languages[8]

		self.row_1_col_1_image.source = "./asmcnc/apps/warranty_app/img/flags/" + self.row_1_col_1.text + ".png"
		self.row_1_col_2_image.source = "./asmcnc/apps/warranty_app/img/flags/" + self.row_1_col_2.text + ".png"
		self.row_1_col_3_image.source = "./asmcnc/apps/warranty_app/img/flags/" + self.row_1_col_3.text + ".png"
		self.row_2_col_1_image.source = "./asmcnc/apps/warranty_app/img/flags/" + self.row_2_col_1.text + ".png"
		self.row_2_col_2_image.source = "./asmcnc/apps/warranty_app/img/flags/" + self.row_2_col_2.text + ".png"
		self.row_2_col_3_image.source = "./asmcnc/apps/warranty_app/img/flags/" + self.row_2_col_3.text + ".png"
		self.row_3_col_1_image.source = "./asmcnc/apps/warranty_app/img/flags/" + self.row_3_col_1.text + ".png"
		# self.row_3_col_2_image.source = "./asmcnc/apps/warranty_app/img/flags/" + self.row_3_col_2.text + ".png"
		# self.row_3_col_3_image.source = "./asmcnc/apps/warranty_app/img/flags/" + self.row_3_col_3.text + ".png"

	# def on_pre_enter(self):
	# 	self.loading_label.text = ""

	def next_screen(self):
		# self.wm.open_warranty_app()
		print(self.chosen_lang)

	def choose_language(self):
		self.l.load_in_new_language(self.chosen_lang)
		self.next_button.text = self.l.get_str("Loading...")
		Clock.schedule_once(lambda dt: self.next_screen(), 0.3)
