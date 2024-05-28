"""
Created on 19 Aug 2017

@author: Ed
"""

import kivy
from asmcnc.comms.logging_system.logging_system import Logger
from asmcnc.comms.model_manager import ModelManagerSingleton
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition, FadeTransition
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty, ListProperty, NumericProperty
from kivy.uix.widget import Widget
from kivy.clock import Clock
import os, sys, threading
from datetime import datetime
from multiprocessing import Process, Manager
from asmcnc.skavaUI import (
    widget_virtual_bed,
    widget_status_bar,
    widget_z_move,
    widget_xy_move,
    widget_common_move,
    widget_quick_commands,
)
from asmcnc.skavaUI import (
    widget_virtual_bed_control,
    widget_gcode_monitor,
    widget_gcode_summary,
    widget_gcode_view,
)
from asmcnc.skavaUI import popup_info
from asmcnc.geometry import job_envelope
from time import sleep

Builder.load_string(
    """

#:import hex kivy.utils.get_color_from_hex
#:import FadeTransition kivy.uix.screenmanager.FadeTransition

<HomeScreen>:

    file_data_label:file_data_label
    virtual_bed_container:virtual_bed_container
    status_container:status_container
    z_move_container:z_move_container
    xy_move_container:xy_move_container
    common_move_container:common_move_container
    quick_commands_container:quick_commands_container
    virtual_bed_control_container:virtual_bed_control_container
    gcode_monitor_container:gcode_monitor_container
    home_tab:home_tab
    tab_panel:tab_panel
    pos_tab:pos_tab
    gcode_preview_container:gcode_preview_container
    move_tab:move_tab

    job_recovery_button:job_recovery_button
    job_recovery_button_image:job_recovery_button_image
    
    on_touch_down:root.on_touch()

    BoxLayout:
        padding: 0
        spacing:0.0208333333333*app.height
        orientation: "vertical"

        BoxLayout:
            size_hint_y: 0.9
            padding: 0
            spacing:0.0125*app.width
            orientation: "horizontal"

            BoxLayout:
                size_hint_x: 0.9

                TabbedPanel:
                    id: tab_panel
                    size_hint: 1, 1
                    pos_hint: {'center_x': .5, 'center_y': .5}
                    do_default_tab: False
                    tab_pos: 'left_top'
                    tab_height: 0.1875*app.height
                    tab_width: 0.1125*app.width

                    TabbedPanelItem:
                        background_normal: 'asmcnc/skavaUI/img/tab_set_normal.png'
                        background_down: 'asmcnc/skavaUI/img/tab_set_up.png'
                        on_press: root.m.laser_off()
                        BoxLayout:
                            padding:[dp(0.025)*app.width, dp(0.0416666666667)*app.height]
                            spacing:0.025*app.width
                            canvas:
                                Color:
                                    rgba: hex('#E5E5E5FF')
                                Rectangle:
                                    size: self.size
                                    pos: self.pos

                            BoxLayout:
                                id: gcode_monitor_container


                    TabbedPanelItem:
                        id: move_tab
                        background_normal: 'asmcnc/skavaUI/img/tab_move_normal.png'
                        background_down: 'asmcnc/skavaUI/img/tab_move_up.png'
                        on_press: root.m.laser_on()
                        BoxLayout:
                            orientation: 'horizontal'
                            padding:[dp(0.025)*app.width, dp(0.0416666666667)*app.height]
                            spacing:0.025*app.width
                            canvas:
                                Color:
                                    rgba: hex('#E5E5E5FF')
                                Rectangle:
                                    size: self.size
                                    pos: self.pos

                            BoxLayout:
                                size_hint_x: 3
                                id: xy_move_container
                                canvas:
                                    Color:
                                        rgba: 1,1,1,1
                                    RoundedRectangle:
                                        size: self.size
                                        pos: self.pos

                            BoxLayout:
                                size_hint_x: 1
                                id: common_move_container

                            BoxLayout:
                                size_hint_x: 2
                                id: z_move_container
                                canvas:
                                    Color:
                                        rgba: 1,1,1,1
                                    RoundedRectangle:
                                        size: self.size
                                        pos: self.pos


                    TabbedPanelItem:
                        id: pos_tab
                        background_normal: 'asmcnc/skavaUI/img/tab_pos_normal.png'
                        background_down: 'asmcnc/skavaUI/img/tab_pos_up.png'
                        on_press: root.m.laser_on()
                        BoxLayout:
                            orientation: 'vertical'
                            padding:[dp(0.025)*app.width, dp(0.0416666666667)*app.height]
                            spacing:0.0416666666667*app.height
                            canvas:
                                Color:
                                    rgba: hex('#E5E5E5FF')
                                Rectangle:
                                    size: self.size
                                    pos: self.pos

                            BoxLayout:
                                size_hint_y: 5
                                padding:[dp(0.0125)*app.width, dp(0.0208333333333)*app.height]
                                canvas:
                                    Color:
                                        rgba: 1,1,1,1
                                    RoundedRectangle:
                                        size: self.size
                                        pos: self.pos
                                id: virtual_bed_container

                            BoxLayout:
                                size_hint_y: 1
                                id: virtual_bed_control_container


                    TabbedPanelItem:
                        background_normal: 'asmcnc/skavaUI/img/tab_job_normal.png'
                        background_down: 'asmcnc/skavaUI/img/tab_job_up.png'
                        on_press: root.m.laser_off()
                        id: home_tab
                        BoxLayout:
                            orientation: 'vertical'
                            padding:[dp(0.025)*app.width, dp(0.0416666666667)*app.height]
                            spacing:0.0416666666667*app.height
                            id: job_container
                            canvas:
                                Color:
                                    rgba: hex('#E5E5E5FF')
                                Rectangle:
                                    size: self.size
                                    pos: self.pos

                            BoxLayout:
                                size_hint_y: 1
                                padding:[dp(0.0125)*app.width, dp(0.0208333333333)*app.height]
                                spacing:0.0125*app.width
                                orientation: 'horizontal'
                                canvas:
                                    Color:
                                        rgba: 1,1,1,1
                                    RoundedRectangle:
                                        size: self.size
                                        pos: self.pos

                                Button:
                                    font_size: str(0.01875 * app.width) + 'sp'
                                    size_hint_x: 1
                                    background_color: hex('#F4433600')
                                    on_press:
                                        root.manager.current = 'local_filechooser'
                                    BoxLayout:
                                        padding: 0
                                        size: self.parent.size
                                        pos: self.parent.pos
                                        Image:
                                            source: "./asmcnc/skavaUI/img/load_file.png"
                                            center_x: self.parent.center_x
                                            y: self.parent.y
                                            size: self.parent.width, self.parent.height
                                            allow_stretch: True

                                Button:
                                    font_size: str(0.01875 * app.width) + 'sp'
                                    id: job_recovery_button
                                    size_hint_x: 1
                                    background_color: hex('#F4433600')
                                    on_press:
                                        root.manager.current = 'recovery_decision'
                                    BoxLayout:
                                        padding: 0
                                        size: self.parent.size
                                        pos: self.parent.pos
                                        Image:
                                            id: job_recovery_button_image
                                            source: "./asmcnc/skavaUI/img/recover_job_disabled.png"
                                            center_x: self.parent.center_x
                                            y: self.parent.y
                                            size: self.parent.width, self.parent.height
                                            allow_stretch: True

                                Label:
                                    id: file_data_label
                                    size_hint_x: 4
                                    text_size: self.size
                                    font_size: str(0.025*app.width) + 'sp'
                                    markup: True
                                    text: '[color=333333]Load a file...[/color]'
                                    halign: 'center'
                                    valign: 'middle'

                            BoxLayout:
                                size_hint_y: 3
                                padding:[dp(0.025)*app.width, dp(0.0416666666667)*app.height]
                                orientation: 'horizontal'
                                canvas:
                                    Color:
                                        rgba: 1,1,1,1
                                    RoundedRectangle:
                                        size: self.size
                                        pos: self.pos
                                BoxLayout:
                                    id: gcode_preview_container
                                    size_hint_x: 1
                                    orientation: 'horizontal'


            BoxLayout:
                size_hint_x: 0.1
                id: quick_commands_container

        BoxLayout:
            size_hint_y: 0.08
            id: status_container

"""
)


