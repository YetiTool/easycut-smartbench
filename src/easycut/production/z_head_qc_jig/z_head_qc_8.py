from asmcnc.comms.logging_system.logging_system import Logger
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.clock import Clock
from asmcnc.skavaUI import widget_status_bar

import datetime

Builder.load_string("""
<ZHeadQC8>:
    status_container:status_container
    connect_button:connect_button

    BoxLayout:
        orientation: 'vertical'

        BoxLayout:
            orientation: 'vertical'
            size_hint_y: 0.92

            Button:
                text: '<<< Back'
                on_press: root.enter_prev_screen()
                text_size: self.size
                markup: 'True'
                halign: 'left'
                valign: 'middle'
                padding: [dp(10),0]
                size_hint_y: 0.2
                size_hint_x: 0.5
                font_size: dp(20)

            GridLayout:
                rows: 2
                padding: [dp(0), dp(10)]
                spacing: dp(10)

                Button:
                    text: 'Disconnect'
                    font_size: dp(30)
                    on_press: root.disconnect()

                Button:
                    id: connect_button
                    text: 'Connect and Restart'
                    font_size: dp(30)
                    on_press: root.connect_and_restart()
                    disabled: True

        # GREEN STATUS BAR

        BoxLayout:
            size_hint_y: 0.08
            id: status_container
            pos: self.pos

""")

class ZHeadQC8(Screen):
    def __init__(self, **kwargs):
        super(ZHeadQC8, self).__init__(**kwargs)

        self.sm = kwargs['sm']
        self.m = kwargs['m']

        # Green status bar
        self.status_bar_widget = widget_status_bar.StatusBar(machine=self.m, screen_manager=self.sm)
        self.status_container.add_widget(self.status_bar_widget)

    def disconnect(self):
        Logger.debug("Disconnect button pressed")
        self.m.s.grbl_scanner_running = False
        Clock.schedule_once(self.m.close_serial_connection, 0.1)
        self.connect_button.disabled = False

    def connect_and_restart(self):
        Logger.debug("Connect button pressed")
        if not self.m.starting_serial_connection:
            self.m.starting_serial_connection = True
            self.m.s.grbl_scanner_running = False
            Clock.schedule_once(self.do_connection, 0.1)
            self.connect_button.text = 'Connecting...'
            self.connect_button.disabled = True

    def do_connection(self, dt):
        self.m.reconnect_serial_connection()
        self.poll_for_reconnection = Clock.schedule_interval(self.try_start_services, 0.4)

    def try_start_services(self, dt):
        if self.m.s.is_connected():
            Clock.unschedule(self.poll_for_reconnection)
            Clock.schedule_once(self.m.s.start_services, 1)
            # hopefully 1 second should always be enough to start services
            Clock.schedule_once(self.back_to_start, 2)

    def back_to_start(self, dt):
        self.sm.get_screen('qc1').reset_checkboxes()
        self.sm.get_screen('qc2').reset_checkboxes()
        self.sm.get_screen('qcW136').reset_checkboxes()
        self.sm.get_screen('qcW112').reset_checkboxes()
        self.sm.get_screen('qc3').reset_timer()
        self.sm.current = 'qcconnecting'
        self.connect_button.text = 'Connect and Restart'

    def enter_prev_screen(self):
        self.sm.current = 'qc7'
