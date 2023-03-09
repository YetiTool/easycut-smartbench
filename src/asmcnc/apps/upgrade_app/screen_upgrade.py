from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

Builder.load_string("""
<UpgradeScreen>:

    instruction_label:instruction_label

    BoxLayout:
        orientation: 'vertical'

        BoxLayout:
            orientation: 'horizontal'

            canvas:
                Color:
                    rgba: hex('#1976d2')
                Rectangle:
                    size: self.size
                    pos: self.pos

            BoxLayout:
                padding: [dp(60),0,0,0]

                Label:
                    text: 'Upgrade SB V1.3 to PrecisionPro +'
                    halign: 'center'
                    valign: 'middle'
                    font_size: dp(30)
                    text_size: self.size

            BoxLayout:
                size_hint_x: 0.08
                padding: dp(5)

                Button:
                    id: exit_button
                    size_hint: (None,None)
                    height: dp(50)
                    width: dp(50)
                    background_color: [0,0,0,0]
                    opacity: 1
                    on_press: root.quit_to_lobby()
                    BoxLayout:
                        padding: 0
                        size: self.parent.size
                        pos: self.parent.pos
                        Image:
                            source: "./asmcnc/apps/shapeCutter_app/img/exit_icon.png"
                            center_x: self.parent.center_x
                            y: self.parent.y
                            size: self.parent.width, self.parent.height
                            allow_stretch: True

        BoxLayout:
            orientation: 'vertical'
            size_hint_y: 7

            canvas: 
                Color:
                    rgba: hex('e5e5e5ff')
                Rectangle:
                    size: self.size
                    pos: self.pos

            BoxLayout:
                orientation: 'vertical'

                Label:
                    id: instruction_label
                    size_hint_y: 2
                    font_size: dp(20)
                    color: 0,0,0,1
                    halign: 'center'
                    valign: 'middle'
                    text_size: self.size

                TextInput

            BoxLayout

""")

class UpgradeScreen(Screen):

    def __init__(self, **kwargs):
        super(UpgradeScreen, self).__init__(**kwargs)

        self.sm = kwargs['screen_manager']
        self.m = kwargs['machine']
        self.l = kwargs['localization']

    def on_pre_enter(self):
        self.update_strings()

    def quit_to_lobby(self):
        self.sm.current = 'lobby'

    def update_strings(self):
        self.instruction_label.text = (
            '1. ' + self.l.get_str('Plug in your SC2 Spindle motor (both power and data cable)') + '\n' + \
            '2. ' + self.l.get_str('Type in your upgrade code below') + '\n' + \
            '3. ' + self.l.get_str('Press "Enter" on the keyboard')
        )
