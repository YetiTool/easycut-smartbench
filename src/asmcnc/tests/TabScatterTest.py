from  kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.base import runTouchApp
from kivy.uix.stencilview import StencilView
from kivy.uix.boxlayout import BoxLayout


class StencilBox(StencilView, BoxLayout):
    def on_touch_down(self, touch):
        if not self.collide_point(*touch.pos):
            return
        return super(StencilBox, self).on_touch_down(touch)

    def on_touch_move(self, touch):
        if not self.collide_point(*touch.pos):
            return
        return super(StencilBox, self).on_touch_move(touch)

    def on_touch_up(self, touch):
        if not self.collide_point(*touch.pos):
            return
        return super(StencilBox, self).on_touch_up(touch)


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
            StencilBox:
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
                        text: 'Tab 1 scatter widget'
                        font_size: 20
                        center: self.parent.width / 2, self.parent.height / 2
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