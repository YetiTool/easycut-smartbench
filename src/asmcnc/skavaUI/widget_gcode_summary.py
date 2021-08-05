'''
Created on 26 Jul 2021
@author: Dennis
Widget to display gcode as an alternative to a drawing
'''

import kivy
from kivy.lang import Builder
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget
from kivy.properties import StringProperty

Builder.load_string("""

<ScrollViewGCode>:

    text_container: text_container

    Label:
        id: text_container
        color: [0, 0, 0, 1]
        size_hint_y: None
        height: self.texture_size[1]
        text_size: self.width, None
        markup: True

<GCodeSummary>:

    gcode_scrollview: gcode_scrollview

    BoxLayout:
        size: self.parent.size
        pos: self.parent.pos

        ScrollViewGCode:
            id: gcode_scrollview

""")

class ScrollViewGCode(ScrollView):
    text = StringProperty('')

class GCodeSummary(Widget):

    def __init__(self, **kwargs):
        super(GCodeSummary, self).__init__(**kwargs)
        self.jd = kwargs['job']

    def display_summary(self):

        summary_list = ['[b]Feeds and Speeds:[/b]\n']
        if self.jd.feedrate_max == 0 and self.jd.feedrate_min == 0:
            summary_list.append('Feed rate range: Undefined')
        else:
            summary_list.append('Feed rate range: ' + str(self.jd.feedrate_min) + ' to ' + str(self.jd.feedrate_max))

        summary_list.append('[b]Comments:[/b]\n')
        summary_list.extend(self.jd.comments_list)

        self.gcode_scrollview.text_container.text = '\n'.join(summary_list)
