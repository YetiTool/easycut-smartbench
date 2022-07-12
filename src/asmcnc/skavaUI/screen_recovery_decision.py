from kivy.uix.screenmanager import Screen
from kivy.lang import Builder

Builder.load_string("""

<RecoveryDecisionScreen>:

    info_label:info_label

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

        Label:
            id: info_label
            size_hint_y: 1.25
            text: "[b]Last job:[/b]"
            markup: True
            color: hex('#333333ff')
            font_size: dp(35)

        BoxLayout:
            orientation: 'horizontal'
            size_hint_y: 2.23
            padding: dp(50), dp(30)
            spacing: dp(50)

            Button:
                text: "Repeat job from the beginning"
                font_size: dp(30)
                valign: "middle"
                halign: "center"
                text_size: self.size
                on_press: root.repeat_job()
                background_normal: "./asmcnc/skavaUI/img/blank_green_button.png"
                background_down: "./asmcnc/skavaUI/img/blank_green_button.png"

            Button:
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
        self.info_label.text = "[b]Last job:[/b]\n" + self.jd.job_name + "\nSmartBench did not finish the last job"

    def go_to_recovery(self):
        self.sm.get_screen('homing_decision').return_to_screen = 'job_recovery'
        self.sm.get_screen('homing_decision').cancel_to_screen = 'job_recovery'
        self.sm.current = 'homing_decision'

    def repeat_job(self):
        self.jd.reset_recovery()
        self.sm.get_screen('homing_decision').return_to_screen = 'home'
        self.sm.get_screen('homing_decision').cancel_to_screen = 'home'
        self.sm.current = 'homing_decision'

    def back_to_home(self):
        self.sm.current = 'home'
