'''
@author Letty
Created for info buttons in the shapecutter app
'''

import kivy
from asmcnc.comms.logging_system.logging_system import Logger

from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.properties import StringProperty  
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.checkbox import CheckBox
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import  Button
from kivy.uix.image import Image


class PopupInputError(Widget):

    def __init__(self, screen_manager, error_message):
        
        self.shapecutter_sm = screen_manager
        
        description = error_message
        
        img = Image(source="./asmcnc/apps/shapeCutter_app/img/error_icon.png", allow_stretch=False)
        label = Label(size_hint_y=1, text_size=(360, None), halign='left', valign='middle', text=description, color=[0,0,0,1], padding=[20,20])
        
        ok_button = Button(text='[b]Ok[/b]', markup = True)
        ok_button.background_normal = ''
        ok_button.background_color = [230 / 255., 74 / 255., 25 / 255., 1.]
        
        btn_layout = BoxLayout(orientation='horizontal', spacing=15, padding=[50,25,50,0])
        btn_layout.add_widget(ok_button)
        
        layout_plan = BoxLayout(orientation='vertical', spacing=10, padding=[50,20,50,20])
        layout_plan.add_widget(img)
        layout_plan.add_widget(label)
        layout_plan.add_widget(btn_layout)
        
        popup = Popup(title='Warning!',
                      title_color=[0, 0, 0, 1],
                      title_size = '20sp',
                      content=layout_plan,
                      size_hint=(None, None),
                      size=(400, 380),
                      auto_dismiss= False
                      )
        
        popup.separator_color = [230 / 255., 74 / 255., 25 / 255., 1.]
        popup.separator_height = '4dp'
        popup.background = './asmcnc/apps/shapeCutter_app/img/popup_background.png'
        
        ok_button.bind(on_press=popup.dismiss)

        popup.open()

class PopupDatum(Widget):

    def __init__(self, screen_manager, machine, xy, warning_message):
        
      self.sm = screen_manager
      self.m = machine
      
      description = warning_message
      chk_message = "            Use laser crosshair?"

      def on_checkbox_active(checkbox, value):
        if value: 
          self.sm.get_screen('home').default_datum_choice = 'laser'
        else:
          self.sm.get_screen('home').default_datum_choice = 'spindle'

      def set_datum(*args):

          if (self.sm.get_screen('home').default_datum_choice == 'laser' and self.m.is_laser_enabled == True):
            Logger.info("setting datum with laser")

            if xy == 'X':
                self.m.set_x_datum_with_laser() #testing!!
            elif xy == 'Y':
                self.m.set_y_datum_with_laser()
                
            elif xy == 'XY':
                self.m.set_workzone_to_pos_xy_with_laser()

          else:
            Logger.info("setting datum without laser")

            if xy == 'X':
                self.m.set_x_datum()
            elif xy == 'Y':
                self.m.set_y_datum()
            elif xy == 'XY':
                self.m.set_workzone_to_pos_xy()


      def set_checkbox_default():
        if self.sm.get_screen('home').default_datum_choice == 'spindle':
          return False
        elif self.sm.get_screen('home').default_datum_choice == 'laser':
          return True

      img = Image(source="./asmcnc/apps/shapeCutter_app/img/error_icon.png", allow_stretch=False)
      label = Label(size_hint_y=1, text_size=(360, None), halign='center', valign='middle', text=description, color=[0,0,0,1], padding=[40,20], markup = True)
      

      ok_button = Button(text='[b]Yes[/b]', markup = True)
      ok_button.background_normal = ''
      ok_button.background_color = [76 / 255., 175 / 255., 80 / 255., 1.]
      back_button = Button(text='[b]No[/b]', markup = True)
      back_button.background_normal = ''
      back_button.background_color = [230 / 255., 74 / 255., 25 / 255., 1.]

     
      btn_layout = BoxLayout(orientation='horizontal', spacing=10, padding=[0,0,0,0])
      btn_layout.add_widget(back_button)
      btn_layout.add_widget(ok_button)


      if self.m.is_laser_enabled == True:
        chk_label = Label(size_hint_y=1, text_size=(360, None), halign='center', valign='middle', text=chk_message, color=[0,0,0,1], padding=[40,20], markup = True)
        checkbox = CheckBox(background_checkbox_normal="./asmcnc/skavaUI/img/checkbox_inactive.png", active=set_checkbox_default())
        chk_layout = BoxLayout(orientation='horizontal', spacing=10, padding=[0,0,0,0])
        chk_layout.add_widget(chk_label)
        chk_layout.add_widget(checkbox)

      layout_plan = BoxLayout(orientation='vertical', spacing=10, padding=[40,20,40,20])
      layout_plan.add_widget(img)
      layout_plan.add_widget(label)
      if self.m.is_laser_enabled == True: layout_plan.add_widget(chk_layout)
      layout_plan.add_widget(btn_layout)
      
      popup = Popup(title='Warning!',
                    title_color=[0, 0, 0, 1],
                    title_size = '20sp',
                    content=layout_plan,
                    size_hint=(None, None),
                    size=(300, 350),
                    auto_dismiss= False
                    )
      
      popup.separator_color = [230 / 255., 74 / 255., 25 / 255., 1.]
      popup.separator_height = '4dp'
      popup.background = './asmcnc/apps/shapeCutter_app/img/popup_background.png'
      
      if self.m.is_laser_enabled == True: checkbox.bind(active=on_checkbox_active)

      ok_button.bind(on_press=popup.dismiss)
      ok_button.bind(on_press=set_datum)
      back_button.bind(on_press=popup.dismiss)

      popup.open()

class PopupBoundary(Widget):

    def __init__(self, screen_manager, error_message):
        
        self.shapecutter_sm = screen_manager
        
        description = error_message
        
        img = Image(source="./asmcnc/apps/shapeCutter_app/img/error_icon.png", allow_stretch=False)
        label = Label(size_hint_y=1, text_size=(360, None), halign='left', valign='middle', text=description, color=[0,0,0,1], padding=[0,0])
        
        ok_button = Button(text='[b]Ok[/b]', markup = True)
        ok_button.background_normal = ''
        ok_button.background_color = [230 / 255., 74 / 255., 25 / 255., 1.]
        
        btn_layout = BoxLayout(orientation='horizontal', spacing=15, padding=[70,25,70,0])
        btn_layout.add_widget(ok_button)
        
        layout_plan = BoxLayout(orientation='vertical', spacing=10, padding=[0,0,0,0])
        layout_plan.add_widget(img)
        layout_plan.add_widget(label)
        layout_plan.add_widget(btn_layout)
        
        popup = Popup(title='Warning!',
                      title_color=[0, 0, 0, 1],
                      title_size = '20sp',
                      content=layout_plan,
                      size_hint=(None, None),
                      size=(600, 420),
                      auto_dismiss= False
                      )
        
        popup.separator_color = [230 / 255., 74 / 255., 25 / 255., 1.]
        popup.separator_height = '4dp'
        popup.background = './asmcnc/apps/shapeCutter_app/img/popup_background.png'
        
        ok_button.bind(on_press=popup.dismiss)

        popup.open()
