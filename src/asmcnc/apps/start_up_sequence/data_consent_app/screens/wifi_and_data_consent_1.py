from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from asmcnc.skavaUI import popup_info
Builder.load_string(
    """

<WiFiAndDataConsentScreen1>

	header_label : header_label
	we_will_collect : we_will_collect
	we_wont_collect : we_wont_collect
	job_critical_events : job_critical_events
	maintenance_data : maintenance_data
	ip_address : ip_address
	console_hostname : console_hostname
	g_code_files : g_code_files
	wifi_network_details : wifi_network_details
	serial_numbers : serial_numbers
	prev_screen_button : prev_screen_button
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
				padding: [0.025*app.width,0.0208333333333*app.height,0.025*app.width,0.0375*app.height]
				spacing: dp(0.0208333333333*app.height)
				orientation: 'vertical'

				Label: 
					id: we_will_collect
					size_hint: (None, None)
					height: dp(0.104166666667*app.height)
					width: dp(0.925*app.width)
					# color: hex('#f9f9f9ff') # white
					color: hex('#333333ff') #grey
					font_size: dp(0.0225*app.width)
					halign: "left"
					valign: "top"
					markup: True
					text_size: self.size

				GridLayout: 
					cols: 2
					rows: 2
					size_hint: (None, None)
					height: dp(0.166666666667*app.height)
					width: dp(0.925*app.width)

					# Row 1 Col 1
					BoxLayout: 
						padding: dp(0.0125*app.width), dp(0)
						spacing: dp(0.0125*app.width)
						orientation: 'horizontal'

						BoxLayout: 
							size_hint_x: None
							width: dp(0.0375*app.width)
			                Image:
			                    source: "./asmcnc/apps/start_up_sequence/data_consent_app/img/green_tick.png"
			                    allow_stretch: True

	                    Label: 
	                    	id: job_critical_events
	                    	# color: hex('#f9f9f9ff') # white
	                    	color: hex('#333333ff') #grey
	                    	font_size: dp(0.0225*app.width)
	                    	halign: "left"
	                    	valign: "middle"
	                    	markup: True
	                    	text_size: self.size

					# Row 1 Col 2
					BoxLayout: 
						padding: dp(0.0125*app.width), dp(0)
						spacing: dp(0.0125*app.width)
						orientation: 'horizontal'

						BoxLayout: 
							size_hint_x: None
							width: dp(0.0375*app.width)
			                Image:
			                    source: "./asmcnc/apps/start_up_sequence/data_consent_app/img/green_tick.png"
			                    allow_stretch: True

	                    Label: 
	                    	id: maintenance_data
	                    	# color: hex('#f9f9f9ff') # white
	                    	color: hex('#333333ff') #grey
	                    	font_size: dp(0.0225*app.width)
	                    	halign: "left"
	                    	valign: "middle"
	                    	markup: True
	                    	text_size: self.size

					# Row 2 Col 1
					BoxLayout: 
						padding: dp(0.0125*app.width), dp(0)
						spacing: dp(0.0125*app.width)
						orientation: 'horizontal'

						BoxLayout: 
							size_hint_x: None
							width: dp(0.0375*app.width)
			                Image:
			                    source: "./asmcnc/apps/start_up_sequence/data_consent_app/img/green_tick.png"
			                    allow_stretch: True

	                    Label: 
	                    	id: ip_address
	                    	# color: hex('#f9f9f9ff') # white
	                    	color: hex('#333333ff') #grey
	                    	font_size: dp(0.0225*app.width)
	                    	halign: "left"
	                    	valign: "middle"
	                    	markup: True
	                    	text_size: self.size

					# Row 2 Col 2
					BoxLayout: 
						padding: dp(0.0125*app.width), dp(0)
						spacing: dp(0.0125*app.width)
						orientation: 'horizontal'

						BoxLayout: 
							size_hint_x: None
							width: dp(0.0375*app.width)
			                Image:
			                    source: "./asmcnc/apps/start_up_sequence/data_consent_app/img/green_tick.png"
			                    allow_stretch: True

	                    Label: 
	                    	id: console_hostname
	                    	# color: hex('#f9f9f9ff') # white
	                    	color: hex('#333333ff') #grey
	                    	font_size: dp(0.0225*app.width)
	                    	halign: "left"
	                    	valign: "middle"
	                    	markup: True
	                    	text_size: self.size

	            BoxLayout: 
					size_hint: (None, None)
					height: dp(0.0625*app.height)
					width: dp(0.925*app.width)
					padding: [0.0*app.width,0.0*app.height,0.0*app.width,0.0*app.height]

					Label: 
						id: we_wont_collect
						size_hint: (None, None)
						height: dp(0.0625*app.height)
						width: dp(0.925*app.width)
						# color: hex('#f9f9f9ff') # white
						color: hex('#333333ff') #grey
						font_size: dp(0.0225*app.width)
						halign: "left"
						valign: "bottom"
						markup: True
						text_size: self.size

				GridLayout: 
					cols: 2
					rows: 2
					size_hint: (None, None)
					height: dp(0.166666666667*app.height)
					width: dp(0.925*app.width)

					# Row 1 Col 1
					BoxLayout: 
						padding: dp(0.0125*app.width), dp(0)
						spacing: dp(0.0125*app.width)
						orientation: 'horizontal'

						BoxLayout: 
							size_hint_x: None
							width: dp(0.0375*app.width)
			                Image:
			                    source: "./asmcnc/apps/start_up_sequence/data_consent_app/img/red_cross.png"
			                    allow_stretch: True

	                    Label: 
	                    	id: g_code_files
	                    	# color: hex('#f9f9f9ff') # white
	                    	color: hex('#333333ff') #grey
	                    	font_size: dp(0.0225*app.width)
	                    	halign: "left"
	                    	valign: "middle"
	                    	markup: True
	                    	text_size: self.size

					# Row 1 Col 2
					BoxLayout: 
						padding: dp(0.0125*app.width), dp(0)
						spacing: dp(0.0125*app.width)
						orientation: 'horizontal'

						BoxLayout: 
							size_hint_x: None
							width: dp(0.0375*app.width)
			                Image:
			                    source: "./asmcnc/apps/start_up_sequence/data_consent_app/img/red_cross.png"
			                    allow_stretch: True

	                    Label: 
	                    	id: wifi_network_details
	                    	# color: hex('#f9f9f9ff') # white
	                    	color: hex('#333333ff') #grey
	                    	font_size: dp(0.0225*app.width)
	                    	halign: "left"
	                    	valign: "middle"
	                    	markup: True
	                    	text_size: self.size

					# Row 2 Col 1
					BoxLayout: 
						padding: dp(0.0125*app.width), dp(0)
						spacing: dp(0.0125*app.width)
						orientation: 'horizontal'

						BoxLayout: 
							size_hint_x: None
							width: dp(0.0375*app.width)
			                Image:
			                    source: "./asmcnc/apps/start_up_sequence/data_consent_app/img/red_cross.png"
			                    allow_stretch: True

	                    Label: 
	                    	id: serial_numbers
	                    	# color: hex('#f9f9f9ff') # white
	                    	color: hex('#333333ff') #grey
	                    	font_size: dp(0.0225*app.width)
	                    	halign: "left"
	                    	valign: "middle"
	                    	markup: True
	                    	text_size: self.size

					# Row 2 Col 2
					BoxLayout: 
						padding: dp(0.0125*app.width), dp(0)
						spacing: dp(0.0125*app.width)
						orientation: 'horizontal'



			# FOOTER
			BoxLayout: 
				padding: [0.0125*app.width,0,0.0125*app.width,0.0208333333333*app.height]
				size_hint: (None, None)
				height: dp(0.254166666667*app.height)
				width: dp(1.0*app.width)
				orientation: 'horizontal'
				BoxLayout: 
					size_hint: (None, None)
					height: dp(0.254166666667*app.height)
					width: dp(0.305625*app.width)
					padding: [0, 0,0.230625*app.width, 0]
					Button:
						id: prev_screen_button
						size_hint: (None,None)
						height: dp(0.108333333333*app.height)
						width: dp(0.075*app.width)
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
					height: dp(0.254166666667*app.height)
					width: dp(0.36375*app.width)
					padding: [0,0,0,0.0666666666667*app.height]
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
					padding: [0.241875*app.width, 0, 0, 0]

"""
    )


