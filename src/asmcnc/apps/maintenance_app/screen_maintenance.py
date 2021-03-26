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
widget_maintenance_brush_save, widget_maintenance_spindle_save, widget_maintenance_spindle_settings, widget_maintenance_z_misc_save, \
widget_maintenance_touchplate_offset, widget_maintenance_z_lubrication_reminder

Builder.load_string("""

<MaintenanceScreenClass>:

    tab_panel:tab_panel

    # Laser Datum Widgets
    laser_tab: laser_tab
    xy_move_container: xy_move_container
    z_move_container: z_move_container
    laser_button_container: laser_button_container
    switch_container: switch_container

    # Laser tab labels
    laser_datum_label : laser_datum_label

    # Brush maintenance widgets
    brush_tab: brush_tab
    brush_monitor_container: brush_monitor_container
    brush_use_container: brush_use_container
    brush_life_container: brush_life_container
    brush_save_container: brush_save_container

    # Brush tab labels
    brush_monitor_label : brush_monitor_label

    # Spindle settings widgets
    spindle_tab: spindle_tab
    spindle_save_container: spindle_save_container
    spindle_settings_container: spindle_settings_container

    # Spindle tab labels
    spindle_cooldown_settings : spindle_cooldown_settings

    # Z touchplate and lead screw widgets
    z_misc_save_container: z_misc_save_container
    touchplate_offset_container: touchplate_offset_container
    z_lubrication_reminder_container: z_lubrication_reminder_container

    TabbedPanel:
        id: tab_panel
        size_hint: (None,None)
        height: dp(480)
        width: dp(804)
        pos: (0, 0)
        padding: [dp(-2),dp(-2),dp(-2),dp(0)]
        spacing: [0,dp(-4)]
        do_default_tab: False
        tab_pos: 'top_left'
        tab_height: dp(90)
        tab_width: dp(142)


        # LASER DATUM SETTINGS

        TabbedPanelItem:
            id: laser_tab
            background_normal: 'asmcnc/apps/maintenance_app/img/laser_datum_tab_blue.png'
            background_down: 'asmcnc/apps/maintenance_app/img/laser_datum_tab_grey.png'

            BoxLayout:
                size_hint: (None,None)
                width: dp(804)
                height: dp(390)
                orientation: "horizontal" 
                padding: (12, 10, 12, 20)
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
                                id: laser_datum_label
                                color: 0,0,0,1
                                font_size: dp(26)
                                markup: True
                                halign: "left"
                                valign: "middle"
                                text_size: self.size
                                size: self.parent.size
                                pos: self.parent.pos

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
            id: brush_tab
            background_normal: 'asmcnc/apps/maintenance_app/img/brush_monitor_tab_blue.png'
            background_down: 'asmcnc/apps/maintenance_app/img/brush_monitor_tab_grey.png'
            BoxLayout:
                size_hint: (None,None)
                width: dp(804)
                height: dp(390)
                orientation: "vertical" 
                padding: (22, 20, 22, 20)
                spacing: (20)
                canvas:
                    Color:
                        rgba: hex('#E5E5E5FF')
                    Rectangle:
                        size: self.size
                        pos: self.pos

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
                            id: brush_monitor_label
                            color: 0,0,0,1
                            font_size: dp(22)
                            markup: True
                            halign: "left"
                            valign: "middle"
                            text_size: self.size
                            size: self.parent.size
                            pos: self.parent.pos

                        BoxLayout:
                            size_hint: (None,None)
                            height: dp(70)
                            width: dp(600)
                            id: brush_monitor_container

        # Spindle cooldown settings
        
        TabbedPanelItem:
            id: spindle_tab
            background_normal: 'asmcnc/apps/maintenance_app/img/spindle_settings_tab_blue.png'
            background_down: 'asmcnc/apps/maintenance_app/img/spindle_settings_tab_grey.png'

            BoxLayout:
                size_hint: (None,None)
                width: dp(804)
                height: dp(390)
                orientation: "vertical" 
                padding: (22, 20, 22, 20)
                spacing: (20)
                canvas:
                    Color:
                        rgba: hex('#E5E5E5FF')
                    Rectangle:
                        size: self.size
                        pos: self.pos

                BoxLayout:
                    size_hint: (None,None)
                    height: dp(50)
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
                        height: dp(50)
                        width: dp(760)
                        padding: [dp(10),dp(5),dp(5),dp(5)]
                        orientation: 'horizontal'

                        Label:
                            id: spindle_cooldown_settings
                            color: 0,0,0,1
                            font_size: dp(22)
                            markup: True
                            halign: "left"
                            valign: "middle"
                            text_size: self.size
                            size: self.parent.size
                            pos: self.parent.pos

                BoxLayout:
                    size_hint: (None,None)
                    width: dp(760)
                    height: dp(280)
                    orientation: "horizontal" 
                    padding: dp(0)
                    spacing: dp(20)

                    BoxLayout:
                        size_hint: (None,None)
                        height: dp(280)
                        width: dp(580)
                        id: spindle_settings_container
                        canvas:
                            Color:
                                rgba: 1,1,1,1
                            RoundedRectangle:
                                size: self.size
                                pos: self.pos

                    BoxLayout:
                        size_hint: (None,None)
                        height: dp(280)
                        width: dp(160)
                        id: spindle_save_container
                        canvas:
                            Color:
                                rgba: 1,1,1,1
                            RoundedRectangle:
                                size: self.size
                                pos: self.pos

        # Z Misc settings (probe plate and time since lead screw lubrication)

        TabbedPanelItem:
            background_normal: 'asmcnc/apps/maintenance_app/img/z_misc_tab_blue.png'
            background_down: 'asmcnc/apps/maintenance_app/img/z_misc_tab_grey.png'

            BoxLayout:
                size_hint: (None,None)
                width: dp(804)
                height: dp(390)
                orientation: "horizontal" 
                padding: (22, 20, 22, 20)
                spacing: (20)
                canvas:
                    Color:
                        rgba: hex('#E5E5E5FF')
                    Rectangle:
                        size: self.size
                        pos: self.pos

                BoxLayout:
                    size_hint: (None,None)
                    width: dp(580)
                    height: dp(350)
                    orientation: "vertical" 
                    padding: dp(0)
                    spacing: dp(20)

                    BoxLayout:
                        size_hint: (None,None)
                        height: dp(130)
                        width: dp(580)
                        id: touchplate_offset_container
                        canvas:
                            Color:
                                rgba: 1,1,1,1
                            RoundedRectangle:
                                size: self.size
                                pos: self.pos

                    BoxLayout:
                        size_hint: (None,None)
                        height: dp(200)
                        width: dp(580)
                        id: z_lubrication_reminder_container
                        canvas:
                            Color:
                                rgba: 1,1,1,1
                            RoundedRectangle:
                                size: self.size
                                pos: self.pos

                BoxLayout:
                    size_hint: (None,None)
                    height: dp(350)
                    width: dp(160)
                    id: z_misc_save_container
                    canvas:
                        Color:
                            rgba: 1,1,1,1
                        RoundedRectangle:
                            size: self.size
                            pos: self.pos



        TabbedPanelItem:
            background_normal: 'asmcnc/apps/maintenance_app/img/blank_blue_tab.png'
            background_down: 'asmcnc/apps/maintenance_app/img/blank_blue_tab.png'     
            disabled: 'True'

    BoxLayout: 
        size_hint: (None,None)
        pos: (dp(568), dp(390))
        height: dp(90)
        width: dp(142)        
        Image:
            size_hint: (None,None)
            height: dp(90)
            width: dp(142)
            # background_color: hex('#2196f3fb')
            center: self.parent.center
            pos: self.parent.pos
            source: "./asmcnc/apps/maintenance_app/img/blank_blue_tab.png"
            allow_stretch: True
            opacity: 1

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


    # LASER DATUM OFFSET
    laser_datum_reset_coordinate_x = 0
    laser_datum_reset_coordinate_y = 0

    landing_tab = StringProperty()

    def __init__(self, **kwargs):
        super(MaintenanceScreenClass, self).__init__(**kwargs)
        self.m=kwargs['machine']
        self.sm=kwargs['screen_manager']
        self.l=kwargs['localization']

        # LASER DATUM WIDGETS
        self.xy_move_widget = widget_maintenance_xy_move.MaintenanceXYMove(machine=self.m, screen_manager=self.sm)
        self.xy_move_container.add_widget(self.xy_move_widget)
    
        self.z_move_widget = widget_maintenance_z_move.MaintenanceZMove(machine=self.m, screen_manager=self.sm, localization=self.l)
        self.z_move_container.add_widget(self.z_move_widget)

        self.laser_datum_buttons_widget = widget_maintenance_laser_buttons.LaserDatumButtons(machine=self.m, screen_manager=self.sm, localization=self.l)
        self.laser_button_container.add_widget(self.laser_datum_buttons_widget)

        self.laser_switch_widget = widget_maintenance_laser_switch.LaserOnOffWidget(machine=self.m, screen_manager=self.sm)
        self.switch_container.add_widget(self.laser_switch_widget)


        # BRUSH MONITOR WIDGETS
        self.brush_use_widget = widget_maintenance_brush_use.BrushUseWidget(machine=self.m, screen_manager=self.sm, localization=self.l)
        self.brush_use_container.add_widget(self.brush_use_widget)

        self.brush_life_widget = widget_maintenance_brush_life.BrushLifeWidget(machine=self.m, screen_manager=self.sm, localization=self.l)
        self.brush_life_container.add_widget(self.brush_life_widget)

        self.brush_save_widget = widget_maintenance_brush_save.BrushSaveWidget(machine=self.m, screen_manager=self.sm, localization=self.l)
        self.brush_save_container.add_widget(self.brush_save_widget)

        self.monitor_percentage = 1 - (self.m.spindle_brush_use_seconds/self.m.spindle_brush_lifetime_seconds)
        self.brush_monitor_widget = widget_maintenance_brush_monitor.BrushMonitorWidget(machine=self.m, screen_manager=self.sm, input_percentage = self.monitor_percentage)
        self.brush_monitor_container.add_widget(self.brush_monitor_widget)


        # SPINDLE SETTINGS WIDGET

        self.spindle_save_widget = widget_maintenance_spindle_save.SpindleSaveWidget(machine=self.m, screen_manager=self.sm, localization=self.l)
        self.spindle_save_container.add_widget(self.spindle_save_widget)       

        self.spindle_settings_widget = widget_maintenance_spindle_settings.SpindleSettingsWidget(machine=self.m, screen_manager=self.sm, localization=self.l)
        self.spindle_settings_container.add_widget(self.spindle_settings_widget)


        # Z TOUCHPLATE OFFSET AND LEAD SCREW REMINDER WIDGETS

        self.z_misc_save_widget = widget_maintenance_z_misc_save.ZMiscSaveWidget(machine=self.m, screen_manager=self.sm, localization=self.l)
        self.z_misc_save_container.add_widget(self.z_misc_save_widget)

        self.touchplate_offset_widget = widget_maintenance_touchplate_offset.TouchplateOffsetWidget(machine=self.m, screen_manager=self.sm, localization=self.l)
        self.touchplate_offset_container.add_widget(self.touchplate_offset_widget)

        self.z_lubrication_reminder_widget = widget_maintenance_z_lubrication_reminder.ZLubricationReminderWidget(machine=self.m, screen_manager=self.sm, localization=self.l)
        self.z_lubrication_reminder_container.add_widget(self.z_lubrication_reminder_widget)

        self.update_strings()

    def quit_to_lobby(self):
        self.sm.current = 'lobby'
        
    def on_pre_enter(self):

        # LASER
        if self.m.is_laser_enabled == True:
            self.laser_switch_widget.laser_switch.active = True
        else: 
            self.laser_switch_widget.laser_switch.active = False

        self.laser_switch_widget.toggle_laser()

        # BRUSHES
        self.brush_use_widget.brush_use.text = str(int(self.m.spindle_brush_use_seconds/3600))
        self.brush_life_widget.brush_life.text = str(int(self.m.spindle_brush_lifetime_seconds/3600))

        value = 1 - (self.m.spindle_brush_use_seconds/self.m.spindle_brush_lifetime_seconds)
        self.brush_monitor_widget.set_percentage(value)

        # SPINDLE
        if self.m.spindle_digital: 
            string_digital = 'digital'
            self.spindle_settings_widget.spindle_cooldown_speed.disabled = False
        else: 
            string_digital = 'manual'
            self.spindle_settings_widget.spindle_cooldown_speed.disabled = True

        self.spindle_settings_widget.spindle_brand.text = ' ' + str(self.m.spindle_brand) + ' ' + string_digital + ' ' + str(self.m.spindle_voltage) + 'V'
        self.spindle_settings_widget.spindle_cooldown_time.text = str(self.m.spindle_cooldown_time_seconds)
        self.spindle_settings_widget.spindle_cooldown_speed.text = str(self.m.spindle_cooldown_rpm)

        # Z MISC
        self.touchplate_offset_widget.touchplate_offset.text = str(self.m.z_touch_plate_thickness)
        self.z_lubrication_reminder_widget.update_time_left()


    def on_enter(self):

        # TAB TO LAND ON
        if self.landing_tab == 'brush_tab':
            self.tab_panel.switch_to(self.brush_tab)
        elif self.landing_tab == 'laser_tab':
            self.tab_panel.switch_to(self.laser_tab)
        elif self.landing_tab == 'spindle_tab':
            self.tab_panel.switch_to(self.spindle_tab)
        else: 
            self.landing_tab = self.tab_panel.current

        self.update_strings()


    def on_pre_leave(self):

        # LASER DATUM
        self.m.write_z_head_laser_offset_values(self.m.is_laser_enabled, self.m.laser_offset_x_value, self.m.laser_offset_y_value)

        if self.m.is_laser_enabled == True: self.sm.get_screen('home').default_datum_choice = 'laser'
        else: self.sm.get_screen('home').default_datum_choice = 'spindle'

        self.m.laser_off()

    def update_strings(self):

        self.laser_datum_label.text = self.l.get_bold("LASER")
        self.brush_monitor_label.text = self.l.get_bold("BRUSH MONITOR")
        self.spindle_cooldown_settings.text = self.l.get_bold("SPINDLE COOLDOWN SETTINGS")
