# -*- coding: utf-8 -*-
'''
@author Letty
Popup for user to choose YetiPilot profiles
'''

import kivy
from kivy.graphics import *
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import  Button
from kivy.uix.image import Image
from kivy.metrics import dp
from kivy.uix.spinner import Spinner
from kivy.clock import Clock
from kivy.uix.checkbox import CheckBox

from functools import partial
import traceback

from asmcnc.core_UI.job_go.widgets.widget_load_slider import LoadSliderWidget
from asmcnc.skavaUI import widget_speed_override



Builder.load_string("""

#:import Factory kivy.factory.Factory

<Options@SpinnerOption>

    background_normal: ''
    size: self.size
    color: hex('#333333ff')
    halign: 'left'
    markup: 'True'
    font_size: 14
    background_color: 0,0,0,0
    canvas.before:
        Color:
            rgba: hex('#e5e5e5ff')
        Rectangle:
            pos: self.pos
            size: self.size


<Choices@Spinner>
    option_cls: Factory.get("Options")
    background_normal: ''
    size: self.size
    color: hex('#333333ff')
    background_color: 0,0,0,0
    font_size: 14
    canvas.before:
        Color:
            rgba: hex('ccccccff')
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [dp(5), dp(5)]

<CloseButton@Button>:
    background_color: 0,0,0,0
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
    size: [150,150]
    background_color: 0,0,0,0
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
            allow_stretch: False



""")

class Choices(Spinner):
    pass

class CloseButton(Button):
    pass

class BigSpindleHealthCheckButton(Button):
    pass

