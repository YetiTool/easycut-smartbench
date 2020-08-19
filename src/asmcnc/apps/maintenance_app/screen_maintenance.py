'''
Created on 8 June 2020
Tabbed maintenance screen, for setting the laser datum; monitoring brush life. 

@author: Letty
'''

from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.metrics import MetricsBase
from kivy.properties import StringProperty, ObjectProperty
from kivy.clock import Clock

from asmcnc.apps.maintenance_app import widget_maintenance_xy_move, widget_maintenance_z_move, widget_maintenance_laser_buttons, \
widget_maintenance_laser_switch, widget_maintenance_brush_use, widget_maintenance_brush_life, widget_maintenance_brush_monitor, \
widget_maintenance_brush_save

Builder.load_string("""

<MaintenanceScreenClass>:

    # Laser Datum Widgets
    xy_move_container: xy_move_container
    z_move_container: z_move_container
    laser_button_container: laser_button_container
    switch_container: switch_container

    # Brush maintenance widgets
    brush_monitor_container: brush_monitor_container
    brush_use_container: brush_use_container
    brush_life_container: brush_life_container
    brush_save_container: brush_save_container


    TabbedPanel:
        id: tab_panel
        size_hint: (None,None)
        height: dp(480)
        width: dp(800)
        pos: (0, 0)
        padding: [dp(-2),dp(-2),dp(-2),dp(0)]
        spacing: [0,dp(-4)]
        do_default_tab: False
        tab_pos: 'top_left'
        tab_height: dp(90)
        tab_width: dp(142)


        # LASER DATUM SETTINGS

        TabbedPanelItem:
            background_normal: 'asmcnc/apps/maintenance_app/img/laser_datum_tab_blue.png'
            background_down: 'asmcnc/apps/maintenance_app/img/laser_datum_tab_grey.png'

            BoxLayout:
                size_hint: (None,None)
                width: dp(800)
                height: dp(390)
                orientation: "horizontal" 
                padding: (10, 10, 10, 20)
                spacing: (10)
                canvas:
                    Color:
                        rgba: hex('#E5E5E5FF')
                    Rectangle:
                        size: self.size
                        pos: self.pos

                BoxLayout:
                    size_hint: (None,None)
                    height: dp(360)
                    width: dp(280)
                    spacing: 10
                    orientation: "vertical"
                    id: left_panel
                    BoxLayout:
                        size_hint: (None,None)
                        height: dp(70)
                        width: dp(280)
                        id: title
                        canvas:
                            Color:
                                rgba: 1,1,1,1
                            RoundedRectangle:
                                size: self.size
                                pos: self.pos
                        BoxLayout: 
                            size_hint: (None, None)
                            height: dp(70)
                            width: dp(280)
                            padding: [dp(20),0,dp(20),0]
                            orientation: 'horizontal'
                            Label: 
                                color: 0,0,0,1
                                font_size: dp(22)
                                markup: True
                                halign: "center"
                                valign: "middle"
                                text_size: self.size
                                size: self.parent.size
                                pos: self.parent.pos
                                text: "[b]LASER DATUM[/b]"

                            BoxLayout:
                                size_hint: (None,None)
                                height: dp(70)
                                width: dp(150)
                                id: switch_container

                    BoxLayout:
                        size_hint: (None,None)
                        height: dp(280)
                        width: dp(280)
                        id: laser_button_container
                        canvas:
                            Color:
                                rgba: 1,1,1,1
                            RoundedRectangle:
                                size: self.size
                                pos: self.pos

                BoxLayout:
                    size_hint: (None,None)
                    height: dp(360)
                    width: dp(270)
                    spacing: 10
                    orientation: "vertical"
                    id: middle_panel

                    BoxLayout:
                        size_hint: (None,None)
                        height: dp(360)
                        width: dp(270)
                        id: xy_move_container
                        canvas:
                            Color:
                                rgba: 1,1,1,1
                            RoundedRectangle:
                                size: self.size
                                pos: self.pos

                BoxLayout:
                    size_hint: (None,None)
                    height: dp(360)
                    width: dp(210)
                    id: z_move_container
                    canvas:
                        Color:
                            rgba: 1,1,1,1
                        RoundedRectangle:
                            size: self.size
                            pos: self.pos
        

        # BRUSH MONITOR

        TabbedPanelItem:
            background_normal: 'asmcnc/apps/maintenance_app/img/brush_monitor_tab_blue.png'
            background_down: 'asmcnc/apps/maintenance_app/img/brush_monitor_tab_grey.png'
            BoxLayout:
                size_hint: (None,None)
                width: dp(800)
                height: dp(390)
                orientation: "vertical" 
                padding: (20, 20, 20, 20)
                spacing: (20)
                canvas:
                    Color:
                        rgba: hex('#E5E5E5FF')
                    Rectangle:
                        size: self.size
                        pos: self.pos

                BoxLayout:
                    size_hint: (None,None)
                    height: dp(80)
                    width: dp(760)
                    id: monitor_strip
                    canvas:
                        Color:
                            rgba: 1,1,1,1
                        RoundedRectangle:
                            size: self.size
                            pos: self.pos
                    BoxLayout: 
                        size_hint: (None, None)
                        height: dp(80)
                        width: dp(760)
                        padding: [dp(10),dp(5),dp(5),dp(5)]
                        orientation: 'horizontal'
                        Label: 
                            color: 0,0,0,1
                            font_size: dp(22)
                            markup: True
                            halign: "left"
                            valign: "middle"
                            text_size: self.size
                            size: self.parent.size
                            pos: self.parent.pos
                            text: "[b]BRUSH MONITOR[/b]"

                        BoxLayout:
                            size_hint: (None,None)
                            height: dp(70)
                            width: dp(600)
                            id: brush_monitor_container

                BoxLayout:
                    size_hint: (None,None)
                    width: dp(760)
                    height: dp(250)
                    orientation: "horizontal" 
                    padding: 0
                    spacing: (20)

                    BoxLayout:
                        size_hint: (None,None)
                        height: dp(250)
                        width: dp(280)
                        id: brush_use_container
                        canvas:
                            Color:
                                rgba: 1,1,1,1
                            RoundedRectangle:
                                size: self.size
                                pos: self.pos

                    BoxLayout:
                        size_hint: (None,None)
                        height: dp(250)
                        width: dp(280)
                        id: brush_life_container
                        canvas:
                            Color:
                                rgba: 1,1,1,1
                            RoundedRectangle:
                                size: self.size
                                pos: self.pos

                    BoxLayout:
                        size_hint: (None,None)
                        height: dp(250)
                        width: dp(160)
                        id: brush_save_container
                        canvas:
                            Color:
                                rgba: 1,1,1,1
                            RoundedRectangle:
                                size: self.size
                                pos: self.pos




        
        TabbedPanelItem:
            background_disabled_image: 'asmcnc/apps/maintenance_app/img/blank_blue_tab.png'
            disabled: 'True'
        TabbedPanelItem:
            background_normal: 'asmcnc/apps/maintenance_app/img/blank_blue_tab.png'
            background_down: 'asmcnc/apps/maintenance_app/img/blank_blue_tab.png'
            disabled: 'True'

        TabbedPanelItem:
            background_normal: 'asmcnc/apps/maintenance_app/img/blank_blue_tab.png'
            background_down: 'asmcnc/apps/maintenance_app/img/blank_blue_tab.png'     
            disabled: 'True'

    BoxLayout: 
        size_hint: (None,None)
        pos: (dp(284), dp(390))
        Image:
            size_hint: (None,None)
            height: dp(90)
            width: dp(426)
            # background_color: [0,0,0,0]
            center: self.parent.center
            pos: self.parent.pos
            source: "./asmcnc/apps/maintenance_app/img/long_blue_tab.png"
            allow_stretch: True

    BoxLayout: 
        size_hint: (None,None)
        pos: (dp(710), dp(390))
        Button:
            size_hint: (None,None)
            height: dp(90)
            width: dp(90)
            background_color: [0,0,0,0]
            center: self.parent.center
            pos: self.parent.pos
            on_press: root.quit_to_lobby()
            BoxLayout:
                padding: 0
                size: self.parent.size
                pos: self.parent.pos
                Image:
                    source: "./asmcnc/apps/shapeCutter_app/img/exit_cross.png"
                    center_x: self.parent.center_x
                    y: self.parent.y
                    size: self.parent.width, self.parent.height
                    allow_stretch: True

""")

