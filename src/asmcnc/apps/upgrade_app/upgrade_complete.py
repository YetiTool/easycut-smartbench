from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

Builder.load_string("""
<UpgradeComplete>:
    BoxLayout:
        orientation: 'vertical'
        
        canvas:
            Color:
                rgba: hex('##e5e5e5')
            Rectangle:
                size: self.size
                pos: self.pos
                
        Label:
            text: ''
            height: dp(200)
        
        Label:
            text: 'Upgrade successful!'
            color: [0, 0, 0, 1]
            font_size: dp(28)
        
        Button:
            text: 'Continue'
            size_hint: None, None
            width: dp(400)
            height: dp(50)
            on_press: root.exit()
            color: hex('#f9f9f9ff')
            background_normal: "asmcnc/skavaUI/img/blank_long_button.png"
            
        Label:
            text: ''
            height: dp(200)
""")


class UpgradeComplete(Screen):
    def __init__(self, **kwargs):
        super(UpgradeComplete, self).__init__(**kwargs)
        self.sm = kwargs['screen_manager']
        self.m = kwargs['machine']
        self.l = kwargs['localization']
        self.localize()

    def localize(self):
        pass

    def exit(self):
        self.sm.current = 'lobby'
