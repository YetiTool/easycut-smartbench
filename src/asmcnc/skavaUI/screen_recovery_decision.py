import os, sys

from kivy.uix.screenmanager import Screen
from kivy.lang import Builder

from asmcnc.skavaUI import popup_info

Builder.load_string("""

<RecoveryDecisionScreen>:

    recover_job_button:recover_job_button
    repeat_job_button:repeat_job_button

    job_name_label:job_name_label
    completion_label:completion_label

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
            padding: [dp(716), dp(0), dp(0), dp(0)]

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
            size_hint_y: 1.25
            orientation: 'vertical'

            Label:
                text: "[b]Last job:[/b]"
                color: hex('#333333ff')
                markup: True
                font_size: dp(30)

            Label:
                id: job_name_label
                color: hex('#333333ff')
                font_size: dp(25)
                text_size: self.size
                halign: "center"
                valign: "middle"
                size_hint_y: 3

            Label:
                id: completion_label
                color: hex('#333333ff')
                font_size: dp(30)

        BoxLayout:
            orientation: 'horizontal'
            size_hint_y: 2.23
            padding: dp(50), dp(30)
            spacing: dp(50)

            Button:
                id: repeat_job_button
                text: "Repeat job from the beginning"
                font_size: dp(30)
                valign: "middle"
                halign: "center"
                text_size: self.size
                on_press: root.repeat_job()
                background_normal: "./asmcnc/skavaUI/img/blank_green_button.png"
                background_down: "./asmcnc/skavaUI/img/blank_green_button.png"

            Button:
                id: recover_job_button
                text: "Recover job"
                font_size: dp(30)
                valign: "middle"
                halign: "center"
                text_size: self.size
                on_press: root.go_to_recovery()
                background_normal: "./asmcnc/skavaUI/img/blank_orange_button.png"
                background_down: "./asmcnc/skavaUI/img/blank_orange_button.png"

""")


class RecoveryDecisionScreen(Screen):

    def __init__(self, **kwargs):

        super(RecoveryDecisionScreen, self).__init__(**kwargs)
        self.sm=kwargs['screen_manager']
        self.m=kwargs['machine']
        self.jd=kwargs['job']
        self.l=kwargs['localization']

    def on_pre_enter(self):
        # Check if job recovery (or job redo) is available
        if self.jd.job_recovery_cancel_line == None:
            self.job_name_label.text = ''
            self.completion_label.text = "No file loaded!"

            self.repeat_job_button.background_normal = "./asmcnc/skavaUI/img/blank_grey_button.png"
            self.repeat_job_button.background_down = "./asmcnc/skavaUI/img/blank_grey_button.png"

            self.recover_job_button.background_normal = "./asmcnc/skavaUI/img/blank_grey_button.png"
            self.recover_job_button.background_down = "./asmcnc/skavaUI/img/blank_grey_button.png"

        else:
            if sys.platform == 'win32':
                job_name = self.jd.job_recovery_filepath.split("\\")[-1]
            else:
                job_name = self.jd.job_recovery_filepath.split("/")[-1]

            self.job_name_label.text = job_name

            self.repeat_job_button.background_normal = "./asmcnc/skavaUI/img/blank_green_button.png"
            self.repeat_job_button.background_down = "./asmcnc/skavaUI/img/blank_green_button.png"

            # Cancel on line -1 represents last job completing successfully
            if self.jd.job_recovery_cancel_line == -1:
                self.completion_label.text = "SmartBench completed the last job 100%"
                self.recover_job_button.background_normal = "./asmcnc/skavaUI/img/blank_grey_button.png"
                self.recover_job_button.background_down = "./asmcnc/skavaUI/img/blank_grey_button.png"
            else:
                self.completion_label.text = "SmartBench did not finish the last job"
                self.recover_job_button.background_normal = "./asmcnc/skavaUI/img/blank_orange_button.png"
                self.recover_job_button.background_down = "./asmcnc/skavaUI/img/blank_orange_button.png"

    def go_to_recovery(self):
        # Doing it this way because disabling the button causes visuals errors
        if self.jd.job_recovery_cancel_line != -1:
            self.repeat_job(recovering=True)

    def repeat_job(self, recovering=False):
        if self.jd.job_recovery_cancel_line != None:
            if os.path.isfile(self.jd.job_recovery_filepath):
                self.jd.reset_values()
                self.jd.job_recovery_from_beginning = True
                self.jd.set_job_filename(self.jd.job_recovery_filepath)

                if recovering:
                    self.sm.get_screen('loading').continuing_to_recovery = True
                else:
                    self.sm.get_screen('loading').skip_check_decision = True

                self.sm.current = 'loading'

            else: 
                error_message = self.l.get_str('File selected does not exist!')
                popup_info.PopupError(self.sm, self.l, error_message)

    def back_to_home(self):
        self.sm.current = 'home'
