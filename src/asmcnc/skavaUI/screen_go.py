# -*- coding: utf-8 -*-
"""
Created on 19 Aug 2017

@author: Ed
"""
import time
import traceback
from datetime import datetime

from asmcnc.comms.logging_system.logging_system import Logger
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen

from asmcnc.core_UI.job_go.screens.screen_spindle_health_check import (
    SpindleHealthCheckActiveScreen,
)
from asmcnc.core_UI.job_go.widgets.widget_disabled_yeti_pilot import (
    DisabledYetiPilotWidget,
    DisabledYPCase,
)
from asmcnc.core_UI.job_go.widgets.widget_yeti_pilot import YetiPilotWidget
from asmcnc.skavaUI import (
    widget_status_bar,
    widget_feed_override,
    widget_speed_override,
    widget_z_height,
    popup_info
)
from asmcnc.apps.drywall_cutter_app.config import config_loader
from asmcnc.comms.model_manager import ModelManagerSingleton
from asmcnc.job.yetipilot.config.yetipilot_profile import YetiPilotProfile

Builder.load_string(
    """

#:import hex kivy.utils.get_color_from_hex

<GoScreen>:

    status_container:status_container
    z_height_container:z_height_container
    job_progress_container:job_progress_container
    feed_override_container:feed_override_container
    speed_override_widget_container:speed_override_widget_container
    start_or_pause_button_image:start_or_pause_button_image
    btn_back: btn_back
    stop_start:stop_start
    file_data_label:file_data_label
    run_time_label:run_time_label
    progress_percentage_label:progress_percentage_label
    btn_back_img:btn_back_img
    overload_status_label:overload_status_label
    spindle_overload_container:spindle_overload_container
    spindle_widgets: spindle_widgets
    speed_override_container: speed_override_container
    override_and_progress_container: override_and_progress_container
    yetipilot_container:yetipilot_container

    feed_label : feed_label
    spindle_label : spindle_label
    job_time_label : job_time_label
    file_lines_streamed_label : file_lines_streamed_label
    spindle_overload_label:spindle_overload_label
    
    BoxLayout:
        padding: 0
        spacing: 0
        orientation: "vertical"

        BoxLayout:
            size_hint_y: 0.92
            padding: 0
            spacing:0.0125*app.width
            orientation: "horizontal"

            BoxLayout:
                size_hint_x: 0.9
                padding:[dp(0.025)*app.width, dp(0.0416666666667)*app.height]
                spacing:0.025*app.width
                orientation: "horizontal"

                canvas:
                    Color:
                        rgba: hex('#E5E5E5FF')
                    Rectangle:
                        size: self.size
                        pos: self.pos

                BoxLayout:
                    orientation: 'vertical'
                    size_hint_x: 0.8
                    spacing:0.0416666666667*app.height

                    BoxLayout:
                        size_hint_y: 0.3
                        padding:[dp(0.025)*app.width, dp(0.0416666666667)*app.height]
                        canvas:
                            Color:
                                rgba: hex('#FFFFFFFF')
                            RoundedRectangle:
                                size: self.size
                                pos: self.pos
                        BoxLayout:
                            orientation: 'horizontal'
                            padding: 0
                            spacing:0.0125*app.width
                            Button:
                                font_size: str(0.01875 * app.width) + 'sp'
                                id: btn_back
                                size_hint_x: 1
                                background_color: hex('#F4433600')
                                on_press:
                                    root.return_to_app()
                                BoxLayout:
                                    padding: 0
                                    size: self.parent.size
                                    pos: self.parent.pos
                                    Image:
                                        id: btn_back_img
                                        # source: "./asmcnc/skavaUI/img/back.png"
                                        center_x: self.parent.center_x
                                        y: self.parent.y
                                        size: self.parent.width, self.parent.height
                                        allow_stretch: True
                            
                            Label:
                                size_hint_x: 5
                                text_size: self.size
                                font_size: str(0.025*app.width) + 'sp'
                                markup: True
                                halign: 'center'
                                valign: 'middle'
                                id: file_data_label
                                color: hex('#333333ff')
                                
                            Button:
                                font_size: str(0.01875 * app.width) + 'sp'
                                id: stop_start
                                size_hint_x: 1
                                disabled: False
                                background_color: hex('#F4433600')

                                on_press:
                                    root.start_or_pause_button_press()

                                BoxLayout:
                                    padding: 0
                                    size: self.parent.size
                                    pos: self.parent.pos
                                    Image:
                                        id: start_or_pause_button_image
                                        # source: "./asmcnc/skavaUI/img/go.png"
                                        center_x: self.parent.center_x
                                        y: self.parent.y
                                        size: self.parent.width, self.parent.height
                                        allow_stretch: True

                    BoxLayout:
                        id: override_and_progress_container
                        orientation: 'horizontal'
                        size_hint_y: 0.7
                        padding:[dp(0.0)*app.width, dp(0.0)*app.height]
                        spacing:0.0416666666667*app.height

                        BoxLayout:
                            orientation: 'vertical'
                            padding:[0, 0, 0, dp(0.0104166666667)*app.height]
                            spacing:0.0208333333333*app.height
                            size_hint_x: 0.2
                            canvas:
                                Color:
                                    rgba: hex('#FFFFFFFF')
                                RoundedRectangle:
                                    size: self.size
                                    pos: self.pos

                            BoxLayout:
                                size_hint_y: 1.8
                                orientation: 'vertical'
                                padding:[dp(0.0)*app.width, dp(0.0)*app.height]
                                spacing:0.0*app.height
                                canvas:
                                    Color:
                                        rgba: hex('#FFFFFFFF')
                                    RoundedRectangle:
                                        size: self.size
                                        pos: self.pos
                                Label:
                                    id: feed_label
                                    markup: True
                                    font_size: str(0.02*app.width) + 'px' 
                                    valign: 'middle'
                                    halign: 'center'
                                    size:self.texture_size
                                    text_size: self.size
                                    color: hex('#808080ff')

                            BoxLayout:
                                id: feed_override_container
                                padding: 0
                                size_hint_y: 9
                                canvas:
                                    Color:
                                        rgba: hex('#FFFFFFFF')
                                    RoundedRectangle:
                                        size: self.size
                                        pos: self.pos
    

                        BoxLayout:
                            id: speed_override_container
                            orientation: 'vertical'
                            padding:[0, 0, 0, dp(0.0104166666667)*app.height]
                            spacing:0.0208333333333*app.height
                            size_hint_x: 0.2
                            canvas:
                                Color:
                                    rgba: hex('#FFFFFFFF')
                                RoundedRectangle:
                                    size: self.size
                                    pos: self.pos

                            BoxLayout:
                                size_hint_y: 1.8
                                orientation: 'vertical'
                                padding:[dp(0.0)*app.width, dp(0.0)*app.height]
                                spacing:0.0*app.height
                                canvas:
                                    Color:
                                        rgba: hex('#FFFFFFFF')
                                    RoundedRectangle:
                                        size: self.size
                                        pos: self.pos
                                Label:
                                    id: spindle_label
                                    markup: True
                                    font_size: str(0.02*app.width) + 'px' 
                                    valign: 'middle'
                                    halign: 'center'
                                    size:self.texture_size
                                    text_size: self.size
                                    color: hex('#808080ff')

                            BoxLayout:
                                id: speed_override_widget_container
                                padding: 0
                                size_hint_y: 9
                                canvas:
                                    Color:
                                        rgba: hex('#FFFFFFFF')
                                    RoundedRectangle:
                                        size: self.size
                                        pos: self.pos
    
                        BoxLayout:
                            size_hint_x: 0.8
                            orientation: 'vertical'
                            spacing:0.0208333333333*app.height
                            
                            BoxLayout:
                                id: yetipilot_container
                                orientation: 'vertical'
                                size_hint_y: 0
                                
                                canvas:
                                    Color:
                                        rgba: hex('#FFFFFFFF')
                                    RoundedRectangle:
                                        size: self.size
                                        pos: self.pos

                            BoxLayout:
                                id: job_progress_container
                                size_hint_y: 2.5
                                orientation: 'vertical'
                                padding:[dp(0.025)*app.width, dp(0.0416666666667)*app.height]
                                spacing:0.0*app.height

                                canvas:
                                    Color:
                                        rgba: hex('#FFFFFFFF')
                                    RoundedRectangle:
                                        size: self.size
                                        pos: self.pos

                                Label:
                                    id: file_lines_streamed_label
                                    size_hint_y: 1
                                    # text: '[color=808080]File lines streamed:[/color]'
                                    markup: True                           
                                    font_size: str(0.02*app.width) + 'px'
                                    valign: 'middle'
                                    halign: 'left'
                                    size:self.texture_size
                                    text_size: self.size
                                    color: hex('#808080ff')
                                Label:
                                    size_hint_y: 3
                                    id: progress_percentage_label
                                    color: hex('#333333ff')
                                    text: '0 %'
                                    markup: True                           
                                    font_size: str(0.125*app.width) + 'px' 
                                    valign: 'middle'
                                    halign: 'left'
                                    size:self.texture_size
                                    text_size: self.size 
                                Label:
                                    id: job_time_label
                                    size_hint_y: 0.9
                                    markup: True                           
                                    font_size: str(0.02*app.width) + 'px' 
                                    valign: 'middle'
                                    halign: 'left'
                                    size:self.texture_size
                                    text_size: self.size
                                    color: hex('#808080ff')
                                Label:
                                    size_hint_y: 1.1
                                    id: run_time_label
                                    markup: True                           
                                    font_size: str(0.0225*app.width) + 'px'
                                    valign: 'middle'
                                    halign: 'left'
                                    size:self.texture_size
                                    text_size: self.size
                                    color: hex('#333333ff')

                BoxLayout:
                    id: spindle_widgets
                    orientation: 'vertical'
                    size_hint_x: 0.15
                    padding:[dp(0.025)*app.width, dp(0.0416666666667)*app.height]
                    spacing:0.0416666666667*app.height

                    canvas:
                        Color:
                            rgba: hex('#FFFFFFFF')
                        RoundedRectangle:
                            size: self.size
                            pos: self.pos

                    BoxLayout:
                        size_hint_y: 0.95
                        id: z_height_container


                    BoxLayout:
                        id: spindle_overload_container
                        orientation: 'vertical'
                        size_hint_y: 0.25
                        padding:[0, 0, 0, dp(-0.0208333333333)*app.height]
                        spacing:0.0208333333333*app.height
 
                        Label:
                            id: spindle_overload_label
                            halign: 'center'
                            font_size: str(0.02*app.width) + 'px' 
                            text: '[color=808080]Spindle\\noverload:[/color]'
                            markup: True
                        
                        Label:
                            font_size: str(0.04*app.width) + 'px' 
                            id: overload_status_label
                            halign: 'center'
                            text: '[color=333333]0 %[/color]'
                            markup: True

        BoxLayout:
            size_hint_y: 0.08
            id: status_container

"""
)


