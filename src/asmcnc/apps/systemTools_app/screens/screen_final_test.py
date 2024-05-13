"""
Created on 16 March 2021
Screen to help production move through final test more quickly

@author: Letty
"""
from asmcnc.comms.logging_system.logging_system import Logger
from kivy.lang import Builder
from kivy.factory import Factory
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from kivy.properties import ObjectProperty
from asmcnc.skavaUI import widget_status_bar, widget_gcode_monitor
from asmcnc.apps.systemTools_app.screens import widget_final_test_xy_move
import os, sys

Builder.load_string(
    """

<FinalTestScreen>

    move_container : move_container
    gcode_monitor_container : gcode_monitor_container
    status_container : status_container

    y_over_count : y_over_count
    x_over_count : x_over_count

    y_pos_label : y_pos_label
    y_neg_label : y_neg_label
    x_pos_label : x_pos_label
    x_neg_label : x_neg_label

    on_touch_down: root.on_touch()

    BoxLayout:
        padding: 0
        spacing: 0
        orientation: "vertical"
        canvas:
            Color:
                rgba: color_provider.get_rgba("light_grey")
            Rectangle:
                size: self.size
                pos: self.pos
        BoxLayout:
            size_hint_y: 0.92
            padding: 0
            spacing: 0
            orientation: "horizontal"

            GridLayout: 
                height: self.parent.height
                pos: self.parent.pos
                rows: 6
                cols: 1
                spacing: 0
                size_hint_x: 0.165

                Button: 
                    font_size: str(0.01875 * app.width) + 'sp'
                    text: 'Home'
                    on_press: root.home()

                Button: 
                    font_size: str(0.01875 * app.width) + 'sp'
                    text: 'Y-Home, X-mid'
                    on_press: root.y_home_x_mid()

                BoxLayout:
                    orientation: 'horizontal'

                    TextInput:
                        id: y_over_count
                        hint_text: "Y"
                        valign: 'middle'
                        halign: 'center'
                        font_size: str(0.03*app.width) + 'sp'
                        text_size: self.size
                        markup: True
                        multiline: False
                        input_filter: 'int'

                    Button:
                        font_size: str(0.01875 * app.width) + 'sp'
                        text: "Set"
                        on_press: root.set_y_steps()

                Button:
                    font_size: str(0.01875 * app.width) + 'sp'
                    id: y_pos_label
                    text: "G91 G0 Y1636.6"
                    on_press: root.Y_plus()

                Button:
                    font_size: str(0.01875 * app.width) + 'sp'
                    id: y_neg_label
                    text: "G91 G0 Y-1636.6"
                    on_press: root.Y_minus()

                Button:
                    font_size: str(0.01875 * app.width) + 'sp'
                    text: "Factory Settings"
                    on_press: root.go_back()


            BoxLayout:
                height: self.parent.height
                padding: 0
                spacing: 0
                orientation: "vertical"
                size_hint_x: 0.33

                GridLayout: 
                    pos: self.parent.pos
                    size_hint_y: 0.33
                    rows: 2
                    cols: 2
                    spacing: 0


                    Button:
                        font_size: str(0.01875 * app.width) + 'sp'
                        id: x_pos_label
                        text: "G91 G0 X1150.3"
                        on_press: root.X_plus()

                    Button:
                        font_size: str(0.01875 * app.width) + 'sp'
                        id: x_neg_label
                        text: "G91 G0 X-1150.3"
                        on_press: root.X_minus()

                    Button:
                        font_size: str(0.01875 * app.width) + 'sp'
                        text: "G91 G0 X575.0"
                        on_press: root.X_575()

                    BoxLayout:
                        orientation: 'horizontal'

                        TextInput:
                            id: x_over_count
                            hint_text: "X"
                            valign: 'middle'
                            halign: 'center'
                            font_size: str(0.03*app.width) + 'sp'
                            text_size: self.size
                            markup: True
                            multiline: False
                            input_filter: 'int'

                        Button:
                            font_size: str(0.01875 * app.width) + 'sp'
                            text: "Set"
                            on_press: root.set_x_steps()

                BoxLayout:
                    size_hint_y: 0.67
                    orientation: 'horizontal'
                    BoxLayout:
                        height: self.parent.height
                        id: move_container
                        canvas:
                            Color:
                                rgba: color_provider.get_rgba("white")
                            RoundedRectangle:
                                size: self.size
                                pos: self.pos
            BoxLayout:
                height: self.parent.height
                id: gcode_monitor_container
                size_hint_x: 0.5
        BoxLayout:
            size_hint_y: 0.08
            id: status_container



"""
)


