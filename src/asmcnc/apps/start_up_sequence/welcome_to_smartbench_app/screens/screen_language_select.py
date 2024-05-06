# -*- coding: utf-8 -*-
"""
Created on nov 2020
@author: Letty
"""
from kivy.lang import Builder
from kivy.factory import Factory
from kivy.uix.screenmanager import ScreenManager, Screen
import sys, os
from kivy.clock import Clock
from kivy.uix.label import Label


"""
DEPRECATED, NOW USING: src/asmcnc/apps/start_up_sequence/screens/screen_language_selection.py
"""


Builder.load_string(
    """


<LanguageSelectScreen>:

	header_label : header_label

	row_1_col_1 : row_1_col_1
	row_1_col_2 : row_1_col_2
	row_1_col_3 : row_1_col_3
	row_2_col_1 : row_2_col_1
	row_2_col_2 : row_2_col_2
	row_2_col_3 : row_2_col_3
	row_3_col_1 : row_3_col_1
	row_3_col_2 : row_3_col_2
	# row_3_col_3 : row_3_col_3

	row_1_col_1_image : row_1_col_1_image
	row_1_col_2_image : row_1_col_2_image
	row_1_col_3_image : row_1_col_3_image
	row_2_col_1_image : row_2_col_1_image
	row_2_col_2_image : row_2_col_2_image
	row_2_col_3_image : row_2_col_3_image
	row_3_col_1_image : row_3_col_1_image
	row_3_col_2_image : row_3_col_2_image
	# row_3_col_3_image : row_3_col_3_image

	next_button : next_button

	BoxLayout:
		height: dp(1.66666666667*app.height)
		width: dp(0.6*app.width)
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
					height: dp(0.125*app.height)
					width: dp(1.0*app.width)
					text: "Welcome to SmartBench"
					color: hex('#f9f9f9ff')
					# color: color_provider.get_rgba("dark_grey") #grey
					font_size: dp(0.0375*app.width)
					halign: "center"
					valign: "bottom"
					markup: True
				   
			# BODY
			BoxLayout:
				size_hint: (None,None)
				width: dp(1.0*app.width)
				height: dp(0.620833333333*app.height)
				padding:[dp(0.0375)*app.width, dp(0.0208333333333)*app.height]
				spacing:dp(0.0208333333333)*app.height
				orientation: 'vertical'

	            GridLayout:
	                pos: self.parent.pos
	                cols: 9
	                rows: 3
	                cols_minimum: {0: dp(15), 1: dp(50), 2: dp(170), 3: dp(15), 4: dp(50), 5: dp(170), 6: dp(15), 7: dp(50), 8: dp(170)}
	                spacing:0.00625*app.width


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
						font_size: str(0.025*app.width) + 'sp'
						text_size: self.size
						markup: True
						halign: "left"
						color: color_provider.get_rgba("dark_grey")


					CheckBox: 
						group: "language_radio_buttons" 
						on_press: root.select_language(self, row_1_col_2)
						color: color_provider.get_rgba("dark_grey")

	                Image: 
	                	id: row_1_col_2_image
	                	allow_stretch: True

	                Label: 
	                	id: row_1_col_2
	                	valign: "middle"
						font_size: str(0.025*app.width) + 'sp'
						text_size: self.size
						markup: True
						halign: "left"
						color: color_provider.get_rgba("dark_grey")


					CheckBox: 
						group: "language_radio_buttons" 
						on_press: root.select_language(self, row_1_col_3)
						color: color_provider.get_rgba("dark_grey")

	                Image: 
	                	id: row_1_col_3_image
	                	allow_stretch: True

	                Label: 
	                	id: row_1_col_3
	                	valign: "middle"
						font_size: str(0.025*app.width) + 'sp'
						text_size: self.size
						markup: True
						halign: "left"
						color: color_provider.get_rgba("dark_grey")


					# ROW 2

					CheckBox: 
						group: "language_radio_buttons" 
						on_press: root.select_language(self, row_2_col_1)
						color: color_provider.get_rgba("dark_grey")

	                Image: 
	                	id: row_2_col_1_image
	                	allow_stretch: True

	                Label: 
	                	id: row_2_col_1
	                	valign: "middle"
						font_size: str(0.025*app.width) + 'sp'
						text_size: self.size
						markup: True
						halign: "left"
						color: color_provider.get_rgba("dark_grey")


					CheckBox: 
						group: "language_radio_buttons" 
						on_press: root.select_language(self, row_2_col_2)
						color: color_provider.get_rgba("dark_grey")

	                Image: 
	                	id: row_2_col_2_image
	                	allow_stretch: True

	                Label: 
	                	id: row_2_col_2
	                	valign: "middle"
						font_size: str(0.025*app.width) + 'sp'
						text_size: self.size
						markup: True
						halign: "left"
						color: color_provider.get_rgba("dark_grey")


					CheckBox: 
						group: "language_radio_buttons" 
						on_press: root.select_language(self, row_2_col_3)
						color: color_provider.get_rgba("dark_grey")

	                Image: 
	                	id: row_2_col_3_image
	                	allow_stretch: True

	                Label: 
	                	id: row_2_col_3
	                	valign: "middle"
						font_size: str(0.025*app.width) + 'sp'
						text_size: self.size
						markup: True
						halign: "left"
						color: color_provider.get_rgba("dark_grey")


					# ROW 3

					CheckBox: 
						group: "language_radio_buttons" 
						on_press: root.select_language(self, row_3_col_1)
						color: color_provider.get_rgba("dark_grey")

	                Image: 
	                	id: row_3_col_1_image
	                	allow_stretch: True

	                Label: 
	                	id: row_3_col_1
	                	valign: "middle"
						font_size: str(0.025*app.width) + 'sp'
						text_size: self.size
						markup: True
						halign: "left"
						color: color_provider.get_rgba("dark_grey")

					CheckBox: 
						group: "language_radio_buttons" 
						on_press: root.select_language(self, row_3_col_2)
						color: color_provider.get_rgba("dark_grey")

	                Image: 
	                	id: row_3_col_2_image
	    				allow_stretch: True

	                Label: 
	                	id: row_3_col_2
	                	valign: "middle"
						font_size: str(0.025*app.width) + 'sp'
						text_size: self.size
						markup: True
						halign: "left"
						color: color_provider.get_rgba("dark_grey")

					BoxLayout: 
					BoxLayout: 
					BoxLayout: 

					# CheckBox: 
					# 	group: "language_radio_buttons" 
					# 	on_press: root.select_language(self, row_3_col_3)
					# 	on_press: root.select_language(self)
					# 	color: color_provider.get_rgba("dark_grey")

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
					# 	color: color_provider.get_rgba("dark_grey")

			# FOOTER
			BoxLayout: 
				padding:[dp(0.0125)*app.width, 0, dp(0.0125)*app.width, dp(0.0208333333333)*app.height]
				size_hint: (None, None)
				height: dp(0.254166666667*app.height)
				width: dp(1.0*app.width)
				orientation: 'horizontal'
				BoxLayout: 
					size_hint: (None, None)
					height: dp(0.254166666667*app.height)
					width: dp(0.305625*app.width)
					padding:[0, 0, dp(0.230625)*app.width, 0]

				BoxLayout: 
					size_hint: (None, None)
					height: dp(0.254166666667*app.height)
					width: dp(0.36375*app.width)
					padding:[0, 0, 0, dp(0.0666666666667)*app.height]
					Button:
						id: next_button
						background_normal: "./asmcnc/skavaUI/img/next.png"
						background_down: "./asmcnc/skavaUI/img/next.png"
						border: [dp(14.5)]*4
						size_hint: (None,None)
						width: dp(0.36375*app.width)
						height: dp(0.164583333333*app.height)
						on_press: root.next_screen()
						text: 'Next...'
						font_size: str(0.0375*app.width) + 'sp'
						color: hex('#f9f9f9ff')
						markup: True
						center: self.parent.center
						pos: self.parent.pos
						opacity: 0
						disabled: True
				BoxLayout: 
					size_hint: (None, None)
					height: dp(0.254166666667*app.height)
					width: dp(0.305625*app.width)
					padding:[dp(0.241875)*app.width, 0, 0, 0]



"""
)


