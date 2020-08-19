'''
Created on 19 August 2020
@author: Letty
'''

import kivy
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty, ListProperty, NumericProperty # @UnresolvedImport
from kivy.uix.widget import Widget
from kivy.base import runTouchApp
from kivy.clock import Clock


Builder.load_string("""


<BrushMonitorWidget>


    Image:
        id: empty_monitor
        source: "./asmcnc/apps/maintenance_app/img/empty_bar.png"
        allow_stretch: True
        keep_ratio: False
        size: self.parent.size
        pos: self.parent.pos
    Image:
        id: fuel_bar
        source: "./asmcnc/apps/maintenance_app/img/green_bar.png"
        allow_stretch: True
        keep_ratio: False
        size: self.parent.width*0.8, self.parent.height*0.9
        x: self.parent.x+(self.parent.width*0.2)
        y: self.parent.y+(self.parent.height*0.05)

    Label: 
        id: percentage
        color: 1,1,1,1
        font_size: dp(50)
        markup: True
        halign: "right"
        valign: "middle"
        text_size: self.size
        text: "80%"
        size: dp(130), self.parent.height
        x: self.parent.x+(self.parent.width*0.75)
        y: self.parent.y

        
""")

class BrushMonitorWidget(Widget):

    def __init__(self, **kwargs):
    
        super(BrushMonitorWidget, self).__init__(**kwargs)
        self.sm=kwargs['screen_manager']
        self.m=kwargs['machine']

    # Here need to do some magic adjusting the size of the fuel bar in line with the percentage


