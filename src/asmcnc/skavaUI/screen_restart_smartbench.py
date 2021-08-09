'''
Created on 9 Aug 2021
@author: Dennis
Screen shown after exiting release notes telling the user to restart
'''

import kivy
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

Builder.load_string("""

<RestartSmartbenchScreen>:

    canvas:
        Color: 
            rgba: hex('#FFFFFF')
        Rectangle: 
            size: self.size
            pos: self.pos

    Label:
        text: 'Please restart SmartBench now.'
        font_size: '40sp'
        color: hex('#000000')

    BoxLayout:
        valign: 'bottom'
        halign: 'left'
        padding: dp(30)

        Button:
            size: dp(100), dp(80)
            size_hint: None, None
            background_color: 0,0,0,0
            on_press: root.switch_screen()
            BoxLayout:
                padding: 0
                size: self.parent.size
                pos: self.parent.pos
                Image:
                    source: "./asmcnc/skavaUI/img/back_arrow.png"
                    center_x: self.parent.center_x
                    y: self.parent.y
                    size: self.parent.width, self.parent.height
                    allow_stretch: True

""")

class RestartSmartbenchScreen(Screen):

    def __init__(self, **kwargs):
        super(RestartSmartbenchScreen, self).__init__(**kwargs)
        self.sm = kwargs['screen_manager']

    def switch_screen(self):
        self.sm.current = 'release_notes'
