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
                    on_press: root.go_back()
                    background_color: hex('#FFFFFF00')
                    FloatLayout:
                        size: self.parent.size
                        pos: self.parent.pos
                        Image:
                            source: "./asmcnc/skavaUI/img/Shapes_lobby_back_button.png"
                            size_hint: None, None
                            size: self.parent.width * 0.7, self.parent.height * 0.7
                            pos_hint: {'center_x': 0.5, 'center_y': 0.5}
                            allow_stretch: False

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
                        background_color: hex('#FFFFFF00')
                        
                        BoxLayout:
                            size: self.parent.size
                            pos: self.parent.pos
                            
                            Image:
                                id: yeticut_apps_image
                                source: "./asmcnc/skavaUI/img/Shapes_lobby_logo.png"
                                center_x: self.parent.center_x
                                y: self.parent.y
                                size: self.parent.width, self.parent.height
                                allow_stretch: True
                                
                Label:
                    text: 'Shapes'
                    font_size: scaling_utils.get_scaled_width(dp(20))
                    bold: True
                    
            BoxLayout:
                orientation: 'vertical'
                
                BoxLayout:
                    size_hint_y: 4
                    padding: [(self.width - self.height) / 2, 0]
                    
                    Button:
                        on_press: pass
                        background_color: hex('#FFFFFF00')
                        
                        FloatLayout:
                            size_hint: None, None
                            size: self.parent.size
                            pos: self.parent.pos
                            
                            Image:
                                source: "./asmcnc/skavaUI/img/Worktop_lobby_logo.png"
                                size_hint: None, None
                                size: self.parent.width * 1.05, self.parent.height * 1.05
                                pos_hint: {'center_x': 0.5, 'center_y': 0.525}
                                allow_stretch: True
            
                Label:
                    text: 'Worktop'
                    font_size: scaling_utils.get_scaled_width(dp(20))
                    bold: True

            BoxLayout

            BoxLayout

            BoxLayout

            BoxLayout

            BoxLayout

            BoxLayout

        BoxLayout:
            padding: scaling_utils.get_scaled_tuple((dp(250), dp(5), dp(250), dp(15)))

            Button:
                background_color: hex('#FFFFFF00')                
                on_press: root.toolbox_app()
                FloatLayout:
                    size: self.parent.size
                    pos: self.parent.pos
                    Image:
                        source: "./asmcnc/skavaUI/img/Shapes_lobby_toolbox_button.png"
                        size_hint: None, None
                        size: self.parent.width, self.parent.height
                        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
                        allow_stretch: False

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
