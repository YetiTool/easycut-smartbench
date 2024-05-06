from kivy.core.window import Window

"""
Created on 8 June 2020
Tabbed maintenance screen, for setting the laser datum; monitoring brush life. 

@author: Letty
"""
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty
from asmcnc.apps.maintenance_app import (
    widget_maintenance_xy_move,
    widget_maintenance_z_move,
    widget_maintenance_laser_buttons,
    widget_maintenance_laser_switch,
    widget_maintenance_brush_use,
    widget_maintenance_brush_life,
    widget_maintenance_brush_monitor,
    widget_maintenance_brush_save,
    widget_maintenance_spindle_settings,
    widget_maintenance_z_misc_save,
    widget_maintenance_touchplate_offset,
    widget_maintenance_z_lubrication_reminder,
    widget_maintenance_spindle_health_check,
    widget_maintenance_general_settings,
)

Builder.load_string("""
#:import LabelBase asmcnc.core_UI.components.labels.base_label
#:import color_provider asmcnc.core_UI.utils.color_provider

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
    spindle_settings_container: spindle_settings_container

    # Z touchplate and lead screw widgets
    z_misc_save_container: z_misc_save_container
    touchplate_offset_container: touchplate_offset_container
    z_lubrication_reminder_container: z_lubrication_reminder_container

    # General settings widgets
    general_settings_container: general_settings_container

    # + tab widgets
    plus_tab : plus_tab
    spindle_health_check_container : spindle_health_check_container

    TabbedPanel:
        id: tab_panel
        size_hint: (None,None)
        height: dp(1.0*app.height)
        width: dp(1.005*app.width)
        pos: (0, 0)
        padding:[dp(-0.0025)*app.width, dp(-0.00416666666667)*app.height, dp(-0.0025)*app.width, 0]
        spacing:[0, dp(-0.00833333333333)*app.height]
        do_default_tab: False
        tab_pos: 'top_left'
        tab_height: dp(90.0/480.0)*app.height
        tab_width: dp((710.0/6.0)/800.0)*app.width
        on_touch_down: root.on_tab_switch()


        # LASER DATUM SETTINGS

        TabbedPanelItem:
            id: laser_tab
            background_normal: 'asmcnc/apps/maintenance_app/img/laser_datum_tab_blue.png'
            background_down: 'asmcnc/apps/maintenance_app/img/laser_datum_tab_grey.png'

            BoxLayout:
                size_hint: (None,None)
                width: dp(1.005*app.width)
                height: dp(0.8125*app.height)
                orientation: "horizontal" 
                padding:[dp(0.015)*app.width, dp(0.0208333333333)*app.height, dp(0.015)*app.width, dp(0.0416666666667)*app.height]
                spacing:0.0125*app.width
                canvas:
                    Color:
                        rgba: hex('#E5E5E5FF')
                    Rectangle:
                        size: self.size
                        pos: self.pos

                BoxLayout:
                    size_hint: (None,None)
                    height: dp(0.75*app.height)
                    width: dp(0.35*app.width)
                    spacing:0.0208333333333*app.height
                    orientation: "vertical"
                    id: left_panel
                    BoxLayout:
                        size_hint: (None,None)
                        height: dp(0.145833333333*app.height)
                        width: dp(0.35*app.width)
                        id: title
                        canvas:
                            Color:
                                rgba: 1,1,1,1
                            RoundedRectangle:
                                size: self.size
                                pos: self.pos
                        BoxLayout: 
                            size_hint: (None, None)
                            height: dp(0.145833333333*app.height)
                            width: dp(0.35*app.width)
                            padding:[dp(0.025)*app.width, 0, dp(0.025)*app.width, 0]
                            orientation: 'horizontal'

                            LabelBase: 
                                id: laser_datum_label
                                color: color_provider.get_rgba("black")
                                font_size: dp(0.0325*app.width)
                                markup: True
                                halign: "left"
                                valign: "middle"
                                text_size: self.size
                                size: self.parent.size
                                pos: self.parent.pos
                                text: "[b]LASER[/b]"

                            BoxLayout:
                                size_hint: (None,None)
                                height: dp(0.145833333333*app.height)
                                width: dp(0.1875*app.width)
                                id: switch_container

                    BoxLayout:
                        size_hint: (None,None)
                        height: dp(0.583333333333*app.height)
                        width: dp(0.35*app.width)
                        id: laser_button_container
                        canvas:
                            Color:
                                rgba: 1,1,1,1
                            RoundedRectangle:
                                size: self.size
                                pos: self.pos

                BoxLayout:
                    size_hint: (None,None)
                    height: dp(0.75*app.height)
                    width: dp(0.3375*app.width)
                    spacing:0.0208333333333*app.height
                    orientation: "vertical"
                    id: middle_panel

                    BoxLayout:
                        size_hint: (None,None)
                        height: dp(0.75*app.height)
                        width: dp(0.3375*app.width)
                        id: xy_move_container
                        canvas:
                            Color:
                                rgba: 1,1,1,1
                            RoundedRectangle:
                                size: self.size
                                pos: self.pos

                BoxLayout:
                    size_hint: (None,None)
                    height: dp(0.75*app.height)
                    width: dp(0.2625*app.width)
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
                width: dp(1.005*app.width)
                height: dp(0.8125*app.height)
                orientation: "vertical" 
                padding:[dp(0.0275)*app.width, dp(0.0416666666667)*app.height, dp(0.0275)*app.width, dp(0.0416666666667)*app.height]
                spacing:0.0416666666667*app.height
                canvas:
                    Color:
                        rgba: hex('#E5E5E5FF')
                    Rectangle:
                        size: self.size
                        pos: self.pos

                BoxLayout:
                    size_hint: (None,None)
                    width: dp(0.95*app.width)
                    height: dp(0.520833333333*app.height)
                    orientation: "horizontal" 
                    padding: 0
                    spacing:0.025*app.width

                    BoxLayout:
                        size_hint: (None,None)
                        height: dp(0.520833333333*app.height)
                        width: dp(0.35*app.width)
                        id: brush_use_container
                        canvas:
                            Color:
                                rgba: 1,1,1,1
                            RoundedRectangle:
                                size: self.size
                                pos: self.pos

                    BoxLayout:
                        size_hint: (None,None)
                        height: dp(0.520833333333*app.height)
                        width: dp(0.35*app.width)
                        id: brush_life_container
                        canvas:
                            Color:
                                rgba: 1,1,1,1
                            RoundedRectangle:
                                size: self.size
                                pos: self.pos

                    BoxLayout:
                        size_hint: (None,None)
                        height: dp(0.520833333333*app.height)
                        width: dp(0.2*app.width)
                        id: brush_save_container
                        canvas:
                            Color:
                                rgba: 1,1,1,1
                            RoundedRectangle:
                                size: self.size
                                pos: self.pos

                BoxLayout:
                    size_hint: (None,None)
                    height: dp(0.166666666667*app.height)
                    width: dp(0.95*app.width)
                    id: monitor_strip
                    canvas:
                        Color:
                            rgba: 1,1,1,1
                        RoundedRectangle:
                            size: self.size
                            pos: self.pos
                    BoxLayout: 
                        size_hint: (None, None)
                        height: dp(0.166666666667*app.height)
                        width: dp(0.95*app.width)
                        padding:[dp(0.0125)*app.width, dp(0.0104166666667)*app.height, dp(0.00625)*app.width, dp(0.0104166666667)*app.height]
                        orientation: 'horizontal'
                        LabelBase: 
                            id: brush_monitor_label
                            color: color_provider.get_rgba("black")
                            font_size: dp(0.0275*app.width)
                            markup: True
                            halign: "left"
                            valign: "middle"
                            text_size: self.size
                            size: self.parent.size
                            pos: self.parent.pos

                        BoxLayout:
                            size_hint: (None,None)
                            height: dp(0.145833333333*app.height)
                            width: dp(0.75*app.width)
                            id: brush_monitor_container

        # Spindle cooldown settings
        
        TabbedPanelItem:
            id: spindle_tab
            background_normal: 'asmcnc/apps/maintenance_app/img/spindle_settings_tab_blue.png'
            background_down: 'asmcnc/apps/maintenance_app/img/spindle_settings_tab_grey.png'

            BoxLayout:
                size_hint: (None,None)
                width: dp(1.005*app.width)
                height: dp(0.8125*app.height)
                orientation: "vertical" 
                padding:[dp(0.0275)*app.width, dp(0.0416666666667)*app.height, dp(0.0275)*app.width, dp(0.0416666666667)*app.height]
                spacing:0.0416666666667*app.height
                canvas:
                    Color:
                        rgba: hex('#E5E5E5FF')
                    Rectangle:
                        size: self.size
                        pos: self.pos

                BoxLayout:
                    size_hint: (None,None)
                    width: dp(0.95*app.width)
                    height: dp(0.729166666667*app.height)
                    orientation: "horizontal" 
                    padding: dp(0)
                    spacing:dp(0.025)*app.width

                    BoxLayout:
                        size_hint: (None,None)
                        height: dp(0.729166666667*app.height)
                        width: dp(0.95*app.width)
                        id: spindle_settings_container

        # Z Misc settings (probe plate and time since lead screw lubrication)

        TabbedPanelItem:
            background_normal: 'asmcnc/apps/maintenance_app/img/z_misc_tab_blue.png'
            background_down: 'asmcnc/apps/maintenance_app/img/z_misc_tab_grey.png'

            BoxLayout:
                size_hint: (None,None)
                width: dp(1.005*app.width)
                height: dp(0.8125*app.height)
                orientation: "horizontal" 
                padding:[dp(0.0275)*app.width, dp(0.0416666666667)*app.height, dp(0.0275)*app.width, dp(0.0416666666667)*app.height]
                spacing:0.025*app.width
                canvas:
                    Color:
                        rgba: hex('#E5E5E5FF')
                    Rectangle:
                        size: self.size
                        pos: self.pos

                BoxLayout:
                    size_hint: (None,None)
                    width: dp(0.725*app.width)
                    height: dp(0.729166666667*app.height)
                    orientation: "vertical" 
                    padding: dp(0)
                    spacing:dp(0.0416666666667)*app.height

                    BoxLayout:
                        size_hint: (None,None)
                        height: dp(0.270833333333*app.height)
                        width: dp(0.725*app.width)
                        id: touchplate_offset_container
                        canvas:
                            Color:
                                rgba: 1,1,1,1
                            RoundedRectangle:
                                size: self.size
                                pos: self.pos

                    BoxLayout:
                        size_hint: (None,None)
                        height: dp(0.416666666667*app.height)
                        width: dp(0.725*app.width)
                        id: z_lubrication_reminder_container
                        canvas:
                            Color:
                                rgba: 1,1,1,1
                            RoundedRectangle:
                                size: self.size
                                pos: self.pos

                BoxLayout:
                    size_hint: (None,None)
                    height: dp(0.729166666667*app.height)
                    width: dp(0.2*app.width)
                    id: z_misc_save_container
                    canvas:
                        Color:
                            rgba: 1,1,1,1
                        RoundedRectangle:
                            size: self.size
                            pos: self.pos

        # General settings tab

        TabbedPanelItem:
            id: general_settings_tab
            background_normal: 'asmcnc/apps/maintenance_app/img/general_settings_tab_blue.png'
            background_down: 'asmcnc/apps/maintenance_app/img/general_settings_tab_grey.png'

            BoxLayout:
                size_hint: (None,None)
                width: dp(1.005*app.width)
                height: dp(0.8125*app.height)
                orientation: "vertical" 
                padding:[dp(0.0275)*app.width, dp(0.0416666666667)*app.height, dp(0.0275)*app.width, dp(0.0416666666667)*app.height]
                spacing:0.0416666666667*app.height
                canvas:
                    Color:
                        rgba: color_provider.get_rgba("light_grey")
                    Rectangle:
                        size: self.size
                        pos: self.pos

                BoxLayout: 
                    id: general_settings_container
                    height: dp(0.729166666667*app.height)
                    width: dp(0.95*app.width)
                    canvas:
                        Color:
                            rgba: color_provider.get_rgba("white")
                        RoundedRectangle:
                            size: self.size
                            pos: self.pos

        # + Tab

        TabbedPanelItem:
            id: plus_tab
            background_normal: 'asmcnc/apps/maintenance_app/img/blank_blue_tab.png'
            background_down: 'asmcnc/apps/maintenance_app/img/blank_blue_tab.png'
            background_disabled_down: 'asmcnc/apps/maintenance_app/img/blank_blue_tab.png'
            background_disabled_normal: 'asmcnc/apps/maintenance_app/img/blank_blue_tab.png'
            disabled: 'True'

            BoxLayout:
                size_hint: (None,None)
                width: dp(1.005*app.width)
                height: dp(0.8125*app.height)
                orientation: "vertical" 
                padding:[dp(0.0275)*app.width, dp(0.0416666666667)*app.height, dp(0.0275)*app.width, dp(0.0416666666667)*app.height]
                spacing:0.0416666666667*app.height
                canvas:
                    Color:
                        rgba: hex('#E5E5E5FF')
                    Rectangle:
                        size: self.size
                        pos: self.pos

                BoxLayout: 
                    id: spindle_health_check_container
                    height: dp(0.729166666667*app.height)
                    width: dp(0.95*app.width)
                    canvas:
                        Color:
                            rgba: 1,1,1,1
                        RoundedRectangle:
                            size: self.size
                            pos: self.pos

    BoxLayout:
        size_hint: (None,None)
        pos: (dp(710.0/800.0)*app.width, dp(390.0/480.0)*app.height + (4 if app.height == 768 else 0))
        Button:
            font_size: str(0.01875 * app.width) + 'sp'
            size_hint: (None,None)
            height: dp(0.1875*app.height)
            width: dp(0.1125*app.width)
            background_color: color_provider.get_rgba("invisible")
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

"""
)


