# -*- coding: utf-8 -*-
"""
@author Letty
Popup for user to choose YetiPilot profiles
"""
from functools import partial

from kivy.clock import Clock
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.spinner import Spinner
from kivy.uix.widget import Widget

from asmcnc.core_UI.job_go.widgets.widget_load_slider import LoadSliderWidget
from asmcnc.skavaUI import widget_speed_override
from asmcnc.comms.model_manager import ModelManagerSingleton

Builder.load_string(
    """

#:import Factory kivy.factory.Factory

<Options@SpinnerOption>

    background_normal: ''
    size: self.size
    color: color_provider.get_rgba("dark_grey")
    halign: 'center'
    markup: 'True'
    font_size: 0.0175*app.width
    background_color: color_provider.get_rgba("transparent")
    text_size : self.width, None
    canvas.before:
        Color:
            rgba: color_provider.get_rgba("light_grey")
        Rectangle:
            pos: self.pos
            size: self.size


<Choices@Spinner>
    option_cls: Factory.get("Options")
    background_normal: ''
    size: self.size
    color: color_provider.get_rgba("dark_grey")
    background_color: color_provider.get_rgba("transparent")
    font_size: 0.0175*app.width
    text_size : self.width, None
    halign: 'center'
    canvas.before:
        Color:
            rgba: hex('ccccccff')
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [dp(5), dp(5)]

<CloseButton@Button>:
    background_color: color_provider.get_rgba("transparent")
    background_normal: ''
    canvas.before:
        Color:
            rgba: hex('#2196f3ff')
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [dp(10), dp(10)]

<BigSpindleHealthCheckButton@Button>:
    size_hint: (None, None)
    size: [150.0/800*app.width,150.0/480*app.height]
    background_color: color_provider.get_rgba("transparent")
    background_normal: ''
    BoxLayout:
        padding: 0
        size: self.parent.size
        pos: self.parent.pos
        Image:
            source: "./asmcnc/core_UI/job_go/img/health_check_button_big.png"
            center_x: self.parent.center_x
            y: self.parent.y
            size: self.parent.width, self.parent.height
            allow_stretch: True



"""
)


class Choices(Spinner):
    pass


class CloseButton(Button):
    pass


class BigSpindleHealthCheckButton(Button):
    pass


