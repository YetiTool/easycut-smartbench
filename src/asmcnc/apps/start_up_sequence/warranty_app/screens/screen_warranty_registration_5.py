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
		width: app.get_scaled_width(800.0)
		height: app.get_scaled_height(480.0)
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
					height: app.get_scaled_height(60.0)
					width: app.get_scaled_width(800.0)
					color: hex('#f9f9f9ff')
					# color: hex('#333333ff') #grey
					font_size: app.get_scaled_width(30.0)
					halign: "center"
					valign: "bottom"
					markup: True

			# BODY
			BoxLayout:
				size_hint: (None,None)
				width: app.get_scaled_width(800.0)
				height: app.get_scaled_height(298.0)
				padding: app.get_scaled_tuple([30.0, 10.0])
				orientation: 'vertical'
				
				Label:
					id: cnc_academy_info
					font_size: app.get_scaled_sp('30.0sp')
					text_size: self.size
					valign: 'bottom'
					halign: 'center'
					markup: 'true'
					color: hex('#333333ff')
					size: self.texture_size

				BoxLayout:
					orientation: 'horizontal'
					width: app.get_scaled_width(800.0)
					height: app.get_scaled_height(200.0)
					padding: app.get_scaled_tuple([20.0, 20.0, 20.0, 0.0])
					size_hint: (None,None)
					spacing: 0
					BoxLayout:
						id: qr_code_container
						padding: app.get_scaled_tuple([10.0, 0.0, 0.0, 0.0])
						# width: app.get_scaled_width(162)
						# height: app.get_scaled_height(180)
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
							padding: app.get_scaled_tuple([10.0, 2.0, 10.0, 0.0])

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
							font_size: app.get_scaled_sp('25.0sp')
							text_size: self.size
							valign: 'top'
							halign: 'center'
							markup: 'true'
							multiline: True
							color: hex('#333333ff')
			# FOOTER
			BoxLayout: 
				padding: app.get_scaled_tuple([10.0, 0.0, 10.0, 10.0])
				size_hint: (None, None)
				height: app.get_scaled_height(122.0)
				width: app.get_scaled_width(800.0)
				orientation: 'horizontal'
				BoxLayout: 
					size_hint: (None, None)
					height: app.get_scaled_height(122.0)
					width: app.get_scaled_width(244.5)
					padding: app.get_scaled_tuple([0.0, 0.0, 184.5, 0.0])
					Button:
					    font_size: app.get_scaled_sp('15.0sp')
						size_hint: (None,None)
						height: app.get_scaled_height(51.9999999998)
						width: app.get_scaled_width(60.0)
						background_color: hex('#F4433600')
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
					height: app.get_scaled_height(122.0)
					width: app.get_scaled_width(291.0)
					padding: app.get_scaled_tuple([0.0, 0.0, 0.0, 32.0])
					Button:
						id: next_button
						background_normal: "./asmcnc/skavaUI/img/next.png"
						background_down: "./asmcnc/skavaUI/img/next.png"
						border: app.get_scaled_tuple([14.5, 14.5, 14.5, 14.5])
						size_hint: (None,None)
						width: app.get_scaled_width(291.0)
						height: app.get_scaled_height(78.9999999998)
						on_press: root.next_screen()
						text: 'Next...'
						font_size: app.get_scaled_sp('30.0sp')
						color: hex('#f9f9f9ff')
						markup: True
						center: self.parent.center
						pos: self.parent.pos
				BoxLayout: 
					size_hint: (None, None)
					height: app.get_scaled_height(122.0)
					width: app.get_scaled_width(244.5)
					padding: app.get_scaled_tuple([193.5, 0.0, 0.0, 0.0])
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
