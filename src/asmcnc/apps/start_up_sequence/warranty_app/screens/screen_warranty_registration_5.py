"""
Created 15th September 2021
@author: Letty
"""
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
import sys, os
from asmcnc.skavaUI import widget_status_bar

Builder.load_string(
    """
<WarrantyScreen5>:

	title_label : title_label
	cnc_academy_info : cnc_academy_info
	qr_code_container : qr_code_container
	qr_code_image : qr_code_image
	cnc_academy_logo_container : cnc_academy_logo_container
	cnc_academy_logo : cnc_academy_logo
	url_label : url_label
	next_button : next_button

	BoxLayout: 
		size_hint: (None,None)
		width: dp(1.0*app.width)
		height: dp(1.0*app.height)
		orientation: 'vertical'
		canvas:
			Color:
				rgba: hex('#e5e5e5')
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
					id: title_label
					size_hint: (None,None)
					height: dp(0.125*app.height)
					width: dp(1.0*app.width)
					color: hex('#f9f9f9ff')
					# color: hex('#333333ff') #grey
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
				orientation: 'vertical'
				
				Label:
					id: cnc_academy_info
					font_size: str(0.0375*app.width) + 'sp'
					text_size: self.size
					valign: 'bottom'
					halign: 'center'
					markup: 'true'
					color: hex('#333333ff')
					size: self.texture_size

				BoxLayout:
					orientation: 'horizontal'
					width: dp(1.0*app.width)
					height: dp(0.416666666667*app.height)
					padding:[dp(0.025)*app.width, dp(0.0416666666667)*app.height, dp(0.025)*app.width, 0]
					size_hint: (None,None)
					spacing: 0
					BoxLayout:
						id: qr_code_container
						padding:[dp(0.0125)*app.width, 0, 0, 0]
						# width: dp(162)
						# height: dp(180)
						# size_hint: (None,None)
						size_hint_x: 0.21
						Image:
							id: qr_code_image
							source: "./asmcnc/apps/start_up_sequence/warranty_app/img/academy-qr-code.png"
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
							padding:[dp(0.0125)*app.width, dp(0.00416666666667)*app.height, dp(0.0125)*app.width, 0]

							Image:
								id: cnc_academy_logo
								source: "./asmcnc/apps/start_up_sequence/warranty_app/img/cnc_academy_logo.png"
								center_x: self.parent.center_x
								y: self.parent.y
								size: self.parent.width, self.parent.height
								allow_stretch: True
						Label:
							id: url_label
							size_hint_y: 0.25
							font_size: str(0.03125*app.width) + 'sp'
							text_size: self.size
							valign: 'top'
							halign: 'center'
							markup: 'true'
							multiline: True
							color: hex('#333333ff')
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
					Button:
					    font_size: str(0.01875 * app.width) + 'sp'
						size_hint: (None,None)
						height: dp(0.108333333333*app.height)
						width: dp(0.075*app.width)
						background_color: color_provider.get_rgba("invisible")
						center: self.parent.center
						pos: self.parent.pos
						on_press: root.prev_screen()
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
				BoxLayout: 
					size_hint: (None, None)
					height: dp(0.254166666667*app.height)
					width: dp(0.305625*app.width)
					padding:[dp(0.241875)*app.width, 0, 0, 0]
"""
)


class WarrantyScreen5(Screen):
    def __init__(self, **kwargs):
        super(WarrantyScreen5, self).__init__(**kwargs)
        self.start_seq = kwargs["start_sequence"]
        self.m = kwargs["machine"]
        self.l = kwargs["localization"]
        self.update_strings()

    def next_screen(self):
        self.start_seq.next_in_sequence()

    def prev_screen(self):
        self.start_seq.prev_in_sequence()

    def update_strings(self):
        self.title_label.text = self.l.get_str("CNC Academy")
        self.cnc_academy_info.text = self.l.get_bold(
            "Visit Yeti Tool CNC Academy for video tutorials on how to get started."
        )
        self.url_label.text = "https://academy.yetitool.com"
        self.next_button.text = self.l.get_str("Next") + "..."
