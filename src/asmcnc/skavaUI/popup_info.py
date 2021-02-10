# -*- coding: utf-8 -*-
'''
@author Letty
Info pop-up
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

class PopupWelcome(Widget):

    def __init__(self, screen_manager, machine, localization, description):
        
        self.sm = screen_manager
        self.m = machine
        self.l = localization

        title_string = self.l.get_str('Welcome to SmartBench')
        ok_string = self.l.get_bold('Ok')
        remind_string = self.l.get_bold('Remind me later')
        
        def set_trigger_to_false(*args):
          self.m.write_set_up_options(False)
          self.sm.get_screen('lobby').carousel.load_next(mode='next')

        def set_trigger_to_true(*args):
          self.m.write_set_up_options(True)

        img = Image(source="./asmcnc/apps/shapeCutter_app/img/info_icon.png", allow_stretch=False)
        label = Label(size_hint_y=2, text_size=(340, None), markup=True, halign='center', valign='middle', text=description, color=[0,0,0,1], padding=[0,0])
        
        ok_button = Button(text=ok_string, markup = True)
        ok_button.background_normal = ''
        ok_button.background_color = [76 / 255., 175 / 255., 80 / 255., 1.]

        remind_me_button = Button(text=remind_string, markup = True)
        remind_me_button.background_normal = ''
        remind_me_button.background_color = [230 / 255., 74 / 255., 25 / 255., 1.]

        btn_layout = BoxLayout(orientation='horizontal', spacing=15, padding=[20,10,20,0])
        btn_layout.add_widget(remind_me_button)       
        btn_layout.add_widget(ok_button)
        
        layout_plan = BoxLayout(orientation='vertical', spacing=10, padding=[10,10,10,10])
        layout_plan.add_widget(img)
        layout_plan.add_widget(label)
        layout_plan.add_widget(btn_layout)
        
        popup = Popup(title=title_string,
#                       title_color=[0.141, 0.596, 0.957, 1],
                      title_color=[0, 0, 0, 1],
                      title_font= 'Roboto-Bold',
                      title_size = '20sp',
                      content=layout_plan,
                      size_hint=(None, None),
                      size=(500, 400),
                      auto_dismiss= False
                      )

        popup.background = './asmcnc/apps/shapeCutter_app/img/popup_background.png'
        popup.separator_color = [249 / 255., 206 / 255., 29 / 255., 1.]
        popup.separator_height = '4dp'

        ok_button.bind(on_press=popup.dismiss)
        ok_button.bind(on_press=set_trigger_to_false)
        remind_me_button.bind(on_press=popup.dismiss)
        remind_me_button.bind(on_press=set_trigger_to_true)

        popup.open()
        
class PopupDatum(Widget):

    def __init__(self, screen_manager, machine, localization, xy, warning_message):
        
      self.sm = screen_manager
      self.m = machine
      self.l = localization
      
      description = warning_message
      title_string = self.l.get_str('Warning!')
      yes_string = self.l.get_bold('Yes')
      no_string = self.l.get_bold('No')
      # chk_message = "         Use laser datum?"
      chk_message = self.l.get_str('Use laser datum?')

      def on_checkbox_active(checkbox, value):
        if value: 
          self.sm.get_screen('home').default_datum_choice = 'laser'
        else:
          self.sm.get_screen('home').default_datum_choice = 'spindle'

      def set_datum(*args):

          if (self.sm.get_screen('home').default_datum_choice == 'laser' and self.m.is_laser_enabled == True):

            if xy == 'X':
                self.m.set_x_datum_with_laser() #testing!!
            elif xy == 'Y':
                self.m.set_y_datum_with_laser()
                
            elif xy == 'XY':
                self.m.set_workzone_to_pos_xy_with_laser()

          else:

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
      

      ok_button = Button(text=yes_string, markup = True)
      ok_button.background_normal = ''
      ok_button.background_color = [76 / 255., 175 / 255., 80 / 255., 1.]
      back_button = Button(text=no_string, markup = True)
      back_button.background_normal = ''
      back_button.background_color = [230 / 255., 74 / 255., 25 / 255., 1.]

     
      btn_layout = BoxLayout(orientation='horizontal', spacing=10, padding=[0,0,0,0])
      btn_layout.add_widget(back_button)
      btn_layout.add_widget(ok_button)


      if self.m.is_laser_enabled == True:
        chk_label = Label(size_hint_y=1, size_hint_x=0.8, halign='center', valign='middle', text=chk_message, color=[0,0,0,1], padding=[0,20], markup = True)
        checkbox = CheckBox(size_hint_x=0.2, background_checkbox_normal="./asmcnc/skavaUI/img/checkbox_inactive.png", active=set_checkbox_default())
        chk_layout = BoxLayout(orientation='horizontal', spacing=0, padding=[5,0,5,0])
        chk_layout.add_widget(chk_label)
        chk_layout.add_widget(checkbox)

      layout_plan = BoxLayout(orientation='vertical', spacing=10, padding=[20,20,20,20])
      layout_plan.add_widget(img)
      layout_plan.add_widget(label)
      if self.m.is_laser_enabled == True: layout_plan.add_widget(chk_layout)
      layout_plan.add_widget(btn_layout)
      
      popup = Popup(title=title_string,
                    title_color=[0, 0, 0, 1],
                    title_font= 'Roboto-Bold',
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


class PopupPark(Widget):

    def __init__(self, screen_manager, machine, localization, warning_message):
        
      self.sm = screen_manager
      self.m = machine
      self.l = localization
      
      description = warning_message
      title_string = self.l.get_str('Warning!')
      yes_string = self.l.get_bold('Yes')
      no_string = self.l.get_bold('No')


      def set_park(*args):
        self.m.set_standby_to_pos()
        self.m.get_grbl_status()

      img = Image(source="./asmcnc/apps/shapeCutter_app/img/error_icon.png", allow_stretch=False)
      label = Label(size_hint_y=1, text_size=(360, None), halign='center', valign='middle', text=description, color=[0,0,0,1], padding=[40,20], markup = True)
      

      ok_button = Button(text=yes_string, markup = True)
      ok_button.background_normal = ''
      ok_button.background_color = [76 / 255., 175 / 255., 80 / 255., 1.]
      back_button = Button(text=no_string, markup = True)
      back_button.background_normal = ''
      back_button.background_color = [230 / 255., 74 / 255., 25 / 255., 1.]

     
      btn_layout = BoxLayout(orientation='horizontal', spacing=10, padding=[0,0,0,0])
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
                    size=(300, 350),
                    auto_dismiss= False
                    )
      
      popup.separator_color = [230 / 255., 74 / 255., 25 / 255., 1.]
      popup.separator_height = '4dp'
      popup.background = './asmcnc/apps/shapeCutter_app/img/popup_background.png'

      ok_button.bind(on_press=popup.dismiss)
      ok_button.bind(on_press=set_park)
      back_button.bind(on_press=popup.dismiss)

      popup.open()

class PopupStop(Widget):


    def __init__(self, machine, screen_manager):
        
      self.m = machine
      self.m.soft_stop()

      self.sm = screen_manager
        
      def machine_reset(*args):
          self.m.stop_from_soft_stop_cancel()


      def machine_resume(*args):
          self.m.resume_from_a_soft_door()
        
      stop_description = "Is everything OK? You can resume the job, or cancel it completely."
      
      img = Image(source="./asmcnc/apps/shapeCutter_app/img/error_icon.png", allow_stretch=False)
      label = Label(size_hint_y=2, text_size=(360, None), halign='center', valign='middle', text=stop_description, color=[0,0,0,1], padding=[0,0], markup = True)
      
      resume_button = Button(text='[b]Resume[/b]', markup = True)
      resume_button.background_normal = ''
      resume_button.background_color = [76 / 255., 175 / 255., 80 / 255., 1.]
      cancel_button = Button(text='[b]Cancel[/b]', markup = True)
      cancel_button.background_normal = ''
      cancel_button.background_color = [230 / 255., 74 / 255., 25 / 255., 1.]

     
      btn_layout = BoxLayout(orientation='horizontal', spacing=15, padding=[0,5,0,0], size_hint_y=2) 
      btn_layout.add_widget(cancel_button)
      btn_layout.add_widget(resume_button)
      
      layout_plan = BoxLayout(orientation='vertical', spacing=5, padding=[30,20,30,0])
      layout_plan.add_widget(img)
      layout_plan.add_widget(label)
      layout_plan.add_widget(btn_layout)
      
      popup = Popup(title='Warning!',
                    title_color=[0, 0, 0, 1],
                    title_font= 'Roboto-Bold',
                    title_size = '20sp',
                    content=layout_plan,
                    size_hint=(None, None),
                    size=(400, 300),
                    auto_dismiss= False
                    )
      
      popup.separator_color = [230 / 255., 74 / 255., 25 / 255., 1.]
      popup.separator_height = '4dp'
      popup.background = './asmcnc/apps/shapeCutter_app/img/popup_background.png'
      
      cancel_button.bind(on_press=machine_reset)
      cancel_button.bind(on_press=popup.dismiss)
      resume_button.bind(on_press=machine_resume)
      resume_button.bind(on_press=popup.dismiss)
      
      popup.open()

class PopupUSBInfo(Widget):

    def __init__(self, screen_manager, localization, safe_to_remove):
        
        self.sm = screen_manager
        self.l = localization

        title_string = self.l.get_str('Warning!')
        ok_string = self.l.get_bold('Ok')

        ok_button = Button(text=ok_string, markup = True)
        ok_button.background_normal = ''
        
        if safe_to_remove == 'mounted':
            
            description = (
              self.l.get_str("USB stick found!") + "\n\n" + \
              self.l.get_str("Please do not remove your USB stick until it is safe to do so.")
              )

            ok_button.background_color = [230 / 255., 74 / 255., 25 / 255., 1.]
        
        elif safe_to_remove == False:

            description = (
              self.l.get_str("Do not remove your USB stick yet.") + "\n\n" + \
              self.l.get_str("Please wait") + "..."
              )

            ok_button.background_color = [230 / 255., 74 / 255., 25 / 255., 1.]

        elif safe_to_remove == True:
            description = self.l.get_str('It is now safe to remove your USB stick.')
            ok_button.background_color = [76 / 255., 175 / 255., 80 / 255., 1.]

        img = Image(source="./asmcnc/apps/shapeCutter_app/img/error_icon.png", allow_stretch=False)
        label = Label(size_hint_y=1, text_size=(260, None), halign='center', valign='middle', text=description, color=[0,0,0,1], padding=[40,20], markup = True)

        btn_layout = BoxLayout(orientation='horizontal', spacing=10, padding=[0,0,0,0])
        btn_layout.add_widget(ok_button)
        
        layout_plan = BoxLayout(orientation='vertical', spacing=10, padding=[40,20,40,20])
        layout_plan.add_widget(img)
        layout_plan.add_widget(label)
        layout_plan.add_widget(btn_layout)
        
        self.popup = Popup(title=title_string,
                      title_color=[0, 0, 0, 1],
                      title_font= 'Roboto-Bold',
                      title_size = '20sp',
                      content=layout_plan,
                      size_hint=(None, None),
                      size=(300, 300),
                      auto_dismiss= False
                      )
        
        self.popup.separator_color = [230 / 255., 74 / 255., 25 / 255., 1.]
        self.popup.separator_height = '4dp'
        self.popup.background = './asmcnc/apps/shapeCutter_app/img/popup_background.png'
        
        ok_button.bind(on_press=self.popup.dismiss)    

        self.popup.open()  

class PopupInfo(Widget):

    def __init__(self, screen_manager, localization, popup_width, description):
        
        self.sm = screen_manager
        self.l = localization
        label_width = popup_width - 40
        
        title_string = self.l.get_str('Information')
        ok_string = self.l.get_bold('Ok')

        img = Image(source="./asmcnc/apps/shapeCutter_app/img/info_icon.png", allow_stretch=False)
        label = Label(size_hint_y=2, text_size=(label_width, None), markup=True, halign='left', valign='middle', text=description, color=[0,0,0,1], padding=[10,10])
        
        ok_button = Button(text=ok_string, markup = True)
        ok_button.background_normal = ''
        ok_button.background_color = [76 / 255., 175 / 255., 80 / 255., 1.]
        
        btn_layout = BoxLayout(orientation='horizontal', spacing=15, padding=[150,20,150,0])
        btn_layout.add_widget(ok_button)
        
        layout_plan = BoxLayout(orientation='vertical', spacing=10, padding=[10,10,10,10])
        layout_plan.add_widget(img)
        layout_plan.add_widget(label)
        layout_plan.add_widget(btn_layout)
        
        popup = Popup(title=title_string,
                      title_color=[0, 0, 0, 1],
                      title_font= 'Roboto-Bold',
                      title_size = '20sp',
                      content=layout_plan,
                      size_hint=(None, None),
                      size=(popup_width, 440),
                      auto_dismiss= False
                      )

        popup.background = './asmcnc/apps/shapeCutter_app/img/popup_background.png'
        popup.separator_color = [249 / 255., 206 / 255., 29 / 255., 1.]
        popup.separator_height = '4dp'

        ok_button.bind(on_press=popup.dismiss)

        popup.open()

class PopupMiniInfo(Widget):

    def __init__(self, screen_manager, description):
        
        self.sm = screen_manager
        
        img = Image(source="./asmcnc/apps/shapeCutter_app/img/info_icon.png", allow_stretch=False)
        label = Label(size_hint_y=1, text_size=(360, None), halign='center', valign='middle', text=description, color=[0,0,0,1], padding=[40,20], markup = True)
        
        ok_button = Button(text='[b]Ok[/b]', markup = True)
        ok_button.background_normal = ''
        ok_button.background_color = [76 / 255., 175 / 255., 80 / 255., 1.]

        
        btn_layout = BoxLayout(orientation='horizontal', spacing=10, padding=[0,0,0,0])
        btn_layout.add_widget(ok_button)
        
        layout_plan = BoxLayout(orientation='vertical', spacing=10, padding=[40,20,40,20])
        layout_plan.add_widget(img)
        layout_plan.add_widget(label)
        layout_plan.add_widget(btn_layout)
        
        popup = Popup(title='Information',
                      title_color=[0, 0, 0, 1],
                      title_font= 'Roboto-Bold',
                      title_size = '20sp',
                      content=layout_plan,
                      size_hint=(None, None),
                      size=(300, 300),
                      auto_dismiss= False
                      )

        popup.background = './asmcnc/apps/shapeCutter_app/img/popup_background.png'
        popup.separator_color = [249 / 255., 206 / 255., 29 / 255., 1.]
        popup.separator_height = '4dp'

        ok_button.bind(on_press=popup.dismiss)

        popup.open()


class PopupSoftwareUpdateSuccess(Widget):
    def __init__(self, screen_manager, message):
        
        self.sm = screen_manager
        
        description = "Software update was successful.\n\n Update message: " + \
                    message + \
                    "\nPlease do not restart your machine until you are prompted to do so."

        def reboot(*args):
            self.sm.current = 'rebooting'
                    
        img = Image(source="./asmcnc/apps/shapeCutter_app/img/info_icon.png", allow_stretch=False)
        label = Label(size_hint_y=1, text_size=(360, None), halign='center', valign='middle', text=description, color=[0,0,0,1], padding=[40,10], markup = True)
   
        ok_button = Button(text='[b]Ok[/b]', markup = True)
        ok_button.background_normal = ''
        ok_button.background_color = [76 / 255., 175 / 255., 80 / 255., 1.]
      
        btn_layout = BoxLayout(orientation='horizontal', spacing=10, padding=[0,0,0,0])
        btn_layout.add_widget(ok_button)
        
        layout_plan = BoxLayout(orientation='vertical', spacing=10, padding=[40,20,40,20])
        layout_plan.add_widget(img)
        layout_plan.add_widget(label)
        layout_plan.add_widget(btn_layout)
        
        popup = Popup(title='Update Successful!',
                      title_color=[0, 0, 0, 1],
                      title_font= 'Roboto-Bold',
                      title_size = '20sp',
                      content=layout_plan,
                      size_hint=(None, None),
                      size=(500, 400),
                      auto_dismiss= False
                      )
        
        popup.separator_color = [249 / 255., 206 / 255., 29 / 255., 1.]
        popup.separator_height = '4dp'
        popup.background = './asmcnc/apps/shapeCutter_app/img/popup_background.png'
        
        ok_button.bind(on_press=popup.dismiss)
        ok_button.bind(on_press=reboot)
        
        popup.open()
        
        Clock.schedule_once(reboot, 6)
    
class PopupSoftwareRepair(Widget):   
    def __init__(self, screen_manager, settings_manager, warning_message):
        
        self.sm = screen_manager
        self.set = settings_manager
        
        description = warning_message

        def repair(*args):

            self.sm.get_screen('update').repair_sw_over_wifi()
        
        img = Image(source="./asmcnc/apps/shapeCutter_app/img/error_icon.png", allow_stretch=False)
        label = Label(size_hint_y=1.4, text_size=(360, None), halign='center', valign='middle', text=description, color=[0,0,0,1], padding=[20,20], markup = True)
        
        ok_button = Button(text='[b]Repair[/b]', markup = True)
        ok_button.background_normal = ''
        ok_button.background_color = [76 / 255., 175 / 255., 80 / 255., 1.]
        back_button = Button(text='[b]Go back[/b]', markup = True)
        back_button.background_normal = ''
        back_button.background_color = [230 / 255., 74 / 255., 25 / 255., 1.]

       
        btn_layout = BoxLayout(orientation='horizontal', spacing=10, padding=[0,0,0,0])
        btn_layout.add_widget(back_button)
        btn_layout.add_widget(ok_button)
        
        layout_plan = BoxLayout(orientation='vertical', spacing=10, padding=[10,20,10,20])
        layout_plan.add_widget(img)
        layout_plan.add_widget(label)
        layout_plan.add_widget(btn_layout)
        

        popup = Popup(title='There was a problem updating the software...',
                      title_color=[0, 0, 0, 1],
                      title_font= 'Roboto-Bold',
                      title_size = '20sp',
                      content=layout_plan,
                      size_hint=(None, None),
                      size=(500, 420),
                      auto_dismiss= False
                      )
        
        popup.separator_color = [230 / 255., 74 / 255., 25 / 255., 1.]
        popup.separator_height = '4dp'
        popup.background = './asmcnc/apps/shapeCutter_app/img/popup_background.png'
        
        ok_button.bind(on_press=popup.dismiss)
        ok_button.bind(on_press=repair)
        back_button.bind(on_press=popup.dismiss)       

        popup.open()     

class PopupError(Widget):   
    def __init__(self, screen_manager, localization, warning_message):
        
        self.sm = screen_manager
        self.l = localization
        
        description = warning_message

        title_string = self.l.get_str('Error!')
        ok_string = self.l.get_bold('Ok')
        
        img = Image(source="./asmcnc/apps/shapeCutter_app/img/error_icon.png", allow_stretch=False)
        label = Label(size_hint_y=1, text_size=(360, None), halign='center', valign='middle', text=description, color=[0,0,0,1], padding=[0,10], markup = True)
        
        ok_button = Button(text=ok_string, markup = True)
        ok_button.background_normal = ''
        ok_button.background_color = [230 / 255., 74 / 255., 25 / 255., 1.]
       
        btn_layout = BoxLayout(orientation='horizontal', spacing=10, padding=[0,0,0,0])
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

        popup.open()

class PopupWarning(Widget):   
    def __init__(self, screen_manager, localization, warning_message):
        
        self.sm = screen_manager
        self.l = localization
        
        description = warning_message
        title_string = self.l.get_str('Warning!')
        ok_string = self.l.get_bold('Ok')
        
        img = Image(source="./asmcnc/apps/shapeCutter_app/img/error_icon.png", allow_stretch=False)
        label = Label(size_hint_y=1, text_size=(360, None), halign='center', valign='middle', text=description, color=[0,0,0,1], padding=[0,0], markup = True)
        
        ok_button = Button(text=ok_string, markup = True)
        ok_button.background_normal = ''
        ok_button.background_color = [230 / 255., 74 / 255., 25 / 255., 1.]
       
        btn_layout = BoxLayout(orientation='horizontal', spacing=10, padding=[20,0,20,0])
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

        popup.open()

class PopupWait(Widget):   
    def __init__(self, screen_manager, description = 'Please wait...'):
        
        self.sm = screen_manager
        
        img = Image(source="./asmcnc/apps/shapeCutter_app/img/info_icon.png", allow_stretch=False)
        label = Label(size_hint_y=1, text_size=(360, None), halign='center', valign='middle', text=description, color=[0,0,0,1], padding=[40,20], markup = True)
        
        ok_button = Button(text='[b]Ok[/b]', markup = True)
        ok_button.background_normal = ''
        ok_button.background_color = [76 / 255., 175 / 255., 80 / 255., 1.]
        
        btn_layout = BoxLayout(orientation='horizontal', spacing=10, padding=[0,0,0,0])
        btn_layout.add_widget(ok_button)
        
        layout_plan = BoxLayout(orientation='vertical', spacing=10, padding=[40,20,40,20])
        layout_plan.add_widget(img)
        layout_plan.add_widget(label)
        layout_plan.add_widget(btn_layout)
        
        self.popup = Popup(title='Please Wait...',
                      title_color=[0, 0, 0, 1],
                      title_font= 'Roboto-Bold',
                      title_size = '20sp',
                      content=layout_plan,
                      size_hint=(None, None),
                      size=(500, 400),
                      auto_dismiss= False
                      )
        
        self.popup.separator_color = [249 / 255., 206 / 255., 29 / 255., 1.]
        self.popup.separator_height = '4dp'
        self.popup.background = './asmcnc/apps/shapeCutter_app/img/popup_background.png'
        
        ok_button.bind(on_press=self.popup.dismiss)    

        self.popup.open()

class PopupDeveloper(Widget):   
    def __init__(self, screen_manager):
        
        self.sm = screen_manager
        
        description = "The developer app is to help our engineers access extra settings " + \
        "and functions that might not be stable, or change how SmartBench behaves.\n\n" + \
        "By using the developer app, you may risk causing damage to SmartBench.\n\n" + \
        "Do you want to continue? "
        
        def dev_app(*args):
            self.sm.current = 'dev'
        
        img = Image(source="./asmcnc/apps/shapeCutter_app/img/error_icon.png", allow_stretch=False)
        label = Label(size_hint_y=2, text_size=(360, None), halign='center', valign='middle', text=description, color=[0,0,0,1], padding=[0,0], markup = True)
        
        ok_button = Button(text='[b]Yes[/b]', markup = True)
        ok_button.background_normal = ''
        ok_button.background_color = [76 / 255., 175 / 255., 80 / 255., 1.]
        back_button = Button(text='[b]No[/b]', markup = True)
        back_button.background_normal = ''
        back_button.background_color = [230 / 255., 74 / 255., 25 / 255., 1.]

       
        btn_layout = BoxLayout(orientation='horizontal', spacing=15, padding=[0,5,0,0])
        btn_layout.add_widget(back_button)
        btn_layout.add_widget(ok_button)
        
        layout_plan = BoxLayout(orientation='vertical', spacing=10, padding=[30,20,30,0])
        layout_plan.add_widget(img)
        layout_plan.add_widget(label)
        layout_plan.add_widget(btn_layout)
        
        popup = Popup(title='Warning!',
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
        ok_button.bind(on_press=dev_app)
        back_button.bind(on_press=popup.dismiss)       


        popup.open()

class PopupDevModePassword(Widget):   
    def __init__(self, screen_manager):
        
        self.sm = screen_manager
        
        description = "Please enter the password"

        def check_password(*args):
          if textinput.text == "dev":
            self.sm.get_screen('dev').dev_mode_toggle.state = "down"
            self.sm.get_screen('dev').developer_mode = True

          else:
            self.sm.get_screen('dev').dev_mode_toggle.state = "normal"
            self.sm.get_screen('dev').developer_mode = False
        
        img = Image(source="./asmcnc/apps/shapeCutter_app/img/error_icon.png", allow_stretch=False)
        label = Label(size_hint_y=1, text_size=(360, None), halign='center', valign='middle', text=description, color=[0,0,0,1], padding=[0,0], markup = True)
        textinput = TextInput(size_hint_y=0.7, text = '')

        ok_button = Button(text='[b]Ok[/b]', markup = True)
        ok_button.background_normal = ''
        ok_button.background_color = [230 / 255., 74 / 255., 25 / 255., 1.]
       
        btn_layout = BoxLayout(orientation='horizontal', spacing=10, padding=[20,0,20,0])
        btn_layout.add_widget(ok_button)
        
        layout_plan = BoxLayout(orientation='vertical', spacing=10, padding=[40,20,40,20])
        layout_plan.add_widget(img)
        layout_plan.add_widget(label)
        layout_plan.add_widget(textinput)
        layout_plan.add_widget(btn_layout)
        
        popup = Popup(title='Warning!',
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
        
        ok_button.bind(on_press=check_password)
        ok_button.bind(on_press=popup.dismiss)    

        popup.open()


class PopupDeleteFile(Widget):   
    def __init__(self, **kwargs):
        
        self.sm = kwargs['screen_manager']
        self.l = kwargs['localization']
        self.function = kwargs['function']
        self.file_selection = kwargs['file_selection']
        
        if self.file_selection == 'all':
          description = self.l.get_str("Are you sure you want to delete these files?")
        else:
          description = self.l.get_str("Are you sure you want to delete this file?")

        title_string = self.l.get_str('Warning!')
        yes_string = self.l.get_bold('Yes')
        no_string = self.l.get_bold('No')
        
        def delete(*args):
          if self.file_selection == 'all':
            self.function()
          else:
            self.function(self.file_selection)

        def back(*args):
          return False
        
        img = Image(source="./asmcnc/apps/shapeCutter_app/img/error_icon.png", allow_stretch=False)
        label = Label(size_hint_y=2, text_size=(260, None), halign='center', valign='middle', text=description, color=[0,0,0,1], padding=[0,0], markup = True)
        
        ok_button = Button(text=yes_string, markup = True)
        ok_button.background_normal = ''
        ok_button.background_color = [76 / 255., 175 / 255., 80 / 255., 1.]
        back_button = Button(text=no_string, markup = True)
        back_button.background_normal = ''
        back_button.background_color = [230 / 255., 74 / 255., 25 / 255., 1.]

       
        btn_layout = BoxLayout(orientation='horizontal', spacing=15, padding=[0,5,0,0])
        btn_layout.add_widget(back_button)
        btn_layout.add_widget(ok_button)
        
        layout_plan = BoxLayout(orientation='vertical', spacing=10, padding=[30,20,30,0])
        layout_plan.add_widget(img)
        layout_plan.add_widget(label)
        layout_plan.add_widget(btn_layout)
        
        popup = Popup(title=title_string,
                      title_color=[0, 0, 0, 1],
                      title_font= 'Roboto-Bold',
                      title_size = '20sp',
                      content=layout_plan,
                      size_hint=(None, None),
                      size=(300, 350),
                      auto_dismiss= False
                      )
        
        popup.separator_color = [230 / 255., 74 / 255., 25 / 255., 1.]
        popup.separator_height = '4dp'
        popup.background = './asmcnc/apps/shapeCutter_app/img/popup_background.png'
        
        ok_button.bind(on_press=popup.dismiss)
        ok_button.bind(on_press=delete)
        back_button.bind(on_press=popup.dismiss)
        back_button.bind(on_press=back)

        popup.open()



class PopupReminder(Widget):

    def __init__(self, screen_manager, app_manager, machine, message, go_to):
        
        self.sm = screen_manager
        self.am = app_manager
        self.m = machine
        
        if go_to == 'calibration':
          description = message
        else:
          description = message + "\n\n[b]WARNING! Delaying key maintenance tasks or dismissing reminders could cause wear and breakage of important parts![/b]"

        def open_app(*args):

            if go_to == 'calibration':
              self.am.start_calibration_app('go')

            elif go_to == 'brushes':
              self.am.start_maintenance_app('brush_tab')

            elif go_to == 'lubrication': 
              self.m.write_z_head_maintenance_settings(0)

        
        def calibration_delay(*args):
          new_time = float(float(320*3600) + self.m.time_to_remind_user_to_calibrate_seconds)
          self.m.write_calibration_settings(self.m.time_since_calibration_seconds, new_time)


        img = Image(source="./asmcnc/apps/shapeCutter_app/img/error_icon.png", allow_stretch=False)
        label = Label(size_hint_y=2, text_size=(680, None), halign='center', valign='middle', text=description, color=[0,0,0,1], padding=[10,0], markup = True)

        if go_to == 'calibration':
          ok_button = Button(text='[b]Calibrate now![/b]', markup = True)
          back_button = Button(text='[b]Remind me in 320 hours[/b]', markup = True)

        if go_to == 'lubrication':
          ok_button = Button(text='[b]Ok! Z-head lubricated![/b]', markup = True)
          back_button = Button(text='[b]Remind me later[/b]', markup = True)

        if go_to == 'brushes':
          ok_button = Button(text='[b]Change brushes now![/b]', markup = True)
          back_button = Button(text='[b]Remind me later[/b]', markup = True)

        ok_button.background_normal = ''
        ok_button.background_color = [76 / 255., 175 / 255., 80 / 255., 1.]
        back_button.background_normal = ''
        back_button.background_color = [230 / 255., 74 / 255., 25 / 255., 1.]

       
        btn_layout = BoxLayout(orientation='horizontal', spacing=10, padding=[0,0,0,0], size_hint_y = 0.6)
        btn_layout.add_widget(back_button)
        btn_layout.add_widget(ok_button)
        
        layout_plan = BoxLayout(orientation='vertical', spacing=0, padding=[10,10,10,5])
        layout_plan.add_widget(img)
        layout_plan.add_widget(label)
        layout_plan.add_widget(btn_layout)
        

        popup = Popup(title='Maintenance reminder!',
                      title_color=[0, 0, 0, 1],
                      title_font= 'Roboto-Bold',
                      title_size = '22sp',
                      content=layout_plan,
                      size_hint=(None, None),
                      size=(700, 460),
                      auto_dismiss= False
                      )
        
        popup.separator_color = [230 / 255., 74 / 255., 25 / 255., 1.]
        popup.separator_height = '4dp'
        popup.background = './asmcnc/apps/shapeCutter_app/img/popup_background.png'
        
        ok_button.bind(on_press=popup.dismiss)
        ok_button.bind(on_press=open_app)
        back_button.bind(on_press=popup.dismiss)

        if go_to == 'calibration':
          back_button.bind(on_press=calibration_delay)      

        popup.open()

class PopupConfirmJobCancel(Widget):

    def __init__(self, screen_manager):

      self.sm = screen_manager
        
      def confirm_cancel(*args):
          self.sm.get_screen('stop_or_resume_job_decision').confirm_job_cancel()
        
      stop_description = "Are you sure you want to cancel the job?"
      
      img = Image(source="./asmcnc/apps/shapeCutter_app/img/error_icon.png", allow_stretch=False)
      label = Label(size_hint_y=2, text_size=(360, None), halign='center', valign='middle', text=stop_description, color=[0,0,0,1], padding=[0,0], markup = True)
      
      resume_button = Button(text='[b]No[/b]', markup = True)
      resume_button.background_normal = ''
      resume_button.background_color = [76 / 255., 175 / 255., 80 / 255., 1.]
      cancel_button = Button(text='[b]Yes[/b]', markup = True)
      cancel_button.background_normal = ''
      cancel_button.background_color = [230 / 255., 74 / 255., 25 / 255., 1.]

     
      btn_layout = BoxLayout(orientation='horizontal', spacing=15, padding=[0,5,0,0], size_hint_y=2) 
      btn_layout.add_widget(cancel_button)
      btn_layout.add_widget(resume_button)
      
      layout_plan = BoxLayout(orientation='vertical', spacing=5, padding=[30,20,30,0])
      layout_plan.add_widget(img)
      layout_plan.add_widget(label)
      layout_plan.add_widget(btn_layout)
      
      popup = Popup(title='Warning!',
                    title_color=[0, 0, 0, 1],
                    title_font= 'Roboto-Bold',
                    title_size = '20sp',
                    content=layout_plan,
                    size_hint=(None, None),
                    size=(400, 300),
                    auto_dismiss= False
                    )
      
      popup.separator_color = [230 / 255., 74 / 255., 25 / 255., 1.]
      popup.separator_height = '4dp'
      popup.background = './asmcnc/apps/shapeCutter_app/img/popup_background.png'
      
      cancel_button.bind(on_press=confirm_cancel)
      cancel_button.bind(on_press=popup.dismiss)
      resume_button.bind(on_press=popup.dismiss)
      
      popup.open()

class PopupHomingWarning(Widget):

    def __init__(self, screen_manager, machine, localization, return_to_screen, cancel_to_screen):

      self.sm = screen_manager
      self.m = machine
      self.l = localization
        
      def home_now(*args):
          self.m.request_homing_procedure(return_to_screen, cancel_to_screen)
        
      stop_description = self.l.get_str("You need to home SmartBench first!")
      title_string = self.l.get_str("Warning!")
      home_string = self.l.get_bold("Home")
      cancel_string = self.l.get_bold("Cancel")
      
      img = Image(source="./asmcnc/apps/shapeCutter_app/img/error_icon.png", allow_stretch=False)
      label = Label(size_hint_y=2, text_size=(360, None), halign='center', valign='middle', text=stop_description, color=[0,0,0,1], padding=[0,0], markup = True)
      
      home_button = Button(text=home_string, markup = True)
      home_button.background_normal = ''
      home_button.background_color = [33 / 255., 150 / 255., 243 / 255., 98 / 100.]

      cancel_button = Button(text=cancel_string, markup = True)
      cancel_button.background_normal = ''
      cancel_button.background_color = [230 / 255., 74 / 255., 25 / 255., 1.]

      btn_layout = BoxLayout(orientation='horizontal', spacing=15, padding=[0,5,0,0], size_hint_y=2) 
      btn_layout.add_widget(cancel_button)
      btn_layout.add_widget(home_button)
      
      layout_plan = BoxLayout(orientation='vertical', spacing=5, padding=[30,20,30,0])
      layout_plan.add_widget(img)
      layout_plan.add_widget(label)
      layout_plan.add_widget(btn_layout)
      
      popup = Popup(title=title_string,
                    title_color=[0, 0, 0, 1],
                    title_font= 'Roboto-Bold',
                    title_size = '20sp',
                    content=layout_plan,
                    size_hint=(None, None),
                    size=(400, 300),
                    auto_dismiss= False
                    )
      
      popup.separator_color = [230 / 255., 74 / 255., 25 / 255., 1.]
      popup.separator_height = '4dp'
      popup.background = './asmcnc/apps/shapeCutter_app/img/popup_background.png'

      home_button.bind(on_press=home_now)
      home_button.bind(on_press=popup.dismiss)
      cancel_button.bind(on_press=popup.dismiss)
      
      popup.open()

class PopupShutdown(Widget):

    def __init__(self, screen_manager, localization):
        
        self.sm = screen_manager
        self.l = localization

        description = (
                      self.l.get_str('The console will close any critical processes and shut down safely after 60 seconds, ready for power off.') + \
                      "\n\n" + \
                      self.l.get_str('This extends the lifetime of the console.') + '\n\n' + \
                      self.l.get_str('You will still need to power down your machine separately after the console has finished shutting down.')
                      )
        title_string = self.l.get_str('Shutting down') + '...'
        shutdown_string = self.l.get_bold('Shutdown now')
        cancel_string = self.l.get_bold('Cancel')

        def cancel_shutdown(*args):
          os.system('sudo shutdown -c')

        def shutdown_now(*args):
          os.system('sudo shutdown -h now')
        
        img = Image(source="./asmcnc/apps/shapeCutter_app/img/info_icon.png", allow_stretch=False)
        label = Label(size_hint_y=1.5, text_size=(480, None), halign='center', valign='middle', text=description, color=[0,0,0,1], padding=[0,0], markup = True)

        ok_button = Button(text=shutdown_string, markup = True)
        ok_button.background_normal = ''
        ok_button.background_color = [76 / 255., 175 / 255., 80 / 255., 1.]
        cancel_button = Button(text=cancel_string, markup = True)
        cancel_button.background_normal = ''
        cancel_button.background_color = [230 / 255., 74 / 255., 25 / 255., 1.]

        btn_layout = BoxLayout(orientation='horizontal', spacing=10, padding=[0,10,0,0])
        btn_layout.add_widget(cancel_button)
        btn_layout.add_widget(ok_button)
        
        layout_plan = BoxLayout(orientation='vertical', spacing=10, padding=[20,10,20,10])
        layout_plan.add_widget(img)
        layout_plan.add_widget(label)
        layout_plan.add_widget(btn_layout)
        
        popup = Popup(title=title_string,
                      title_color=[0, 0, 0, 1],
                      title_font= 'Roboto-Bold',
                      title_size = '20sp',
                      content=layout_plan,
                      size_hint=(None, None),
                      # size=(300, 300),
                      size=(540, 400),
                      auto_dismiss= False
                      )

        popup.background = './asmcnc/apps/shapeCutter_app/img/popup_background.png'
        popup.separator_color = [249 / 255., 206 / 255., 29 / 255., 1.]
        popup.separator_height = '4dp'

        ok_button.bind(on_press=shutdown_now)
        cancel_button.bind(on_press=cancel_shutdown)
        cancel_button.bind(on_press=popup.dismiss)

        popup.open()