from kivy.core.window import Window
import re
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.clock import Clock
from asmcnc.skavaUI import widget_status_bar
from asmcnc.skavaUI import widget_z_move_recovery
from asmcnc.skavaUI import popup_info

Builder.load_string(
    """
<JobRecoveryScreen>:
    status_container:status_container
    z_move_container:z_move_container
    gcode_container:gcode_container

    gcode_label:gcode_label
    pos_label:pos_label
    speed_label:speed_label
    stopped_on_label:stopped_on_label
    arc_movement_error_label:arc_movement_error_label

    line_input_header:line_input_header
    pos_label_header:pos_label_header

    line_input:line_input

    go_xy_button:go_xy_button
    
    on_touch_down: root.on_touch()

    BoxLayout:
        orientation: 'vertical'

        BoxLayout:
            orientation: 'horizontal'
            size_hint_y: 0.9
            spacing:dp(0.01875)*app.width
            canvas:
                Color:
                    rgba: hex('#E2E2E2FF')
                Rectangle:
                    size: self.size
                    pos: self.pos

            BoxLayout:
                padding:[dp(0.01875)*app.width, dp(0.03125)*app.height, 0, dp(0.03125)*app.height]

                BoxLayout:
                    orientation: 'vertical'
                    spacing:dp(0.03125)*app.height

                    BoxLayout:
                        orientation: 'vertical'
                        size_hint_y: 3.5
                        spacing:dp(0.03125)*app.height

                        BoxLayout:
                            orientation: 'vertical'

                            Label:
                                id: line_input_header
                                text: "Go to line:"
                                color: hex('#333333FF')
                                bold: True
                                font_size: dp(0.03125*app.width)

                            BoxLayout:
                                padding:[0, dp(0.00833333333333)*app.height, 0, 0]
                                canvas:
                                    Color:
                                        rgba: 1,1,1,1
                                    RoundedRectangle:
                                        size: self.size
                                        pos: self.pos

                                TextInput:
                                    id: line_input
                                    font_size: dp(0.03125*app.width)
                                    halign: 'center'
                                    input_filter: 'int'
                                    multiline: False
                                    background_color: (0,0,0,0)
                                    hint_text: "Enter #"

                        BoxLayout:
                            orientation: 'vertical'
                            size_hint_y: 2
                            padding:[dp(0.0625)*app.width, 0]
                            spacing:dp(0.0208333333333)*app.height

                            Button:
                                font_size: str(0.01875 * app.width) + 'sp'
                                background_color: [0,0,0,0]
                                on_press:
                                    root.start_scrolling_up()
                                    self.background_color = hex('#F44336FF')
                                on_release:
                                    self.background_color = hex('#F4433600')
                                    root.stop_scrolling_up()
                                BoxLayout:
                                    padding: 0
                                    size: self.parent.size
                                    pos: self.parent.pos
                                    Image:
                                        source: "./asmcnc/skavaUI/img/arrow_up.png"
                                        center_x: self.parent.center_x
                                        y: self.parent.y
                                        size: self.parent.width, self.parent.height
                                        allow_stretch: True

                            Button:
                                font_size: str(0.01875 * app.width) + 'sp'
                                background_color: [0,0,0,0]
                                on_press:
                                    root.start_scrolling_down()
                                    self.background_color = hex('#F44336FF')
                                on_release:
                                    root.stop_scrolling_down()
                                    self.background_color = hex('#F4433600')
                                BoxLayout:
                                    padding: 0
                                    size: self.parent.size
                                    pos: self.parent.pos
                                    Image:
                                        source: "./asmcnc/skavaUI/img/arrow_down.png"
                                        center_x: self.parent.center_x
                                        y: self.parent.y
                                        size: self.parent.width, self.parent.height
                                        allow_stretch: True

                    Button:
                        id: go_xy_button
                        valign: "middle"
                        halign: "center"
                        markup: True
                        font_size: dp(0.0375*app.width)
                        text_size: self.size[0] - dp(20), self.size[1]
                        text: "GO XY"
                        background_normal: "./asmcnc/skavaUI/img/blank_small_button.png"
                        background_down: "./asmcnc/skavaUI/img/blank_small_button.png"
                        on_press: root.go_xy()

            BoxLayout:
                size_hint_x: 2
                padding:[0, dp(0.03125)*app.height]

                BoxLayout:
                    orientation: 'vertical'
                    spacing:dp(0.03125)*app.height

                    BoxLayout:
                        id: gcode_container
                        orientation: 'vertical'
                        size_hint_y: 3.5
                        padding:[dp(0.015)*app.width, dp(0.025)*app.height, dp(0.015)*app.width, 0]
                        canvas:
                            Color:
                                rgba: 1,1,1,1
                            RoundedRectangle:
                                size: self.size
                                pos: self.pos

                        FloatLayout:
                            Label:
                                id: gcode_label
                                color: 0,0,0,1
                                font_size: dp(0.02*app.width)
                                halign: "left"
                                valign: "top"
                                text_size: self.size[0] * 2, self.size[1]
                                size: self.parent.size
                                pos: self.parent.pos[0] + self.size[0]/2, self.parent.pos[1]
                                markup: True

                                canvas.before:
                                    Color:
                                        rgba: hex('#A7D5FAFF')
                                    Rectangle:
                                        size: self.parent.parent.size[0], dp(20.0/480.0)*app.height
                                        pos: self.parent.parent.pos[0], self.center_y - dp(3.0/480.0)*app.height

                        Label:
                            id: stopped_on_label
                            size_hint_y: 0.13
                            color: 1,0,0,1
                            font_size: dp(0.02*app.width)
                            halign: "left"
                            valign: "top"
                            text_size: self.size
                            size: self.parent.size
                            pos: self.parent.pos

                    BoxLayout:
                        orientation: 'vertical'
                        padding:[dp(0.015)*app.width, dp(0.025)*app.height]
                        spacing:dp(0.0145833333333)*app.height
                        canvas:
                            Color:
                                rgba: 1,1,1,1
                            RoundedRectangle:
                                size: self.size
                                pos: self.pos

                        Label:
                            id: pos_label_header
                            text: "Job resumes at:"
                            color: hex('#333333FF')
                            bold: True
                            font_size: dp(0.01875*app.width)
                            halign: 'left'
                            valign: 'middle'
                            text_size: self.size

                        Label:
                            id: pos_label
                            text: "wX: | wY: | wZ:"
                            color: 0,0,0,1
                            font_size: dp(0.02*app.width)
                            halign: 'left'
                            valign: 'middle'
                            text_size: self.size

                        Label:
                            id: speed_label
                            text: "F: | S:"
                            color: 0,0,0,1
                            font_size: dp(0.02*app.width)
                            halign: 'left'
                            valign: 'middle'
                            text_size: self.size

            BoxLayout:
                orientation: 'vertical'
                spacing:dp(0.03125)*app.height

                BoxLayout:
                    orientation: 'horizontal'
                    spacing:dp(0.03125)*app.width

                    BoxLayout:
                        padding:[dp(0.01875)*app.width, dp(0.03125)*app.height, 0, dp(0.03125)*app.height]
                        Button:
                            font_size: str(0.01875 * app.width) + 'sp'
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
                        font_size: str(0.01875 * app.width) + 'sp'
                        background_color: [0,0,0,0]
                        on_press: root.back_to_home()
                        BoxLayout:
                            size: self.parent.size
                            pos: self.parent.pos[0], self.parent.pos[1] + dp(1.0/480.0)*app.height
                            Image:
                                source: "./asmcnc/apps/shapeCutter_app/img/exit_cross.png"
                                center_x: self.parent.center_x
                                y: self.parent.y
                                size: self.parent.width, self.parent.height
                                allow_stretch: True

                BoxLayout:
                    orientation: 'vertical'
                    size_hint_y: 4
                    padding:[0, 0, dp(0.01875)*app.width, dp(0.03125)*app.height]
                    spacing:dp(0.03125)*app.height

                    BoxLayout:
                        id: z_move_container
                        size_hint_y: 2.5
                        canvas:
                            Color:
                                rgba: 1,1,1,1
                            RoundedRectangle:
                                size: self.size
                                pos: self.pos

                    BoxLayout:

                        padding:[0, dp(0.00208333333333)*app.height]

                        Button:
                            font_size: str(0.01875 * app.width) + 'sp'
                            background_color: [0,0,0,0]
                            on_press: root.next_screen()
                            size_hint: (None, None)
                            height: dp(0.139583333333*app.height)
                            width: dp(0.11*app.width)
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
        BoxLayout:
            pos: gcode_container.pos
            size: gcode_container.size
            padding: gcode_container.padding
            size_hint: None, None

            Label:
                id: arc_movement_error_label
                color: 1,0,0,1
                font_size: dp(0.0175*app.width)
                halign: "left"
                valign: "top"
                text_size: self.size
                size: self.parent.size
                pos: self.parent.pos

"""
)


