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


<LanguageSelectScreen>:

	status_container : status_container

	row_1_col_1 : row_1_col_1
	row_1_col_2 : row_1_col_2
	row_1_col_3 : row_1_col_3
	# row_2_col_1 : row_2_col_1
	# row_2_col_2 : row_2_col_2
	# row_2_col_3 : row_2_col_3
	# row_3_col_1 : row_3_col_1
	# row_3_col_2 : row_3_col_2
	# row_3_col_3 : row_3_col_3

	row_1_col_1_image : row_1_col_1_image
	row_1_col_2_image : row_1_col_2_image
	row_1_col_3_image : row_1_col_3_image
	# row_2_col_1_image : row_2_col_1_image
	# row_2_col_2_image : row_2_col_2_image
	# row_2_col_3_image : row_2_col_3_image
	# row_3_col_1_image : row_3_col_1_image
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

			BoxLayout:
				padding: [dp(30), dp(10)]

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


					# # ROW 2

					# CheckBox: 
					# 	group: "language_radio_buttons" 
					# 	on_press: root.select_language(self, row_2_col_1)
					# 	color: hex('#333333ff')

	    #             Image: 
	    #             	id: row_2_col_1_image
	    #             	allow_stretch: True

	    #             Label: 
	    #             	id: row_2_col_1
	    #             	valign: "middle"
					# 	font_size: '20sp'
					# 	text_size: self.size
					# 	markup: True
					# 	halign: "left"
					# 	color: hex('#333333ff')


					# CheckBox: 
					# 	group: "language_radio_buttons" 
					# 	on_press: root.select_language(self, row_2_col_2)
					# 	color: hex('#333333ff')

	    #             Image: 
	    #             	id: row_2_col_2_image
	    #             	allow_stretch: True

	    #             Label: 
	    #             	id: row_2_col_2
	    #             	valign: "middle"
					# 	font_size: '20sp'
					# 	text_size: self.size
					# 	markup: True
					# 	halign: "left"
					# 	color: hex('#333333ff')


					# CheckBox: 
					# 	group: "language_radio_buttons" 
					# 	on_press: root.select_language(self, row_2_col_3)
					# 	color: hex('#333333ff')

	    #             Image: 
	    #             	id: row_2_col_3_image
	    #             	allow_stretch: True

	    #             Label: 
	    #             	id: row_2_col_3
	    #             	valign: "middle"
					# 	font_size: '20sp'
					# 	text_size: self.size
					# 	markup: True
					# 	halign: "left"
					# 	color: hex('#333333ff')


					# # ROW 3

					# CheckBox: 
					# 	group: "language_radio_buttons" 
					# 	on_press: root.select_language(self, row_3_col_1)
					# 	color: hex('#333333ff')

	    #             Image: 
	    #             	id: row_3_col_1_image
	    #             	allow_stretch: True

	    #             Label: 
	    #             	id: row_3_col_1
	    #             	valign: "middle"
					# 	font_size: '20sp'
					# 	text_size: self.size
					# 	markup: True
					# 	halign: "left"
					# 	color: hex('#333333ff')

					BoxLayout: 
					BoxLayout: 
					BoxLayout: 
					BoxLayout: 
					BoxLayout: 
					BoxLayout: 
					BoxLayout: 
					BoxLayout: 
					BoxLayout: 
					BoxLayout: 
					BoxLayout: 
					BoxLayout: 
					BoxLayout: 
					BoxLayout: 
					BoxLayout: 
					BoxLayout: 
					BoxLayout: 
					BoxLayout: 



					# CheckBox: 
					# 	group: "language_radio_buttons" 
						# on_press: root.select_language(self, row_3_col_2)
						# on_press: root.select_language(self)
						# color: hex('#333333ff')

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
						# on_press: root.select_language(self, row_3_col_3)
						# on_press: root.select_language(self)
						# color: hex('#333333ff')

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
	                    background_disabled_normal: "./asmcnc/apps/warranty_app/img/next.png"
	                    background_disabled_down: "./asmcnc/apps/warranty_app/img/next.png"
	                    border: [dp(14.5)]*4
						size_hint: (None,None)
						width: dp(291)
						height: dp(79)
						on_press: root.load_next_screen()
						text: 'Next...'
						font_size: '30sp'
						color: hex('#f9f9f9ff')
						markup: True
	                    center: self.parent.center
	                    pos: self.parent.pos
	                    opacity: 0 
	                    disabled: True
								
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

	loading_warranty_app = False

	def __init__(self, **kwargs):
		super(LanguageSelectScreen, self).__init__(**kwargs)
		self.wm=kwargs['warranty_manager']
		self.m=kwargs['machine']
		self.l=kwargs['localization']
		
		self.status_bar_widget = widget_status_bar.StatusBar(screen_manager=self.wm.sm, machine=self.m)
		self.status_container.add_widget(self.status_bar_widget)
		self.status_bar_widget.cheeky_color = '#1976d2'

		self.row_1_col_1.text = self.l.supported_languages[0]
		self.row_1_col_2.text = self.l.supported_languages[1]
		self.row_1_col_3.text = self.l.supported_languages[2]
		# self.row_2_col_1.text = self.l.supported_languages[3]
		# self.row_2_col_2.text = self.l.supported_languages[4]
		# self.row_2_col_3.text = self.l.supported_languages[5]
		# self.row_3_col_1.text = self.l.supported_languages[6]
		# self.row_3_col_2.text = self.l.supported_languages[7]
		# self.row_3_col_3.text = self.l.supported_languages[8]

		self.row_1_col_1_image.source = "./asmcnc/apps/warranty_app/img/flags/" + self.row_1_col_1.text + ".png"
		self.row_1_col_2_image.source = "./asmcnc/apps/warranty_app/img/flags/" + self.row_1_col_2.text + ".png"
		self.row_1_col_3_image.source = "./asmcnc/apps/warranty_app/img/flags/" + self.row_1_col_3.text + ".png"
		# self.row_2_col_1_image.source = "./asmcnc/apps/warranty_app/img/flags/" + self.row_2_col_1.text + ".png"
		# self.row_2_col_2_image.source = "./asmcnc/apps/warranty_app/img/flags/" + self.row_2_col_2.text + ".png"
		# self.row_2_col_3_image.source = "./asmcnc/apps/warranty_app/img/flags/" + self.row_2_col_3.text + ".png"
		# self.row_3_col_1_image.source = "./asmcnc/apps/warranty_app/img/flags/" + self.row_3_col_1.text + ".png"
		# self.row_3_col_2_image.source = "./asmcnc/apps/warranty_app/img/flags/" + self.row_3_col_2.text + ".png"
		# self.row_3_col_3_image.source = "./asmcnc/apps/warranty_app/img/flags/" + self.row_3_col_3.text + ".png"

	def select_language(self, radio_button, language_label):

		if not self.loading_warranty_app:

			if radio_button.state == 'down':
				radio_button.color = [25 / 255., 118 / 255., 210 / 255., 1]
				self.l.load_in_new_language(language_label.text)
				self.next_button.text = self.l.get_str("Next") + "..."
				self.next_button.opacity = 1
				self.next_button.disabled = False

			else: 
				radio_button.color = [51 / 255., 51 / 255., 51 / 255., 1.]

	def next_screen(self):
		self.wm.open_warranty_app()

	def load_next_screen(self):
		self.next_button.disabled = True
		self.loading_warranty_app = True
		self.next_button.text = self.l.get_str("Loading...")
		Clock.schedule_once(lambda dt: self.next_screen(), 0.3)

	def on_leave(self):
		self.next_button.disabled = False
		self.loading_warranty_app = False
		self.next_button.text = self.l.get_str("Next") + "..."