class PopupYetiPilotSettings(Widget):
    def __init__(
        self,
        screen_manager,
        localization,
        machine,
        database,
        yetipilot,
        version=False,
        closing_func=None,
    ):
        self.sm = screen_manager
        self.l = localization
        self.m = machine
        self.db = database
        self.yp = yetipilot
        clock_speed_2 = None
        img_path = "./asmcnc/core_UI/job_go/img/"
        img_1_src = img_path + "yp_setting_1.png"
        img_2_src = img_path + "yp_setting_2.png"
        img_3_src = img_path + "yp_setting_3.png"
        pop_width = 530.0/800*Window.width
        pop_height = 430.0/480*Window.height
        title_height = 70.0/480*Window.height
        subtitle_height = 50.0/480*Window.height
        vertical_BL_height = pop_height - title_height
        radio_BL_height = 50.0/480*Window.height
        body_BL_height = 210.0/480*Window.height
        sum_of_middle_heights = subtitle_height + radio_BL_height + body_BL_height
        close_button_BL_height = vertical_BL_height - sum_of_middle_heights  # unused
        dropdowns_container_width = 330.0/800*Window.width
        dropdowns_width = dropdowns_container_width - (80.0/800*Window.width)
        dropdowns_cols_dict = {(0): dp(70.0/800*Window.width), (1): dp(dropdowns_width)}
        advice_container_width = pop_width - dropdowns_container_width - (30.0/800.0*Window.width)
        spindle_health_check_button_size = 150.0/800*Window.width
        spindle_health_check_button = BigSpindleHealthCheckButton()
        transparent = [0, 0, 0, 0]
        subtle_white = [249 / 255.0, 249 / 255.0, 249 / 255.0, 1.0]
        blue = [33 / 255.0, 150 / 255.0, 243 / 255.0, 1.0]
        dark_grey = [51 / 255.0, 51 / 255.0, 51 / 255.0, 1.0]
        # Title
        title_string = self.l.get_str("YetiPilot Settings")
        # Body boxlayout
        body_BL = BoxLayout(
            orientation="horizontal", size_hint_y=None, height=body_BL_height
        )
        left_BL = BoxLayout(orientation="vertical", padding=[10.0/800*Window.width, 10.0/480.0*Window.height])
        right_BL = BoxLayout(
            orientation="vertical", size_hint_x=None, width=advice_container_width
        )

        # Close button
        close_string = self.l.get_bold("Ok")
        close_button = CloseButton(
            text=close_string, markup=True, color=subtle_white, font_size=str(15.0/800.0*Window.width) + "sp"
        )
        close_button_BL = BoxLayout(orientation="horizontal", padding=[160.0/800*Window.width, 0])
        close_button_BL.add_widget(close_button)

        # BODY PRE CUT PROFILES ---------------------------

        def build_pre_cut_profiles():
            # Drop down menus (i.e. actual profile selection)
            left_BL_grid = GridLayout(cols=2, rows=3, cols_minimum=dropdowns_cols_dict)
            sizing_args = {'allow_stretch': True, 'keep_ratio': True, 'height': 100 * Window.height / 480}
            optn_img_1 = Image(source=img_1_src, **sizing_args)
            optn_img_2 = Image(source=img_2_src, **sizing_args)
            optn_img_3 = Image(source=img_3_src, **sizing_args)

            def update_step_down(step_down_range):
                try:
                    step_downs_msg_label.text = (
                        self.l.get_str(
                            "Recommended step downs based on these profile settings:"
                        )
                        + "\n[size=" + str(16.0/800*Window.width) + "sp][b]"
                        + str(step_down_range)
                        + "[/size][/b]"
                    )
                except:  # label doesn't exist yet
                    pass

            def get_profile():
                chosen_profile = self.yp.get_profile(
                    diameter_choice.text, tool_choice.text, material_choice.text
                )
                self.yp.use_profile(chosen_profile)
                update_step_down(self.yp.get_active_step_down())

            # User chooses material first
            # If next cutter diameter/type is not available, these selections then clear

            def select_material(spinner, val):
                profiles_filtered_by_material = self.yp.filter_available_profiles(
                    material_type=material_choice.text
                )
                diameter_choice.values = self.yp.get_sorted_cutter_diameters(
                    profiles_filtered_by_material
                )
                tool_choice.values = self.yp.get_sorted_cutter_types(
                    profiles_filtered_by_material
                )
                if diameter_choice.text not in diameter_choice.values:
                    diameter_choice.text = ""
                if tool_choice.text not in tool_choice.values:
                    tool_choice.text = ""
                get_profile()

            def select_diameter(spinner, val):
                profiles_filtered_by_material_and_cutter_diameter = (
                    self.yp.filter_available_profiles(
                        material_type=material_choice.text,
                        cutter_diameter=diameter_choice.text,
                    )
                )
                tool_choice.values = self.yp.get_sorted_cutter_types(
                    profiles_filtered_by_material_and_cutter_diameter
                )
                if tool_choice.text not in tool_choice.values:
                    tool_choice.text = ""
                get_profile()

            def select_tool(spinner, val):
                get_profile()

            material_values = self.yp.get_available_material_types()

            self.model_manager = ModelManagerSingleton()
            if not self.model_manager.is_machine_drywall():
                try:
                    material_values.remove("Drywall")
                except:
                    pass

            if (
                self.yp.get_active_material_type()
                and self.yp.get_active_cutter_diameter()
                and self.yp.get_active_cutter_type()
            ):
                profiles_filtered_by_material = self.yp.filter_available_profiles(
                    material_type=self.yp.get_active_material_type()
                )
                profiles_filtered_by_material_and_cutter_diameter = (
                    self.yp.filter_available_profiles(
                        material_type=self.yp.get_active_material_type(),
                        cutter_diameter=self.yp.get_active_cutter_diameter(),
                    )
                )
                diameter_values = self.yp.get_sorted_cutter_diameters(
                    profiles_filtered_by_material
                )
                tool_values = self.yp.get_sorted_cutter_types(
                    profiles_filtered_by_material_and_cutter_diameter
                )
            else:
                diameter_values = self.yp.get_available_cutter_diameters()
                tool_values = self.yp.get_available_cutter_types()
            material_choice = Choices(
                values=material_values, text=self.yp.get_active_material_type()
            )
            diameter_choice = Choices(
                values=diameter_values, text=self.yp.get_active_cutter_diameter()
            )
            tool_choice = Choices(
                values=tool_values, text=self.yp.get_active_cutter_type()
            )
            get_profile()
            diameter_choice.bind(text=select_diameter)
            tool_choice.bind(text=select_tool)
            material_choice.bind(text=select_material)
            diameter_BL = BoxLayout(orientation="vertical", padding=[5.0/800*Window.width, 2.5/480*Window.height])
            tool_BL = BoxLayout(orientation="vertical", padding=[5.0/800*Window.width, 2.5/480.0*Window.height])
            material_BL = BoxLayout(orientation="vertical", padding=[5.0/800*Window.width, 2.5/480.0*Window.height])
            diameter_label = Label(
                text=self.l.get_str("Tool diameter"),
                font_size = str(15.0/800*Window.width) + "sp",
                color=dark_grey,
                markup=True,
                halign="left",
                text_size=(dropdowns_width - (10.0/800*Window.width), None),
                size_hint_y=0.4,
            )
            tool_label = Label(
                text=self.l.get_str("Tool type"),
                font_size = str(15.0/800*Window.width) + "sp",
                color=dark_grey,
                markup=True,
                halign="left",
                text_size=(dropdowns_width - (10.0/800*Window.width), None),
                size_hint_y=0.4,
            )
            material_label = Label(
                text=self.l.get_str("Material"),
                font_size = str(15.0/800*Window.width) + "sp",
                color=dark_grey,
                markup=True,
                halign="left",
                text_size=(dropdowns_width - (10.0/800*Window.width), None),
                size_hint_y=0.4,
            )
            material_BL.add_widget(material_label)
            material_BL.add_widget(material_choice)
            diameter_BL.add_widget(diameter_label)
            diameter_BL.add_widget(diameter_choice)
            tool_BL.add_widget(tool_label)
            tool_BL.add_widget(tool_choice)
            left_BL_grid.add_widget(optn_img_3)
            left_BL_grid.add_widget(material_BL)
            left_BL_grid.add_widget(optn_img_1)
            left_BL_grid.add_widget(diameter_BL)
            left_BL_grid.add_widget(optn_img_2)
            left_BL_grid.add_widget(tool_BL)
            left_BL.add_widget(left_BL_grid)

            # Step down advice labels

            step_downs_msg_label = Label(
                text_size=(advice_container_width, body_BL_height * 0.6),
                markup=True,
                font_size=str(14.0/800*Window.width) + "sp",
                halign="left",
                valign="top",
                color=dark_grey,
                padding=[10.0/800*Window.width, (10.0/480*Window.height)],
                size_hint_y=0.6,
            )
            update_step_down(self.yp.get_active_step_down())

            # Specifically roboto is required here, to line up the text with the image consistently

            unexpected_results_string = "[font=Roboto]   (!)  [/font]" + self.l.get_str(
                "Exceeding this range may produce unexpected results."
            )
            unexpected_results_label = Label(
                text_size=(advice_container_width, body_BL_height * 0.4),
                markup=True,
                font_size=str(14.0/800*Window.width) + "sp",
                halign="left",
                valign="top",
                text=unexpected_results_string,
                color=dark_grey,
                padding=[10.0/800*Window.width, 0],
                size_hint_y=0.4,
            )
            right_BL.add_widget(step_downs_msg_label)
            right_BL.add_widget(unexpected_results_label)

            # END OF BODY PRE-CUT PROFILES --------------------------------

        # BODY CUSTOM PROFILES

        def start_spindle_health_check():
            self.yp.set_using_advanced_profile(True)
            if self.sm.has_screen("go"):
                self.sm.get_screen("go").run_spindle_health_check(
                    return_to_advanced_tab=True
                )

        def build_advanced_settings():
            self.yp.set_using_advanced_profile(True)
            target_ml_string = self.l.get_str("Target Spindle motor load")
            target_ml_label = Label(
                size_hint_y=0.1,
                text_size=(dropdowns_width - (10.0/800*Window.width), self.height),
                markup=True,
                font_size=str(17.0/800*Window.width) + "sp",
                halign="center",
                valign="middle",
                text=target_ml_string,
                color=dark_grey,
                padding=[0, 0],
            )
            load_slider_container = BoxLayout(size_hint_y=0.9)
            load_slider = LoadSliderWidget(screen_manager=self.sm, yetipilot=self.yp)
            load_slider_container.add_widget(load_slider)
            speedOverride = widget_speed_override.SpeedOverride(
                machine=self.m, screen_manager=self.sm, database=self.db
            )
            right_BL.add_widget(speedOverride)
            if self.m.has_spindle_health_check_passed():
                left_BL.add_widget(target_ml_label)
                left_BL.add_widget(load_slider_container)
            else:
                speedOverride.opacity = 0.6
                left_BL.padding = [
                    (dropdowns_container_width - spindle_health_check_button_size) / 2,
                    (body_BL_height - spindle_health_check_button_size) / 2,
                ]
                left_BL.add_widget(spindle_health_check_button)
            clock_speed_2 = Clock.schedule_interval(
                lambda dt: speedOverride.update_speed_percentage_override_label(), 0.1
            )

        def unschedule_clocks(*args):
            if clock_speed_2:
                Clock.unschedule(clock_speed_2)

        if version:
            build_pre_cut_profiles()
            subtitle_string = self.l.get_str(
                "Auto adjust feed rate to optimise Spindle motor load"
            )
        else:
            build_advanced_settings()
            subtitle_string = self.l.get_str(
                "Create your own custom Spindle motor load profile"
            )
        body_BL.add_widget(left_BL)
        body_BL.add_widget(right_BL)

        # Subtitle

        subtitle_label = Label(
            size_hint_y=None,
            height=subtitle_height,
            text_size=(pop_width, subtitle_height),
            markup=True,
            font_size=str(15.0/800*Window.width) + "sp",
            halign="center",
            valign="middle",
            text=subtitle_string,
            color=dark_grey,
            padding=[10.0/800*Window.width, 0],
        )

        # Profile radio buttons

        def switch_version(state, instance=None):
            if state:
                instance.active = True
                return
            self.yp.standard_profiles = not version
            unschedule_clocks()
            self.popup.dismiss()
            if self.sm.has_screen("go"):
                self.sm.get_screen(
                    "go"
                ).yp_widget.yp_settings_popup = PopupYetiPilotSettings(
                    self.sm,
                    self.l,
                    self.m,
                    self.db,
                    self.yp,
                    version=not version,
                    closing_func=closing_func,
                )

        radio_button_width = 30.0/800*Window.width
        pad_width = 30.0/800*Window.width
        text_width = (pop_width - pad_width) / 2 - radio_button_width
        radio_BL = BoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=radio_BL_height,
            padding=[pad_width, 0],
        )

        def make_option(version_text, version):
            label_radio_container = GridLayout(
                cols=2,
                rows=1,
                cols_minimum={(0): dp(radio_button_width), (1): dp(text_width)},
            )
            checkbox_func = partial(switch_version, version)
            label_radio_container.add_widget(
                CheckBox(
                    group="yp_settings",
                    color=blue,
                    on_press=checkbox_func,
                    active=version,
                )
            )
            label_radio_container.add_widget(
                Label(
                    text=version_text,
                    color=dark_grey,
                    markup=True,
                    font_size=str(15.0/800*Window.width) + "sp",
                    halign="left",
                    text_size=(text_width, None),
                )
            )
            radio_BL.add_widget(label_radio_container)

        make_option(self.l.get_str("Pre-set profiles"), version)
        make_option(self.l.get_str("Advanced profile"), not version)
        vertical_BL = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            height=vertical_BL_height,
            spacing=0,
        )
        vertical_BL.add_widget(subtitle_label)
        vertical_BL.add_widget(radio_BL)
        vertical_BL.add_widget(body_BL)
        vertical_BL.add_widget(close_button_BL)
        AL = AnchorLayout()
        AL.add_widget(vertical_BL)
        if version:
            floating_warning = FloatLayout()
            image_source_base = "./asmcnc/core_UI/job_go/img/micro_warning"
            image_source = image_source_base + ".png" if Window.width < 1280 else image_source_base + "_big.png"
            pos_y = -15.0/480.0*Window.height if Window.width < 1280 else -18.0/480.0*Window.height
            floating_warning.add_widget(
                Image(
                    source=image_source,
                    pos=(dropdowns_container_width - 76.0/800*Window.width, pos_y),
                )
            )
            AL.add_widget(floating_warning)

        # Create popup & format

        self.popup = Popup(
            title=title_string,
            title_color=subtle_white,
            title_size=str(20.0/800.0*Window.width) + "sp",
            title_align="center",
            content=AL,
            size_hint=(None, None),
            size=(pop_width, pop_height),
            auto_dismiss=False,
            padding=[0, 0],
        )
        self.popup.background = "./asmcnc/core_UI/job_go/img/yp_settings_bg.png"
        self.popup.separator_color = transparent
        self.popup.separator_height = "0dp"
        if closing_func:
            close_button.bind(on_press=closing_func)
        close_button.bind(on_press=unschedule_clocks)
        close_button.bind(on_press=self.popup.dismiss)
        spindle_health_check_button.bind(
            on_press=lambda instance: start_spindle_health_check()
        )
        spindle_health_check_button.bind(on_press=self.popup.dismiss)
        self.popup.open()

    def dismiss(self):
        self.popup.dismiss()
