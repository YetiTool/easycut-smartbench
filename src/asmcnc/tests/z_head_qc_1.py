from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.clock import Clock

from asmcnc.skavaUI import widget_status_bar
from functools import partial

Builder.load_string("""
<ZHeadQC1>:
    status_container:status_container

    BoxLayout:
        orientation: 'vertical'
        size_hint_y: 0.92

        GridLayout:
            size: self.parent.size
            pos: self.parent.pos
            cols: 3
            rows: 5
            spacing: dp(1)

            Label:
                text: 'FW Version: ...'

            GridLayout:
                cols: 2

                Label:
                    text: '7. Z Motors'

                GridLayout:
                    cols: 2

                    Button:
                        text: 'Up'
                    
                    Button: 
                        text: 'Down'

            Button:
                text: 'STOP'
                background_color: [1,0,0,1]

            Button:
                text: '2. Bake GRBL Settings'

            GridLayout:
                cols: 3

                Button: 
                    text: '8. Spindle'

                Button:
                    text: '9. Laser'

                Button:
                    text: '10. Vac'

            GridLayout:
                cols: 2

                Label:
                    text: '14. X Home'

                Image:
                    id: x_home_check
                    source: "./asmcnc/skavaUI/img/checkbox_inactive.png"
                    center_x: self.parent.center_x
                    y: self.parent.y
                    size: self.parent.width, self.parent.height
                    allow_stretch: True

            GridLayout:
                cols: 2

                Button: 
                    text: '3. Home'

                Button: 
                    text: '4. RESET'

            GridLayout:
                cols: 2

                Label:
                    text: '11. Dust shoe'

                GridLayout:
                    cols: 3

                    Button: 
                        text: 'R'

                    Button:
                        text: 'G'

                    Button:
                        text: 'B'

            GridLayout:
                cols: 2

                Label:
                    text: '15. X Max'

                Image:
                    id: x_home_check
                    source: "./asmcnc/skavaUI/img/checkbox_inactive.png"
                    center_x: self.parent.center_x
                    y: self.parent.y
                    size: self.parent.width, self.parent.height
                    allow_stretch: True

            GridLayout:
                cols: 2

                Button:
                    text: '5. Test motor chips'

                Image:
                    id: x_home_check
                    source: "./asmcnc/skavaUI/img/checkbox_inactive.png"
                    center_x: self.parent.center_x
                    y: self.parent.y
                    size: self.parent.width, self.parent.height
                    allow_stretch: True

            GridLayout:
                cols: 2

                Label:
                    text: '12. Temp/power'

                Image:
                    id: x_home_check
                    source: "./asmcnc/skavaUI/img/checkbox_inactive.png"
                    center_x: self.parent.center_x
                    y: self.parent.y
                    size: self.parent.width, self.parent.height
                    allow_stretch: True
            
            GridLayout:
                cols: 2

                Label:
                    text: '16. Probe'

                Image:
                    id: x_home_check
                    source: "./asmcnc/skavaUI/img/checkbox_inactive.png"
                    center_x: self.parent.center_x
                    y: self.parent.y
                    size: self.parent.width, self.parent.height
                    allow_stretch: True

            GridLayout:
                cols: 2

                Label:
                    text: '6. X Motors'

                GridLayout:
                    cols: 2

                    Button:
                        text: 'Up'

                    Button: 
                        text: 'Down'

            Button:
                text: '13. Disable alarms'

            Button:
                text: '17. >>> Next screen'
                on_press: root.enter_next_screen()
    
    BoxLayout:
        size_hint_y: 0.08
        id: status_container 
        pos: self.pos

""")

class ZHeadQC1(Screen):
    def __init__(self, **kwargs):
        super(ZHeadQC1, self).__init__(**kwargs)

        self.sm = kwargs['sm']
        self.m = kwargs['m']

        self.MINUTE = 60

        self.start_calibration_timer(0.1)
        # self.status_bar_widget = widget_status_bar.StatusBar(machine=self.m, screen_manager=self.sm)
        # self.status_container.add_widget(self.status_bar_widget)

    def enter_next_screen(self):
        self.sm.current = 'qc2'

    def start_calibration_timer(self, minutes):
        Clock.schedule_once(self.sm.get_screen('qc2').enable_button, minutes*60)

        self.sm.get_screen('qc2').update_time(minutes*60)

    def set_test_status(self, checkbox_id, pass_fail):
        pass
