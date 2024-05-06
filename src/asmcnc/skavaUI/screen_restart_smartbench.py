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

    restart_label : restart_label

    canvas:
        Color: 
            rgba: hex('#e5e5e5')
        Rectangle: 
            size: self.size
            pos: self.pos

    Label:
        id: restart_label
        padding: [dp(10),dp(0)]
        font_size: '40sp'
        color: hex('#333333')
        text_size: self.size
        size: self.texture_size
        halign: "center"
        valign: "middle"
        markup: True

    BoxLayout:
        valign: 'bottom'
        halign: 'left'
        padding: dp(30)

        Button:
            size: dp(80), dp(70) # Slightly bigger than image size, but image is tiny and I think slightly bigger looks fine
            size_hint: None, None
            background_color: color_provider.get_rgba("invisible")
            on_press: root.switch_screen()
            BoxLayout:
                padding: 0
                size: self.parent.size
                pos: self.parent.pos
                Image:
                    source: "./asmcnc/apps/systemTools_app/img/back_to_menu.png"
                    center_x: self.parent.center_x
                    y: self.parent.y
                    size: self.parent.width, self.parent.height
                    allow_stretch: True

""")

class RestartSmartbenchScreen(Screen):

    def __init__(self, **kwargs):
        super(RestartSmartbenchScreen, self).__init__(**kwargs)
        self.sm = kwargs['screen_manager']
        self.l=kwargs['localization']

        self.restart_label.text = self.l.get_str("Please restart SmartBench now.")

    def switch_screen(self):
        self.sm.current = 'release_notes'
