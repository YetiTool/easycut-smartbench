from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.clock import Clock

from asmcnc.skavaUI import widget_status_bar

Builder.load_string("""
<ZHeadQC2>:
    console_status_text:console_status_text
    status_container:status_container

    BoxLayout:
        orientation: 'vertical'

        BoxLayout:
            orientation: 'vertical'
            size_hint_y: 0.92

            GridLayout:
                size_hint_y: 0.85
                cols: 3
                rows: 5

                Button:
                    text: '<<< Back'
                    on_press: root.enter_prev_screen()
                    text_size: self.size
                    markup: 'True'
                    halign: 'left'
                    valign: 'middle'
                    padding: [dp(10),0]

                Label:
                    text: '20. Plug in digital spindle'
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

                GridLayout:
                    cols: 2

                    Label:
                        text: '16. Probe'
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
                        text: '21. Test digital spindle'
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
                        text: '25. Test USB "spindle"'
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
                        text: '17. Z Home'
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
                    text: '22. Remove digital spindle'
                    text_size: self.size
                    markup: 'True'
                    halign: 'left'
                    valign: 'middle'
                    padding: [dp(10),0]

                Label:
                    text: '26. Remove USB "spindle"'
                    text_size: self.size
                    markup: 'True'
                    halign: 'left'
                    valign: 'middle'
                    padding: [dp(10),0]

                Button:
                    text: '18. Enable alarms'
                    text_size: self.size
                    markup: 'True'
                    halign: 'left'
                    valign: 'middle'
                    padding: [dp(10),0]

                Label: 
                    text: '23. Plug in USB "spindle"'
                    text_size: self.size
                    markup: 'True'
                    halign: 'left'
                    valign: 'middle'
                    padding: [dp(10),0]

                Label: 
                    text: '27. TAKE BELT OFF Z MOTOR'
                    text_size: self.size
                    markup: 'True'
                    halign: 'left'
                    valign: 'middle'
                    padding: [dp(10),0]

                Button:
                    text: '19. Set spindle to digital'
                    text_size: self.size
                    markup: 'True'
                    halign: 'left'
                    valign: 'middle'
                    padding: [dp(10),0]

                Button:
                    text: '24. Set spindle to analogue'
                    text_size: self.size
                    markup: 'True'
                    halign: 'left'
                    valign: 'middle'
                    padding: [dp(10),0]

                Button:
                    text: '28. CONFIRM BELT OFF: START AUTO-CALIBRATE'
                    text_size: self.size
                    markup: 'True'
                    halign: 'left'
                    valign: 'middle'
                    padding: [dp(10),0]
                    on_press: root.enter_next_screen()

            ScrollableLabelStatus:
                size_hint_y: 0.15 
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

    def enter_next_screen(self):
        self.sm.current = 'qc3'

    def update_status_text(self, dt):
        try:
            self.console_status_text.text = self.sm.get_screen('home').gcode_monitor_widget.consoleStatusText.text
        except:
            pass