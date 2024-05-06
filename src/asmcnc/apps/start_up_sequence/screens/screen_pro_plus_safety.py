from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
import os

Builder.load_string(
    """
<ProPlusSafetyScreen>:

    title_label:title_label
    context:context
    instructions_grid:instructions_grid
    clamp_warning_label:clamp_warning_label
    rpm_warning_label:rpm_warning_label

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

            Label:
                id: title_label
                text: 'Safety Information: PrecisionPro +'
                halign: 'center'
                valign: 'middle'
                font_size: dp(0.0375*app.width)
                text_size: self.size

        BoxLayout:
            orientation: 'vertical'
            size_hint_y: 7
            padding:[dp(0.025)*app.width, dp(0.0208333333333)*app.height, dp(0.025)*app.width, 0]

            canvas: 
                Color:
                    rgba: hex('e5e5e5ff')
                Rectangle:
                    size: self.size
                    pos: self.pos

            Label:
                id: context
                size_hint_y: 0.41
                font_size: dp(0.0225*app.width)
                color: color_provider.get_rgba("black")
                halign: 'center'
                valign: 'middle'
                text_size: self.size
                markup: True

            GridLayout:
                id: instructions_grid
                size_hint_y: 0.3
                cols_minimum: {0: dp(60), 1: dp(700)}
                rows: 2
                cols: 2

                BoxLayout:
                    padding:[dp(0.0125)*app.width, 0]
                    Image:                         
                        source: "./asmcnc/skavaUI/img/popup_error_visual.png"
                        center_x: self.parent.center_x
                        center_y: self.parent.center_y
                        # size: self.parent.width, self.parent.height
                        allow_stretch: True

                Label:
                    id: clamp_warning_label
                    font_size: dp(0.0225*app.width)
                    color: color_provider.get_rgba("black")
                    halign: 'left'
                    valign: 'middle'
                    text_size: self.size
                    markup: True
                    text: "The Spindle motor MUST be clamped securely BEFORE plugging in the Spindle motor cables."

                BoxLayout:
                    padding:[dp(0.0125)*app.width, 0]
                    Image:                         
                        source: "./asmcnc/skavaUI/img/popup_error_visual.png"
                        center_x: self.parent.center_x
                        center_y: self.parent.center_y
                        # size: self.parent.width, self.parent.height
                        allow_stretch: True

                Label:
                    id: rpm_warning_label
                    font_size: dp(0.0225*app.width)
                    color: color_provider.get_rgba("black")
                    halign: 'left'
                    valign: 'middle'
                    text_size: self.size
                    markup: True
                    text: "If you start any job with the Spindle motor health check enabled, your tool MUST be rated up to 24,000 RPM."


            BoxLayout:
                size_hint_y: 0.29
                padding:[dp(0.0125)*app.width, 0, dp(0.0125)*app.width, dp(0.0208333333333)*app.height]
                size_hint: (None, None)
                height: dp(0.254166666667*app.height)
                width: dp(1.0*app.width)
                orientation: 'horizontal'
                BoxLayout: 
                    size_hint: (None, None)
                    height: dp(0.254166666667*app.height)
                    width: dp(0.305625*app.width)
                    padding:[0, 0, dp(0.230625)*app.width, 0]
                    Button:
                        font_size: str(0.01875 * app.width) + 'sp'
                        size_hint: (None,None)
                        height: dp(0.108333333333*app.height)
                        width: dp(0.075*app.width)
                        background_color: color_provider.get_rgba("invisible")
                        center: self.parent.center
                        pos: self.parent.pos
                        on_press: root.prev_screen()
                        BoxLayout:
                            padding: 0
                            size: self.parent.size
                            pos: self.parent.pos
                            Image:
                                source: "./asmcnc/apps/systemTools_app/img/back_to_menu.png"
                                center_x: self.parent.center_x
                                y: self.parent.y
                                size: self.parent.width, self.parent.height
                                allow_stretch: True
                BoxLayout: 
                    size_hint: (None, None)
                    height: dp(0.254166666667*app.height)
                    width: dp(0.36375*app.width)
                    padding:[0, 0, 0, dp(0.0666666666667)*app.height]
                    Button:
                        id: continue_button
                        background_normal: "./asmcnc/skavaUI/img/next.png"
                        background_down: "./asmcnc/skavaUI/img/next.png"
                        border: [dp(14.5)]*4
                        size_hint: (None,None)
                        width: dp(0.36375*app.width)
                        height: dp(0.164583333333*app.height)
                        on_press: root.next_screen()
                        text: 'Next...'
                        font_size: str(0.0375*app.width) + 'sp'
                        color: hex('#f9f9f9ff')
                        markup: True
                        center: self.parent.center
                        pos: self.parent.pos
                BoxLayout: 
                    size_hint: (None, None)
                    height: dp(0.254166666667*app.height)
                    width: dp(0.305625*app.width)
                    padding:[dp(0.241875)*app.width, 0, 0, 0]

"""
)


class ProPlusSafetyScreen(Screen):
    def __init__(self, **kwargs):
        super(ProPlusSafetyScreen, self).__init__(**kwargs)
        self.sm = kwargs["screen_manager"]
        self.l = kwargs["localization"]
        self.start_seq = kwargs["start_sequence"]
        self.update_strings()

    def next_screen(self):
        self.update_seen()
        try:
            self.start_seq.next_in_sequence()
        except:
            self.sm.current = "lobby"

    def prev_screen(self):
        try:
            self.start_seq.prev_in_sequence()
        except:
            if self.sm.has_screen("already_upgraded"):
                self.sm.current = "already_upgraded"
            elif self.sm.has_screen("upgrade_successful"):
                self.sm.current = "upgrade_successful"

    def update_seen(self):
        user_has_seen_pro_plus_safety = os.popen(
            'grep "user_has_seen_pro_plus_safety" /home/pi/easycut-smartbench/src/config.txt'
        ).read()
        if not user_has_seen_pro_plus_safety:
            os.system(
                "sudo sed -i -e '$auser_has_seen_pro_plus_safety=True' /home/pi/easycut-smartbench/src/config.txt"
            )
        elif "False" in user_has_seen_pro_plus_safety:
            os.system(
                'sudo sed -i "s/user_has_seen_pro_plus_safety=False/user_has_seen_pro_plus_safety=True/" /home/pi/easycut-smartbench/src/config.txt'
            )

    def update_strings(self):
        self.title_label.text = self.l.get_str("Safety Information: PrecisionPro +")
        self.context.text = (
            self.l.get_str(
                "PrecisionPro + reads data from the smart SC2 Spindle motor."
            )
            + "\n\n"
            + self.l.get_str(
                "You can disable and enable PrecisionPro + features at any time in the maintenance app."
            )
            + "\n\n"
            + self.l.get_str(
                "In order to read and analyse the data, SmartBench must be able to turn the Spindle motor on safely."
            ).replace(
                self.l.get_str(
                    "SmartBench must be able to turn the Spindle motor on safely"
                ),
                self.l.get_bold(
                    "SmartBench must be able to turn the Spindle motor on safely"
                ),
            )
        )
        self.continue_button.text = self.l.get_str("I understand")
        self.clamp_warning_label.text = self.l.get_str(
            "The Spindle motor MUST be clamped securely BEFORE plugging in the Spindle motor cables."
        )
        self.rpm_warning_label.text = self.l.get_str(
            "If you start any job with the Spindle motor health check enabled, your tool MUST be rated up to 24,000 RPM."
        )
