'''
Created on 19 March 2020
Wifi screen

@author: Letty
'''

from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

Builder.load_string("""

<WifiScreen>:
    
    BoxLayout:
        size_hint: (None, None)
        height: dp(480)
        width: dp(800)
        orientation: 'vertical'
        canvas:
            Color:
                rgba: [226 / 255., 226 / 255., 226 / 255., 1.]
            Rectangle:
                pos: self.pos
                size: self.size
        
        BoxLayout:
            size_hint: (None, None)
            height: dp(190)
            width: dp(800)
            padding: [30, 30, 30, 20]
            spacing: 30
            orientation: 'horizontal'
            
            BoxLayout: 
                size_hint: (None, None)
                height: dp(140)
                width: dp(150)
                orientation: 'vertical'
                padding: [0,35,0,10]
                spacing: 10
                canvas:
                    Color:
                        rgba: [76 / 255., 175 / 255., 80 / 255., 1.]
                    RoundedRectangle:
                        pos: self.pos
                        size: self.size
                BoxLayout: 
                    size_hint: (None, None)
                    height: dp(25)
                    width: dp(150)
                    Image:
                        source: "./asmcnc/skavaUI/img/wifi_on.png"
                        center_x: self.parent.center_x
                        y: self.parent.y
                        size: self.parent.width, self.parent.height
                        allow_stretch: True                    

                BoxLayout: 
                    size_hint: (None, None)
                    height: dp(60)
                    width: dp(150)
                    orientation: 'vertical'
                    Label:
                        color: 1,1,1,1
                        font_size: 20
                        markup: True
                        halign: "center"
                        valign: "middle"
                        text_size: self.size
                        size: self.parent.size
                        pos: self.parent.pos
                        text: "IP address:"
                    Label:
                        color: 1,1,1,1
                        font_size: 20
                        markup: True
                        halign: "center"
                        valign: "middle"
                        text_size: self.size
                        size: self.parent.size
                        pos: self.parent.pos
                        text: "(ip address)"
       
            BoxLayout: 
                size_hint: (None, None)
                height: dp(140)
                width: dp(560)
                padding: [10,20,10,20]
                spacing: 10
                canvas:
                    Color:
                        rgba: [1,1,1,1]
                    RoundedRectangle:
                        pos: self.pos
                        size: self.size
                BoxLayout: 
                    size_hint: (None, None)
                    height: dp(100)
                    width: dp(220)     
                    canvas:
                        Color:
                            rgba: [0,1,1,1]  
                        RoundedRectangle:
                            pos: self.pos
                            size: self.size                               
                BoxLayout: 
                    size_hint: (None, None)
                    height: dp(100)
                    width: dp(220)
                    canvas:
                        Color:
                            rgba: [0,1,1,1]
                        RoundedRectangle:
                            pos: self.pos
                            size: self.size                                              
                BoxLayout: 
                    size_hint: (None, None)
                    height: dp(100)
                    width: dp(80)      
                    canvas:
                        Color:
                            rgba: [0,1,1,1] 
                        RoundedRectangle:
                            pos: self.pos
                            size: self.size  
        BoxLayout:
            size_hint: (None, None)
            height: dp(290)
            width: dp(800)
            padding: [30,0,30,30]
            spacing: 30
            
            BoxLayout: 
                size_hint: (None, None)
                height: dp(260)
                width: dp(550)
                orientation: 'horizontal'
                canvas:
                    Color:
                        rgba: [1,1,1,1]
                    RoundedRectangle:
                        pos: self.pos
                        size: self.size
                                                                                   
            BoxLayout: 
                size_hint: (None, None)
                height: dp(260)
                width: dp(160)
                orientation: 'vertical'
                spacing: 30
                canvas:
                    Color:
                        rgba: [226 / 255., 226 / 255., 226 / 255., 1.]
                    RoundedRectangle:
                        pos: self.pos
                        size: self.size
                BoxLayout: 
                    size_hint: (None, None)
                    height: dp(115)
                    width: dp(160)
                    padding: [2,0,0,0]                   
                    Button:
                        size_hint: (None,None)
                        height: dp(115)
                        width: dp(158)
                        background_color: hex('#F4433600')
                        center: self.parent.center
                        pos: self.parent.pos
                        on_press: root.cut_circle()
                        BoxLayout:
                            padding: 0
                            size: self.parent.size
                            pos: self.parent.pos
                            Image:
                                source: "./asmcnc/apps/wifi_app/img/connect.png"
                                center_x: self.parent.center_x
                                y: self.parent.y
                                size: self.parent.width, self.parent.height
                                allow_stretch: True
                BoxLayout: 
                    size_hint: (None, None)
                    height: dp(112)
                    width: dp(160)
                    padding: [28,0,20,0]   
                    Button:
                        size_hint: (None,None)
                        height: dp(112)
                        width: dp(112)
                        background_color: hex('#F4433600')
                        center: self.parent.center
                        pos: self.parent.pos
    #                         on_press: root.cut_circle()
                        BoxLayout:
                            padding: 0
                            size: self.parent.size
                            pos: self.parent.pos
                            Image:
                                source: "./asmcnc/apps/wifi_app/img/quit.png"
                                center_x: self.parent.center_x
                                y: self.parent.y
                                size: self.parent.width, self.parent.height
                                allow_stretch: True
""")

class WifiScreen(Screen):
    
    def __init__(self, **kwargs):
        super(WifiScreen, self).__init__(**kwargs)
        self.sm = kwargs['screen_manager']
        
        
