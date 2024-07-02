from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

Builder.load_string("""

<YeticutLobbyScreen>:
#:import paths asmcnc.paths
#:import color_provider asmcnc.core_UI.utils.color_provider
#:import get_color_from_hex kivy.utils.get_color_from_hex

    BoxLayout:
        orientation: 'vertical'

        canvas.before:
            Color:
                rgba: color_provider.get_rgba('primary')
            Rectangle:
                size: self.size
                pos: self.pos

        BoxLayout:
            orientation: 'horizontal'

            BoxLayout:
                padding: scaling_utils.get_scaled_tuple((dp(10), dp(10)))

                Button:
                    on_press: root.go_back()
                    background_color: color_provider.get_rgba('transparent')
                    FloatLayout:
                        size: self.parent.size
                        pos: self.parent.pos
                        Image:
                            source: paths.get_resource("back_yc.png")
                            size_hint: None, None
                            size: self.parent.width * 0.9, self.parent.height * 0.9
                            pos_hint: {'center_x': 0.5, 'center_y': 0.5}
                            allow_stretch: False

            Label:
                size_hint_x: 5
                text: ''
                font_size: scaling_utils.get_scaled_width(dp(45))
                bold: True

            BoxLayout

        GridLayout:
            size_hint_y: 3
            rows: 1
            cols: 3
            padding: [scaling_utils.get_scaled_width(dp(100)), scaling_utils.get_scaled_width(dp(40))]
            spacing: [scaling_utils.get_scaled_width(dp(80)), 0]

            BoxLayout:
                orientation: 'vertical'
                
                BoxLayout:
                    size_hint_y: 4
                    # padding: [(self.width - self.height) / 2, 0]
                    
                    Button:
                        on_press: pass
                        background_color: color_provider.get_rgba('transparent')
                        
                        FloatLayout:
                            size_hint: None, None
                            size: self.parent.size
                            pos: self.parent.pos
                            
                            Image:
                                source: paths.get_resource("shapes.png")
                                size_hint: None, None
                                size: self.parent.width * 1.05, self.parent.height * 1.05
                                pos_hint: {'center_x': 0.5, 'center_y': 0.525}
                                allow_stretch: True
                                    
            
                Label:
                    text: 'Shapes'
                    font_size: scaling_utils.get_scaled_width(dp(24))
                    
            BoxLayout:
                orientation: 'vertical'
                
                BoxLayout:
                    size_hint_y: 4
                    # padding: [(self.width - self.height) / 2, 0]
                    
                    Button:
                        on_press: pass
                        background_color: color_provider.get_rgba('transparent')
                        
                        FloatLayout:
                            size_hint: None, None
                            size: self.parent.size
                            pos: self.parent.pos
                            
                            Image:
                                source: paths.get_resource("worktop.png")
                                size_hint: None, None
                                size: self.parent.width * 1.15, self.parent.height * 1.15
                                pos_hint: {'center_x': 0.5, 'center_y': 0.525}
                                allow_stretch: True
                                
                                Image:
                                    source: paths.get_resource("coming_soon.png")
                                    size_hint: None, None
                                    size: self.parent.width / 1.75, self.parent.height / 1.75
                                    allow_stretch: True
                                    pos: self.parent.right - self.width / 1.3, self.parent.top - self.height / 1.3
                                    
            
                Label:
                    text: 'Worktop'
                    font_size: scaling_utils.get_scaled_width(dp(24))

            BoxLayout:
                orientation: 'vertical'
                
                BoxLayout:
                    size_hint_y: 4
                    # padding: [(self.width - self.height) / 2, 0]
                    
                    Button:
                        on_press: pass
                        background_color: color_provider.get_rgba('transparent')
                        
                        FloatLayout:
                            size_hint: None, None
                            size: self.parent.size
                            pos: self.parent.pos
                            
                            Image:
                                source: paths.get_resource("trace.png")
                                size_hint: None, None
                                size: self.parent.width * 1.15, self.parent.height * 1.15
                                pos_hint: {'center_x': 0.5, 'center_y': 0.525}
                                allow_stretch: True
                                
                                Image:
                                    source: paths.get_resource("coming_soon.png")
                                    size_hint: None, None
                                    size: self.parent.width / 1.75, self.parent.height / 1.75
                                    allow_stretch: True
                                    pos: self.parent.right - self.width / 1.3, self.parent.top - self.height / 1.3
            
                Label:
                    text: 'Trace'
                    font_size: scaling_utils.get_scaled_width(dp(24))

        BoxLayout:
            padding: scaling_utils.get_scaled_tuple((dp(250), dp(5), dp(250), dp(15)))

            Button:
                background_color: color_provider.get_rgba('transparent')              
                on_press: root.toolbox_app()
                FloatLayout:
                    size: self.parent.size
                    pos: self.parent.pos
                    Image:
                        source: paths.get_resource("shapes_lobby_toolbox_button_coming_soon.png")
                        size_hint: 0.9, 0.9
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