class JobRecoveryScreen(Screen):
    initial_line_index = 0
    selected_line_index = 0
    display_list = []
    gcode_without_comments = []

    scroll_up_event = None
    scroll_down_event = None

    using_inches = False

    def __init__(self, **kwargs):
        super(JobRecoveryScreen, self).__init__(**kwargs)
        self.sm = kwargs["screen_manager"]
        self.m = kwargs["machine"]
        self.jd = kwargs["job"]
        self.l = kwargs["localization"]
        self.kb = kwargs["keyboard"]
        self.line_input.bind(text=self.jump_to_line)
        self.status_container.add_widget(
            widget_status_bar.StatusBar(machine=self.m, screen_manager=self.sm)
        )
        self.z_move_container.add_widget(
            widget_z_move_recovery.ZMoveRecovery(machine=self.m, screen_manager=self.sm)
        )
        self.update_strings()
        self.text_inputs = [self.line_input]

    def on_touch(self):
        for text_input in self.text_inputs:
            text_input.focus = False

    def on_pre_enter(self):
        self.m.set_led_colour("WHITE")

        def remove_comments(line):
            # Comments are anything contained in parentheses, or anything after a semicolon
            return re.sub('\(.*?\)|;.*', '', line)

        self.gcode_without_comments = map(remove_comments, self.jd.job_gcode)

        self.gcode_label.font_name = "Roboto"
        if self.jd.job_recovery_selected_line == -1:
            self.line_input.text = ""
            self.initial_line_index = self.jd.job_recovery_cancel_line - 1
            self.selected_line_index = self.initial_line_index
            self.display_list = (
                ["" for _ in range(6)]
                + [
                    (str(i) + ": " + self.jd.job_gcode[i])
                    for i in range(self.initial_line_index + 1)
                ]
                + ["" for _ in range(6)]
            )
            self.stopped_on_label.text = self.l.get_str(
                "Job failed during line N"
            ).replace("N", str(self.initial_line_index))
            self.display_list[self.selected_line_index + 6] = (
                "[color=FF0000]"
                + self.display_list[self.selected_line_index + 6]
                + "[/color]"
            )
            self.update_display()
        if self.initial_line_index == 0:
            self.arc_movement_error_label.opacity = 1
        else:
            self.arc_movement_error_label.opacity = 0

    def on_enter(self):
        self.kb.setup_text_inputs(self.text_inputs)

    def start_scrolling_up(self):
        self.scrolling_up = True
        self.do_scroll_up()
        self.scroll_up_event = Clock.schedule_once(self.scroll_up, 0.5)

    def do_scroll_up(self):
        if self.selected_line_index > 0:
            self.selected_line_index -= 1
            self.line_input.text = str(self.selected_line_index)
            self.update_display()

    def scroll_up(self, dt=0):
        if self.scrolling_up:
            self.do_scroll_up()
            self.scroll_up_event = Clock.schedule_once(self.scroll_up, 0.03)

    def stop_scrolling_up(self):
        self.scrolling_up = False
        if self.scroll_up_event:
            Clock.unschedule(self.scroll_up_event)

    def start_scrolling_down(self):
        self.scrolling_down = True
        self.do_scroll_down()
        self.scroll_down_event = Clock.schedule_once(self.scroll_down, 0.5)

    def do_scroll_down(self):
        if self.selected_line_index < self.initial_line_index:
            self.selected_line_index += 1
            self.line_input.text = str(self.selected_line_index)
            self.update_display()

    def scroll_down(self, dt=0):
        if self.scrolling_down:
            self.do_scroll_down()
            self.scroll_down_event = Clock.schedule_once(self.scroll_down, 0.03)

    def stop_scrolling_down(self):
        self.scrolling_down = False
        if self.scroll_down_event:
            Clock.unschedule(self.scroll_down_event)

    def jump_to_line(self, instance, value):
        if value:
            if value.startswith("-"):
                instance.text = ""
            else:
                self.selected_line_index = min(int(value), self.initial_line_index)
                self.update_display()
        else:
            self.selected_line_index = self.initial_line_index
            self.update_display()

    def update_display(self):
        self.gcode_label.text = "\n".join(
            self.display_list[self.selected_line_index : self.selected_line_index + 13]
        )
        spindle_speed_line = next(
            (
                s
                for s in reversed(self.gcode_without_comments[: self.selected_line_index + 1])
                if "S" in s
            ),
            None,
        )
        try:
            if spindle_speed_line:
                self.speed = spindle_speed_line[
                    spindle_speed_line.find("S") + 1 :
                ].split("M")[0]
            else:
                self.speed = self.l.get_str("Undefined")
        except:
            self.speed = self.l.get_str("Undefined")
        feedrate_line = next(
            (
                s
                for s in reversed(self.gcode_without_comments[: self.selected_line_index + 1])
                if "F" in s
            ),
            None,
        )
        try:
            if feedrate_line:
                self.feed = re.match(
                    "\\d+(\\.\\d+)?", feedrate_line[feedrate_line.find("F") + 1 :]
                ).group()
            else:
                self.feed = self.l.get_str("Undefined")
        except:
            self.feed = self.l.get_str("Undefined")
        x_line = next(
            (
                s
                for s in reversed(self.gcode_without_comments[: self.selected_line_index + 1])
                if "X" in s
            ),
            None,
        )
        if x_line:
            self.pos_x = float(
                re.split("(X|Y|Z|F|S|I|J|K|G|R)", x_line)[
                    re.split("(X|Y|Z|F|S|I|J|K|G|R)", x_line).index("X") + 1
                ]
            )
        else:
            self.pos_x = 0.0
        y_line = next(
            (
                s
                for s in reversed(self.gcode_without_comments[: self.selected_line_index + 1])
                if "Y" in s
            ),
            None,
        )
        if y_line:
            self.pos_y = float(
                re.split("(X|Y|Z|F|S|I|J|K|G|R)", y_line)[
                    re.split("(X|Y|Z|F|S|I|J|K|G|R)", y_line).index("Y") + 1
                ]
            )
        else:
            self.pos_y = 0.0
        z_line = next(
            (
                s
                for s in reversed(self.gcode_without_comments[: self.selected_line_index + 1])
                if "Z" in s
            ),
            None,
        )
        if z_line:
            self.pos_z = float(
                re.split("(X|Y|Z|F|S|I|J|K|G|R)", z_line)[
                    re.split("(X|Y|Z|F|S|I|J|K|G|R)", z_line).index("Z") + 1
                ]
            )
        else:
            self.pos_z = 0.0

        # Check if these distances are measured in inches, so that GO XY can work correctly
        unit_line = next((s for s in reversed(self.jd.job_gcode[:self.selected_line_index + 1]) if re.search("G2[0,1]", s)), None)
        if unit_line:
            self.using_inches = "G20" in unit_line
        else:
            self.using_inches = False

        self.pos_label.text = "wX: %s | wY: %s | wZ: %s" % (
            str(self.pos_x),
            str(self.pos_y),
            str(self.pos_z),
        )
        self.speed_label.text = "%s: %s | %s: %s" % (
            self.l.get_str("F"),
            str(self.feed),
            self.l.get_str("S"),
            str(self.speed),
        )

    def get_info(self):
        info = (
            self.l.get_str("This screen allows you to recover an incomplete job.")
            + "\n\n"
            + self.l.get_bold(
                "Ensure that you recover the job from a point where it was running normally, and SmartBench's position was accurate."
            )
            + "\n\n"
            + self.l.get_bold(
                "Choose a visually obvious restart point, such as a corner."
            )
            + "\n\n"
            + self.l.get_str("The red text indicates where the job failed.")
            + " "
            + self.l.get_str(
                "Use the arrows to navigate through the lines of the job file, and select a point to recover the job from."
            )
            + "\n\n"
            + self.l.get_str('To confirm this start point, use the "GO XY" button.')
            + " "
            + self.l.get_str("This will move the Z Head over the selected start point.")
            + " "
            + self.l.get_str(
                "You can lower the spindle to check the tool is approximately where you expect it to be in the XY plane."
            )
            + " "
            + self.l.get_str(
                "This XY position can be fine adjusted in the next screen."
            )
            + "\n\n"
            + self.l.get_str(
                "Arc movements (G2 and G3) may cause the software to think that the job failed earlier than it did."
            )
            + "\n\n"
            + self.l.get_str(
                "SmartBench does not yet support recovery of jobs that contain incremental or arc distance modes, or less commonly used G-Codes."
            )
        )
        popup_info.PopupScrollableInfo(self.sm, self.l, 760, info)

    def go_xy(self):
        # Pick min out of safe z height and limit_switch_safety_distance, in case positive value is calculated, which causes errors
        z_safe_height = min(
            self.m.z_wco() + self.sm.get_screen("home").job_box.range_z[1],
            -self.m.limit_switch_safety_distance,
        )
        # If Z is below safe height, then raise it up
        if self.m.mpos_z() < z_safe_height:
            self.m.s.write_command("G53 G0 Z%s F750" % z_safe_height)
        if self.using_inches:
            self.m.set_machine_unit_to_inch()
        self.m.s.write_command('G90 G0 X%s Y%s' % (self.pos_x, self.pos_y))
        self.m.set_machine_unit_to_mm()

    def back_to_home(self):
        self.jd.reset_recovery()
        self.jd.job_recovery_from_beginning = True
        self.sm.current = "home"

    def next_screen(self):
        if self.m.state().startswith("Idle"):
            self.wait_popup = popup_info.PopupWait(self.sm, self.l)
            self.jd.job_recovery_selected_line = self.selected_line_index + 1
            self.go_xy()
            Clock.schedule_once(self.wait_for_idle, 0.4)
        else:
            error_message = self.l.get_str(
                "Please ensure machine is idle before continuing."
            )
            popup_info.PopupError(self.sm, self.l, error_message)

    def wait_for_idle(self, dt):
        if self.m.state().startswith("Idle"):
            self.m.get_grbl_status()
            Clock.schedule_once(self.proceed_to_next_screen, 0.4)
        elif self.m.state().startswith("Run"):
            Clock.schedule_once(self.wait_for_idle, 0.4)
        else:
            self.wait_popup.popup.dismiss()

    def proceed_to_next_screen(self, dt):
        self.wait_popup.popup.dismiss()
        self.sm.current = "nudge"

    def update_strings(self):
        self.line_input_header.text = self.l.get_str("Go to line:")
        self.line_input.hint_text = self.l.get_str("Enter #")
        self.go_xy_button.text = self.l.get_str("GO XY")
        self.pos_label_header.text = self.l.get_str("Job resumes at:")
        self.arc_movement_error_label.text = (
            self.l.get_str(
                "It was not possible to recover the file any later than the beginning of the job."
            )
            + "\n\n"
            + self.l.get_str(
                "Arc movements (G2 and G3) may cause the software to think that the job failed earlier than it did."
            )
        )
        self.update_font_size(self.go_xy_button)

    def update_font_size(self, value):
        text_length = self.l.get_text_length(value.text)
        if text_length > 10:
            value.font_size = 0.03125 * Window.width
        else:
            value.font_size = 0.0375 * Window.width
