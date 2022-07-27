from kivy.clock import Clock
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from asmcnc.skavaUI import widget_status_bar
from asmcnc.skavaUI import widget_z_move_nudge
from asmcnc.skavaUI import widget_xy_move_recovery
from asmcnc.skavaUI import widget_nudge_speed
from asmcnc.skavaUI import popup_info

Builder.load_string("""
<NudgeScreen>:
    status_container:status_container
    xy_move_container:xy_move_container
    z_move_container:z_move_container
    nudge_speed_container:nudge_speed_container

    BoxLayout:
        orientation: 'vertical'

        BoxLayout:
            orientation: 'vertical'
            size_hint_y: 0.9
            spacing: dp(8)
            canvas:
                Color:
                    rgba: hex('#E2E2E2FF')
                Rectangle:
                    size: self.size
                    pos: self.pos

            BoxLayout:
                orientation: 'horizontal'

                Label:
                    size_hint_x: 3.15
                    text: 'Nudge:'
                    bold: True
                    color: hex('#333333ff')
                    font_size: dp(25)
                    halign: 'left'
                    valign: 'middle'
                    text_size: self.size
                    padding: [dp(50), dp(0)]

                BoxLayout:
                    orientation: 'horizontal'
                    spacing: dp(25)

                    BoxLayout:
                        padding: [dp(15), dp(15), dp(0), dp(15)]
                        Button:
                            background_color: [0,0,0,0]
                            on_press: root.get_info()
                            BoxLayout:
                                size: self.parent.size
                                pos: self.parent.pos
                                Image:
                                    source: "./asmcnc/apps/shapeCutter_app/img/info_icon.png"
                                    center_x: self.parent.center_x
                                    y: self.parent.y
                                    size: self.parent.width, self.parent.height
                                    allow_stretch: True   

                    Button:
                        background_color: [0,0,0,0]
                        on_press: root.back_to_home()
                        BoxLayout:
                            size: self.parent.size
                            pos: self.parent.pos
                            Image:
                                source: "./asmcnc/apps/shapeCutter_app/img/exit_cross.png"
                                center_x: self.parent.center_x
                                y: self.parent.y
                                size: self.parent.width, self.parent.height
                                allow_stretch: True

            BoxLayout:
                orientation: 'horizontal'
                size_hint_y: 3
                padding: [dp(100), dp(0)]
                spacing: dp(30)

                BoxLayout:
                    size_hint_x: 2.5
                    padding: [(self.size[0] - dp(275)) / 2, (self.size[1] - dp(275)) / 2]
                    canvas:
                        Color:
                            rgba: 1,1,1,1
                        RoundedRectangle:
                            size: self.size
                            pos: self.pos

                    BoxLayout:
                        id: xy_move_container
                        size_hint: (None, None)
                        height: dp(275)
                        width: dp(275)

                BoxLayout:
                    id: nudge_speed_container
                    canvas:
                        Color:
                            rgba: 1,1,1,1
                        RoundedRectangle:
                            size: self.size
                            pos: self.pos

                BoxLayout:
                    id: z_move_container
                    size_hint_x: 2
                    canvas:
                        Color:
                            rgba: 1,1,1,1
                        RoundedRectangle:
                            size: self.size
                            pos: self.pos

            BoxLayout:
                orientation: 'horizontal'
                padding: [dp(70), dp(10), dp(0), dp(10)]
                spacing: dp(200)

                Button:
                    on_press: root.previous_screen()
                    background_color: [0,0,0,0]
                    size_hint: (None, None)
                    height: dp(67)
                    width: dp(88)
                    BoxLayout:
                        size: self.parent.size
                        pos: self.parent.pos
                        Image:
                            source: "./asmcnc/apps/shapeCutter_app/img/arrow_back.png"
                            center_x: self.parent.center_x
                            y: self.parent.y
                            size: self.parent.width, self.parent.height
                            allow_stretch: True

                BoxLayout:
                    size_hint: (None, None)
                    height: dp(67)
                    width: dp(67)

                Button:
                    on_press: root.next_screen()
                    background_color: [0,0,0,0]
                    size_hint: (None, None)
                    height: dp(67)
                    width: dp(88)
                    BoxLayout:
                        size: self.parent.size
                        pos: self.parent.pos
                        Image:
                            source: "./asmcnc/apps/shapeCutter_app/img/arrow_next.png"
                            center_x: self.parent.center_x
                            y: self.parent.y
                            size: self.parent.width, self.parent.height
                            allow_stretch: True

        # GREEN STATUS BAR

        BoxLayout:
            size_hint_y: 0.08
            id: status_container

    FloatLayout:
        Label:
            x: dp(110)
            y: dp(345)
            size_hint: None, None
            height: dp(30)
            width: dp(30)
            text: 'XY'
            markup: True
            bold: True
            color: hex('#333333ff')
            font_size: dp(20)

""")

