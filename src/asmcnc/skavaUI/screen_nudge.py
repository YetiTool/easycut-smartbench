import math
from kivy.clock import Clock
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from asmcnc.skavaUI import widget_status_bar
from asmcnc.skavaUI import widget_z_move_nudge
from asmcnc.skavaUI import widget_xy_move_recovery
from asmcnc.skavaUI import widget_nudge_speed
from asmcnc.skavaUI import popup_info
from asmcnc.skavaUI import popup_nudge

Builder.load_string(
    """
<NudgeScreen>:
    status_container:status_container
    xy_move_container:xy_move_container
    z_move_container:z_move_container
    nudge_speed_container:nudge_speed_container

    nudge_header:nudge_header

    BoxLayout:
        orientation: 'vertical'

        BoxLayout:
            orientation: 'vertical'
            size_hint_y: 0.9
            spacing: app.get_scaled_width(8.00000000002)
            canvas:
                Color:
                    rgba: hex('#E2E2E2FF')
                Rectangle:
                    size: self.size
                    pos: self.pos

            BoxLayout:
                orientation: 'horizontal'

                Label:
                    id: nudge_header
                    size_hint_x: 3.15
                    text: 'Optional Nudge:'
                    bold: True
                    color: hex('#333333ff')
                    font_size: app.get_scaled_width(25.0)
                    halign: 'left'
                    valign: 'middle'
                    text_size: self.size
                    padding: app.get_scaled_tuple([50.0, 0.0])

                BoxLayout:
                    orientation: 'horizontal'
                    spacing: app.get_scaled_width(25.0)

                    BoxLayout:
                        padding: app.get_scaled_tuple([15.0, 15.0, 0.0, 15.0])
                        Button:
                            font_size: app.get_scaled_sp('15.0sp')
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
                        font_size: app.get_scaled_sp('15.0sp')
                        background_color: [0,0,0,0]
                        on_press: root.back_to_home()
                        BoxLayout:
                            size: self.parent.size
                            pos: self.parent.pos[0], self.parent.pos[1] + dp(1)
                            Image:
                                source: "./asmcnc/apps/shapeCutter_app/img/exit_cross.png"
                                center_x: self.parent.center_x
                                y: self.parent.y
                                size: self.parent.width, self.parent.height
                                allow_stretch: True

            BoxLayout:
                orientation: 'horizontal'
                size_hint_y: 3
                padding: app.get_scaled_tuple([100.0, 0.0])
                spacing: app.get_scaled_width(30.0)

                BoxLayout:
                    size_hint_x: 2.5
                    padding: app.get_scaled_tuple([0.0, 1.0])
                    canvas:
                        Color:
                            rgba: 1,1,1,1
                        RoundedRectangle:
                            size: self.size
                            pos: self.pos

                    BoxLayout:
                        id: xy_move_container
                        size_hint: (None, None)
                        height: app.get_scaled_height(275.0)
                        width: app.get_scaled_width(275.0)

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
                padding: app.get_scaled_tuple([70.0, 10.0, 0.0, 10.0])
                spacing: app.get_scaled_width(200.0)

                Button:
                    font_size: app.get_scaled_sp('15.0sp')
                    on_press: root.previous_screen()
                    background_color: [0,0,0,0]
                    size_hint: (None, None)
                    height: app.get_scaled_height(66.9999999998)
                    width: app.get_scaled_width(88.0)
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
                    height: app.get_scaled_height(66.9999999998)
                    width: app.get_scaled_width(67.0)

                Button:
                    font_size: app.get_scaled_sp('15.0sp')
                    on_press: root.next_screen()
                    background_color: [0,0,0,0]
                    size_hint: (None, None)
                    height: app.get_scaled_height(66.9999999998)
                    width: app.get_scaled_width(88.0)
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
            x: dp(110.0/800.0)*app.width
            y: dp(345.0/480.0)*app.height
            size_hint: None, None
            height: app.get_scaled_height(30.0)
            width: app.get_scaled_width(30.0)
            text: 'XY'
            markup: True
            bold: True
            color: hex('#333333ff')
            font_size: app.get_scaled_width(20.0)

"""
)


