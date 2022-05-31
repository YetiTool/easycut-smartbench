'''
Created 31 May 2022
@author Letty
'''

import kivy
from kivy.lang import Builder
from kivy.uix.widget import Widget


Builder.load_string("""

#:import hex kivy.utils.get_color_from_hex

<FeedThresholdGrid>

    GridLayout: 

        size: self.size
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
            text: ""

        Button: 
            on_press: root.choose_test(root.f[0], root.t[0])

        Button: 
            on_press: root.choose_test(root.f[1], root.t[0])

        Button: 
            on_press: root.choose_test(root.f[2], root.t[0])

        Button: 
            on_press: root.choose_test(root.f[3], root.t[0])

        Button: 
            on_press: root.choose_test(root.f[4], root.t[0])

        Button: 
            on_press: root.choose_test(root.f[5], root.t[0])

        Button: 
            on_press: root.choose_test(root.f[6], root.t[0])





""")

##  AttributeError: 'FeedThresholdGrid' object has no attribute 'f'
# need object properties

class FeedThresholdGrid(Widget):

    def __init__(self, **kwargs):

        super(FeedThresholdGrid, self).__init__(**kwargs)
        self.m=kwargs['machine']
        self.sm=kwargs['screen_manager']
        self.parent_screen=kwargs['parent_screen']

        self.axis = "W"
        self.f = ['1','2','3','4','5','6','7']
        self.t = ['1',2,3,4,5]

    def choose_test(self, feed, threshold):
        if not isinstance(feed,int) or not isinstance(threshold, int):
            return

        self.parent_screen.choose_test(self.axis, feed, threshold)



