from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.clock import Clock
from asmcnc.skavaUI import popup_info
from asmcnc.skavaUI import widget_status_bar

import datetime
import os, sys

Builder.load_string("""
<ZHeadQC7>:
    disconnect_button:disconnect_button
    cycle_button:cycle_button
    status_container : status_container

    BoxLayout:
        orientation: 'vertical'

        BoxLayout:
            orientation: 'vertical'
            size_hint_y: 0.92
            spacing: dp(15)

            GridLayout:
                cols: 2
                rows: 1
                size_hint_y: 0.35
                valign: 'top'

                Button:
                    text: '<<< Back'
                    on_press: root.enter_prev_screen()
                    text_size: self.size
                    markup: 'True'
                    halign: 'left'
                    valign: 'middle'
                    padding: [dp(10),0]
                    font_size: dp(20)

                Label:
                    text: ''

            GridLayout:
                cols: 3
                spacing: dp(5)

                Button:
                    text: 'Home'
                    background_color: [1,1,0,1]
                    background_normal: ''
                    color: color_provider.get_rgba("black")
                    font_size: dp(30)
                    on_press: root.home()

                Button:
                    text: 'Reset'
                    background_color: [1,1,0,1]
                    background_normal: ''
                    color: color_provider.get_rgba("black")
                    font_size: dp(30)
                    on_press: root.resume_from_alarm()

                Button:
                    id: cycle_button
                    text: 'Cycle Z (3x)'
                    background_color: color_provider.get_rgba("monochrome_green"),0,1]
                    background_normal: ''
                    color: color_provider.get_rgba("black")
                    font_size: dp(30)
                    on_press: root.do_cycle()

            Button:
                id: disconnect_button
                text: 'Cycle finished - go to next screen'
                font_size: dp(30)
                size_hint_y: 0.55
                disabled: True
                on_press: root.enter_next_screen()

        # GREEN STATUS BAR

        BoxLayout:
            size_hint_y: 0.08
            id: status_container
            pos: self.pos

""")

class ZHeadQC7(Screen):
    def __init__(self, **kwargs):
        super(ZHeadQC7, self).__init__(**kwargs)

        self.sm = kwargs['sm']
        self.m = kwargs['m']
        self.l = kwargs['l']

        # Green status bar
        self.status_bar_widget = widget_status_bar.StatusBar(machine=self.m, screen_manager=self.sm)
        self.status_container.add_widget(self.status_bar_widget)

    def on_enter(self):
        self.disconnect_button.disabled = True
        self.cycle_button.disabled = True
        Clock.schedule_once(self.enable_buttons, 2)

    def enable_buttons(self, dt):
        self.disconnect_button.disabled = False
        self.cycle_button.disabled = False

    def home(self):
        self.m.is_machine_completed_the_initial_squaring_decision = True
        self.m.is_squaring_XY_needed_after_homing = False
        self.m.request_homing_procedure('qc7','qc7')

    def resume_from_alarm(self):
        self.m.resume_from_alarm()

    def do_cycle(self):
        self.m.s.write_command('G53 G0 Z-' + str(self.m.grbl_z_max_travel))
        self.m.s.write_command('G53 G0 Z-1')
        self.m.s.write_command('G53 G0 Z-' + str(self.m.grbl_z_max_travel))
        self.m.s.write_command('G53 G0 Z-1')
        self.m.s.write_command('G53 G0 Z-' + str(self.m.grbl_z_max_travel))
        self.m.s.write_command('G53 G0 Z-1')

    def enter_prev_screen(self):
        self.sm.current = 'qc6'

    def enter_next_screen(self):
        self.sm.current = 'qc8'