class NudgeScreen(Screen):
    selected_line_index = 0
    max_index = 0
    display_list = []

    def __init__(self, **kwargs):
        super(NudgeScreen, self).__init__(**kwargs)
        self.sm = kwargs["screen_manager"]
        self.m = kwargs["machine"]
        self.jd = kwargs["job"]
        self.l = kwargs["localization"]
        self.status_container.add_widget(
            widget_status_bar.StatusBar(machine=self.m, screen_manager=self.sm)
        )
        self.z_move_container.add_widget(
            widget_z_move_nudge.ZMoveNudge(
                machine=self.m, screen_manager=self.sm, job=self.jd
            )
        )
        self.xy_move_widget = widget_xy_move_recovery.XYMoveRecovery(
            machine=self.m, screen_manager=self.sm
        )
        self.xy_move_container.add_widget(self.xy_move_widget)
        self.nudge_speed_widget = widget_nudge_speed.NudgeSpeed(
            machine=self.m, screen_manager=self.sm
        )
        self.nudge_speed_container.add_widget(self.nudge_speed_widget)
        self.update_strings()

    def on_pre_enter(self):
        self.initial_x = self.m.mpos_x()
        self.initial_y = self.m.mpos_y()
        self.initial_g54_x = self.m.s.g54_x
        self.initial_g54_y = self.m.s.g54_y

    def get_info(self):
        info = (
            self.l.get_str("Nudging is an optional manual adjustment in the XY plane.")
            + " "
            + self.l.get_str(
                "It is only necessary if SmartBench has suffered any positional loss e.g. due to a stall, or a re-home."
            )
            + "\n\n"
            + self.l.get_str(
                "Nudging allows the user to apply micro-corrections to the XY starting point of the tool, allowing the tool to re-start in exact registration with previous cut paths."
            )
            + "\n\n"
            + self.l.get_str(
                "Check X and Y axes individually. Any adjustments you make should be minor (normally < 3 mm)."
            )
            + " "
            + self.l.get_bold(
                "The toolpiece should lightly touch the edge of the cut path."
            )
            + "\n\n"
            + self.l.get_str(
                'Once you have nudged your X and Y axis, press the "SET" button to save your new datum.'
            )
            + "\n\n"
            + self.l.get_str(
                "To correct for a stall in Z axis or tool change, please use the standard functions in the manual move screen to set the Z datum."
            )
            + "\n\n"
            + self.l.get_str(
                "Warning: Nudging your tool incorrectly (putting the start point too far away from last physical cut path) could result in damage to your spindle, cutting tool and/or workpiece."
            )
        )
        popup_info.PopupScrollableInfo(self.sm, self.l, 760, info)

    def back_to_home(self):
        self.jd.reset_recovery()
        self.jd.job_recovery_from_beginning = True
        self.sm.current = "home"

    def on_pre_leave(self):
        z_safe_height = min(
            self.m.z_wco() + self.sm.get_screen("home").job_box.range_z[1],
            -self.m.limit_switch_safety_distance,
        )
        if self.m.mpos_z() < z_safe_height:
            self.m.s.write_command("G53 G0 Z%s F750" % z_safe_height)

    def previous_screen(self):
        self.sm.current = "job_recovery"

    def next_screen(self):
        # wait_popup = popup_info.PopupWait(self.sm, self.l)
        self.sm.pm.show_wait_popup()

        def generate_gcode():
            success, message = self.jd.generate_recovery_gcode()
            self.sm.pm.close_wait_popup()
            if not success:
                # popup_info.PopupError(self.sm, self.l, message)
                self.sm.pm.show_error_popup(message)
                self.jd.reset_recovery()
                self.jd.job_recovery_from_beginning = True
            else:
                self.jd.job_recovery_from_beginning = False
            self.sm.current = "home"

        Clock.schedule_once(lambda dt: generate_gcode(), 0.5)

    def set_datum_popup(self):
        self.diff_x = self.m.mpos_x() - self.initial_x
        self.diff_y = self.m.mpos_y() - self.initial_y
        if abs(self.diff_x) > 3 or abs(self.diff_y) > 3:
            nudge_distance = "{:.2f}".format(math.hypot(self.diff_x, self.diff_y))
            popup_nudge.PopupNudgeWarning(self.sm, self.m, self.l, nudge_distance)
        else:
            popup_nudge.PopupNudgeDatum(self.sm, self.m, self.l)

    def set_datum(self):
        new_x = float(self.initial_g54_x) + self.diff_x
        new_y = float(self.initial_g54_y) + self.diff_y
        self.m.set_datum(x=new_x, y=new_y, relative=True)

    def update_strings(self):
        self.nudge_header.text = self.l.get_str("Optional Nudge:")
