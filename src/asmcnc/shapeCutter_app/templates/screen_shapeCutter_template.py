'''
Created on 20 February 2020
Template Screen for the Shape Cutter App

@author: Letty
'''

from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.tabbedpanel import TabbedPanel

Builder.load_string("""

<ShapeCutterTemplateScreenClass>

    BoxLayout:
        padding: 0
        spacing: 10
        orientation: "vertical"

        BoxLayout:
            size_hint_y: 0.9
            padding: 0
            spacing: 10
            orientation: "horizontal"

            BoxLayout:
                size_hint_x: 0.9

                TabbedPanel:
                    size_hint: 1, 1
                    pos_hint: {'center_x': .5, 'center_y': .5}
                    do_default_tab: False
                    tab_pos: 'top_mid'
                    tab_height: 90
                    tab_width: 90

                    TabbedPanelItem:
                        background_normal: 'asmcnc/skavaUI/img/tab_set_normal.png'
                        background_down: 'asmcnc/skavaUI/img/tab_set_up.png'
                        BoxLayout:
                            padding: 20
                            spacing: 20
                            canvas:
                                Color:
                                    rgba: hex('#E5E5E5FF')
                                Rectangle:
                                    size: self.size
                                    pos: self.pos

                            BoxLayout:
                                size_hint_x: 3
                                canvas:
                                    Color:
                                        rgba: 1,1,1,1
                                    RoundedRectangle:
                                        size: self.size
                                        pos: self.pos

                    TabbedPanelItem:
                        background_normal: 'asmcnc/skavaUI/img/tab_move_normal.png'
                        background_down: 'asmcnc/skavaUI/img/tab_move_up.png'
                        BoxLayout:
                            orientation: 'horizontal'
                            padding: 20
                            spacing: 20
                            canvas:
                                Color:
                                    rgba: hex('#E5E5E5FF')
                                Rectangle:
                                    size: self.size
                                    pos: self.pos

                            BoxLayout:
                                size_hint_x: 3
                                canvas:
                                    Color:
                                        rgba: 1,1,1,1
                                    RoundedRectangle:
                                        size: self.size
                                        pos: self.pos

""")

class ShapeCutterTemplateScreenClass(Screen):
    
    def __init__(self, **kwargs):
        super(ShapeCutterTemplateScreenClass, self).__init__(**kwargs)
        self.sm=kwargs['screen_manager']
        self.m=kwargs['machine']

        