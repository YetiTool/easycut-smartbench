# -*- coding: utf-8 -*-
'''
Created on nov 2020
@author: Letty
'''

from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

Builder.load_string("""


<LanguageSelectScreen>:

	header_label : header_label

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
		height: dp(800)
		width: dp(480)
		canvas.before:
			Color: 
				rgba: hex('#e5e5e5ff')
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
					id: header_label
					size_hint: (None,None)
					height: dp(60)
					width: dp(800)
					text: "Welcome to SmartBench"
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
				padding: [dp(30), dp(10)]
				spacing: dp(10)
				orientation: 'vertical'

	            GridLayout:
	                pos: self.parent.pos
	                cols: 9
	                rows: 3
	                cols_minimum: {0: dp(15), 1: dp(50), 2: dp(170), 3: dp(15), 4: dp(50), 5: dp(170), 6: dp(15), 7: dp(50), 8: dp(170)}
	                spacing: 5


	                # ROW 1

					CheckBox: 
						group: "language_radio_buttons" 
						on_press: root.select_language(self, row_1_col_1)
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
						on_press: root.select_language(self, row_1_col_2)
						color: hex('#333333ff')

	                Image: 
	                	id: row_1_col_2_image
	                	allow_stretch: True

	                Label: 
	                	id: row_1_col_2
	                	valign: "middle"
						font_size: '20sp'
						text_size: self.size
						markup: True
						halign: "left"
						color: hex('#333333ff')


					CheckBox: 
						group: "language_radio_buttons" 
						on_press: root.select_language(self, row_1_col_3)
						color: hex('#333333ff')

	                Image: 
	                	id: row_1_col_3_image
	                	allow_stretch: True

	                Label: 
	                	id: row_1_col_3
	                	valign: "middle"
						font_size: '20sp'
						text_size: self.size
						markup: True
						halign: "left"
						color: hex('#333333ff')


					# ROW 2

					CheckBox: 
						group: "language_radio_buttons" 
						on_press: root.select_language(self, row_2_col_1)
						color: hex('#333333ff')

	                Image: 
	                	id: row_2_col_1_image
	                	allow_stretch: True

	                Label: 
	                	id: row_2_col_1
	                	valign: "middle"
						font_size: '20sp'
						text_size: self.size
						markup: True
						halign: "left"
						color: hex('#333333ff')


					CheckBox: 
						group: "language_radio_buttons" 
						on_press: root.select_language(self, row_2_col_2)
						color: hex('#333333ff')

	                Image: 
	                	id: row_2_col_2_image
	                	allow_stretch: True

	                Label: 
	                	id: row_2_col_2
	                	valign: "middle"
						font_size: '20sp'
						text_size: self.size
						markup: True
						halign: "left"
						color: hex('#333333ff')


					CheckBox: 
						group: "language_radio_buttons" 
						on_press: root.select_language(self, row_2_col_3)
						color: hex('#333333ff')

	                Image: 
	                	id: row_2_col_3_image
	                	allow_stretch: True

	                Label: 
	                	id: row_2_col_3
	                	valign: "middle"
						font_size: '20sp'
						text_size: self.size
						markup: True
						halign: "left"
						color: hex('#333333ff')


					# ROW 3

					CheckBox: 
						group: "language_radio_buttons" 
						on_press: root.select_language(self, row_3_col_1)
						color: hex('#333333ff')

	                Image: 
	                	id: row_3_col_1_image
	                	allow_stretch: True

	                Label: 
	                	id: row_3_col_1
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
					# 	on_press: root.select_language(self, row_3_col_2)
					# 	on_press: root.select_language(self)
					# 	color: hex('#333333ff')

	    #             Image: 
	    #             	id: row_3_col_2_image
	    # 				allow_stretch: True

	    #             Label: 
	    #             	id: row_3_col_2
	    #             	text: "Suomalainen (FI)"
	    #             	valign: "middle"
					# 	font_size: '20sp'
					# 	text_size: self.size
					# 	markup: True
					# 	halign: "left"
					# 	color: hex('#333333ff')


					# CheckBox: 
					# 	group: "language_radio_buttons" 
					# 	on_press: root.select_language(self, row_3_col_3)
					# 	on_press: root.select_language(self)
					# 	color: hex('#333333ff')

	    #             Image: 
	    #             	id: row_3_col_3_image
	    # 				allow_stretch: True

	    #             Label: 
	    #             	id: row_3_col_3
	    #             	text: "Suomalainen (FI)"
	    #             	valign: "middle"
					# 	font_size: '20sp'
					# 	text_size: self.size
					# 	markup: True
					# 	halign: "left"
					# 	color: hex('#333333ff')

			# FOOTER
			BoxLayout: 
				padding: [10,0,10,10]
				size_hint: (None, None)
				height: dp(122)
				width: dp(800)
				orientation: 'horizontal'
				BoxLayout: 
					size_hint: (None, None)
					height: dp(122)
					width: dp(244.5)
					padding: [0, 0, 184.5, 0]

				BoxLayout: 
					size_hint: (None, None)
					height: dp(122)
					width: dp(291)
					padding: [0,0,0,32]
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
						opacity: 0
						disabled: True
				BoxLayout: 
					size_hint: (None, None)
					height: dp(122)
					width: dp(244.5)
					padding: [193.5, 0, 0, 0]



""")

