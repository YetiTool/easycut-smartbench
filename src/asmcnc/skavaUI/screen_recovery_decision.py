from kivy.core.window import Window
import os, sys
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from asmcnc.skavaUI import popup_info

Builder.load_string(
    """

<RecoveryDecisionScreen>:

    recover_job_button:recover_job_button
    repeat_job_button:repeat_job_button

    job_name_label:job_name_label
    completion_label:completion_label

    job_name_header:job_name_header

    BoxLayout:
        orientation: 'vertical'
        canvas:
            Color:
                rgba: hex('#E2E2E2FF')
            Rectangle:
                size: self.size
                pos: self.pos

        BoxLayout:
            size_hint_y: 0.75
            padding:[dp(0.895)*app.width, 0, 0, 0]

            Button:
                font_size: str(0.01875 * app.width) + 'sp'
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
            size_hint_y: 1.25
            orientation: 'vertical'

            Label:
                id: job_name_header
                text: "[b]Last job:[/b]"
                color: hex('#333333ff')
                markup: True
                font_size: dp(0.0375*app.width)

            Label:
                id: job_name_label
                color: hex('#333333ff')
                font_size: dp(0.03125*app.width)
                text_size: self.size
                halign: "center"
                valign: "middle"
                size_hint_y: 3

            Label:
                id: completion_label
                color: hex('#333333ff')
                font_size: dp(0.0375*app.width)

        BoxLayout:
            orientation: 'horizontal'
            size_hint_y: 2.23
            padding:[dp(0.0625)*app.width, dp(0.0625)*app.height]
            spacing:dp(0.0625)*app.width

            Button:
                id: repeat_job_button
                text: "Repeat job from the beginning"
                font_size: dp(0.0375*app.width)
                valign: "middle"
                halign: "center"
                text_size: self.size[0] - dp(50), self.size[1]
                on_press: root.repeat_job()
                background_normal: "./asmcnc/skavaUI/img/blank_green_button.png"
                background_down: "./asmcnc/skavaUI/img/blank_green_button.png"

            Button:
                id: recover_job_button
                text: "Recover job"
                font_size: dp(0.0375*app.width)
                valign: "middle"
                halign: "center"
                text_size: self.size[0] - dp(50), self.size[1]
                on_press: root.go_to_recovery()
                background_normal: "./asmcnc/skavaUI/img/blank_orange_button.png"
                background_down: "./asmcnc/skavaUI/img/blank_orange_button.png"

"""
)


class RecoveryDecisionScreen(Screen):

    def __init__(self, **kwargs):
        self.sm = kwargs.pop("screen_manager")
        self.m = kwargs.pop("machine")
        self.jd = kwargs.pop("job")
        self.l = kwargs.pop("localization")
        super(RecoveryDecisionScreen, self).__init__(**kwargs)
        self.update_strings()

    def on_pre_enter(self):
        self.update_completion_label_and_button_colours()

    def update_completion_label_and_button_colours(self):
        if self.jd.job_recovery_cancel_line == None:
            self.job_name_label.text = ""
            self.completion_label.text = self.l.get_str("No file available!")
            self.repeat_job_button.background_normal = (
                "./asmcnc/skavaUI/img/blank_grey_button.png"
            )
            self.repeat_job_button.background_down = (
                "./asmcnc/skavaUI/img/blank_grey_button.png"
            )
            self.recover_job_button.background_normal = (
                "./asmcnc/skavaUI/img/blank_grey_button.png"
            )
            self.recover_job_button.background_down = (
                "./asmcnc/skavaUI/img/blank_grey_button.png"
            )
        else:
            if sys.platform == "win32":
                job_name = self.jd.job_recovery_filepath.split("\\")[-1]
            else:
                job_name = self.jd.job_recovery_filepath.split("/")[-1]
            self.job_name_label.text = job_name
            self.repeat_job_button.background_normal = (
                "./asmcnc/skavaUI/img/blank_green_button.png"
            )
            self.repeat_job_button.background_down = (
                "./asmcnc/skavaUI/img/blank_green_button.png"
            )
            if self.jd.job_recovery_cancel_line == -1:
                self.completion_label.text = self.l.get_str(
                    "SmartBench completed the last job 100%"
                )
                self.recover_job_button.background_normal = (
                    "./asmcnc/skavaUI/img/blank_grey_button.png"
                )
                self.recover_job_button.background_down = (
                    "./asmcnc/skavaUI/img/blank_grey_button.png"
                )
            else:
                self.completion_label.text = self.l.get_str(
                    "SmartBench did not finish the last job"
                )
                self.recover_job_button.background_normal = (
                    "./asmcnc/skavaUI/img/blank_orange_button.png"
                )
                self.recover_job_button.background_down = (
                    "./asmcnc/skavaUI/img/blank_orange_button.png"
                )
        self.update_font_size(self.completion_label)

    def go_to_recovery(self):
        if self.jd.job_recovery_cancel_line != -1:
            self.repeat_job(recovering=True)

    def repeat_job(self, recovering=False):
        if self.jd.job_recovery_cancel_line != None:
            if os.path.isfile(self.jd.job_recovery_filepath):
                if self.jd.job_recovery_filepath != self.jd.filename:
                    self.jd.reset_values()
                    self.jd.job_recovery_from_beginning = True
                    self.jd.set_job_filename(self.jd.job_recovery_filepath)
                    if recovering:
                        self.sm.get_screen("loading").continuing_to_recovery = True
                    else:
                        self.sm.get_screen("loading").skip_check_decision = True
                    self.sm.current = "loading"
                else:
                    self.sm.get_screen("home").z_datum_reminder_flag = True
                    self.jd.reset_recovery()
                    if recovering:
                        self.sm.get_screen("homing_decision").return_to_screen = (
                            "job_recovery"
                        )
                        self.sm.get_screen("homing_decision").cancel_to_screen = (
                            "job_recovery"
                        )
                        self.sm.current = "homing_decision"
                    else:
                        self.jd.job_recovery_from_beginning = True
                        self.back_to_home()
            else:
                error_message = self.l.get_str("File selected does not exist!")
                popup_info.PopupError(self.sm, self.l, error_message)

    def back_to_home(self):
        self.sm.current = "home"

    def update_strings(self):
        self.job_name_header.text = self.l.get_bold("Last job:")
        self.repeat_job_button.text = self.l.get_str("Repeat job from the beginning")
        self.recover_job_button.text = self.l.get_str("Recover job")
        self.update_completion_label_and_button_colours()

    def update_font_size(self, value):
        text_length = self.l.get_text_length(value.text)
        if text_length > 50:
            value.font_size = 0.035 * Window.width
        else:
            value.font_size = 0.0375 * Window.width