class MaintenanceScreenClass(Screen):


    laser_datum_reset_coordinate_x = 0
    laser_datum_reset_coordinate_y = 0

    def __init__(self, **kwargs):
        super(MaintenanceScreenClass, self).__init__(**kwargs)
        self.m=kwargs['machine']
        self.sm=kwargs['screen_manager']

        # LASER DATUM WIDGETS
        self.xy_move_widget = widget_maintenance_xy_move.MaintenanceXYMove(machine=self.m, screen_manager=self.sm)
        self.xy_move_container.add_widget(self.xy_move_widget)
    
        self.z_move_widget = widget_maintenance_z_move.MaintenanceZMove(machine=self.m, screen_manager=self.sm)
        self.z_move_container.add_widget(self.z_move_widget)

        self.laser_datum_buttons_widget = widget_maintenance_laser_buttons.LaserDatumButtons(machine=self.m, screen_manager=self.sm)
        self.laser_button_container.add_widget(self.laser_datum_buttons_widget)

        self.laser_switch_widget = widget_maintenance_laser_switch.LaserOnOffWidget(machine=self.m, screen_manager=self.sm)
        self.switch_container.add_widget(self.laser_switch_widget)


        # BRUSH MONITOR WIDGETS
        self.brush_use_widget = widget_maintenance_brush_use.BrushUseWidget(machine=self.m, screen_manager=self.sm)
        self.brush_use_container.add_widget(self.brush_use_widget)

        self.brush_life_widget = widget_maintenance_brush_life.BrushLifeWidget(machine=self.m, screen_manager=self.sm)
        self.brush_life_container.add_widget(self.brush_life_widget)

        self.brush_save_widget = widget_maintenance_brush_save.BrushSaveWidget(machine=self.m, screen_manager=self.sm)
        self.brush_save_container.add_widget(self.brush_save_widget)

        self.brush_monitor_widget = widget_maintenance_brush_monitor.BrushMonitorWidget(machine=self.m, screen_manager=self.sm)
        self.brush_monitor_container.add_widget(self.brush_monitor_widget)

    def quit_to_lobby(self):
        self.sm.current = 'lobby'
        
    def on_pre_enter(self):

        if self.m.is_laser_enabled == True:
            self.laser_switch_widget.laser_switch.active = True
        else: 
            self.laser_switch_widget.laser_switch.active = False

        self.laser_switch_widget.toggle_laser()

    def on_pre_leave(self):
        self.m.write_z_head_laser_offset_values(self.m.is_laser_enabled, self.m.laser_offset_x_value, self.m.laser_offset_y_value)

        if self.m.is_laser_enabled == True: self.sm.get_screen('home').default_datum_choice = 'laser'
        else: self.sm.get_screen('home').default_datum_choice = 'spindle'

        self.m.laser_off()