class LanguageSelectScreen(Screen):

	flag_img_path = "./asmcnc/apps/start_up_sequence/welcome_to_smartbench_app/img/"

	welcome_to_smartbench_labels = [
		"Welcome to SmartBench",
		"Willkommen bei SmartBench",
		"Benvenuto in Smartbench",
		"Benvenuti in Smartbench",
		"Tervetuloa Smartbenchiin",
		"Witamy w SmartBench",
		"Velkommen til SmartBench"
	]

	welcome_i = 0
	update_welcome_header = None

	def __init__(self, **kwargs):
		super(LanguageSelectScreen, self).__init__(**kwargs)
		self.start_seq=kwargs['start_sequence']
		self.sm=kwargs['screen_manager']
		self.l=kwargs['localization']

		self.row_1_col_1.text = self.l.approved_languages[0]
		self.row_1_col_2.text = self.l.approved_languages[1]
		self.row_1_col_3.text = self.l.approved_languages[2]
		self.row_2_col_1.text = self.l.approved_languages[3]
		self.row_2_col_2.text = self.l.approved_languages[4]
		self.row_2_col_3.text = self.l.approved_languages[5]
		self.row_3_col_1.text = self.l.approved_languages[6]
		# self.row_3_col_2.text = self.l.approved_languages[7]
		# self.row_3_col_3.text = self.l.approved_languages[8]

		self.row_1_col_1_image.source = self.get_image_filename(self.row_1_col_1)
		self.row_1_col_2_image.source = self.get_image_filename(self.row_1_col_2)
		self.row_1_col_3_image.source = self.get_image_filename(self.row_1_col_3)
		self.row_2_col_1_image.source = self.get_image_filename(self.row_2_col_1)
		self.row_2_col_2_image.source = self.get_image_filename(self.row_2_col_2)
		self.row_2_col_3_image.source = self.get_image_filename(self.row_2_col_3)
		self.row_3_col_1_image.source = self.get_image_filename(self.row_3_col_1)
		# self.row_3_col_2_image.source = self.flag_img_path + self.row_3_col_2.text + ".png"
		# self.row_3_col_3_image.source = self.flag_img_path + self.row_3_col_3.text + ".png"

	def get_image_filename(self, value):
		# If french flag needs to be shown, then filename will not match language name due to special character
		if value.text == "Français (FR)":
			return self.flag_img_path + "Francais (FR)" + ".png"
		return self.flag_img_path + value.text + ".png"

	def on_enter(self):
		self.update_welcome_header = Clock.schedule_interval(self.change_welcome_label, 1)

	def change_welcome_label(self, dt):

		self.header_label.text = self.welcome_to_smartbench_labels[self.welcome_i]

		if self.welcome_i < 6:
			self.welcome_i += 1

		else:
			self.welcome_i = 0

	def select_language(self, radio_button, language_label):

		if radio_button.state == 'down':
			radio_button.color = [25 / 255., 118 / 255., 210 / 255., 1]
			self.l.load_in_new_language(language_label.text)
			[self.sm.get_screen(screen).update_strings() for screen in self.start_seq.screen_sequence]
			self.next_button.opacity = 1
			self.next_button.disabled = False

		else: 
			radio_button.color = [51 / 255., 51 / 255., 51 / 255., 1.]
			self.next_button.opacity = 0
			self.next_button.disabled = True

	def next_screen(self):
		self.start_seq.next_in_sequence()

	def update_strings(self):
		self.header_label.text = self.l.get_str("Welcome to SmartBench")
		self.next_button.text = self.l.get_str("Next") + "..."
		if self.update_welcome_header: Clock.unschedule(self.update_welcome_header)

	def on_leave(self):
		self.next_button.disabled = False
		self.loading_warranty_app = False