class FinalTestScreen(Screen):
    fast_x_speed = 6000
    fast_y_speed = 6000
    fast_z_speed = 750
    feedSpeedJogX = fast_x_speed / 5
    feedSpeedJogY = fast_y_speed / 5
    feedSpeedJogZ = fast_z_speed / 5
    y_calibration_scale_factor = 0.0036
    x_calibration_scale_factor = 0.0048
    y_board = 1234.5
    x_board = 1234.5
    board_type = "pink"
    y_pos_command = ""
    y_neg_command = ""
    x_pos_command = ""
    x_neg_command = ""

    def __init__(self, **kwargs):
        super(FinalTestScreen, self).__init__(**kwargs)
        self.systemtools_sm = kwargs["system_tools"]
        self.m = kwargs["machine"]
        self.l = kwargs["localization"]
        self.kb = kwargs["keyboard"]
        self.status_container.add_widget(
            widget_status_bar.StatusBar(
                machine=self.m, screen_manager=self.systemtools_sm.sm
            )
        )
        self.gcode_monitor_container.add_widget(
            widget_gcode_monitor.GCodeMonitor(
                machine=self.m,
                screen_manager=self.systemtools_sm.sm,
                localization=self.l,
            )
        )
        self.move_container.add_widget(
            widget_final_test_xy_move.FinalTestXYMove(
                machine=self.m, screen_manager=self.systemtools_sm.sm
            )
        )
        self.text_inputs = [self.y_over_count, self.x_over_count]

    def on_enter(self):
        self.m.send_any_gcode_command("AZ")
        self.m.set_led_colour("BLUE")
        self.kb.setup_text_inputs(self.text_inputs)

    def on_leave(self):
        self.m.send_any_gcode_command("AX")

    def on_touch(self):
        for text_input in self.text_inputs:
            text_input.focus = False

    def go_back(self):
        self.systemtools_sm.open_factory_settings_screen()

    def exit_app(self):
        self.systemtools_sm.exit_app()

    def set_board_up(self, board):
        self.board_type = board
        if self.board_type == "pink":
            self.y_board = 1636.6
            self.x_board = 1150.3
        elif self.board_type == "blue":
            self.y_board = 1636.9
            self.x_board = 1149.1
        elif self.board_type == "green":
            self.y_board = 1250
            self.x_board = 1150
        elif self.board_type == "red":
            self.y_board = 1250
            self.x_board = 1150
        self.y_pos_command = "G91 G0 Y" + str(self.y_board)
        self.y_neg_command = "G91 G0 Y-" + str(self.y_board)
        self.x_pos_command = "G91 G0 X" + str(self.x_board)
        self.x_neg_command = "G91 G0 X-" + str(self.x_board)
        self.y_pos_label.text = self.y_pos_command
        self.y_neg_label.text = self.y_neg_command
        self.x_pos_label.text = self.x_pos_command
        self.x_neg_label.text = self.x_neg_command

    def X_plus(self):
        self.m.send_any_gcode_command(self.x_pos_command)
        self.m.set_led_colour("BLUE")

    def X_minus(self):
        self.m.send_any_gcode_command(self.x_neg_command)
        self.m.set_led_colour("BLUE")

    def Y_plus(self):
        self.m.send_any_gcode_command(self.y_pos_command)
        self.m.set_led_colour("BLUE")

    def Y_minus(self):
        self.m.send_any_gcode_command(self.y_neg_command)
        self.m.set_led_colour("BLUE")

    def X_575(self):
        self.m.send_any_gcode_command("G91 G0 X575.0")
        self.m.set_led_colour("BLUE")

    def y_home_x_mid(self):
        self.m.jog_absolute_single_axis(
            "Y", self.m.y_min_jog_abs_limit, self.fast_y_speed
        )
        self.m.jog_absolute_single_axis("X", -705, self.fast_x_speed)
        self.m.set_led_colour("BLUE")

    def home(self):
        normal_homing_sequence = ["$H"]
        self.m.s.start_sequential_stream(normal_homing_sequence)

    def set_x_steps(self):
        try:
            x_overstep = float(self.x_over_count.text) * self.x_calibration_scale_factor
            Logger.info(x_overstep)
            self.m.write_dollar_setting(
                100,
                float(self.m.s.setting_100) - x_overstep,
                reset_grbl_after_stream=False,
            )
            self.x_over_count.text = ""
        except:
            pass

    def set_y_steps(self):
        try:
            y_overstep = float(self.y_over_count.text) * self.y_calibration_scale_factor
            Logger.info(y_overstep)
            self.m.write_dollar_setting(
                101,
                float(self.m.s.setting_101) - y_overstep,
                reset_grbl_after_stream=False,
            )
            self.y_over_count.text = ""
        except:
            pass