class NudgeScreen(Screen):

    selected_line_index = 0
    max_index = 0
    display_list = []

    def __init__(self, **kwargs):
        super(NudgeScreen, self).__init__(**kwargs)

        self.sm = kwargs['screen_manager']
        self.m = kwargs['machine']
        self.jd = kwargs['job']
        self.l = kwargs['localization']

        # Green status bar
        self.status_container.add_widget(widget_status_bar.StatusBar(machine=self.m, screen_manager=self.sm))

        # Z move widget
        self.z_move_container.add_widget(widget_z_move_nudge.ZMoveNudge(machine=self.m, screen_manager=self.sm, job=self.jd))

        # XY move widget
        self.xy_move_container.add_widget(widget_xy_move_recovery.XYMoveRecovery(machine=self.m, screen_manager=self.sm))

        # Nudge speed widget
        self.nudge_speed_widget = widget_nudge_speed.NudgeSpeed(machine=self.m, screen_manager=self.sm)
        self.nudge_speed_container.add_widget(self.nudge_speed_widget)

    def on_pre_enter(self):
        self.initial_x = self.m.mpos_x()
        self.initial_y = self.m.mpos_y()

    def get_info(self):

        info = ('"Nudging" is using a manual movement to micro-position your cutting tool into the position you selected in the previous gcode viewer screen.\n\n'
                'Nudging is used to identify minor differences in machine position between homing cycles, or in the event of an axis stall in the previous operation. '
                'By "nudging", SmartBench can compensate for this.\n\n'
                'Now that you have selected a start point in your gcode, use the movement buttons to position the tool exactly where you think it should be.\n\n'
                'Check each axis individually. Any adjustments you make should be minor (normally < 3 mm).'
        )

        popup_info.PopupInfo(self.sm, self.l, 700, info)

    def popup_help(self):

        info = "Use buttons to move to a more accurate position."

        popup_info.PopupInfo(self.sm, self.l, 700, info)   

    def back_to_home(self):
        self.jd.reset_values()
        self.sm.current = 'home'

    def previous_screen(self):
        self.sm.current = 'job_recovery'

    def next_screen(self):
        wait_popup = popup_info.PopupWait(self.sm, self.l)

        diff_x = (self.m.mpos_x() - self.initial_x)
        diff_y = (self.m.mpos_y() - self.initial_y)

        # If user nudged, update datum
        if diff_x or diff_y:
            new_x = float(self.m.s.g54_x) + diff_x
            new_y = float(self.m.s.g54_y) + diff_y
            self.m.s.write_command('G10 L2 X%s Y%s' % (new_x, new_y))

        def generate_gcode():
            success, message = self.jd.generate_recovery_gcode()
            wait_popup.popup.dismiss()
            if not success:
                popup_info.PopupError(self.sm, self.l, message)
                self.jd.reset_values()
            self.jd.job_recovery_from_beginning = False
            self.sm.current = 'home'

        # Give time for wait popup to appear
        Clock.schedule_once(lambda dt: generate_gcode(), 0.5)
