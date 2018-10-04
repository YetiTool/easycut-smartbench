from  kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.base import runTouchApp
from kivy.properties import ObjectProperty  # @UnresolvedImport
from kivy.clock import Clock
from kivy.graphics import *
from kivy.utils import *
import math


Builder.load_string("""

<GCodeView>:

    gCodePreview:gCodePreview
    
    BoxLayout:
        Scatter:
            id: gCodePreview
            canvas.before:
                Color:
                    rgba: 1,1,1,1
                Rectangle:
                    size: self.size
                    pos: self.pos
        
        

""")


class GCodeView(Screen):
    

    g0_move_colour = get_color_from_hex('#f4433655')
    feed_move_colour = get_color_from_hex('#2196f355')
    line_width = 1.1

    def __init__(self, **kwargs):
        super(GCodeView, self).__init__(**kwargs)

        with self.gCodePreview.canvas:
            # (center_x, center_y, radius, angle_start, angle_end, segments)
            Color(self.feed_move_colour[0],self.feed_move_colour[1],self.feed_move_colour[2],self.feed_move_colour[3])
            Line(circle=(100, 100, 50, int(90), int(-90), 10),
                 close=False, 
                 width=self.line_width)



runTouchApp(GCodeView())