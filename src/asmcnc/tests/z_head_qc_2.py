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

            Label: 
                text: '21. Plug in USB "spindle"'

            Button:
                text: 'STOP'
                background_color: [1,0,0,1]

            Button:
                text: '17. Set spindle to digital'

            Button:
                text: '22. Set spindle to analogue'

            Button:
                id: calibrate_button
                disabled: 'True'
                text: '26. Wait for '

            Label:
                text: '18. Plug in digital spindle'

            GridLayout:
                cols: 2

                Button:
                    text: '23. Test USB "spindle"'
                    text_size: self.width, None
                    halign: 'center'

                Image:
                    id: x_home_check
                    source: "./asmcnc/skavaUI/img/checkbox_inactive.png"
                    center_x: self.parent.center_x
                    y: self.parent.y
                    size: self.parent.width, self.parent.height
                    allow_stretch: True

            Label:
                text: '27. PUT BELT ON Z MOTOR'

            GridLayout:
                cols: 2

                Button:
                    text: '19. Test digital spindle'
                    text_size: self.width, None
                    halign: 'center'

                Image:
                    id: x_home_check
                    source: "./asmcnc/skavaUI/img/checkbox_inactive.png"
                    center_x: self.parent.center_x
                    y: self.parent.y
                    size: self.parent.width, self.parent.height
                    allow_stretch: True

            Label:
                text: '24. Remove USB "spindle"'

            GridLayout:
                cols: 2

                Button: 
                    text: '28. Home'

                Button: 
                    text: '29. RESET'

            Label: 
                text: '20. Remove digital spindle'

            Label: 
                text: '25. TAKE BELT OFF Z MOTOR'

            Button:
                text: '30. Cycle Z Head'

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

    def update_time(self, time_left):
        seconds = time_left

        def count_down(seconds):
            if seconds == 0:
                self.calibrate_button.background_color = [0,1,0,1]
                return
            
            seconds -= 1

            self.calibrate_button.text = '26. Wait ' + str(datetime.timedelta(seconds=seconds)) + ' to calibrate'

            Clock.schedule_once(lambda dt: count_down(seconds), 1)

        Clock.schedule_once(lambda dt: count_down(seconds), 0)

    def update_status_text(self, dt):
        try:
            self.consoleStatusText.text = self.sm.get_screen('home').gcode_monitor_widget.consoleStatusText
        except:
            pass