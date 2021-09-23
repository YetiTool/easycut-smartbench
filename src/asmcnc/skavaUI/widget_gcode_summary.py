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

        summary_list = []
        metadata_list = self.jd.metadata_dict.items()
        if len(metadata_list) > 0:
            summary_list.append("[b]SmartTransfer data[/b]")
            [summary_list.append(': '.join(sublist)) for sublist in metadata_list]
            summary_list = [x for x in summary_list if not "ProductionNotes" in x]
            summary_list.append('')


        summary_list.append('[b]Feeds and Speeds:[/b]\n')
        if self.jd.feedrate_max == None and self.jd.feedrate_min == None:
            summary_list.append('Feed rate range: Undefined')
        else:
            summary_list.append('Feed rate range: ' + str(self.jd.feedrate_min) + ' to ' + str(self.jd.feedrate_max))

        if self.jd.spindle_speed_max == None and self.jd.feedrate_min == None:
            summary_list.append('Spindle speed range: Undefined\n')
        else:
            summary_list.append('Spindle speed range: ' + str(self.jd.spindle_speed_min) + ' to ' + str(self.jd.spindle_speed_max) + '\n')


        summary_list.append('[b]Working volume:[/b]\n')
        if self.jd.x_max == -999999 and self.jd.x_min == 999999:
            summary_list.append('X range: Undefined\n')
        else:
            summary_list.append('X min: ' + str(self.jd.x_min))
            summary_list.append('X max: ' + str(self.jd.x_max) + '\n')

        if self.jd.y_max == -999999 and self.jd.y_min == 999999:
            summary_list.append('Y range: Undefined\n')
        else:
            summary_list.append('Y min: ' + str(self.jd.y_min))
            summary_list.append('Y max: ' + str(self.jd.y_max) + '\n')

        if self.jd.z_max == -999999 and self.jd.z_min == 999999:
            summary_list.append('Z range: Undefined\n')
        else:
            summary_list.append('Z min: ' + str(self.jd.z_min))
            summary_list.append('Z max: ' + str(self.jd.z_max) + '\n')


        summary_list.append('[b]Check info and warnings:[/b]\n')
        if self.jd.checked == False:
            summary_list.append('Checked: No\n')
        else:
            summary_list.append('Checked: Yes')
            summary_list.append('Check warning: ' + self.jd.check_warning + '\n')


        summary_list.append('[b]Comments:[/b]\n')
        summary_list.extend(self.jd.comments_list)

        self.gcode_scrollview.text_container.text = '\n'.join(summary_list)

    def hide_summary(self):

        self.gcode_scrollview.text_container.text = ''
