from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.clock import Clock

from asmcnc.skavaUI import widget_status_bar, popup_info
from asmcnc.comms import serial_connection

Builder.load_string("""
<ZHeadCycle>:

    status_container:status_container
    console_status_text:console_status_text
    connection_status_label:connection_status_label

    BoxLayout:
        orientation: 'vertical'

        BoxLayout:
            size_hint_y: 0.92
            orientation: 'vertical'
            padding: [dp(10), dp(50)]
            spacing: dp(10)

            GridLayout:
                cols: 3
                spacing: dp(5)

                Button:
                    text: 'Connect'
                    on_press: root.connect()

                BoxLayout:
                    orientation: 'vertical'
                    spacing: dp(5)

                    GridLayout:
                        cols: 2
                        spacing: dp(5)

                        Button:
                            text: 'Home'
                            background_color: [1,1,0,1]
                            background_normal: ''
                            color: [0,0,0,1]
                            on_press: root.home()

                        Button:
                            text: 'Reset'
                            background_color: [1,1,0,1]
                            background_normal: ''
                            color: [0,0,0,1]
                            on_press: root.resume_from_alarm()

                    Button:
                        text: 'Cycle Z (10x)'
                        background_color: [0,1,0,1]
                        background_normal: ''
                        color: [0,0,0,1]
                        on_press: root.do_cycle()

                Button:
                    text: 'Disconnect'
                    on_press: root.disconnect()

            GridLayout:
                cols: 2
                spacing: dp(10)

                GridLayout:
                    rows: 2

                    Label:
                        id: connection_status_label
                        text: 'Connection status: '
                        size_hint_y: 0.5
                        markup: True
                        font_size: dp(30)

                    # RECIEVED STATUS MONITOR
                    ScrollableLabelStatus:
                        id: console_status_text
                        text: "status update"

                Button:
                    text: 'STOP'
                    background_color: [1,0,0,1]
                    background_normal: ''
                    size_hint_x: 0.25
                    on_press: root.stop()

        # GREEN STATUS BAR
        BoxLayout:
            size_hint_y: 0.08
            id: status_container 
            pos: self.pos

""")

Cmport = 'COM3'

class ZHeadCycle(Screen):
    def __init__(self, **kwargs):
        super(ZHeadCycle, self).__init__(**kwargs)

        self.sm = kwargs['sm']
        self.m = kwargs['m']
        self.l = kwargs['l']
        self.sett = kwargs['sett']
        self.jd = kwargs['jd']

        # Green status bar
        self.status_bar_widget = widget_status_bar.StatusBar(machine=self.m, screen_manager=self.sm)
        self.status_container.add_widget(self.status_bar_widget)

        self.poll_for_status = Clock.schedule_interval(self.update_status_text, 0.4)       # Status monitor widget
        self.poll_for_connection_status = Clock.schedule_interval(self.update_connection_status_text, 0.4)

    def update_status_text(self, dt):
        try:
            self.console_status_text.text = self.sm.get_screen('home').gcode_monitor_widget.consoleStatusText.text

        except: 
            pass

    def update_connection_status_text(self, dt):
        try:
            if self.m.s.s.isOpen():
                self.connection_status_label.text = 'Connection status: [color=00ff00]Connected[/color]'
            else:
                self.connection_status_label.text = 'Connection status: [color=ff0000]Disconnected[/color]'
        except:
            self.connection_status_label.text = 'Connection status: [color=ffff00]COM Port not found[/color]'

    def home(self):
        self.m.is_machine_completed_the_initial_squaring_decision = True
        self.m.is_squaring_XY_needed_after_homing = False
        self.m.request_homing_procedure('cycle','cycle')

    def resume_from_alarm(self):
        self.m.resume_from_alarm()

    def do_cycle(self):
        self.m.s.write_command('G53 G0 Z-150')
        self.m.s.write_command('G53 G0 Z-1')
        self.m.s.write_command('G53 G0 Z-150')
        self.m.s.write_command('G53 G0 Z-1')
        self.m.s.write_command('G53 G0 Z-150')
        self.m.s.write_command('G53 G0 Z-1')
        self.m.s.write_command('G53 G0 Z-150')
        self.m.s.write_command('G53 G0 Z-1')
        self.m.s.write_command('G53 G0 Z-150')
        self.m.s.write_command('G53 G0 Z-1')
        self.m.s.write_command('G53 G0 Z-150')
        self.m.s.write_command('G53 G0 Z-1')
        self.m.s.write_command('G53 G0 Z-150')
        self.m.s.write_command('G53 G0 Z-1')
        self.m.s.write_command('G53 G0 Z-150')
        self.m.s.write_command('G53 G0 Z-1')
        self.m.s.write_command('G53 G0 Z-150')
        self.m.s.write_command('G53 G0 Z-1')
        self.m.s.write_command('G53 G0 Z-150')
        self.m.s.write_command('G53 G0 Z-1')

    def connect(self):
        if not self.m.starting_serial_connection:
            self.m.s.grbl_scanner_running = False
            Clock.schedule_once(self.do_connection, 0.1)

    def do_connection(self, dt):
        self.m.reconnect_serial_connection()
        self.poll_for_reconnection = Clock.schedule_interval(self.try_start_services, 0.4)

    def try_start_services(self, dt):
        if self.m.s.is_connected():
            Clock.unschedule(self.poll_for_reconnection)
            Clock.schedule_once(self.m.s.start_services, 1)

    def disconnect(self):
        self.m.s.grbl_scanner_running = False
        Clock.schedule_once(self.m.close_serial_connection, 0.1)

    def stop(self):
    	popup_info.PopupStop(self.m, self.sm, self.l)
