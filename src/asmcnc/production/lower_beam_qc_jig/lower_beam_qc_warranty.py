from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import  Button

from asmcnc.skavaUI import widget_status_bar, popup_info
from asmcnc.production.lower_beam_qc_jig.widget_lower_beam_qc_xy_move import LowerBeamQCXYMove
from asmcnc.core_UI import console_utils

import sys, os

Builder.load_string("""
<LowerBeamQCWarranty>:

	vac_toggle:vac_toggle
	spindle_toggle:spindle_toggle
	y_home_check:y_home_check
	y_max_check:y_max_check
	warranty_toggle:warranty_toggle

	xy_move_container: xy_move_container

	console_status_text : console_status_text
	status_container : status_container

	BoxLayout:
		orientation: 'vertical'
		BoxLayout:
			orientation: 'vertical'
			size_hint_y: 0.92

			BoxLayout:
				orientation: 'horizontal'
				size_hint_y: 0.85

				# COLUMN 1
				BoxLayout:
					orientation: 'vertical'

					Button:
						text: '1. Disable alarms'
						text_size: self.size
						halign: 'left'
						valign: 'middle'
						padding: [dp(10),0]
						on_press: root.disable_alarms()

					GridLayout:
						cols: 2
						Label:
							text: '2. Y max'
							text_size: self.size
							halign: 'left'
							valign: 'middle'
							padding: [dp(10),0]
						Image:
							id: y_max_check
							source: "./asmcnc/skavaUI/img/checkbox_inactive.png"
							center_x: self.parent.center_x
							y: self.parent.y
							size: self.parent.width, self.parent.height
							allow_stretch: True

					GridLayout:
						cols: 2
						Label:
							text: '3. Y home'
							text_size: self.size
							halign: 'left'
							valign: 'middle'
							padding: [dp(10),0]
						Image:
							id: y_home_check
							source: "./asmcnc/skavaUI/img/checkbox_inactive.png"
							center_x: self.parent.center_x
							y: self.parent.y
							size: self.parent.width, self.parent.height
							allow_stretch: True

					Button:
						text: '4. Enable alarms'
						text_size: self.size
						halign: 'left'
						valign: 'middle'
						padding: [dp(10),0]
						on_press: root.enable_alarms()

					GridLayout:
						cols: 2
						ToggleButton:
							id: vac_toggle
							text: '5. Extractor'
							text_size: self.size
							halign: 'left'
							valign: 'middle'
							padding: [dp(10),0]
							on_press: root.set_vac()

						ToggleButton:
							id: spindle_toggle
							text: '6. Spindle'
							text_size: self.size
							halign: 'left'
							valign: 'middle'
							padding: [dp(10),0]
							on_press: root.set_spindle()

				# COLUMN 2
				BoxLayout:
					orientation: 'vertical'

					GridLayout:
						cols: 2
						orientation: 'horizontal'

						BoxLayout:
							orientation: 'vertical'

							Label:
								text: 'DTI check'
								size_hint_y: 0.1

							BoxLayout:
								id: xy_move_container
								size_hint: (None,None)
								pos_hint: {'center_x': .5, 'center_y': .5}
								height: dp(270)
								width: dp(270)

						BoxLayout:
							orientation: 'vertical'
							size_hint_x: 0.25
							padding: [0,0,0,dp(150)]

							Button:
								text: 'OFF'
								text_size: self.size
								halign: 'left'
								valign: 'middle'
								padding: [dp(10),0]
								on_press: console_utils.shutdown()

							ToggleButton:
								id: warranty_toggle
								text: 'Test v1.2'
								text_size: self.size
								halign: 'left'
								valign: 'middle'
								padding: [dp(10),0]
								on_press: root.switch_screen()

					Button:
						text_size: self.size
						markup: 'True'
						halign: 'center'
						valign: 'middle'
						padding: [dp(10),0]
						text: 'STOP'
						background_color: [1,0,0,1]
						background_normal: ''
						size_hint_y: 0.25
						on_press: root.stop()

			# RECIEVED STATUS MONITOR
			ScrollableLabelStatus:
				size_hint_y: 0.15
				id: console_status_text
				text: "status update" 
		
		# GREEN STATUS BAR
		BoxLayout:
			size_hint_y: 0.08
			id: status_container 
			pos: self.pos

""")