class GoScreen(Screen):
    btn_back = ObjectProperty()
    btn_back_img = ObjectProperty()
    start_or_pause_button_image = ObjectProperty()
    show_spindle_overload = False
    spindle_speed_showing = True
    is_job_started_already = False
    temp_suppress_prompts = False
    return_to_screen = "home"  # screen to go to after job runs
    cancel_to_screen = "home"  # # screen to go back to before job runs, or set to return to after job started
    loop_for_job_progress = None
    loop_for_feeds_and_speeds = None
    listen_for_pauses = None
    lift_z_on_job_pause = False
    overload_peak = 0
    spindle_speed_max_percentage = 0
    spindle_speed_max_absolute = 0
    feed_rate_max_percentage = 0
    feed_rate_max_absolute = 0
    total_runtime_seconds = 0
    dwt_config = None

    def __init__(self, **kwargs):
        super(GoScreen, self).__init__(**kwargs)
        self.m = kwargs["machine"]
        self.sm = kwargs["screen_manager"]
        self.jd = kwargs["job"]
        self.am = kwargs["app_manager"]
        self.l = kwargs["localization"]
        self.database = kwargs["database"]
        self.yp = kwargs["yetipilot"]
        # bind on updates:
        self.m.s.bind(on_update_overload_peak=self.update_overload_peak)
        self.m.s.bind(on_reset_runtime=self.on_reset_runtime)
        self.feedOverride = widget_feed_override.FeedOverride(
            machine=self.m, screen_manager=self.sm, database=self.database
        )
        self.speedOverride = widget_speed_override.SpeedOverride(
            machine=self.m, screen_manager=self.sm, database=self.database
        )
        self.model_manager = ModelManagerSingleton()

        # Graphics commands

        self.z_height_container.add_widget(
            widget_z_height.VirtualZ(
                machine=self.m, screen_manager=self.sm, job=self.jd
            )
        )
        self.feed_override_container.add_widget(self.feedOverride)
        self.speed_override_widget_container.add_widget(self.speedOverride)

        # Status bar

        self.status_container.add_widget(
            widget_status_bar.StatusBar(machine=self.m, screen_manager=self.sm)
        )

        # initialise for db send

        self.time_taken_seconds = 0
        self.jd.percent_thru_job = 0

        # Optional containers
        self.yp_widget = YetiPilotWidget(
            screen_manager=self.sm,
            localization=self.l,
            machine=self.m,
            database=self.database,
            yetipilot=self.yp,
        )
        self.disabled_yp_widget = DisabledYetiPilotWidget(
            screen_manager=self.sm,
            localization=self.l,
            machine=self.m,
            database=self.database,
            yetipilot=self.yp,
        )
        self.update_strings()

    ### PRE-ENTER CONTEXTS: Call one before switching to screen
    def on_pre_enter(self, *args):
        self.return_to_screen = self.jd.screen_to_return_to_after_job
        self.cancel_to_screen = self.jd.screen_to_return_to_after_cancel
        self.sm.get_screen("job_feedback").return_to_screen = self.return_to_screen

        # get initial values on screen loading
        self.poll_for_job_progress(0)
        # show overload status if running precision pro
        if (
                str(self.m.serial_number()).endswith("03")
                or self.show_spindle_overload == True
        ) and self.m.stylus_router_choice != "stylus":
            # self.update_overload_label(self.m.s.overload_state)
            self.update_overload_label(0)
            self.spindle_overload_container.size_hint_y = 0.25
            self.spindle_overload_container.opacity = 1
            self.spindle_overload_container.padding = [0, 0, 0, -10]
            self.spindle_overload_container.spacing = 10
            self.spindle_widgets.spacing = 20
        else:
            self.spindle_overload_container.height = 0
            self.spindle_overload_container.size_hint_y = 0
            self.spindle_overload_container.opacity = 0
            self.spindle_overload_container.padding = 0
            self.spindle_overload_container.spacing = 0
            self.spindle_widgets.spacing = 0
        # Hide/show spindle speed depending on if stylus is chosen
        if (
                self.m.stylus_router_choice != "stylus"
                and self.spindle_speed_showing == False
        ):
            self.override_and_progress_container.add_widget(
                self.speed_override_container, index=1
            )
            self.spindle_speed_showing = True
        elif (
                self.m.stylus_router_choice == "stylus"
                and self.spindle_speed_showing == True
        ):
            self.override_and_progress_container.remove_widget(
                self.speed_override_container
            )
            self.spindle_speed_showing = False

        # Show stylus or router graphic depending on choice
        if self.m.stylus_router_choice == "stylus":
            self.z_height_container.children[
                0
            ].z_bit.source = "./asmcnc/skavaUI/img/zBit_stylus.png"
        else:
            self.z_height_container.children[
                0
            ].z_bit.source = "./asmcnc/skavaUI/img/zBit.png"
        use_sc2 = self.m.is_using_sc2()
        self.show_hide_yp_container(use_sc2)
        self.loop_for_job_progress = Clock.schedule_interval(
            self.poll_for_job_progress, 1
        )
        self.loop_for_feeds_and_speeds = Clock.schedule_interval(
            self.poll_for_feeds_and_speeds, 0.2
        )
        self.yp_widget.switch_reflects_yp()
        if not self.is_job_started_already:
            self.reset_go_screen_prior_to_job_start()
        if self.show_maintenance_prompts():
            self.check_brush_use_and_lifetime(
                self.m.spindle_brush_use_seconds, self.m.spindle_brush_lifetime_seconds
            )
        if self.temp_suppress_prompts:
            self.temp_suppress_prompts = False

    def on_reset_runtime(self, *args):
        Logger.debug('total_runtime_seconds has been reset.')
        self.total_runtime_seconds = 0

    def show_hide_yp_container(self, use_sc2):
        if use_sc2:
            # Show yetipilot container
            self.job_progress_container.padding = [20.0/800.0*Window.width, 10.0/480.0*Window.height]
            self.yetipilot_container.size_hint_y = 1
            self.yetipilot_container.opacity = 1
            self.yetipilot_container.parent.spacing = 10.0/480.0*Window.height
            if (
                    self.m.is_spindle_health_check_active()
                    and not self.m.has_spindle_health_check_failed()
            ):
                if not self.yp_widget.parent:
                    self.yetipilot_container.add_widget(self.yp_widget)
                if self.disabled_yp_widget.parent:
                    self.yetipilot_container.remove_widget(self.disabled_yp_widget)
                self.yp_widget.switch.disabled = False
                self.yp_widget.yp_cog_button.disabled = False

                if self.return_to_screen == "drywall_cutter":
                    self.yp.enable()

                    diameter = str(self.dwt_config.active_cutter.generic_definition.dimension)
                    unit = self.dwt_config.active_cutter.generic_definition.unit.encode('utf-8')

                    chosen_profile = YetiPilotProfile(
                        cutter_diameter=(diameter + unit).encode('utf-8'),
                        cutter_type=self.dwt_config.active_cutter.generic_definition.type,
                        material_type=self.dwt_config.active_profile.material.description,
                        step_down=self.dwt_config.active_profile.cutting_parameters.recommendations.stepdown,
                        parameters=[
                            {"Name": "spindle_tool_load_watts", "Value": self.dwt_config.active_profile.cutting_parameters.target_tool_load},
                            {"Name": "target_spindle_speed", "Value": self.dwt_config.active_profile.cutting_parameters.spindle_speed}
                        ]
                    )                    

                    self.yp.use_profile(chosen_profile)
                    self.yp_widget.update_profile_selection()
            else:
                if not self.disabled_yp_widget.parent:
                    self.yetipilot_container.add_widget(self.disabled_yp_widget)
                if self.yp_widget.parent:
                    self.yetipilot_container.remove_widget(self.yp_widget)
                if not self.m.has_spindle_health_check_failed():
                    self.disabled_yp_widget.set_version(DisabledYPCase.DISABLED)
                elif self.is_job_started_already:
                    self.disabled_yp_widget.set_version(DisabledYPCase.FAILED)
                else:
                    self.disabled_yp_widget.set_version(
                        DisabledYPCase.FAILED_AND_CAN_RUN_AGAIN
                    )
        else:
            # Hide yetipilot container
            if self.disabled_yp_widget.parent:
                self.yetipilot_container.remove_widget(self.disabled_yp_widget)
            if self.yp_widget.parent:
                self.yetipilot_container.remove_widget(self.yp_widget)
            self.job_progress_container.padding = (20.0/800.0*Window.width, 20.0/480.0*Window.height)
            self.yetipilot_container.size_hint_y = 0
            self.yetipilot_container.opacity = 0
            self.yetipilot_container.parent.spacing = 0
            self.yp_widget.disable_yeti_pilot()
            self.yp_widget.switch.disabled = True
            self.yp_widget.yp_cog_button.disabled = True

    def show_maintenance_prompts(self):
        return (
                not self.is_job_started_already
                and not self.temp_suppress_prompts
                and self.m.reminders_enabled
        )

    def get_sc2_brush_data(self):
        self.m.turn_on_spindle_for_data_read()
        Clock.schedule_once(self.get_spindle_info, 0.1)
        self.wait_popup = popup_info.PopupWait(self.sm, self.l)

    def get_spindle_info(self, dt):
        self.m.s.write_protocol(
            self.m.p.GetDigitalSpindleInfo(), "GET DIGITAL SPINDLE INFO"
        )
        Clock.schedule_once(self.read_spindle_info, 1)

    def read_spindle_info(self, dt):
        self.m.turn_off_spindle()
        self.wait_popup.popup.dismiss()

        # If info was not obtained successfully, spindle production year will equal 99
        if self.m.s.spindle_production_year != 99:
            try:
                self.check_brush_use_and_lifetime(
                    self.m.s.spindle_brush_run_time_seconds,
                    self.m.spindle_brush_lifetime_seconds,
                )
                return
            except:
                Logger.exception('Failed to check brush use and lifetime!')
        popup_info.PopupError(self.sm, self.l, self.l.get_str("Error!"))

    def check_brush_use_and_lifetime(self, use, lifetime):
        if use >= 0.9 * lifetime:
            brush_use_string = "[b]" + str(int(use / 3600)) + "[/b]"
            brush_lifetime_string = "[b]" + str(int(lifetime / 3600)) + "[/b]"
            brush_warning = (
                    self.l.get_bold("Check your spindle brushes before starting your job!")
                    + "\n\n"
                    + self.l.get_str(
                "You have used your SmartBench for N00 hours since you updated your spindle brush settings."
            )
                    .replace(self.l.get_str("hours"), self.l.get_bold("hours"))
                    .replace("N00", brush_use_string)
                    + " "
                    + self.l.get_str(
                "You have told us they only have a lifetime of N00 hours!"
            )
                    .replace(self.l.get_str("hours"), self.l.get_bold("hours"))
                    .replace("N00", brush_lifetime_string)
            )
            brush_reminder_popup = popup_info.PopupReminder(
                self.sm, self.am, self.m, self.l, brush_warning, "brushes"
            )
        if (
                self.m.time_since_z_head_lubricated_seconds
                >= self.m.time_to_remind_user_to_lube_z_seconds
        ):
            time_since_lubricated_string = (
                    "[b]"
                    + str(int(self.m.time_since_z_head_lubricated_seconds / 3600))
                    + "[/b]"
            )
            lubrication_warning = (
                    self.l.get_bold("Lubricate the z head before starting your job!")
                    + "\n\n"
                    + self.l.get_str(
                "You have used SmartBench for N00 hours since you last told us that you lubricated the Z head."
            )
                    .replace(self.l.get_str("hours"), self.l.get_bold("hours"))
                    .replace("N00", time_since_lubricated_string)
                    + "\n\n"
                    + self.l.get_str("Will you lubricate the Z head now?")
                    + "\n\n"
                    + self.l.get_str("Saying 'OK' will reset this reminder.")
            )
            lubrication_reminder_popup = popup_info.PopupReminder(
                self.sm, self.am, self.m, self.l, lubrication_warning, "lubrication"
            )
        if (
                self.m.time_since_calibration_seconds
                >= self.m.time_to_remind_user_to_calibrate_seconds
        ):
            time_since_calibration_string = (
                    "[b]" + str(int(self.m.time_since_calibration_seconds / 3600)) + "[/b]"
            )
            calibration_warning = (
                    self.l.get_str(
                        "You have used SmartBench for N00 hours since its last calibration."
                    )
                    .replace(self.l.get_str("hours"), self.l.get_bold("hours"))
                    .replace("N00", time_since_calibration_string)
                    + "\n\n"
                    + self.l.get_str(
                "A calibration procedure may improve the accuracy of SmartBench in the X and Y axis."
            )
                    + "\n\n"
                    + self.l.get_str(
                "A calibration procedure can take approximately 10 minutes with basic tools."
            )
                    + "\n\n"
                    + self.l.get_str("Calibration is not compulsory.")
                    + "\n\n"
                    + self.l.get_str("Will you calibrate SmartBench now?")
            )
            calibration_reminder_popup = popup_info.PopupReminder(
                self.sm, self.am, self.m, self.l, calibration_warning, "calibration"
            )

    ### COMMON SCREEN PREP METHOD
    def reset_go_screen_prior_to_job_start(self):
        Logger.debug("RESET GO SCREEN FIRES")
        # Update images
        self.start_or_pause_button_image.source = "./asmcnc/skavaUI/img/go.png"
        # Show back button
        self.btn_back_img.source = "./asmcnc/skavaUI/img/back.png"
        self.btn_back.disabled = False
        # scrape filename title
        self.file_data_label.text = self.jd.job_name
        # Reset flag & light
        self.is_job_started_already = False
        self.m.set_led_colour("GREEN")
        self.feedOverride.feed_norm()
        self.speedOverride.speed_norm()
        self.overload_peak = 0.0
        self.time_taken_seconds = 0
        self.jd.percent_thru_job = 0
        if (
                self.jd.job_recovery_filepath == self.jd.filename
                and self.jd.job_recovery_selected_line != -1
        ):
            self.progress_percentage_label.text = "- %"
        else:
            self.progress_percentage_label.text = str(self.jd.percent_thru_job) + " %"
        self.spindle_speed_max_percentage = 100
        self.spindle_speed_max_absolute = 0
        self.feed_rate_max_percentage = 100
        self.feed_rate_max_absolute = 0
        # Reset job tracking flags
        self.sm.get_screen("home").has_datum_been_reset = False
        self.sm.get_screen("home").z_datum_reminder_flag = False
        # Reset YP toggle
        if not self.m.has_spindle_health_check_passed():
            self.yp_widget.disable_yeti_pilot()

    ### GENERAL ACTIONS

    def start_or_pause_button_press(self):
        Logger.debug("start/pause button pressed")
        if self.is_job_started_already:
            if not self.m.is_machine_paused:
                self._pause_job()
                self.start_or_pause_button_image.source = (
                    "./asmcnc/skavaUI/img/resume.png"
                )
            else:
                self.m.resume_after_a_stream_pause()
                self.start_or_pause_button_image.source = (
                    "./asmcnc/skavaUI/img/pause.png"
                )
                # Job resumed, send event
                self.database.send_event(
                    0, "Job resumed", "Resumed job: " + self.jd.job_name, 4
                )
                self.m.s.is_ready_to_assess_spindle_for_shutdown = True  # allow spindle overload assessment to resume
        elif (
                self.m.is_spindle_health_check_active()
                and not self.m.has_spindle_health_check_run()
                and self.m.is_using_sc2()
        ):
            self.run_spindle_health_check(start_after_pass=True)
        else:
            if not self.m.has_spindle_health_check_passed():
                # If spindle health check fails for some reason, it will put SB into a door/pause state.
                # This will fix that, but also won't cause the same disruption as a soft reset.
                # This is a temporary patch; ideally the handling of the spindle health check needs refactoring.
                if self.m.has_spindle_health_check_run():
                    self.m.resume_from_a_soft_door()
                if self.m.is_spindle_health_check_active():
                    self.disabled_yp_widget.set_version(DisabledYPCase.FAILED)
                else:
                    self.disabled_yp_widget.set_version(DisabledYPCase.DISABLED)
            self._start_running_job()
        self.listen_for_pauses = Clock.schedule_interval(
            lambda dt: self.raise_pause_screens_if_paused(), self.POLL_FOR_PAUSE_SCREENS
        )

    def run_spindle_health_check(
            self, start_after_pass=False, return_to_advanced_tab=False
    ):
        if not self.sm.has_screen("spindle_health_check_active"):
            shc_screen = SpindleHealthCheckActiveScreen(
                name="spindle_health_check_active",
                screen_manager=self.sm,
                machine=self.m,
                localization=self.l,
            )
            self.sm.add_widget(shc_screen)
        self.sm.get_screen(
            "spindle_health_check_active"
        ).start_after_pass = start_after_pass
        self.sm.get_screen(
            "spindle_health_check_active"
        ).return_to_advanced_tab = return_to_advanced_tab
        self.sm.current = "spindle_health_check_active"

    # Pausing
    def _pause_job(self):
        self.m.stop_for_a_stream_pause("job_pause")
        self.sm.get_screen("spindle_shutdown").reason_for_pause = "job_pause"
        self.sm.get_screen("spindle_shutdown").return_screen = "go"
        self.sm.current = "spindle_shutdown"

    POLL_FOR_PAUSE_SCREENS = 0.5

    def raise_pause_screens_if_paused(self, dt=0, override=False):
        # Ok so 'spindle_shutdown' & the above func needs renaming & refactoring,
        # and the shutdown UI commands need pulling out of serial comms altogether, but that's for another day.
        # For now, this is enough:
        if (
                self.m.s.is_job_streaming
                and self.m.is_machine_paused
                and self.m.reason_for_machine_pause
                and self.m.reason_for_machine_pause != "Resuming"
                and not str(self.m.state()).startswith("Door:3")
                and self.start_or_pause_button_image.source
                == "./asmcnc/skavaUI/img/pause.png"
                or override
        ):
            if self.listen_for_pauses != None:
                self.listen_for_pauses.cancel()
                self.listen_for_pauses = None
            Logger.warning("RAISE PAUSE SCREEN: " + str(self.m.reason_for_machine_pause))
            self.sm.get_screen(
                "spindle_shutdown"
            ).reason_for_pause = self.m.reason_for_machine_pause
            self.sm.get_screen("spindle_shutdown").return_screen = "go"
            self.sm.current = "spindle_shutdown"
            self.start_or_pause_button_image.source = "./asmcnc/skavaUI/img/go.png"

    # Running
    def _start_running_job(self):
        self.database.send_job_start()
        self.jd.job_start_time = time.time()
        self.start_or_pause_button_image.source = "./asmcnc/skavaUI/img/pause.png"
        # Hide back button
        self.btn_back_img.source = "./asmcnc/skavaUI/img/file_running.png"
        self.btn_back.disabled = True
        self.m.set_pause(False)
        self.is_job_started_already = True
        Logger.info("Starting job...")

        # Vac_fix. Not very tidy but will probably work.
        # Also inject zUp-on-pause code if needed
        def prep_gcode(job_to_modify):
            modified_gcode = []
            # Spindle command??
            if self.lift_z_on_job_pause and self.m.fw_can_operate_zUp_on_pause():
                modified_gcode.append("M56")
                self.jd.job_recovery_offset += 1
            # Turn vac on if spindle gets turned on during job
            if (
                    str(job_to_modify).count("M3") > str(job_to_modify).count("M30")
                    or str(job_to_modify).count("M03") > 0
            ) and self.m.stylus_router_choice != "stylus":
                modified_gcode.append("AE")
                modified_gcode.append("G4 P2")
                modified_gcode.extend(job_to_modify)
                modified_gcode.append("G4 P2")
                modified_gcode.append("AF")
                self.jd.job_recovery_offset += 2
            else:
                modified_gcode.extend(job_to_modify)

            # Spindle command??
            if self.lift_z_on_job_pause and self.m.fw_can_operate_zUp_on_pause():
                modified_gcode.append("M56 P0")
            return modified_gcode

        # Check if job recovery is being performed
        if (
                self.jd.job_recovery_filepath == self.jd.filename
                and self.jd.job_recovery_selected_line != -1
        ):
            modified_job_gcode = prep_gcode(self.jd.job_recovery_gcode)
        else:
            self.jd.job_recovery_offset = 0
            modified_job_gcode = prep_gcode(self.jd.job_gcode)

        def mapGcodes(line):
            if self.m.stylus_router_choice == "router":
                culprits = ["M30", "M2"]
            else:
                culprits = ["M30", "M2", "AE"]
            if "S0" in line:
                line = line.replace("S0", "")
            if self.m.stylus_router_choice == "stylus":
                if "M3" in line:
                    line = ""
                if "M03" in line:
                    line = ""
            if line in culprits:
                line = ""
            return line

        self.jd.job_gcode_modified = map(mapGcodes, modified_job_gcode)
        try:
            self.m.s.run_job(self.jd.job_gcode_modified)
            Logger.info("Job started ok from go screen...")
        except:
            Logger.exception("Job start from go screen failed!")

    def return_to_app(self):
        if self.m.fw_can_operate_zUp_on_pause():  # precaution
            self.m.send_any_gcode_command("M56 P0")
        self.sm.current = self.cancel_to_screen
        self.m._grbl_soft_reset()

    ### GLOBAL ENTER/LEAVE ACTIONS

    def on_leave(self, *args):
        if self.loop_for_job_progress != None:
            self.loop_for_job_progress.cancel()
        if self.loop_for_feeds_and_speeds != None:
            self.loop_for_feeds_and_speeds.cancel()
        if self.listen_for_pauses != None:
            self.listen_for_pauses.cancel()
            self.listen_for_pauses = None
        if self.yp_widget.yp_settings_popup:
            self.yp_widget.yp_settings_popup.dismiss()


    ### SCREEN UPDATES
    def get_hms(self, seconds):
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        return h, m, s

    def poll_for_job_progress(self, dt):
        # % progress
        if len(self.jd.job_gcode_running) != 0:
            self.jd.percent_thru_job = int(
                round(
                    (self.m.s.g_count - min(0, self.jd.job_recovery_offset))
                    * 1.0
                    / (
                            len(self.jd.job_gcode_running)
                            - min(0, self.jd.job_recovery_offset)
                            + 4
                    )
                    * 1.0
                    * 100.0
                )
            )
            if self.jd.percent_thru_job > 100:
                self.jd.percent_thru_job = 100
            self.progress_percentage_label.text = str(self.jd.percent_thru_job) + " %"
        if (
                len(self.jd.job_gcode_running) != 0
                and self.m.s.g_count != 0
                and self.m.s.stream_start_time != 0
        ):
            if self.m.is_machine_paused:
                return
            self.total_runtime_seconds += 1
            hours, minutes, seconds = self.get_hms(self.total_runtime_seconds)
            if hours > 0:
                self.run_time_label.text = (
                        str(hours)
                        + " "
                        + self.l.get_str("hours")
                        + " "
                        + str(minutes)
                        + " "
                        + self.l.get_str("minutes")
                        + " "
                        + str(seconds)
                        + " "
                        + self.l.get_str("seconds")
                )
            elif minutes > 0:
                self.run_time_label.text = (
                        str(minutes)
                        + " "
                        + self.l.get_str("minutes")
                        + " "
                        + str(seconds)
                        + " "
                        + self.l.get_str("seconds")
                )
            else:
                self.run_time_label.text = (
                        str(seconds) + " " + self.l.get_str("seconds")
                )
        else:
            self.run_time_label.text = self.l.get_str("Waiting for job to be started")

    def poll_for_feeds_and_speeds(self, dt):
        # Spindle speed and feed rate
        self.speedOverride.update_speed_percentage_override_label()
        self.feedOverride.update_feed_rate_label()
        self.feedOverride.update_feed_percentage_override_label()
        if abs(self.speedOverride.speed_override_percentage - 100) > abs(
                self.spindle_speed_max_percentage - 100
        ):
            self.spindle_speed_max_percentage = (
                self.speedOverride.speed_override_percentage
            )
        if self.speedOverride.spindle_rpm.text > self.spindle_speed_max_absolute:
            self.spindle_speed_max_absolute = self.speedOverride.spindle_rpm.text
        if abs(self.feedOverride.feed_override_percentage - 100) > abs(
                self.feed_rate_max_percentage - 100
        ):
            self.feed_rate_max_percentage = self.feedOverride.feed_override_percentage
        if self.feedOverride.feed_absolute.text > self.feed_rate_max_absolute:
            self.feed_rate_max_absolute = self.feedOverride.feed_absolute.text

    # Called from serial_connection if change in state seen
    def update_overload_label(self, state):
        if state == 0:
            self.overload_status_label.text = (
                    "[color=4CA82B][b]" + str(state) + "[size=25px] %[/size][b][/color]"
            )
        elif state == 20:
            self.overload_status_label.text = (
                    "[color=E6AA19][b]" + str(state) + "[size=25px] %[/size][/b][/color]"
            )
        elif state == 40:
            self.overload_status_label.text = (
                    "[color=E27A1D][b]" + str(state) + "[size=25px] %[/size][/b][/color]"
            )
        elif state == 60:
            self.overload_status_label.text = (
                    "[color=DE5003][b]" + str(state) + "[size=25px] %[/size][/b][/color]"
            )
        elif state == 80:
            self.overload_status_label.text = (
                    "[color=DE5003][b]" + str(state) + "[size=25px] %[/size][/b][/color]"
            )
        elif state == 90:
            self.overload_status_label.text = (
                    "[color=C11C17][b]" + str(state) + "[size=25px] %[/size][/b][/color]"
            )
        elif state == 100:
            self.overload_status_label.text = (
                    "[color=C11C17][b]" + str(state) + "[size=25px] %[/size][/b][/color]"
            )
        else:
            Logger.warning("Overload state not recognised: " + str(state))

    def update_overload_peak(self, instance, state):
        if state > self.overload_peak:
            self.overload_peak = state
            Logger.info("New overload peak: " + str(self.overload_peak))

    def update_strings(self):
        self.feed_label.text = self.l.get_str("Feed") + "\n" + self.l.get_str("rate")
        self.spindle_label.text = (
                self.l.get_str("Spindle") + "\n" + self.l.get_str("speed")
        )
        self.job_time_label.text = self.l.get_str("Total job time") + ":"
        self.file_lines_streamed_label.text = (
                self.l.get_str("File lines streamed") + ":"
        )
        self.spindle_overload_label.text = (
                "[color=808080]"
                + self.l.get_str("Spindle overload").replace(" ", "\n", 1)
                + "[/color]"
        )
        self.update_font_size(self.feed_label)
        self.update_font_size(self.spindle_label)

    def update_font_size(self, value):
        text_length = self.l.get_text_length(value.text)
        if text_length < 20:
            value.font_size = str(16.0/800.0*Window.width) + "px"
        if text_length >= 20:
            value.font_size = str(12.0/800.0*Window.width) + "px"
        if text_length >= 25:
            value.font_size = str(11.0/800.0*Window.width) + "px"
