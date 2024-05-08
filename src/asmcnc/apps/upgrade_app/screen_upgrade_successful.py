from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from asmcnc.apps.start_up_sequence.screens import screen_pro_plus_safety

Builder.load_string("""
#:import LabelBase asmcnc.core_UI.components.labels.base_label

<UpgradeSuccessfulScreen>:

    title_label:title_label
    success_label:success_label

    continue_button:continue_button

    BoxLayout:
        orientation: 'vertical'

        BoxLayout:
            canvas:
                Color:
                    rgba: color_provider.get_rgba("blue")
                Rectangle:
                    size: self.size
                    pos: self.pos

            LabelBase:
                id: title_label
                text: 'Upgrade SB V1.3 to PrecisionPro +'
                halign: 'center'
                valign: 'middle'
                font_size: dp(0.0375*app.width)
                text_size: self.size

        BoxLayout:
            orientation: 'vertical'
            size_hint_y: 7

            canvas: 
                Color:
                    rgba: color_provider.get_rgba("light_grey")
                Rectangle:
                    size: self.size
                    pos: self.pos

            LabelBase:
                id: success_label
                font_size: dp(0.04*app.width)
                color: color_provider.get_rgba("black")
                halign: 'center'
                valign: 'middle'
                text_size: self.size

            BoxLayout:
                size_hint_y: 0.25
                padding:[dp(0.21875)*app.width, 0, dp(0.21875)*app.width, dp(0.229166666667)*app.height]

                Button:
                    id: continue_button
                    on_press: root.next_screen()
                    font_size: dp(0.0375*app.width)
                    background_normal: "./asmcnc/skavaUI/img/next.png"
                    background_down: "./asmcnc/skavaUI/img/next.png"
                    border: [dp(14.5)]*4
                    size_hint: (None,None)
                    width: dp(0.5625*app.width)
                    height: dp(0.125*app.height)
                    color: color_provider.get_rgba("near_white")
                    center: self.parent.center
                    pos: self.parent.pos
                    text_size: self.size
                    halign: "center"
                    valign: "middle"

"""
)


class UpgradeSuccessfulScreen(Screen):
    def __init__(self, **kwargs):
        super(UpgradeSuccessfulScreen, self).__init__(**kwargs)
        self.sm = kwargs["screen_manager"]
        self.m = kwargs["machine"]
        self.l = kwargs["localization"]
        self.update_strings()

    def next_screen(self):
        if not self.sm.has_screen("pro_plus_safety"):
            pro_plus_safety_screen = screen_pro_plus_safety.ProPlusSafetyScreen(
                name="pro_plus_safety",
                start_sequence=None,
                screen_manager=self.sm,
                localization=self.l,
            )
            self.sm.add_widget(pro_plus_safety_screen)
        self.sm.current = "pro_plus_safety"

    def update_strings(self):
        self.title_label.text = self.l.get_str("Upgrade SB V1.3 to PrecisionPro +")
        self.success_label.text = self.l.get_str("Upgrade successful!")
        self.continue_button.text = self.l.get_str("Continue")