class MaintenanceScreenClass(Screen):
    laser_datum_reset_coordinate_x = 0
    laser_datum_reset_coordinate_y = 0
    landing_tab = StringProperty()

    def __init__(self, **kwargs):
        super(MaintenanceScreenClass, self).__init__(**kwargs)
        self.m = kwargs["machine"]
        self.sm = kwargs["screen_manager"]
        self.jd = kwargs["job"]
        self.l = kwargs["localization"]
        self.kb = kwargs["keyboard"]
        self.xy_move_widget = widget_maintenance_xy_move.MaintenanceXYMove(
            machine=self.m, screen_manager=self.sm
        )
        self.xy_move_container.add_widget(self.xy_move_widget)
        self.z_move_widget = widget_maintenance_z_move.MaintenanceZMove(
            machine=self.m, screen_manager=self.sm, localization=self.l, job=self.jd
        )
        self.z_move_container.add_widget(self.z_move_widget)
        self.laser_datum_buttons_widget = (
            widget_maintenance_laser_buttons.LaserDatumButtons(
                machine=self.m, screen_manager=self.sm, localization=self.l
            )
        )
        self.laser_button_container.add_widget(self.laser_datum_buttons_widget)
        self.laser_switch_widget = widget_maintenance_laser_switch.LaserOnOffWidget(
            machine=self.m, screen_manager=self.sm
        )
        self.switch_container.add_widget(self.laser_switch_widget)
        self.brush_use_widget = widget_maintenance_brush_use.BrushUseWidget(
            machine=self.m, screen_manager=self.sm, localization=self.l
        )
        self.brush_use_container.add_widget(self.brush_use_widget)
        self.brush_life_widget = widget_maintenance_brush_life.BrushLifeWidget(
            machine=self.m, screen_manager=self.sm, localization=self.l
        )
        self.brush_life_container.add_widget(self.brush_life_widget)
        self.brush_save_widget = widget_maintenance_brush_save.BrushSaveWidget(
            machine=self.m, screen_manager=self.sm, localization=self.l
        )
        self.brush_save_container.add_widget(self.brush_save_widget)
        self.monitor_percentage = (
            1 - self.m.spindle_brush_use_seconds / self.m.spindle_brush_lifetime_seconds
        )
        self.brush_monitor_widget = widget_maintenance_brush_monitor.BrushMonitorWidget(
            machine=self.m,
            screen_manager=self.sm,
            input_percentage=self.monitor_percentage,
        )
        self.brush_monitor_container.add_widget(self.brush_monitor_widget)
        self.spindle_settings_widget = (
            widget_maintenance_spindle_settings.SpindleSettingsWidget(
                machine=self.m, screen_manager=self.sm, localization=self.l
            )
        )
        self.spindle_settings_container.add_widget(self.spindle_settings_widget)
        self.z_misc_save_widget = widget_maintenance_z_misc_save.ZMiscSaveWidget(
            machine=self.m, screen_manager=self.sm, localization=self.l
        )
        self.z_misc_save_container.add_widget(self.z_misc_save_widget)
        self.touchplate_offset_widget = (
            widget_maintenance_touchplate_offset.TouchplateOffsetWidget(
                machine=self.m, screen_manager=self.sm, localization=self.l
            )
        )
        self.touchplate_offset_container.add_widget(self.touchplate_offset_widget)
        self.z_lubrication_reminder_widget = (
            widget_maintenance_z_lubrication_reminder.ZLubricationReminderWidget(
                machine=self.m, screen_manager=self.sm, localization=self.l
            )
        )
        self.z_lubrication_reminder_container.add_widget(
            self.z_lubrication_reminder_widget
        )
        self.general_settings_widget = (
            widget_maintenance_general_settings.GeneralSettingsWidget(
                machine=self.m, screen_manager=self.sm, localization=self.l
            )
        )
        self.general_settings_container.add_widget(
            self.general_settings_widget
        )
        if self.m.theateam():
            self.add_plus_tab()
        self.update_strings()
        self.text_inputs = [
            self.brush_use_widget.brush_use,
            self.brush_life_widget.brush_life,
            self.touchplate_offset_widget.touchplate_offset,
        ]

    def quit_to_lobby(self):
        self.on_tab_switch()
        self.sm.current = "lobby"

    def on_pre_enter(self):
        if self.m.is_laser_enabled == True:
            self.laser_switch_widget.laser_switch.active = True
        else:
            self.laser_switch_widget.laser_switch.active = False
        self.laser_switch_widget.toggle_laser()
        self.brush_use_widget.brush_use.text = str(
            int(self.m.spindle_brush_use_seconds / 3600)
        )
        self.brush_life_widget.brush_life.text = str(
            int(self.m.spindle_brush_lifetime_seconds / 3600)
        )
        value = (
            1 - self.m.spindle_brush_use_seconds / self.m.spindle_brush_lifetime_seconds
        )
        self.brush_monitor_widget.set_percentage(value)
        if self.m.spindle_digital:
            string_digital = "digital"
            self.spindle_settings_widget.cooldown_speed_slider.disabled = False
        else:
            string_digital = "manual"
            self.spindle_settings_widget.cooldown_speed_slider.disabled = True
        if self.m.is_stylus_enabled:
            self.spindle_settings_widget.stylus_switch.active = True
        else:
            self.spindle_settings_widget.stylus_switch.active = False
        self.spindle_settings_widget.spindle_brand.text = (
            " "
            + str(self.m.spindle_brand)
            + " "
            + string_digital
            + " "
            + str(self.m.spindle_voltage)
            + "V"
        )
        if "SC2" in self.m.spindle_brand:
            self.spindle_settings_widget.show_spindle_data_container()
        else:
            self.spindle_settings_widget.hide_spindle_data_container()
        self.spindle_settings_widget.cooldown_time_slider.value = (
            self.m.spindle_cooldown_time_seconds
        )
        self.spindle_settings_widget.cooldown_speed_slider.value = (
            self.m.spindle_cooldown_rpm
        )
        self.spindle_settings_widget.rpm_override = self.m.spindle_cooldown_rpm_override
        self.spindle_settings_widget.spindle_brand.values = (
            self.spindle_settings_widget.brand_list_sc1
        )
        if self.m.get_dollar_setting(51) != -1:
            if self.m.theateam():
                self.spindle_settings_widget.spindle_brand.values = (
                    self.spindle_settings_widget.brand_list_sc2
                )
        self.touchplate_offset_widget.touchplate_offset.text = str(
            self.m.z_touch_plate_thickness
        )
        self.z_lubrication_reminder_widget.update_time_left()
        if self.m.theateam() and self.plus_tab.disabled:
            self.add_plus_tab()
            self.spindle_health_check_widget.update_strings()

    def on_enter(self):
        self.kb.setup_text_inputs(self.text_inputs)
        if self.landing_tab == "brush_tab":
            self.tab_panel.switch_to(self.brush_tab)
        elif self.landing_tab == "laser_tab":
            self.tab_panel.switch_to(self.laser_tab)
        elif self.landing_tab == "spindle_tab":
            self.tab_panel.switch_to(self.spindle_tab)
        elif self.m.theateam() and self.landing_tab == "spindle_health_check_tab":
            self.tab_panel.switch_to(self.plus_tab)
        else:
            try:
                self.landing_tab = self.tab_panel.current
            except:
                self.tab_panel.switch_to(self.laser_tab)

    def on_pre_leave(self):
        self.laser_datum_buttons_widget.save_button_image.source = (
            "./asmcnc/apps/maintenance_app/img/save_button_132_greyscale.png"
        )
        self.laser_datum_buttons_widget.save_button.disabled = True
        self.m.write_z_head_laser_offset_values(
            self.m.is_laser_enabled,
            self.m.laser_offset_x_value,
            self.m.laser_offset_y_value,
        )
        if self.m.is_laser_enabled == True:
            self.sm.get_screen("home").default_datum_choice = "laser"
        else:
            self.sm.get_screen("home").default_datum_choice = "spindle"
        self.m.laser_off()

    def add_plus_tab(self):
        self.plus_tab.disabled = False
        self.plus_tab.background_normal = (
            "asmcnc/apps/maintenance_app/img/pro_plus_tab.png"
        )
        self.plus_tab.background_down = (
            "asmcnc/apps/maintenance_app/img/pro_plus_tab_active.png"
        )
        self.spindle_health_check_widget = (
            widget_maintenance_spindle_health_check.WidgetSpindleHealthCheck(
                machine=self.m, screen_manager=self.sm, localization=self.l
            )
        )
        self.spindle_health_check_container.add_widget(self.spindle_health_check_widget)

    def update_strings(self):
        self.laser_datum_label.text = self.l.get_bold("LASER")
        self.brush_monitor_label.text = self.l.get_bold("BRUSH MONITOR")
        self.brush_use_widget.update_strings()
        self.brush_life_widget.update_strings()
        self.spindle_settings_widget.update_strings()
        self.z_lubrication_reminder_widget.update_strings()
        self.touchplate_offset_widget.update_strings()
        try:
            self.spindle_health_check_widget.update_strings()
        except:
            pass
        self.update_font_size(self.brush_monitor_label)

    def update_font_size(self, value):
        text_length = self.l.get_text_length(value.text)
        if text_length > 18:
            value.font_size = 0.02375 * Window.width
        else:
            value.font_size = 0.0275 * Window.width

    def on_tab_switch(self):
        for text_input in self.text_inputs:
            text_input.focus = False
        if self.tab_panel.current_tab != self.laser_tab:
            self.laser_datum_buttons_widget.save_button_image.source = (
                "./asmcnc/apps/maintenance_app/img/save_button_132_greyscale.png"
            )
            self.laser_datum_buttons_widget.save_button.disabled = True
