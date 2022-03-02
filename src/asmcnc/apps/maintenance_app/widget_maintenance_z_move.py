'''
Created on 1 Feb 2018
@author: Ed
'''

import kivy
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty, ListProperty, NumericProperty # @UnresolvedImport
from kivy.uix.widget import Widget
from kivy.base import runTouchApp

from asmcnc.skavaUI import widget_z_height
from kivy.clock import Clock

from asmcnc.skavaUI import popup_info


Builder.load_string("""

<MaintenanceZMove>

    virtual_z_container:virtual_z_container

    BoxLayout:

        size: self.parent.size
        pos: self.parent.pos      
        padding: 20
        spacing: 20
        orientation: 'horizontal'
        
        BoxLayout:
            spacing: 10
            orientation: "vertical"
            
            BoxLayout:
                size_hint_y: 3.4
                id: virtual_z_container

        BoxLayout:
            spacing: 10
            orientation: "vertical"
            
            Button:
                size_hint_y: 1
                background_color: hex('#F4433600')
                on_release:
                    root.quit_jog_z()
                    self.background_color = hex('#F4433600')
                on_press:
                    root.jog_z('Z+') 
                    self.background_color = hex('#F44336FF')
                BoxLayout:
                    padding: 0
                    size: self.parent.size
                    pos: self.parent.pos
                    Image:
#                         source: "./asmcnc/skavaUI/img/z_jog_up.png"
                        source: "./asmcnc/skavaUI/img/xy_arrow_up.png"
                        center_x: self.parent.center_x
                        y: self.parent.y
                        size: self.parent.width, self.parent.height
                        allow_stretch: True   

            Button:
                size_hint_y: 1
                background_color: hex('#F4433600')
                on_release: 
                    root.quit_jog_z()
                    self.background_color = hex('#F4433600')
                on_press:
                    root.jog_z('Z-') 
                    self.background_color = hex('#F44336FF')
                BoxLayout:
                    padding: 0
                    size: self.parent.size
                    pos: self.parent.pos
                    Image:
                        source: "./asmcnc/skavaUI/img/z_jog_down.png"
                        source: "./asmcnc/skavaUI/img/xy_arrow_down.png"
                        center_x: self.parent.center_x
                        y: self.parent.y
                        size: self.parent.width, self.parent.height
                        allow_stretch: True   
                        
            Button:
                background_color: hex('#F4433600')
                on_press: root.get_info()
                BoxLayout:
                    padding: (dp(7.5), dp(20), dp(32.5), dp(20))
                    size_hint: (None,None)
                    height: dp(100)
                    width: dp(100)
                    pos: self.parent.pos
                    Image:
                        source: "./asmcnc/apps/shapeCutter_app/img/info_icon.png"
                        center_x: self.parent.center_x
                        y: self.parent.y
                        size: self.parent.width, self.parent.height
                        allow_stretch: True   
 
                        
    FloatLayout:
        
        Label:
            x: 662
            y: 420
            size_hint: None, None            
            height: 30
            width: 30
            text: 'Z'
            markup: True
            bold: True
            color: 0,0,0,0.2
            font_size: 20     
        
""")
    

class MaintenanceZMove(Widget):

    def __init__(self, **kwargs):
        super(MaintenanceZMove, self).__init__(**kwargs)
        self.m=kwargs['machine']
        self.sm=kwargs['screen_manager']
        self.l=kwargs['localization']
        self.jd = kwargs['job']
        self.virtual_z_container.add_widget(widget_z_height.VirtualZ(machine=self.m, screen_manager=self.sm, job=self.jd))

    def jog_z(self, case):

        self.m.set_led_colour('WHITE')

        feed_speed = self.sm.get_screen('maintenance').xy_move_widget.feedSpeedJogZ
        
        if self.sm.get_screen('maintenance').xy_move_widget.jogMode == 'free':
            if case == 'Z-': self.m.jog_absolute_single_axis('Z', 
                                                             self.m.z_min_jog_abs_limit,
                                                             feed_speed)
            if case == 'Z+': self.m.jog_absolute_single_axis('Z', 
                                                             self.m.z_max_jog_abs_limit,
                                                             feed_speed)

        elif self.sm.get_screen('maintenance').xy_move_widget.jogMode == 'plus_0-01':
            if case == 'Z+': self.m.jog_relative('Z', 0.01, feed_speed)
            if case == 'Z-': self.m.jog_relative('Z', -0.01, feed_speed)
        
        elif self.sm.get_screen('maintenance').xy_move_widget.jogMode == 'plus_0-1':
            if case == 'Z+': self.m.jog_relative('Z', 0.1, feed_speed)
            if case == 'Z-': self.m.jog_relative('Z', -0.1, feed_speed)
        
        elif self.sm.get_screen('maintenance').xy_move_widget.jogMode == 'plus_1':
            if case == 'Z+': self.m.jog_relative('Z', 1, feed_speed)
            if case == 'Z-': self.m.jog_relative('Z', -1, feed_speed)
        
        elif self.sm.get_screen('maintenance').xy_move_widget.jogMode == 'plus_10':
            if case == 'Z+': self.m.jog_relative('Z', 10, feed_speed)
            if case == 'Z-': self.m.jog_relative('Z', -10, feed_speed)
        
        elif self.sm.get_screen('maintenance').xy_move_widget.jogMode == 'job':
            if case == 'Z-': self.m.jog_absolute_single_axis('Z', 
                                                             self.m.z_min_jog_abs_limit,
                                                             feed_speed)
            if case == 'Z+': self.m.jog_absolute_single_axis('Z', 
                                                             self.m.z_max_jog_abs_limit,
                                                             feed_speed)

    def quit_jog_z(self):
        if self.sm.get_screen('maintenance').xy_move_widget.jogMode == 'free': self.m.quit_jog()
        elif self.sm.get_screen('maintenance').xy_move_widget.jogMode == 'job': self.m.quit_jog()

    def get_info(self):

        info = (
                self.l.get_bold("To set, if laser hardware is fitted:") + \
                "\n\n" + \
                self.l.get_str("1. Enable laser crosshair (switch to on).").replace(self.l.get_str("on"), self.l.get_bold("on")) + \
                "\n\n" + \
                self.l.get_str("2. On a test piece, cut a mark using manual moves.") + \
                "\n\n" + \
                self.l.get_str("3. Lift Z Head and press the reset button in the bottom left.").replace(self.l.get_str("reset"), self.l.get_bold("reset")) + \
                "\n\n" + \
                self.l.get_str("4. Move the Z Head so that the cross hair lines up with the mark centre.") + \
                "\n\n" + \
                self.l.get_str("5. Press save.").replace(self.l.get_str("save"), self.l.get_bold("save"))
                )

        popup_info.PopupInfo(self.sm, self.l, 700, info)   

