# -*- coding: utf-8 -*-
'''
@author Letty
Warning pop-up for data and consent app
'''

import kivy
import os
from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.properties import StringProperty  # @UnresolvedImport
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import  Button
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.uix.checkbox import CheckBox
from kivy.graphics import Color, Rectangle

class PopupDataAndWiFiDisableWarning(Widget):   
    def __init__(self, consent_manager, localization):

    	self.c = consent_manager
        self.l = localization
        
        description = (
        	"[b]" + "Are you sure?" + "[/b]" + \
        	"\n\n" + \
			"Declining the data collection policy will cause the Console Wi-Fi to be disabled." + \
			"\n\n" + \
			"You can change your data preferences in the System Tools app at any time."
			)

        title_string = self.l.get_str('Warning!')
        # ok_string = self.l.get_bold('Ok')
        ok_string = "[b]Yes, I'm sure[/b]"
        back_string = "[b]No, [/b]" + self.l.get_bold('Go Back')
        
        img = Image(source="./asmcnc/apps/shapeCutter_app/img/error_icon.png", allow_stretch=False)
        label = Label(size_hint_y=1, text_size=(360, None), halign='center', valign='middle', text=description, color=[0,0,0,1], padding=[0,0], markup = True)
        
        ok_button = Button(text=ok_string, markup = True)
        ok_button.background_normal = ''
        ok_button.background_color = [230 / 255., 74 / 255., 25 / 255., 1.]
       	back_button = Button(text=back_string, markup = True)
        back_button.background_normal = ''
        back_button.background_color = [230 / 255., 74 / 255., 25 / 255., 1.]
       
        btn_layout = BoxLayout(orientation='horizontal', spacing=10, padding=[20,0,20,0])
        btn_layout.add_widget(back_button)
        btn_layout.add_widget(ok_button)
        
        layout_plan = BoxLayout(orientation='vertical', spacing=10, padding=[40,20,40,20])
        layout_plan.add_widget(img)
        layout_plan.add_widget(label)
        layout_plan.add_widget(btn_layout)
        
        popup = Popup(title=title_string,
                      title_color=[0, 0, 0, 1],
                      title_font= 'Roboto-Bold',
                      title_size = '20sp',
                      content=layout_plan,
                      size_hint=(None, None),
                      size=(500, 400),
                      auto_dismiss= False
                      )
        
        popup.separator_color = [230 / 255., 74 / 255., 25 / 255., 1.]
        popup.separator_height = '4dp'
        popup.background = './asmcnc/apps/shapeCutter_app/img/popup_background.png'
        
        ok_button.bind(on_press=popup.dismiss)
        ok_button.bind(on_press=popup.c.decline_terms_and_disable_wifi)
        back_button.bind(on_press=popup.dismiss)

        popup.open()