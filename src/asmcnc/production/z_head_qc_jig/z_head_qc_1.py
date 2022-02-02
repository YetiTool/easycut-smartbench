from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.clock import Clock

from asmcnc.skavaUI import widget_status_bar

Builder.load_string("""
<ZHeadQC1>:
    status_container:status_container
    console_status_text:console_status_text
    home_button:home_button
    reset_button:reset_button

    BoxLayout:
        orientation: 'vertical'

        BoxLayout:
            orientation: 'vertical'
            size_hint_y: 0.92

            GridLayout:
                cols: 3
                rows: 5
                size_hint_y: 0.85

                Button:
                    text: '<<< Back'
                    on_press: root.back_to_home()
                    text_size: self.size
                    markup: 'True'
                    halign: 'left'
                    valign: 'middle'
                    padding: [dp(10),0]

                GridLayout:
                    cols: 2

                    Label:
                        text: '5. X Motors'
                        text_size: self.size
                        markup: 'True'
                        halign: 'left'
                        valign: 'middle'
                        padding: [dp(10),0]

                    GridLayout:
                        cols: 2

                        Button:
                            text: 'Up'
                            text_size: self.size
                            markup: 'True'
                            halign: 'left'
                            valign: 'middle'
                            padding: [dp(10),0]
                        
                        Button: 
                            text: 'Down'
                            text_size: self.size
                            markup: 'True'
                            halign: 'left'
                            valign: 'middle'
                            padding: [dp(10),0]

                Button:
                    text_size: self.size
                    markup: 'True'
                    halign: 'center'
                    valign: 'middle'
                    padding: [dp(10),0]
                    text: 'STOP'
                    background_color: [1,0,0,1]
                    background_normal: ''

                Label:
                    text: 'FW Version: ...'
                    text_size: self.size
                    markup: 'True'
                    halign: 'left'
                    valign: 'middle'
                    padding: [dp(10),0]

                GridLayout:
                    cols: 2

                    Label:
                        text: '6. Z Motors'
                        text_size: self.size
                        markup: 'True'
                        halign: 'left'
                        valign: 'middle'
                        padding: [dp(10),0]

                    GridLayout:
                        cols: 2

                        Button:
                            text: 'Up'
                            text_size: self.size
                            markup: 'True'
                            halign: 'left'
                            valign: 'middle'
                            padding: [dp(10),0]

                        Button: 
                            text: 'Down'
                            text_size: self.size
                            markup: 'True'
                            halign: 'left'
                            valign: 'middle'
                            padding: [dp(10),0]

                Button:
                    text: '12. Disable alarms'
                    text_size: self.size
                    markup: 'True'
                    halign: 'left'
                    valign: 'middle'
                    padding: [dp(10),0]

                Button:
                    text_size: self.size
                    markup: 'True'
                    halign: 'left'
                    valign: 'middle'
                    padding: [dp(10),0]
                    text: '1. Bake GRBL Settings'

                GridLayout:
                    cols: 3

                    Button: 
                        text: '7. Spindle'
                        text_size: self.size
                        markup: 'True'
                        halign: 'left'
                        valign: 'middle'
                        padding: [dp(10),0]

                    Button:
                        text_size: self.size
                        markup: 'True'
                        halign: 'left'
                        valign: 'middle'
                        padding: [dp(10),0]
                        text: '8. Laser'

                    Button:
                        text_size: self.size
                        markup: 'True'
                        halign: 'left'
                        valign: 'middle'
                        padding: [dp(10),0]
                        text: '9. Vac'

                GridLayout:
                    cols: 2

                    Label:
                        text: '13. X Home'
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

                GridLayout:
                    cols: 2

                    Button:
                        text: '2. Test motor chips'
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

                GridLayout:
                    cols: 2

                    Label:
                        text: '10. Dust shoe'
                        text_size: self.size
                        markup: 'True'
                        halign: 'left'
                        valign: 'middle'
                        padding: [dp(10),0]

                    GridLayout:
                        cols: 3

                        Button: 
                            text: 'R'
                            text_size: self.size
                            markup: 'True'
                            valign: 'middle'
                            padding: [dp(10),0]

                        Button:
                            text: 'G'
                            text_size: self.size
                            markup: 'True'
                            valign: 'middle'
                            padding: [dp(10),0]

                        Button:
                            text: 'B'

                GridLayout:
                    cols: 2

                    Label:
                        text: '14. X Max'
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

                GridLayout:
                    cols: 2

                    Button:
                        id: home_button
                        text: '3. HOME'
                        text_size: self.size
                        markup: 'True'
                        halign: 'left'
                        valign: 'middle'
                        padding: [dp(10),0]

                    Button: 
                        id: reset_button
                        text: '4. RESET'
                        text_size: self.size
                        markup: 'True'
                        halign: 'left'
                        valign: 'middle'
                        padding: [dp(10),0]

                GridLayout:
                    cols: 2

                    Label:
                        text: '11. Temp/power'
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

                Button:
                    text: '15. >>> Next screen'
                    on_press: root.enter_next_screen()
                    text_size: self.size
                    markup: 'True'
                    halign: 'left'
                    valign: 'middle'
                    padding: [dp(10),0]

            ScrollableLabelStatus:
                size_hint_y: 0.15
                id: console_status_text
                text: "status update" 
        
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

        self.poll_for_status = Clock.schedule_interval(self.update_status_text, 0.4) 
        self.status_bar_widget = widget_status_bar.StatusBar(machine=self.m, screen_manager=self.sm)
        self.status_container.add_widget(self.status_bar_widget)

    def enter_next_screen(self):
        self.sm.current = 'qc2'

    def back_to_home(self):
        self.sm.current = 'qchome'

    def update_status_text(self, dt):
        try:
            self.console_status_text.text = self.sm.get_screen('home').gcode_monitor_widget.consoleStatusText.text
        except: 
            pass
