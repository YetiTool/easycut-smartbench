'''
Created 31 May 2022
@author Letty
'''

import kivy
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.properties import ListProperty

Builder.load_string("""

#:import hex kivy.utils.get_color_from_hex

<FeedThresholdGrid>

    GridLayout: 

        size: self.parent.size
        pos: self.parent.pos
        cols: 8
        rows: 2

        # AXIS LABEL
        Label:
            text: root.axis

        # FEED LABELS
        Label: 
            text: root.f[0]

        Label: 
            text: root.f[1]

        Label: 
            text: root.f[2]

        Label: 
            text: root.f[3]

        Label: 
            text: root.f[4]

        Label: 
            text: root.f[5]

        Label: 
            text: root.f[6]

        # THRESHOLD 1

        Label: 
            text: str(root.t[0])

        Button: 
            on_press: root.choose_test(root.f[0], str(root.t[0]))

        Button: 
            on_press: root.choose_test(root.f[1], str(root.t[0]))

        Button: 
            on_press: root.choose_test(root.f[2], str(root.t[0]))

        Button: 
            on_press: root.choose_test(root.f[3], str(root.t[0]))

        Button: 
            on_press: root.choose_test(root.f[4], str(root.t[0]))

        Button: 
            on_press: root.choose_test(root.f[5], str(root.t[0]))

        Button: 
            on_press: root.choose_test(root.f[6], str(root.t[0]))





""")

# THESE WILL NEED TO BE SET UP FOR EACH AXIS INDIVIDUALLY, OTHERWISE CLASS LISTS WILL GET MESSED UP

class FeedThresholdGrid(Widget):

    axis = "W"
    f = ['1','2','3','4','5','6','7']
    t = [1,2,3,4,5]

    def __init__(self, **kwargs):

        super(FeedThresholdGrid, self).__init__(**kwargs)
        self.m=kwargs['machine']
        self.sm=kwargs['screen_manager']
        self.parent_screen=kwargs['parent_screen']

        self.axis = "X"
        self.f = ['1','2','3','4','5','6','7']
        self.t = [1,2,3,4,5]

    def choose_test(self, feed, threshold):
        if not isinstance(feed,int) or not isinstance(threshold, int):
            return

        self.parent_screen.choose_test(self.axis, feed, threshold)



