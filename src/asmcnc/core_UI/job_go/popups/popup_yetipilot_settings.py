# -*- coding: utf-8 -*-
'''
@author Letty
Popup for user to choose YetiPilot profiles
'''

from kivy.clock import Clock
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.spinner import Spinner
from kivy.uix.widget import Widget

from asmcnc.core_UI.job_go.widgets import widget_load_slider
from asmcnc.skavaUI import widget_speed_override


class PopupYetiPilotSettings(Widget):

    def __init__(self, screen_manager, localization, machine, database, yetipilot, version=False, **kwargs):
        super(PopupYetiPilotSettings, self).__init__(**kwargs)
        self.sm = screen_manager
        self.l = localization
        self.m = machine
        self.db = database
        self.yp = yetipilot

        self.yp.get_available_profiles()

        clock_speed_1 = None
        clock_speed_2 = None

        diameter_values = self.m.s.yp.get_available_cutter_diameters()
        tool_values = self.m.s.yp.get_available_cutter_types()
        material_values = self.m.s.yp.get_available_material_types()

        img_path = './asmcnc/core_UI/job_go/img/'
        sep_top_img_src = img_path + 'yp_settings_sep_top.png'
        img_1_src = img_path + 'yp_setting_1.png'
        img_2_src = img_path + 'yp_setting_2.png'
        img_3_src = img_path + 'yp_setting_3.png'

        pop_width = 530
        pop_height = 430

        box_width = 500

        title_height = 70
        subtitle_height = 50
        vertical_BL_height = pop_height - title_height
        radio_BL_height = 50
        body_BL_height = 210
        sum_of_middle_heights = subtitle_height + radio_BL_height + body_BL_height
        close_button_BL_height = vertical_BL_height - sum_of_middle_heights

        dropdowns_container_width = 350
        dropdowns_width = 270
        dropdowns_cols_dict = {0: dp(70), 1: dp(dropdowns_width)}
        advice_container_width = pop_width - dropdowns_container_width - 30

        transparent = [0, 0, 0, 0]
        subtle_white = [249 / 255., 249 / 255., 249 / 255., 1.]
        blue = [33 / 255., 150 / 255., 243 / 255., 1.]
        dark_grey = [51 / 255., 51 / 255., 51 / 255., 1.]

        def switch_version(*args):
            PopupYetiPilotSettings(self.sm, self.l, self.m, self.db, self.yp, version=not version)

        # Title
        title_string = self.l.get_str('YetiPilot Settings')

        # Body boxlayout
        body_BL = BoxLayout(orientation='horizontal',
                            size_hint_y=None,
                            height=body_BL_height
                            )

        left_BL = BoxLayout(orientation='vertical', padding=[10, 10])
        right_BL = BoxLayout(orientation="vertical", size_hint_x=None, width=advice_container_width)

        # Close button
        close_string = self.l.get_bold('Close')
        close_button = Button(text=close_string, markup=True, color=subtle_white)
        close_button.background_normal = ''
        close_button.background_color = blue
        close_button_BL = BoxLayout(orientation='horizontal',
                                    padding=[0, 0]
                                    # padding=[190,20,190,20]
                                    )
        close_button_BL.add_widget(close_button)

        # BODY PRE CUT PROFILES ---------------------------

        def build_pre_cut_profiles():

            # Drop down menus (i.e. actual profile selection)
            left_BL_grid = GridLayout(cols=2, rows=3, cols_minimum=dropdowns_cols_dict)

            optn_img_1 = Image(source=img_1_src)
            optn_img_2 = Image(source=img_2_src)
            optn_img_3 = Image(source=img_3_src)

            def get_profile():
                profile = yetipilot.get_profile(diameter_choice.text, tool_choice.text, material_choice.text)
                if profile is None:
                    return

                yetipilot.use_profile(profile)

            def select_diameter(spinner, val):
                get_profile()
                return val

            def select_tool(spinner, val):
                get_profile()
                return val

            def select_material(spinner, val):
                get_profile()
                return val

            diameter_choice = Spinner(values=diameter_values, text=self.yp.get_active_cutter_diameter())
            tool_choice = Spinner(values=tool_values, text=self.yp.get_active_cutter_type())
            material_choice = Spinner(values=material_values, text=self.yp.get_active_material_type())

            diameter_choice.bind(text=select_diameter)
            tool_choice.bind(text=select_tool)
            material_choice.bind(text=select_material)

            diameter_BL = BoxLayout(orientation='vertical', padding=[5, 0])
            tool_BL = BoxLayout(orientation='vertical', padding=[5, 0])
            material_BL = BoxLayout(orientation='vertical', padding=[5, 0])

            diameter_label = Label(text=self.l.get_str('Tool diameter'), color=dark_grey, markup=True, halign='left',
                                   text_size=(dropdowns_width - 10, None), size_hint_y=0.4)
            tool_label = Label(text=self.l.get_str('Tool type'), color=dark_grey, markup=True, halign='left',
                               text_size=(dropdowns_width - 10, None), size_hint_y=0.4)
            material_label = Label(text=self.l.get_str('Material'), color=dark_grey, markup=True, halign='left',
                                   text_size=(dropdowns_width - 10, None), size_hint_y=0.4)

            diameter_BL.add_widget(diameter_label)
            diameter_BL.add_widget(diameter_choice)
            tool_BL.add_widget(tool_label)
            tool_BL.add_widget(tool_choice)
            material_BL.add_widget(material_label)
            material_BL.add_widget(material_choice)

            left_BL_grid.add_widget(optn_img_1)
            left_BL_grid.add_widget(diameter_BL)
            left_BL_grid.add_widget(optn_img_2)
            left_BL_grid.add_widget(tool_BL)
            left_BL_grid.add_widget(optn_img_3)
            left_BL_grid.add_widget(material_BL)

            left_BL.add_widget(left_BL_grid)

            # Step down advice labels

            step_downs_msg_string = self.l.get_str("Recommended step downs based on these profile settings:") + \
                                    "\n[b]" + \
                                    "3-6mm" \
                                    + "[/b]"
            unexpected_results_string = "  (!)  " + self.l.get_str(
                "Exceeding this range may produce unexpected results.")

            step_downs_msg_label = Label(
                text_size=(advice_container_width, body_BL_height / 2),
                markup=True,
                font='Roboto',
                font_size='15sp',
                halign='left',
                valign='top',
                text=step_downs_msg_string,
                color=[0, 0, 0, 1],
                padding=[10, 10]
            )

            unexpected_results_label = Label(
                text_size=(advice_container_width, body_BL_height / 2),
                markup=True,
                font='Roboto',
                font_size='15sp',
                halign='left',
                valign='top',
                text=unexpected_results_string,
                color=[0, 0, 0, 1],
                padding=[10, 0]
            )

            right_BL.add_widget(step_downs_msg_label)
            right_BL.add_widget(unexpected_results_label)

        # END OF BODY PRE-CUT PROFILES --------------------------------

        # BODY CUSTOM PROFILES
        def build_advanced_settings():

            target_ml_string = self.l.get_str("Target Spindle motor load")
            target_ml_label = Label(size_hint_y=0.2,
                                    text_size=(dropdowns_width - 10, self.height),
                                    markup=True,
                                    font='Roboto',
                                    font_size='15sp',
                                    halign='center',
                                    valign='middle',
                                    text=target_ml_string,
                                    color=[0, 0, 0, 1],
                                    padding=[0, 0]
                                    )

            load_slider_container = BoxLayout(size_hint_y=0.8)
            load_slider_container.add_widget(widget_load_slider.LoadSliderWidget(screen_manager=self.sm, yetipilot=yetipilot))

            left_BL.add_widget(target_ml_label)
            left_BL.add_widget(load_slider_container)

            speedOverride = widget_speed_override.SpeedOverride(machine=self.m, screen_manager=self.sm,
                                                                database=self.db)
            right_BL.add_widget(speedOverride)

            clock_speed_1 = Clock.schedule_interval(lambda dt: speedOverride.update_spindle_speed_label(), 0.1)
            clock_speed_2 = Clock.schedule_interval(lambda dt: speedOverride.update_speed_percentage_override_label(),
                                                    0.1)

        def unschedule_clocks(*args):
            if clock_speed_1: Clock.unschedule(clock_speed_1)
            if clock_speed_2: Clock.unschedule(clock_speed_2)

        if version:
            build_pre_cut_profiles()
            subtitle_string = self.l.get_str('Auto adjust feed rate to optimise Spindle motor load')
        else:
            build_advanced_settings()
            subtitle_string = self.l.get_str('Create your own custom spindle motor load profile')

        body_BL.add_widget(left_BL)
        body_BL.add_widget(right_BL)

        # Subtitle
        subtitle_label = Label(size_hint_y=None,
                               height=subtitle_height,
                               text_size=(pop_width, subtitle_height),
                               markup=True,
                               font='Roboto',
                               font_size='15sp',
                               halign='center',
                               valign='middle',
                               text=subtitle_string,
                               color=[0, 0, 0, 1],
                               padding=[0, 0]
                               )

        # Profile radio buttons
        radio_BL = BoxLayout(orientation='horizontal',
                             size_hint_y=None,
                             height=radio_BL_height
                             )

        radio_btn = Button(background_normal='', background_color=[0, 1, 0, 1], text="Press me")
        radio_BL.add_widget(radio_btn)

        vertical_BL = BoxLayout(orientation='vertical',
                                size_hint_y=None,
                                height=vertical_BL_height,
                                spacing=0
                                )
        vertical_BL.add_widget(subtitle_label)
        vertical_BL.add_widget(radio_BL)
        vertical_BL.add_widget(body_BL)
        vertical_BL.add_widget(close_button_BL)

        # Create popup & format

        popup = Popup(title=title_string,
                      title_color=subtle_white,
                      title_font='Roboto-Bold',
                      title_size='20sp',
                      title_align='center',
                      content=vertical_BL,
                      size_hint=(None, None),
                      size=(pop_width, pop_height),
                      auto_dismiss=False,
                      padding=[0, 0]
                      )

        popup.background = './asmcnc/core_UI/job_go/img/yp_settings_bg.png'
        popup.separator_color = transparent
        popup.separator_height = '0dp'

        close_button.bind(on_press=unschedule_clocks)
        close_button.bind(on_press=popup.dismiss)
        radio_btn.bind(on_press=switch_version)
        radio_btn.bind(on_press=unschedule_clocks)
        radio_btn.bind(on_press=popup.dismiss)

        popup.open()
