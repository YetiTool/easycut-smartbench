from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

Builder.load_string("""

<YeticutLobbyScreen>:

    BoxLayout:
        orientation: 'vertical'

        canvas.before:
            Color: 
                rgba: hex('#0d47a1FF')
            Rectangle: 
                size: self.size
                pos: self.pos

        BoxLayout:
            orientation: 'horizontal'

            BoxLayout:
                padding: scaling_utils.get_scaled_tuple((dp(10), dp(10)))

                Button:
                    text: 'Back up ^'
                    on_press: root.go_back()

            Label:
                size_hint_x: 4
                text: 'YetiCut'
                font_size: scaling_utils.get_scaled_width(dp(45))
                bold: True

            BoxLayout

        GridLayout:
            size_hint_y: 3
            rows: 2
            cols: 4
            padding: [scaling_utils.get_scaled_width(dp(120)), 0]

            BoxLayout:
                orientation: 'vertical'

                BoxLayout:
                    size_hint_y: 4
                    padding: [(self.width - self.height) / 2, 0]

                    Button:
                        on_press: root.shapes_app()

                Label:
                    text: 'Shapes'
                    font_size: scaling_utils.get_scaled_width(dp(20))
                    bold: True

            BoxLayout

            BoxLayout

            BoxLayout

            BoxLayout

            BoxLayout

            BoxLayout

            BoxLayout

        BoxLayout:
            padding: scaling_utils.get_scaled_tuple((dp(250), dp(5), dp(250), dp(15)))

            Button:
                text: 'ToolBox'
                on_press: root.toolbox_app()

""")


class YeticutLobbyScreen(Screen):

    def __init__(self, **kwargs):
        super(YeticutLobbyScreen, self).__init__(**kwargs)
        self.sm = kwargs['screen_manager']
        self.m = kwargs['machine']
        self.l = kwargs['localization']
        self.am = kwargs['app_manager']

    def shapes_app(self):
        self.am.start_drywall_cutter_app()

    def toolbox_app(self):
        pass

    def go_back(self):
        self.sm.current = 'lobby'