class HomeScreen(Screen):
    no_image_preview_path = "asmcnc/skavaUI/img/image_preview_inverted.png"
    gcode_has_been_checked_and_its_ok = False
    non_modal_gcode_list = []
    job_box = job_envelope.BoundingBox()
    default_datum_choice = "spindle"
    z_datum_reminder_flag = False
    has_datum_been_reset = False

    def __init__(self, **kwargs):
        self.m = kwargs.pop("machine")
        self.sm = kwargs.pop("screen_manager")
        self.jd = kwargs.pop("job")
        self.set = kwargs.pop("settings")
        self.l = kwargs.pop("localization")
        self.kb = kwargs.pop("keyboard")
        super(HomeScreen, self).__init__(**kwargs)
        Clock.schedule_once(lambda *args: self.tab_panel.switch_to(self.home_tab))
        self.model_manager = ModelManagerSingleton()
        self.m.bind(probe_z_coord=self.dismiss_z_datum_reminder)
        self.gcode_summary_widget = widget_gcode_summary.GCodeSummary(job=self.jd)
        self.gcode_preview_container.add_widget(self.gcode_summary_widget)
        self.gcode_preview_widget = widget_gcode_view.GCodeView(job=self.jd)
        self.gcode_preview_container.add_widget(self.gcode_preview_widget)
        self.virtual_bed_container.add_widget(
            widget_virtual_bed.VirtualBed(machine=self.m, screen_manager=self.sm)
        )
        self.status_container.add_widget(
            widget_status_bar.StatusBar(machine=self.m, screen_manager=self.sm)
        )
        self.virtual_bed_control_container.add_widget(
            widget_virtual_bed_control.VirtualBedControl(
                machine=self.m, screen_manager=self.sm, localization=self.l
            ),
            index=100,
        )
        self.xy_move_widget = widget_xy_move.XYMove(
            machine=self.m, screen_manager=self.sm, localization=self.l
        )
        self.common_move_widget = widget_common_move.CommonMove(
            machine=self.m, screen_manager=self.sm
        )
        self.xy_move_container.add_widget(self.xy_move_widget)
        self.common_move_container.add_widget(self.common_move_widget)
        self.z_move_container.add_widget(
            widget_z_move.ZMove(
                machine=self.m, screen_manager=self.sm, job=self.jd, localization=self.l
            )
        )
        self.gcode_monitor_widget = widget_gcode_monitor.GCodeMonitor(
            machine=self.m, screen_manager=self.sm, localization=self.l
        )
        self.gcode_monitor_container.add_widget(self.gcode_monitor_widget)
        self.quick_commands_container.add_widget(
            widget_quick_commands.QuickCommands(
                machine=self.m, screen_manager=self.sm, job=self.jd, localization=self.l
            )
        )
        self.text_inputs = [self.gcode_monitor_widget.gCodeInput]

    def on_enter(self):
        self.kb.setup_text_inputs(self.text_inputs)
        self.m.stylus_router_choice = "router"
        if (
            self.tab_panel.current_tab == self.move_tab
            or self.tab_panel.current_tab == self.pos_tab
        ):
            Clock.schedule_once(lambda dt: self.m.laser_on(), 0.2)
        else:
            Clock.schedule_once(lambda dt: self.m.set_led_colour("GREEN"), 0.2)
        if self.jd.job_gcode != []:
            self.gcode_summary_widget.display_summary()
            try:
                Clock.schedule_once(self.preview_job_file, 0.05)
            except:
                Logger.exception("Unable to preview file")

    def on_pre_enter(self):
        if self.jd.job_gcode == []:
            self.file_data_label.text = (
                "[color=333333]" + self.l.get_str("Load a file") + "..." + "[/color]"
            )
            self.job_filename = ""
            self.job_box.range_x[0] = 0
            self.job_box.range_x[1] = 0
            self.job_box.range_y[0] = 0
            self.job_box.range_y[1] = 0
            self.job_box.range_z[0] = 0
            self.job_box.range_z[1] = 0
            try:
                self.gcode_preview_widget.draw_file_in_xy_plane([])
                self.gcode_preview_widget.get_non_modal_gcode([])
            except:
                Logger.exception("No G-code loaded.")
            self.gcode_summary_widget.hide_summary()
        else:
            self.file_data_label.text = "[color=333333]" + self.jd.job_name + "[/color]"
        if not self.model_manager.is_machine_drywall():
            if self.jd.job_recovery_cancel_line != None:
                if self.jd.job_recovery_cancel_line == -1:
                    self.job_recovery_button_image.source = (
                        "./asmcnc/skavaUI/img/recover_job_disabled.png"
                    )
                else:
                    self.job_recovery_button_image.source = (
                        "./asmcnc/skavaUI/img/recover_job.png"
                    )
                if self.jd.job_recovery_selected_line == -1:
                    if self.jd.job_recovery_from_beginning:
                        self.file_data_label.text += (
                            "\n[color=FF0000]"
                            + self.l.get_str("Restart from beginning")
                            + "[/color]"
                        )
                else:
                    self.file_data_label.text += (
                        "\n[color=FF0000]"
                        + self.l.get_str("From line N").replace(
                            "N", str(self.jd.job_recovery_selected_line)
                        )
                        + "[/color]"
                    )
            else:
                self.job_recovery_button_image.source = (
                    "./asmcnc/skavaUI/img/recover_job_disabled.png"
                )
        else:
            self.job_recovery_button.disabled = True
            self.job_recovery_button.opacity = 0

    def on_touch(self):
        for text_input in self.text_inputs:
            text_input.focus = False

    def preview_job_file(self, dt):
        try:
            Logger.debug("> draw_file_in_xy_plane")
            self.gcode_preview_widget.draw_file_in_xy_plane(self.non_modal_gcode_list)
            Logger.debug("< draw_file_in_xy_plane")
        except:
            Logger.exception("Unable to draw gcode")
        Logger.info("DONE")

    def on_pre_leave(self):
        self.m.laser_off()

    def dismiss_z_datum_reminder(self, *args):
        self.z_datum_reminder_flag = False
        Logger.debug("Z datum reminder disabled")