class PopupMotorChipsTest(Widget):

	def __init__(self, screen_manager, report_string):

		self.sm = screen_manager

		# img = Image(source="./asmcnc/apps/shapeCutter_app/img/info_icon.png", allow_stretch=False)
		label1 = Label(size_hint_y=1, text_size=(None, None), markup=True, halign='left', valign='middle', text=report_string, color=[0,0,0,1], padding=[10,10])

		ok_button = Button(text='[b]Ok[/b]', markup = True)
		ok_button.background_normal = ''
		ok_button.background_color = [76 / 255., 175 / 255., 80 / 255., 1.]

		text_layout = BoxLayout(orientation='horizontal', spacing=0, padding=0)
		text_layout.add_widget(label1)

		btn_layout = BoxLayout(orientation='horizontal', spacing=15, padding=[150,10,150,0], size_hint_y = 0.3)
		btn_layout.add_widget(ok_button)

		layout_plan = BoxLayout(orientation='vertical', spacing=10, padding=[10,10,10,10])
		# layout_plan.add_widget(img)
		layout_plan.add_widget(text_layout)
		layout_plan.add_widget(btn_layout)

		popup = Popup(title='Output',
					  title_color=[0, 0, 0, 1],
					  title_size = '20sp',
					  content=layout_plan,
					  size_hint=(None, None),
					  size=(700, 400),
					  auto_dismiss= False
					  )

		popup.background = './asmcnc/apps/shapeCutter_app/img/popup_background.png'
		popup.separator_color = [249 / 255., 206 / 255., 29 / 255., 1.]
		popup.separator_height = '4dp'

		ok_button.bind(on_press=popup.dismiss)

		popup.open()


class LowerBeamQCWarranty(Screen):
	def __init__(self, **kwargs):
		super(LowerBeamQCWarranty, self).__init__(**kwargs)

		self.sm = kwargs['sm']
		self.m = kwargs['m']
		self.l = kwargs['l']

		# Movement widget
		self.xy_move_widget = LowerBeamQCXYMove(machine=self.m, screen_manager=self.sm, localization=self.l)
		self.xy_move_container.add_widget(self.xy_move_widget)

		# Green status bar
		self.status_bar_widget = widget_status_bar.StatusBar(machine=self.m, screen_manager=self.sm)
		self.status_container.add_widget(self.status_bar_widget)

		self.poll_for_status = Clock.schedule_interval(self.update_status_text, 0.4)       # Status monitor widget
		self.poll_for_checks = Clock.schedule_interval(self.update_checkboxes, 0.4)      # Poll for status

	def on_enter(self):
		self.warranty_toggle.state = 'down'

	def update_status_text(self, dt):
		try:
			self.console_status_text.text = self.sm.get_screen('home').gcode_monitor_widget.consoleStatusText.text

		except:
			pass

	def set_vac(self):
		if self.vac_toggle.state == 'normal':
			self.m.turn_off_vacuum()
		else:
			self.m.turn_on_vacuum()

	def set_spindle(self):
		if self.spindle_toggle.state == 'normal':
			self.m.turn_off_spindle()
		else:
			self.m.turn_on_spindle()

	def update_checkboxes(self, dt):
		self.y_home_switch()
		self.y_max_switch()

	def y_home_switch(self):
		if self.m.s.limit_y:
			self.y_home_check.source = "./asmcnc/skavaUI/img/file_select_select.png"
		else:
			self.y_home_check.source = "./asmcnc/skavaUI/img/checkbox_inactive.png"

	def y_max_switch(self):
		if self.m.s.limit_Y:
			self.y_max_check.source = "./asmcnc/skavaUI/img/file_select_select.png"
		else:
			self.y_max_check.source = "./asmcnc/skavaUI/img/checkbox_inactive.png"

	def disable_alarms(self):
		self.m.s.write_command('$21 = 0')

	def enable_alarms(self):
		self.m.s.write_command('$21 = 1')

	def switch_screen(self):
		self.sm.current = 'qc'

	def stop(self):
		popup_info.PopupStop(self.m, self.sm, self.l)