class LanguageSelectScreen(Screen):
    flag_img_path = "./asmcnc/apps/start_up_sequence/welcome_to_smartbench_app/img/"
    welcome_to_smartbench_labels = [
        "Welcome to SmartBench",
        "Willkommen bei SmartBench",
        "Benvenuto in Smartbench",
        "Benvenuti in Smartbench",
        "Tervetuloa Smartbenchiin",
        "Witamy w SmartBench",
        "Velkommen til SmartBench",
        "SmartBench\xec\x97\x90 \xec\x98\xa4\xec\x8b\xa0 \xea\xb2\x83\xec\x9d\x84 \xed\x99\x98\xec\x98\x81\xed\x95\xa9\xeb\x8b\x88\xeb\x8b\xa4",
    ]
    welcome_i = 0
    update_welcome_header = None

    def __init__(self, **kwargs):
        super(LanguageSelectScreen, self).__init__(**kwargs)
        self.start_seq = kwargs["start_sequence"]
        self.sm = kwargs["screen_manager"]
        self.l = kwargs["localization"]
        self.row_1_col_1.text = self.l.approved_languages[0]
        self.row_1_col_2.text = self.l.approved_languages[1]
        self.row_1_col_3.text = self.l.approved_languages[2]
        self.row_2_col_1.text = self.l.approved_languages[3]
        self.row_2_col_2.text = self.l.approved_languages[4]
        self.row_2_col_3.text = self.l.approved_languages[5]
        self.row_3_col_1.text = self.l.approved_languages[6]
        self.row_3_col_2.text = self.l.approved_languages[7]
        # self.row_3_col_3.text = self.l.approved_languages[8]
        self.row_1_col_1_image.source = self.get_image_filename(self.row_1_col_1)
        self.row_1_col_2_image.source = self.get_image_filename(self.row_1_col_2)
        self.row_1_col_3_image.source = self.get_image_filename(self.row_1_col_3)
        self.row_2_col_1_image.source = self.get_image_filename(self.row_2_col_1)
        self.row_2_col_2_image.source = self.get_image_filename(self.row_2_col_2)
        self.row_2_col_3_image.source = self.get_image_filename(self.row_2_col_3)
        self.row_3_col_1_image.source = self.get_image_filename(self.row_3_col_1)
        self.row_3_col_2_image.source = self.get_image_filename(self.row_3_col_2)
        # self.row_3_col_3_image.source = self.get_image_filename(self.row_3_col_3)
		# Need specific font to show korean characters
        self.row_3_col_2.font_name = self.l.korean_font

    def get_image_filename(self, value):
        return self.flag_img_path + value.text + ".png"

    def on_enter(self):
        self.update_welcome_header = Clock.schedule_interval(
            self.change_welcome_label, 1
        )

    def change_welcome_label(self, dt):
        if self.welcome_i == 7:
            self.header_label.font_name = self.l.korean_font
        else:
            self.header_label.font_name = self.l.standard_font
        self.header_label.text = self.welcome_to_smartbench_labels[self.welcome_i]
        if self.welcome_i < 7:
            self.welcome_i += 1
        else:
            self.welcome_i = 0

    def select_language(self, radio_button, language_label):
        if radio_button.state == "down":
            current_font = self.l.font_regular
            radio_button.color = [25 / 255.0, 118 / 255.0, 210 / 255.0, 1]
            self.l.load_in_new_language(language_label.text)
            [
                self.sm.get_screen(screen).update_strings()
                for screen in self.start_seq.screen_sequence
            ]
            # If korean is selected, the startup sequence needs font updated to display it correctly
            if current_font != self.l.font_regular:
                # I know this is a nested for loop, but it executes very quickly
                for screen in self.start_seq.screen_sequence[1:] + ["rebooting"]:
                    for widget in self.sm.get_screen(screen).walk():
                        if isinstance(widget, Label):
                            widget.font_name = self.l.font_regular
            self.next_button.opacity = 1
            self.next_button.disabled = False
        else:
            radio_button.color = [51 / 255.0, 51 / 255.0, 51 / 255.0, 1.0]
            self.next_button.opacity = 0
            self.next_button.disabled = True

    def next_screen(self):
        self.start_seq.next_in_sequence()

    def update_strings(self):
        if self.l.lang == self.l.ko:
            self.header_label.font_name = self.l.korean_font
            self.next_button.font_name = self.l.korean_font
        else:
            self.header_label.font_name = self.l.standard_font
            self.next_button.font_name = self.l.standard_font
        self.header_label.text = self.l.get_str("Welcome to SmartBench")
        self.next_button.text = self.l.get_str("Next") + "..."
        if self.update_welcome_header:
            Clock.unschedule(self.update_welcome_header)

    def on_leave(self):
        self.next_button.disabled = False
        self.loading_warranty_app = False
