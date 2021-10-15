# -*- coding: utf-8 -*-

from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock

from asmcnc.skavaUI import popup_info

Builder.load_string("""

<WiFiAndDataConsentScreen1>

	we_will_collect : we_will_collect
	we_wont_collect : we_wont_collect
	job_critical_events : job_critical_events
	maintenance_data : maintenance_data
	ip_address : ip_address
	console_hostname : console_hostname
	g_code_files : g_code_files
	wifi_network_details : wifi_network_details
	serial_numbers : serial_numbers
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
				padding: [dp(20), dp(10), dp(20), dp(18)]
				spacing: dp(10)
				orientation: 'vertical'

				Label: 
					id: we_will_collect
					size_hint: (None, None)
					height: dp(50)
					width: dp(740)
					# color: hex('#f9f9f9ff') # white
					color: hex('#333333ff') #grey
					font_size: dp(18)
					halign: "left"
					valign: "top"
					markup: True
					text_size: self.size

				GridLayout: 
					cols: 2
					rows: 2
					size_hint: (None, None)
					height: dp(80)
					width: dp(740)

					# Row 1 Col 1
					BoxLayout: 
						padding: dp(10), dp(0)
						spacing: dp(10)
						orientation: 'horizontal'

						BoxLayout: 
							size_hint_x: None
							width: dp(30)
			                Image:
			                    source: "./asmcnc/core_UI/data_and_wifi/img/green_tick.png"
			                    allow_stretch: True

	                    Label: 
	                    	id: job_critical_events
	                    	# color: hex('#f9f9f9ff') # white
	                    	color: hex('#333333ff') #grey
	                    	font_size: dp(18)
	                    	halign: "left"
	                    	valign: "middle"
	                    	markup: True
	                    	text_size: self.size

					# Row 1 Col 2
					BoxLayout: 
						padding: dp(10), dp(0)
						spacing: dp(10)
						orientation: 'horizontal'

						BoxLayout: 
							size_hint_x: None
							width: dp(30)
			                Image:
			                    source: "./asmcnc/core_UI/data_and_wifi/img/green_tick.png"
			                    allow_stretch: True

	                    Label: 
	                    	id: maintenance_data
	                    	# color: hex('#f9f9f9ff') # white
	                    	color: hex('#333333ff') #grey
	                    	font_size: dp(18)
	                    	halign: "left"
	                    	valign: "middle"
	                    	markup: True
	                    	text_size: self.size

					# Row 2 Col 1
					BoxLayout: 
						padding: dp(10), dp(0)
						spacing: dp(10)
						orientation: 'horizontal'

						BoxLayout: 
							size_hint_x: None
							width: dp(30)
			                Image:
			                    source: "./asmcnc/core_UI/data_and_wifi/img/green_tick.png"
			                    allow_stretch: True

	                    Label: 
	                    	id: ip_address
	                    	# color: hex('#f9f9f9ff') # white
	                    	color: hex('#333333ff') #grey
	                    	font_size: dp(18)
	                    	halign: "left"
	                    	valign: "middle"
	                    	markup: True
	                    	text_size: self.size

					# Row 2 Col 2
					BoxLayout: 
						padding: dp(10), dp(0)
						spacing: dp(10)
						orientation: 'horizontal'

						BoxLayout: 
							size_hint_x: None
							width: dp(30)
			                Image:
			                    source: "./asmcnc/core_UI/data_and_wifi/img/green_tick.png"
			                    allow_stretch: True

	                    Label: 
	                    	id: console_hostname
	                    	# color: hex('#f9f9f9ff') # white
	                    	color: hex('#333333ff') #grey
	                    	font_size: dp(18)
	                    	halign: "left"
	                    	valign: "middle"
	                    	markup: True
	                    	text_size: self.size

	            BoxLayout: 
					size_hint: (None, None)
					height: dp(30)
					width: dp(740)
					padding: [dp(0), dp(10), dp(0), dp(0)]

					Label: 
						id: we_wont_collect
						size_hint: (None, None)
						height: dp(20)
						width: dp(740)
						# color: hex('#f9f9f9ff') # white
						color: hex('#333333ff') #grey
						font_size: dp(18)
						halign: "left"
						valign: "top"
						markup: True
						text_size: self.size

				GridLayout: 
					cols: 2
					rows: 2
					size_hint: (None, None)
					height: dp(80)
					width: dp(740)

					# Row 1 Col 1
					BoxLayout: 
						padding: dp(10), dp(0)
						spacing: dp(10)
						orientation: 'horizontal'

						BoxLayout: 
							size_hint_x: None
							width: dp(30)
			                Image:
			                    source: "./asmcnc/core_UI/data_and_wifi/img/red_cross.png"
			                    allow_stretch: True

	                    Label: 
	                    	id: g_code_files
	                    	# color: hex('#f9f9f9ff') # white
	                    	color: hex('#333333ff') #grey
	                    	font_size: dp(18)
	                    	halign: "left"
	                    	valign: "middle"
	                    	markup: True
	                    	text_size: self.size

					# Row 1 Col 2
					BoxLayout: 
						padding: dp(10), dp(0)
						spacing: dp(10)
						orientation: 'horizontal'

						BoxLayout: 
							size_hint_x: None
							width: dp(30)
			                Image:
			                    source: "./asmcnc/core_UI/data_and_wifi/img/red_cross.png"
			                    allow_stretch: True

	                    Label: 
	                    	id: wifi_network_details
	                    	# color: hex('#f9f9f9ff') # white
	                    	color: hex('#333333ff') #grey
	                    	font_size: dp(18)
	                    	halign: "left"
	                    	valign: "middle"
	                    	markup: True
	                    	text_size: self.size

					# Row 2 Col 1
					BoxLayout: 
						padding: dp(10), dp(0)
						spacing: dp(10)
						orientation: 'horizontal'

						BoxLayout: 
							size_hint_x: None
							width: dp(30)
			                Image:
			                    source: "./asmcnc/core_UI/data_and_wifi/img/red_cross.png"
			                    allow_stretch: True

	                    Label: 
	                    	id: serial_numbers
	                    	# color: hex('#f9f9f9ff') # white
	                    	color: hex('#333333ff') #grey
	                    	font_size: dp(18)
	                    	halign: "left"
	                    	valign: "middle"
	                    	markup: True
	                    	text_size: self.size

					# Row 2 Col 2
					BoxLayout: 
						padding: dp(10), dp(0)
						spacing: dp(10)
						orientation: 'horizontal'



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
					Button:
						size_hint: (None,None)
						height: dp(52)
						width: dp(60)
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
				BoxLayout: 
					size_hint: (None, None)
					height: dp(122)
					width: dp(244.5)
					padding: [193.5, 0, 0, 0]

""")

class WiFiAndDataConsentScreen1(Screen):

	def __init__(self, **kwargs):
		super(WiFiAndDataConsentScreen1, self).__init__(**kwargs)
		self.c=kwargs['consent_manager']
		self.l = kwargs['localization']
		self.update_strings()

	def next_screen(self):
		self.c.sm.current='consent_2'

	def prev_screen(self):
		self.c.back_to_previous_screen()

	def update_strings(self):
		self.we_will_collect.text = self.l.get_bold("To keep improving our services, we want to collect data from your SmartBench. " + \
			"With your consent, we will collect the following data:")
		self.we_wont_collect.text = self.l.get_bold("We will NEVER collect the following from your Console:")
		self.job_critical_events.text = self.l.get_str("Job critical events")
		self.maintenance_data.text = self.l.get_str("Maintenance data")
		self.ip_address.text = self.l.get_str("IP address")
		self.console_hostname.text = self.l.get_str("Console hostname")
		self.g_code_files.text = self.l.get_str("G-Code files")
		self.wifi_network_details.text = self.l.get_str("Wi-Fi network details")
		self.serial_numbers.text = self.l.get_str("Serial numbers")

		self.next_button.text = self.l.get_str("Next") + "..."
