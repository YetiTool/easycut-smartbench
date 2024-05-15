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
                    rgba: hex('#1976d2')
                Rectangle:
                    size: self.size
                    pos: self.pos

            LabelBase:
                id: title_label
                text: 'Upgrade SB V1.3 to PrecisionPro +'
                halign: 'center'
                valign: 'middle'
                font_size: app.get_scaled_width(30.0)
                text_size: self.size

        BoxLayout:
            orientation: 'vertical'
            size_hint_y: 7

            canvas: 
                Color:
                    rgba: hex('e5e5e5ff')
                Rectangle:
                    size: self.size
                    pos: self.pos

            LabelBase:
                id: success_label
                font_size: app.get_scaled_width(32.0)
                color: 0,0,0,1
                halign: 'center'
                valign: 'middle'
                text_size: self.size

            BoxLayout:
                size_hint_y: 0.25
                padding: app.get_scaled_tuple([175.0, 0, 175.0, 110.0])

                Button:
                    id: continue_button
                    on_press: root.next_screen()
                    font_size: app.get_scaled_width(30.0)
                    background_normal: "./asmcnc/skavaUI/img/next.png"
                    background_down: "./asmcnc/skavaUI/img/next.png"
                    border: app.get_scaled_tuple([14.5, 14.5, 14.5, 14.5])
                    size_hint: (None,None)
                    width: app.get_scaled_width(450.0)
                    height: app.get_scaled_height(60.0)
                    color: hex('#f9f9f9ff')
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
