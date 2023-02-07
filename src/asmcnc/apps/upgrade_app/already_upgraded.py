from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

Builder.load_string("""
<AlreadyUpgraded>:
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
            text: 'Your machine is already upgraded to PrecisionPro +!'
            color: [0, 0, 0, 1]
            font_size: dp(28)
        
        BoxLayout:
            padding: [dp(200),0,0,0]
            
            Button:
                text: 'Continue'
                on_press: root.exit()
                color: hex('#f9f9f9ff')
                background_normal: "asmcnc/skavaUI/img/blank_long_button.png"
                font_size: dp(24)
                size_hint: None, None
                width: dp(400)
                height: dp(90)
                halign: 'center'
            
        Label:
            text: ''
            height: dp(200)
""")


class AlreadyUpgraded(Screen):
    def __init__(self, **kwargs):
        super(AlreadyUpgraded, self).__init__(**kwargs)
        self.sm = kwargs['screen_manager']
        self.m = kwargs['machine']
        self.l = kwargs['localization']
        self.localize()

    def localize(self):
        pass

    def exit(self):
        self.sm.current = 'lobby'
