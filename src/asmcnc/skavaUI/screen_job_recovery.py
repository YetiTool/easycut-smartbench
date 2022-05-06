from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from asmcnc.skavaUI import widget_status_bar
from asmcnc.skavaUI import widget_z_move_recovery

Builder.load_string("""
<JobRecoveryScreen>:
    status_container:status_container
    gcode_container:gcode_container
    pos_container:pos_container
    z_move_container:z_move_container

    BoxLayout:
        orientation: 'vertical'

        BoxLayout:
            orientation: 'horizontal'
            size_hint_y: 0.9
            spacing: dp(15)
            canvas:
                Color:
                    rgba: hex('#E2E2E2FF')
                Rectangle:
                    size: self.size
                    pos: self.pos

            BoxLayout:
                padding: [dp(15), dp(15), dp(0), dp(15)]

                BoxLayout:
                    orientation: 'vertical'
                    spacing: dp(15)

                    BoxLayout:
                        orientation: 'vertical'
                        size_hint_y: 3.5
                        spacing: dp(15)

                        BoxLayout:
                            orientation: 'vertical'

                            Label:
                                text: "[b][color=333333]Go to line:[/color][/b]"
                                font_size: dp(25)
                                markup: True

                            BoxLayout:
                                canvas:
                                    Color:
                                        rgba: 1,1,1,1
                                    RoundedRectangle:
                                        size: self.size
                                        pos: self.pos

                        BoxLayout:
                            orientation: 'vertical'
                            size_hint_y: 2
                            padding: [dp(50), dp(0)]
                            spacing: dp(10)

                            Button

                            Button

                    Button

            BoxLayout:
                size_hint_x: 2
                padding: [dp(0), dp(15)]

                BoxLayout:
                    orientation: 'vertical'
                    spacing: dp(15)

                    BoxLayout:
                        id: gcode_container
                        size_hint_y: 3.5
                        canvas:
                            Color:
                                rgba: 1,1,1,1
                            RoundedRectangle:
                                size: self.size
                                pos: self.pos

                    BoxLayout:
                        id: pos_container
                        canvas:
                            Color:
                                rgba: 1,1,1,1
                            RoundedRectangle:
                                size: self.size
                                pos: self.pos

            BoxLayout:
                orientation: 'vertical'
                spacing: dp(15)

                BoxLayout:
                    orientation: 'horizontal'
                    spacing: dp(15)

                    Button

                    Button:
                        background_color: [0,0,0,0]
                        on_press: root.back_to_home()
                        BoxLayout:
                            padding: 0
                            size: self.parent.size
                            pos: self.parent.pos
                            Image:
                                source: "./asmcnc/apps/shapeCutter_app/img/exit_cross.png"
                                center_x: self.parent.center_x
                                y: self.parent.y
                                size: self.parent.width, self.parent.height
                                allow_stretch: True

                BoxLayout:
                    orientation: 'vertical'
                    size_hint_y: 4
                    padding: [dp(0), dp(0), dp(15), dp(15)]
                    spacing: dp(15)

                    BoxLayout:
                        id: z_move_container
                        size_hint_y: 2.5
                        canvas:
                            Color:
                                rgba: 1,1,1,1
                            RoundedRectangle:
                                size: self.size
                                pos: self.pos

                    Button

        # GREEN STATUS BAR

        BoxLayout:
            size_hint_y: 0.08
            id: status_container

""")

class JobRecoveryScreen(Screen):
    def __init__(self, **kwargs):
        super(JobRecoveryScreen, self).__init__(**kwargs)

        self.sm = kwargs['screen_manager']
        self.m = kwargs['machine']
        self.l = kwargs['localization']

        # Green status bar
        self.status_container.add_widget(widget_status_bar.StatusBar(machine=self.m, screen_manager=self.sm))

        # Z move widget
        self.z_move_container.add_widget(widget_z_move_recovery.ZMoveRecovery(machine=self.m, screen_manager=self.sm))

    def back_to_home(self):
        self.sm.current = 'home'