class WiFiAndDataConsentScreen1(Screen):

    def __init__(self, **kwargs):
        super(WiFiAndDataConsentScreen1, self).__init__(**kwargs)
        self.start_seq = kwargs['start_sequence']
        self.c = kwargs['consent_manager']
        self.l = kwargs['localization']
        self.update_strings()

    def next_screen(self):
        try:
            self.start_seq.next_in_sequence()
        except:
            self.c.sm.current = 'consent_2'

    def prev_screen(self):
        try:
            self.start_seq.prev_in_sequence()
        except:
            self.c.back_to_previous_screen()

    def update_strings(self):
        self.header_label.text = self.l.get_str('Wi-Fi and Data Consent')
        self.we_will_collect.text = self.l.get_bold(
            'To keep improving our services, we want to collect data from your SmartBench. '
             + 'With your consent, we will collect the following data:')
        self.we_wont_collect.text = self.l.get_bold(
            'We will NEVER collect the following from your Console:')
        self.job_critical_events.text = self.l.get_str('Job critical events')
        self.maintenance_data.text = self.l.get_str('Maintenance data')
        self.ip_address.text = self.l.get_str('IP address')
        self.console_hostname.text = self.l.get_str('Console hostname')
        self.g_code_files.text = self.l.get_str('G-Code files')
        self.wifi_network_details.text = self.l.get_str('Wi-Fi network details'
            )
        self.serial_numbers.text = self.l.get_str('Serial numbers')
        self.next_button.text = self.l.get_str('Next') + '...'
