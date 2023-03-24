from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

Builder.load_string("""
<ProPlusSafetyScreen>:

    title_label:title_label
    context:context
    instructions_grid:instructions_grid

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
                font_size: dp(30)
                text_size: self.size

        BoxLayout:
            orientation: 'vertical'
            size_hint_y: 7
            padding: [20,10,20,0]

            canvas: 
                Color:
                    rgba: hex('e5e5e5ff')
                Rectangle:
                    size: self.size
                    pos: self.pos

            Label:
                id: context
                size_hint_y: 0.41
                font_size: dp(18)
                color: 0,0,0,1
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
                    padding: [10,0]
                    Image:                         
                        source: "./asmcnc/skavaUI/img/popup_error_visual.png"
                        center_x: self.parent.center_x
                        center_y: self.parent.center_y
                        # size: self.parent.width, self.parent.height
                        allow_stretch: True

                Label:
                    font_size: dp(18)
                    color: 0,0,0,1
                    halign: 'left'
                    valign: 'middle'
                    text_size: self.size
                    markup: True
                    text: "The Spindle motor MUST be clamped securely BEFORE plugging in the Spindle motor cables."

                BoxLayout:
                    padding: [10,0]
                    Image:                         
                        source: "./asmcnc/skavaUI/img/popup_error_visual.png"
                        center_x: self.parent.center_x
                        center_y: self.parent.center_y
                        # size: self.parent.width, self.parent.height
                        allow_stretch: True

                Label:
                    font_size: dp(18)
                    color: 0,0,0,1
                    halign: 'left'
                    valign: 'middle'
                    text_size: self.size
                    markup: True
                    text: "If you start any job with the Spindle motor health check enabled, your tool MUST be rated upto 24,000 RPM."


            BoxLayout:
                size_hint_y: 0.29
                padding: [dp(175),dp(0),dp(175),dp(42)]

                Button:
                    id: continue_button
                    on_press: root.next_screen()
                    font_size: dp(30)
                    background_normal: "./asmcnc/skavaUI/img/next.png"
                    background_down: "./asmcnc/skavaUI/img/next.png"
                    border: [dp(14.5)]*4
                    size_hint: (None,None)
                    width: dp(450)
                    height: dp(79)
                    color: hex('#f9f9f9ff')
                    text_size: self.size
                    halign: "center"
                    valign: "middle"

""")

class ProPlusSafetyScreen(Screen):

    def __init__(self, **kwargs):
        super(ProPlusSafetyScreen, self).__init__(**kwargs)

        self.sm = kwargs['screen_manager']
        self.l = kwargs['localization']
        self.start_seq=kwargs['start_sequence']

        self.update_strings()

        def next_screen(self):
            os.system('sudo sed -i "s/user_has_seen_pro_plus_safety=True/user_has_seen_pro_plus_safety=False/" /home/pi/easycut-smartbench/src/config.txt')
            try: 
                self.start_seq.next_in_sequence()
            except: 
                self.sm.current = 'lobby'

    def update_strings(self):
        self.title_label.text = self.l.get_str('Safety Information: PrecisionPro +')
        self.context.text = \
            self.l.get_str("PrecisionPro + reads data from the smart SC2 Spindle motor.") + "\n\n" + \
            self.l.get_str("You can disable and enable PrecisionPro + features at any time in the maintenance app.") + "\n\n" + \
            self.l.get_str("In order to read and analyse the data, SmartBench must be able to turn the Spindle motor on safely.").replace(
                "SmartBench must be able to turn the Spindle motor on safely", self.l.get_bold("SmartBench must be able to turn the Spindle motor on safely")
                )
        self.continue_button.text = self.l.get_str("I understand")
