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

    BoxLayout:
        orientation: 'vertical'
        size_hint_y: 0.92

        GridLayout:
            size: self.parent.size
            pos: self.parent.pos
            cols: 3
            rows: 5

            GridLayout:
                cols: 2

                Label:
                    text: '18. Z Home'

                Image:
                    id: x_home_check
                    source: "./asmcnc/skavaUI/img/checkbox_inactive.png"
                    center_x: self.parent.center_x
                    y: self.parent.y
                    size: self.parent.width, self.parent.height
                    allow_stretch: True

            Label: 
                text: '23. Remove digital spindle'

            Button:
                text: 'STOP'
                background_color: [1,0,0,1]

            Button:
                text: '19. Enable alarms'

            Label: 
                text: '24. Plug in USB "spindle"'

            Label: 
                text: '28. TAKE BELT OFF Z MOTOR'

            Button:
                text: '20. Set spindle to digital'

            Button:
                text: '25. Set spindle to analogue'

            Button:
                id: calibrate_button
                disabled: 'True'
                text: '29. Wait for '

            Label:
                text: '21. Plug in digital spindle'

            GridLayout:
                cols: 2

                Button:
                    text: '26. Test USB "spindle"'
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
                text: '30. PUT BELT ON Z MOTOR'

            GridLayout:
                cols: 2

                Button:
                    text: '22. Test digital spindle'
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
                text: '27. Remove USB "spindle"'

            Button:
                text: '31. Cycle Z Head'
    
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

            self.calibrate_button.text = 'Wait ' + str(datetime.timedelta(seconds=seconds)) + ' to calibrate'

            Clock.schedule_once(lambda dt: count_down(seconds), 1)

        Clock.schedule_once(lambda dt: count_down(seconds), 0)