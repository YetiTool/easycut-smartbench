from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

Builder.load_string("""
<UpgradeAppHome>:
    unlock_code:unlock_code

    BoxLayout:
        orientation: 'vertical'

        canvas:
            Color:
                rgba: hex('##e5e5e5')
            Rectangle:
                size: self.size
                pos: self.pos
        
        GridLayout:
            orientation: 'vertical'
            rows: 2
            cols: 1
            
            BoxLayout:
                orientation: 'vertical'
                
                Label:
                    text: "This app allows you to upgrade your SmartBench v1.3 [b]PrecisionPro[/b] to a [b]PrecisionPro +[/b].\\nYou will have needed to purchase an upgrade package. For more information on the upgrade,\\n please visit www.yetitool.com/PRODUCTS/upgrades"
                    halign: "center"
                    markup: True
                    color: 0,0,0,1
                    size_hint_y: None
                    height: dp(90)
                    
                Label:
                    text: "This app allows you to upgrade your SmartBench v1.3 [b]PrecisionPro[/b] to a [b]PrecisionPro +[/b].\\nYou will have needed to purchase an upgrade package. For more information on the upgrade,\\n please visit www.yetitool.com/PRODUCTS/upgrades"
                    halign: "center"
                    markup: True
                    color: 0,0,0,1
                    size_hint_y: None
                    height: dp(90)
            
            AnchorLayout:

                TextInput:
                    id: unlock_code
                    multiline: False
                    font_size: dp(28)
                    color: 0,0,0,1  
                    size_hint: None, None
                    height: dp(50)
                    width: dp(300)
                    padding: 0
""")


class UpgradeAppHome(Screen):
    def __init__(self, **kwargs):
        super(UpgradeAppHome, self).__init__(**kwargs)

        self.sm = kwargs['screen_manager']
        self.m = kwargs['machine']

