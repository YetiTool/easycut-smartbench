from  kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.base import runTouchApp

Builder.load_string("""

<TabbedTestScreen>:
    TabbedPanel:
        id: tab_panel
        do_default_tab: False
        tab_pos: 'left_top'
        tab_height: 90
        tab_width: 90

        TabbedPanelItem:
            text: '1'
            BoxLayout:
                size: self.size
                pos: self.pos

                Scatter:
                    canvas.after:
                        Color: 
                            rgba: 1,0,0,0.5
                        Rectangle:
                            size: self.size
                            pos: self.pos
                    auto_bring_to_front: False     # this doesn't make any difference
                    center: self.parent.center
                    size: self.parent.size
                    do_rotation: False
                    do_translation: True
                    do_scale: True
                    Label:
                        text: 'Red area = Scatter widget from tab 1'
                        font_size: 20
                        center: self.parent.center
                        size: self.parent.size

        TabbedPanelItem:
            text: '2'
            Label:
                text: '2'
        TabbedPanelItem:
            text: '3' 
            id: home_tab
            Label:
                text: '3'                    
                
""")

class TabbedTestScreen(Screen):

    def __init__(self, **kwargs):
        super(TabbedTestScreen, self).__init__(**kwargs)

runTouchApp(TabbedTestScreen())