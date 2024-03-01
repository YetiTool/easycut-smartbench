# -*- coding: utf-8 -*-
'''
@author Letty
Popups used by Z Head QC
'''

import kivy
import os
from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.properties import StringProperty  
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import  Button
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.uix.checkbox import CheckBox
from kivy.graphics import Color, Rectangle

class PopupTempPowerDiagnosticsInfo(Widget):

    def __init__(self, screen_manager, report_string):
        
        self.sm = screen_manager
        
        # img = Image(source="./asmcnc/apps/shapeCutter_app/img/info_icon.png", allow_stretch=False)
        label1 = Label(size_hint_y=1, text_size=(None, None), markup=True, halign='left', valign='middle', text=report_string, color=[0,0,0,1], padding=[10,10])

        ok_button = Button(text='[b]Ok[/b]', markup = True)
        ok_button.background_normal = ''
        ok_button.background_color = [76 / 255., 175 / 255., 80 / 255., 1.]

        text_layout = BoxLayout(orientation='horizontal', spacing=0, padding=0)
        text_layout.add_widget(label1)

        btn_layout = BoxLayout(orientation='horizontal', spacing=15, padding=[150,10,150,0], size_hint_y = 0.3)
        btn_layout.add_widget(ok_button)
        
        layout_plan = BoxLayout(orientation='vertical', spacing=10, padding=[10,10,10,10])
        # layout_plan.add_widget(img)
        layout_plan.add_widget(text_layout)
        layout_plan.add_widget(btn_layout)
        
        popup = Popup(title='Output',
                      title_color=[0, 0, 0, 1],
                      title_size = '20sp',
                      content=layout_plan,
                      size_hint=(None, None),
                      size=(700, 400),
                      auto_dismiss= False
                      )

        popup.background = './asmcnc/apps/shapeCutter_app/img/popup_background.png'
        popup.separator_color = [249 / 255., 206 / 255., 29 / 255., 1.]
        popup.separator_height = '4dp'

        ok_button.bind(on_press=popup.dismiss)

        popup.open()

class PopupSpindleDiagnosticsInfo(Widget):

    def __init__(self, screen_manager, test1, test2, test3, test4, test5):

        self.sm = screen_manager

        # img = Image(source="./asmcnc/apps/shapeCutter_app/img/info_icon.png", allow_stretch=False)
        label1 = Label(size_hint_y=1, text_size=(None, None), markup=True, halign='left', valign='middle', text=test1, color=[0,0,0,1], padding=[5,5])
        label2 = Label(size_hint_y=1, text_size=(None, None), markup=True, halign='left', valign='middle', text=test2, color=[0,0,0,1], padding=[5,5])
        label3 = Label(size_hint_y=1, text_size=(None, None), markup=True, halign='left', valign='middle', text=test3, color=[0,0,0,1], padding=[5,5])
        label4 = Label(size_hint_y=1, text_size=(None, None), markup=True, halign='left', valign='middle', text=test4, color=[0,0,0,1], padding=[5,5])
        label5 = Label(size_hint_y=1, text_size=(None, None), markup=True, halign='left', valign='middle', text=test5, color=[0,0,0,1], padding=[5,5])

        ok_button = Button(text='[b]Ok[/b]', markup = True)
        ok_button.background_normal = ''
        ok_button.background_color = [76 / 255., 175 / 255., 80 / 255., 1.]

        text_layout = BoxLayout(orientation='horizontal', spacing=0, padding=0)
        text_layout.add_widget(label1)
        text_layout.add_widget(label2)
        text_layout.add_widget(label3)
        text_layout.add_widget(label4)
        text_layout.add_widget(label5)

        btn_layout = BoxLayout(orientation='horizontal', spacing=15, padding=[150,10,150,0], size_hint_y = 0.4)
        btn_layout.add_widget(ok_button)

        layout_plan = BoxLayout(orientation='vertical', spacing=10, padding=[10,10,10,10])
        # layout_plan.add_widget(img)
        layout_plan.add_widget(text_layout)
        layout_plan.add_widget(btn_layout)

        popup = Popup(title='Output',
                      title_color=[0, 0, 0, 1],
                      title_size = '20sp',
                      content=layout_plan,
                      size_hint=(None, None),
                      size=(780, 460),
                      auto_dismiss= False
                      )

        popup.background = './asmcnc/apps/shapeCutter_app/img/popup_background.png'
        popup.separator_color = [249 / 255., 206 / 255., 29 / 255., 1.]
        popup.separator_height = '4dp'

        ok_button.bind(on_press=popup.dismiss)

        popup.open()

class PopupFWUpdateDiagnosticsInfo(Widget):

    def __init__(self, screen_manager, outcome, message):

        self.sm = screen_manager
        label1 = Label(size_hint_y=0.92, text_size=(None, None), markup=True, halign='left', valign='top', text=message, font_size = '11sp', color=[0,0,0,1])

        back_button = Button(text='[b]Ok[/b]', markup = True)
        back_button.background_normal = ''
        back_button.background_color = [230 / 255., 74 / 255., 25 / 255., 1.]

        text_layout = BoxLayout(orientation='horizontal', spacing=0, padding=0)
        text_layout.add_widget(label1)

        btn_layout = BoxLayout(orientation='horizontal', spacing=20, padding=[100,0,100,0], size_hint_y = 0.2)
        btn_layout.add_widget(back_button)

        layout_plan = BoxLayout(orientation='vertical', spacing=0, padding=[10,0,10,0])
        # layout_plan.add_widget(img)
        layout_plan.add_widget(text_layout)
        layout_plan.add_widget(btn_layout)

        popup = Popup(title=outcome,
                      title_color=[0, 0, 0, 1],
                      title_size = '20sp',
                      content=layout_plan,
                      size_hint=(None, None),
                      size=(780, 480),
                      auto_dismiss= False
                      )

        popup.background = './asmcnc/apps/shapeCutter_app/img/popup_background.png'
        popup.separator_color = [249 / 255., 206 / 255., 29 / 255., 1.]
        popup.separator_height = '4dp'

        back_button.bind(on_press=popup.dismiss)

        popup.open()