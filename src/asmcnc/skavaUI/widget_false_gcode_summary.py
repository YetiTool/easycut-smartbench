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

    def display_summary(self):
        summary_list = [

        '[b]Project:[/b]' + "\n" + \
        "Aaron's custom kitchen" + "\n" + \
        '[b]Process Step:[/b]' + "\n" + \
        "1" + "\n" + \
        '[b]Production Notes:[/b]' + "\n" + \
        "Use mahogany" + "\n" + \
        '[b]Client:[/b]' + "\n" + \
        "Aaron" + "\n" + \
        '[b]Order Code:[/b]' + "\n" + \
        "0895" + "\n" + \
        '[b]Part Code:[/b]' + "\n" + \
        "141b" + "\n" + \
        '[b]Work Description:[/b]' + "\n" + \
        "Cabinet doors" + "\n" + \
        '[b]Primary Operator:[/b]' + "\n" + \
        "Trev" + "\n" + \
        '[b]Batch Number:[/b]' + "\n" + \
        "677" + "\n" + \
        '[b]Estimated Production Time:[/b]' + "\n" + \
        "00:37:00" + "\n" + \
        '[b]Total Number of Parts Required:[/b]' + "\n" + \
        "24" + "\n" + \
        '[b]Parts made per job:[/b]' + "\n" + \
        "8" + "\n" + \
        '[b]Feeds and Speeds:[/b]\n' + \
        'Feed rate range: 0 - 300 mm/min\n' + \
        'Spindle speed range: 15000 - 25000\n' + \
        '[b]Comments:[/b]\n' + \
        "This is gonna be ace!!"
        ]

        self.gcode_scrollview.text_container.text = '\n'.join(summary_list)


    #     self.jd = kwargs['job']

    # def display_summary(self):

    #     summary_list = ['[b]Feeds and Speeds:[/b]\n']
    #     if self.jd.feedrate_max == None and self.jd.feedrate_min == None:
    #         summary_list.append('Feed rate range: Undefined')
    #     else:
    #         summary_list.append('Feed rate range: ' + str(self.jd.feedrate_min) + ' to ' + str(self.jd.feedrate_max))

    #     if self.jd.spindle_speed_max == None and self.jd.feedrate_min == None:
    #         summary_list.append('Spindle speed range: Undefined\n')
    #     else:
    #         summary_list.append('Spindle speed range: ' + str(self.jd.spindle_speed_min) + ' to ' + str(self.jd.spindle_speed_max) + '\n')


    #     summary_list.append('[b]Working volume:[/b]\n')
    #     if self.jd.x_max == -999999 and self.jd.x_min == 999999:
    #         summary_list.append('X range: Undefined\n')
    #     else:
    #         summary_list.append('X min: ' + str(self.jd.x_min))
    #         summary_list.append('X max: ' + str(self.jd.x_max) + '\n')

    #     if self.jd.y_max == -999999 and self.jd.y_min == 999999:
    #         summary_list.append('Y range: Undefined\n')
    #     else:
    #         summary_list.append('Y min: ' + str(self.jd.y_min))
    #         summary_list.append('Y max: ' + str(self.jd.y_max) + '\n')

    #     if self.jd.z_max == -999999 and self.jd.z_min == 999999:
    #         summary_list.append('Z range: Undefined\n')
    #     else:
    #         summary_list.append('Z min: ' + str(self.jd.z_min))
    #         summary_list.append('Z max: ' + str(self.jd.z_max) + '\n')


    #     summary_list.append('[b]Comments:[/b]\n')
    #     summary_list.extend(self.jd.comments_list)

    #     self.gcode_scrollview.text_container.text = '\n'.join(summary_list)

    def hide_summary(self):

        self.gcode_scrollview.text_container.text = ''