class PopupYetiPilotSettings(Widget):

    def __init__(self, screen_manager, localization, machine, database, yetipilot, version=False, closing_func=None):

        self.sm = screen_manager
        self.l = localization
        self.m = machine
        self.db = database
        self.yp = yetipilot

        clock_speed_1 = None
        clock_speed_2 = None

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
        sum_of_middle_heights = subtitle_height  + radio_BL_height + body_BL_height
        close_button_BL_height = vertical_BL_height - sum_of_middle_heights

        dropdowns_container_width = 330
        dropdowns_width = dropdowns_container_width - 80
        dropdowns_cols_dict = {0: dp(70), 1: dp(dropdowns_width)}
        advice_container_width = pop_width - dropdowns_container_width - 30

        spindle_health_check_button_size = 150
        spindle_health_check_button = BigSpindleHealthCheckButton()

        transparent = [0,0,0,0]
        subtle_white = [249 / 255., 249 / 255., 249 / 255., 1.]
        blue = [33 / 255., 150 / 255., 243 / 255., 1.]
        dark_grey = [51 / 255., 51 / 255., 51 / 255., 1.]

        # Title
        title_string = self.l.get_str('YetiPilot Settings')

        # Body boxlayout
        body_BL = BoxLayout(orientation='horizontal',
                            size_hint_y=None,
                            height=body_BL_height
        )

        left_BL = BoxLayout(orientation='vertical', padding=[10,10])
        right_BL = BoxLayout(orientation= "vertical", size_hint_x=None, width=advice_container_width)

        # Close button
        close_string = self.l.get_bold('Ok')
        close_button = CloseButton(text=close_string, markup = True, color=subtle_white, font_size='15sp')
        # close_button.background_normal = ''
        # close_button.background_color = blue
        close_button_BL = BoxLayout(orientation='horizontal',
                                  padding = [160,0]
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

            def update_step_down(step_down_range):
                try: 
                    step_downs_msg_label.text = \
                                    self.l.get_str("Recommended step downs based on these profile settings:") + \
                                    "\n[size=16sp][b]" + str(step_down_range) + "[/size][/b]"

                except: # label doesn't exist yet
                    pass

            def get_profile():
                chosen_profile = self.yp.get_profile(diameter_choice.text, tool_choice.text, material_choice.text)                
                self.yp.use_profile(chosen_profile)
                update_step_down(self.yp.get_active_step_down())

            # User chooses material first
            # If next cutter diameter/type is not available, these selections then clear
            def select_material(spinner, val):
                profiles_filtered_by_material = self.yp.filter_available_profiles(material_type=material_choice.text)
                diameter_choice.values = self.yp.get_sorted_cutter_diameters(profiles_filtered_by_material)
                tool_choice.values = self.yp.get_sorted_cutter_types(profiles_filtered_by_material)
                if diameter_choice.text not in diameter_choice.values: diameter_choice.text = ''
                if tool_choice.text not in tool_choice.values: tool_choice.text = ''
                get_profile()

            def select_diameter(spinner, val):
                profiles_filtered_by_material_and_cutter_diameter = self.yp.filter_available_profiles(material_type=material_choice.text, cutter_diameter=diameter_choice.text)
                tool_choice.values = self.yp.get_sorted_cutter_types(profiles_filtered_by_material_and_cutter_diameter)
                if tool_choice.text not in tool_choice.values: tool_choice.text = ''
                get_profile()

            def select_tool(spinner, val):
                get_profile()

            material_values = self.yp.get_available_material_types()

            if  self.yp.get_active_material_type() and \
                self.yp.get_active_cutter_diameter() and \
                self.yp.get_active_cutter_type(): 

                profiles_filtered_by_material = self.yp.filter_available_profiles(material_type=self.yp.get_active_material_type())
                profiles_filtered_by_material_and_cutter_diameter = self.yp.filter_available_profiles(material_type=self.yp.get_active_material_type(), cutter_diameter=self.yp.get_active_cutter_diameter())
                diameter_values = self.yp.get_sorted_cutter_diameters(profiles_filtered_by_material)
                tool_values = self.yp.get_sorted_cutter_types(profiles_filtered_by_material_and_cutter_diameter)

            else:
                diameter_values = self.yp.get_available_cutter_diameters()
                tool_values = self.yp.get_available_cutter_types()

            material_choice = Choices(values=material_values, text=self.yp.get_active_material_type())
            diameter_choice = Choices(values=diameter_values, text=self.yp.get_active_cutter_diameter())
            tool_choice = Choices(values=tool_values, text=self.yp.get_active_cutter_type())

            get_profile()

            diameter_choice.bind(text=select_diameter)
            tool_choice.bind(text=select_tool)
            material_choice.bind(text=select_material)
    
            diameter_BL = BoxLayout(orientation='vertical', padding=[5,2.5])
            tool_BL = BoxLayout(orientation='vertical', padding=[5,2.5])
            material_BL = BoxLayout(orientation='vertical', padding=[5,2.5])
    
            diameter_label = Label(text = self.l.get_str('Tool diameter'), color=dark_grey, markup=True, halign='left', text_size=(dropdowns_width-10, None), size_hint_y=0.4)
            tool_label = Label(text = self.l.get_str('Tool type'), color=dark_grey, markup=True, halign='left', text_size=(dropdowns_width-10, None), size_hint_y=0.4)
            material_label = Label(text = self.l.get_str('Material'), color=dark_grey, markup=True, halign='left', text_size=(dropdowns_width-10, None), size_hint_y=0.4)
    
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
                                    text_size=(advice_container_width, body_BL_height*0.6),
                                    markup=True,
                                    font= 'Roboto',
                                    font_size='14sp',
                                    halign='left', 
                                    valign='top',
                                    color=dark_grey,
                                    padding=[10,10],
                                    size_hint_y=0.6
                                    )

            update_step_down(self.yp.get_active_step_down())
    
            unexpected_results_string = "   (!)  " + self.l.get_str("Exceeding this range may produce unexpected results.")
            unexpected_results_label = Label(
                                    text_size=(advice_container_width, body_BL_height*0.4),
                                    markup=True,
                                    font= 'Roboto',
                                    font_size='14sp',
                                    halign='left',
                                    valign='top',
                                    text=unexpected_results_string,
                                    color=dark_grey,
                                    padding=[10,0],
                                    size_hint_y=0.4
                                    )
    
            right_BL.add_widget(step_downs_msg_label)
            right_BL.add_widget(unexpected_results_label)
    
    
        # END OF BODY PRE-CUT PROFILES --------------------------------


        # BODY CUSTOM PROFILES
        def start_spindle_health_check():
            if self.sm.has_screen('go'):
                self.sm.get_screen('go').run_spindle_health_check()

        def build_advanced_settings():
            self.yp.set_using_advanced_profile(True)

            target_ml_string = self.l.get_str("Target Spindle motor load")
            target_ml_label = Label( size_hint_y=0.1,
                                    text_size=(dropdowns_width-10, self.height),
                                    markup=True,
                                    font= 'Roboto',
                                    font_size='17sp',
                                    halign='center', 
                                    valign='middle', 
                                    text=target_ml_string,
                                    color=dark_grey,
                                    padding=[0,0]
                                    )
    
    
            load_slider_container = BoxLayout(size_hint_y=0.9)
            load_slider = LoadSliderWidget(screen_manager=self.sm, yetipilot=self.yp)
            load_slider_container.add_widget(load_slider)
    
            speedOverride = widget_speed_override.SpeedOverride(machine=self.m, screen_manager=self.sm, database=self.db)
            right_BL.add_widget(speedOverride)

            if self.m.has_spindle_health_check_passed():

                left_BL.add_widget(target_ml_label)
                left_BL.add_widget(load_slider_container)

            else:

                speedOverride.opacity = 0.6
                left_BL.padding = [
                                    (dropdowns_container_width - spindle_health_check_button_size)/2,
                                    (body_BL_height - spindle_health_check_button_size)/2
                                    ]
                
                left_BL.add_widget(spindle_health_check_button)
    
            clock_speed_1 = Clock.schedule_interval(lambda dt: speedOverride.update_spindle_speed_label(), 0.1)
            clock_speed_2 = Clock.schedule_interval(lambda dt: speedOverride.update_speed_percentage_override_label(), 0.1)

        def unschedule_clocks(*args):
            if clock_speed_1: Clock.unschedule(clock_speed_1)
            if clock_speed_2: Clock.unschedule(clock_speed_2)

        if version:
            build_pre_cut_profiles()
            subtitle_string = self.l.get_str('Auto adjust feed rate to optimise Spindle motor load')
        else: 
            build_advanced_settings()
            subtitle_string = self.l.get_str('Create your own custom Spindle motor load profile')

        body_BL.add_widget(left_BL)
        body_BL.add_widget(right_BL)

        # Subtitle
        subtitle_label = Label( size_hint_y=None,
                              height=subtitle_height,
                              text_size=(pop_width, subtitle_height),
                              markup=True,
                              font= 'Roboto',
                              font_size='15sp',
                              halign='center', 
                              valign='middle', 
                              text=subtitle_string,
                              color=dark_grey, 
                              padding=[10,0]
                              )

        # Profile radio buttons

        def switch_version(state, instance=None):
            if state: 
                instance.active=True
                return

            self.yp.standard_profiles = not version
            unschedule_clocks()
            popup.dismiss()
            PopupYetiPilotSettings(self.sm, self.l, self.m, self.db, self.yp, version= not version, closing_func=closing_func)

        radio_button_width = 30
        pad_width = 30      
        text_width = (pop_width - pad_width)/2 -radio_button_width

        radio_BL = BoxLayout( orientation='horizontal',
                            size_hint_y=None,
                            height=radio_BL_height,
                            padding=[pad_width, 0]
                          )
        def make_option(version_text, version):
            label_radio_container = GridLayout(cols=2, rows=1, cols_minimum={0: dp(radio_button_width), 1: dp(text_width)})
            checkbox_func =partial(switch_version, version)
            label_radio_container.add_widget(CheckBox(group="yp_settings", color=blue, on_press=checkbox_func, active=version))
            label_radio_container.add_widget(Label(text=version_text, color=dark_grey, markup=True, halign='left', text_size=(text_width, None)))
            radio_BL.add_widget(label_radio_container)

        make_option(self.l.get_str("Pre-set profiles"), version)
        make_option(self.l.get_str("Advanced profile"), not version)


        vertical_BL = BoxLayout(orientation='vertical',
                              size_hint_y=None,
                              height=vertical_BL_height,
                              spacing=0
        )

        vertical_BL.add_widget(subtitle_label)
        vertical_BL.add_widget(radio_BL)
        vertical_BL.add_widget(body_BL)
        vertical_BL.add_widget(close_button_BL)

        AL = AnchorLayout()
        AL.add_widget(vertical_BL)
        
        # Little warning icon
        if version: 
            floating_warning = FloatLayout()
            floating_warning.add_widget(Image(source="./asmcnc/core_UI/job_go/img/micro_warning.png", pos=(dropdowns_container_width-76, -15)))
            AL.add_widget(floating_warning)

        # Create popup & format

        popup = Popup(title=title_string,
                    title_color= subtle_white,
                    title_font= 'Roboto-Bold',
                    title_size = '20sp',
                    title_align = 'center',
                    content=AL,
                    size_hint=(None, None),
                    size=(pop_width, pop_height),
                    auto_dismiss= False,
                    padding=[0,0]
                    )

        popup.background = './asmcnc/core_UI/job_go/img/yp_settings_bg.png'
        popup.separator_color = transparent
        popup.separator_height = '0dp'

        if closing_func: close_button.bind(on_press=closing_func)
        close_button.bind(on_press=unschedule_clocks)
        close_button.bind(on_press=popup.dismiss)

        # if spindle_health_check_button: 
        spindle_health_check_button.bind(on_press=lambda instance: start_spindle_health_check())
        spindle_health_check_button.bind(on_press=popup.dismiss)

        popup.open()


