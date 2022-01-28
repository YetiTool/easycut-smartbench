from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.clock import Clock
import datetime

from asmcnc.skavaUI import widget_status_bar

Builder.load_string("""
<ZHeadQC2>:
    calibrate_button:calibrate_button
    console_status_text:console_status_text
    status_container:status_container
    cycle_z_head_button:cycle_z_head_button
    home_button:home_button
    reset_button:reset_button

    BoxLayout:
        orientation: 'vertical'
        size_hint_y: 0.92

        GridLayout:
            size: self.parent.size
            pos: self.parent.pos
            cols: 3
            rows: 5

            Button:
                text: '16. Enable alarms'
                text_size: self.size
                markup: 'True'
                halign: 'left'
                valign: 'middle'
                padding: [dp(10),0]

            Label: 
                text: '21. Plug in USB "spindle"'
                text_size: self.size
                markup: 'True'
                halign: 'left'
                valign: 'middle'
                padding: [dp(10),0]

            Button:
                text: 'STOP'
                background_color: [1,0,0,1]
                text_size: self.size
                markup: 'True'
                halign: 'left'
                valign: 'middle'
                padding: [dp(10),0]

            Button:
                text: '17. Set spindle to digital'
                text_size: self.size
                markup: 'True'
                halign: 'left'
                valign: 'middle'
                padding: [dp(10),0]

            Button:
                text: '22. Set spindle to analogue'
                text_size: self.size
                markup: 'True'
                halign: 'left'
                valign: 'middle'
                padding: [dp(10),0]

            Button:
                id: calibrate_button
                disabled: 'True'
                text: '26. Wait for '
                text_size: self.size
                markup: 'True'
                halign: 'left'
                valign: 'middle'
                padding: [dp(10),0]

            Label:
                text: '18. Plug in digital spindle'
                text_size: self.size
                markup: 'True'
                halign: 'left'
                valign: 'middle'
                padding: [dp(10),0]

            GridLayout:
                cols: 2

                Button:
                    text: '23. Test USB "spindle"'
                    text_size: self.size
                    markup: 'True'
                    halign: 'left'
                    valign: 'middle'
                    padding: [dp(10),0]

                Image:
                    id: x_home_check
                    source: "./asmcnc/skavaUI/img/checkbox_inactive.png"
                    center_x: self.parent.center_x
                    y: self.parent.y
                    size: self.parent.width, self.parent.height
                    allow_stretch: True

            Label:
                text: '27. PUT BELT ON Z MOTOR'
                text_size: self.size
                markup: 'True'
                halign: 'left'
                valign: 'middle'
                padding: [dp(10),0]

            GridLayout:
                cols: 2

                Button:
                    text: '19. Test digital spindle'
                    text_size: self.size
                    markup: 'True'
                    halign: 'left'
                    valign: 'middle'
                    padding: [dp(10),0]

                Image:
                    id: x_home_check
                    source: "./asmcnc/skavaUI/img/checkbox_inactive.png"
                    center_x: self.parent.center_x
                    y: self.parent.y
                    size: self.parent.width, self.parent.height
                    allow_stretch: True

            Label:
                text: '24. Remove USB "spindle"'
                text_size: self.size
                markup: 'True'
                halign: 'left'
                valign: 'middle'
                padding: [dp(10),0]

            GridLayout:
                cols: 2

                Button:
                    id: home_button
                    text: '28. HOME'
                    text_size: self.size
                    markup: 'True'
                    halign: 'left'
                    valign: 'middle'
                    padding: [dp(10),0]
                    disabled: 'True'

                Button: 
                    id: reset_button
                    text: '29. RESET'
                    text_size: self.size
                    markup: 'True'
                    halign: 'left'
                    valign: 'middle'
                    padding: [dp(10),0]
                    disabled: 'True'

            Label: 
                text: '20. Remove digital spindle'
                text_size: self.size
                markup: 'True'
                halign: 'left'
                valign: 'middle'
                padding: [dp(10),0]

            Label: 
                text: '25. TAKE BELT OFF Z MOTOR'
                text_size: self.size
                markup: 'True'
                halign: 'left'
                valign: 'middle'
                padding: [dp(10),0]

            Button:
                id: cycle_z_head_button
                text: '30. Cycle Z Head'
                text_size: self.size
                markup: 'True'
                halign: 'left'
                valign: 'middle'
                padding: [dp(10),0]
                disabled: 'True'

        ScrollableLabelStatus:
            size_hint_y: 0.2        
            id: console_status_text
            text: "status update" 
    
    BoxLayout:
        size_hint_y: 0.08
        id: status_container 
        pos: self.pos
""")

class ZHeadQC2(Screen):
    def __init__(self, **kwargs):
        super(ZHeadQC2, self).__init__(**kwargs)

        self.sm = kwargs['sm']
        self.m = kwargs['m']

        self.poll_for_status = Clock.schedule_interval(self.update_status_text, 0.4) 
        self.status_bar_widget = widget_status_bar.StatusBar(machine=self.m, screen_manager=self.sm)
        self.status_container.add_widget(self.status_bar_widget)

    def enter_prev_screen(self):
        self.sm.current = 'qc1'

    def enable_button(self, dt):
        self.calibrate_button.disabled = False
        self.cycle_z_head_button.disabled = False
        self.home_button.disabled = False
        self.reset_button.disabled = False

    def update_time(self, time_left):
        seconds = time_left

        def count_down(seconds):
            if seconds == 0:
                self.calibrate_button.background_color = [0,1,0,1]
                return
            
            seconds -= 1

            self.calibrate_button.text = '26. WAIT ' + str(datetime.timedelta(seconds=seconds)) + ' TO CALIBRATE'

            Clock.schedule_once(lambda dt: count_down(seconds), 1)

        Clock.schedule_once(lambda dt: count_down(seconds), 0)

    def update_status_text(self, dt):
        try:
            self.consoleStatusText.text = self.sm.get_screen('home').gcode_monitor_widget.consoleStatusText
        except:
            pass