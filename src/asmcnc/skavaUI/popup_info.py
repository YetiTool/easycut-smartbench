'''
@author Letty
Info pop-up
'''

import kivy

from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.properties import StringProperty  # @UnresolvedImport
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget

from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.label import Label
from kivy.uix.button import  Button
from kivy.uix.image import Image


class PopupWelcome(Widget):

    def __init__(self, screen_manager, description):
        
        self.shapecutter_sm = screen_manager
        
        img = Image(source="./asmcnc/apps/shapeCutter_app/img/info_icon.png", allow_stretch=False)
        label = Label(size_hint_y=2, text_size=(360, None), markup=True, halign='center', valign='middle', text=description, color=[0,0,0,1], padding=[0,0])
        
        ok_button = Button(text='[b]Ok[/b]', markup = True)
        ok_button.background_normal = ''
        ok_button.background_color = [76 / 255., 175 / 255., 80 / 255., 1.]
        
        btn_layout = BoxLayout(orientation='horizontal', spacing=15, padding=[150,20,150,0])
        btn_layout.add_widget(ok_button)
        
        layout_plan = BoxLayout(orientation='vertical', spacing=10, padding=[10,10,10,10])
        layout_plan.add_widget(img)
        layout_plan.add_widget(label)
        layout_plan.add_widget(btn_layout)
        
        popup = Popup(title='Welcome to EasyCut',
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

        popup.open()
        
class PopupDatum(Widget):

    def __init__(self, screen_manager, machine, xy, warning_message):
        
        self.sm = screen_manager
        self.m = machine
        
        description = warning_message

        def go_datum(*args):
    
            if xy == 'X':
                self.m.set_x_datum()
            elif xy == 'Y':
                self.m.set_y_datum()
                
            elif xy == 'XY':
                self.m.set_workzone_to_pos_xy()
        
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
        
        layout_plan = BoxLayout(orientation='vertical', spacing=10, padding=[40,20,40,20])
        layout_plan.add_widget(img)
        layout_plan.add_widget(label)
        layout_plan.add_widget(btn_layout)
        
        popup = Popup(title='Warning!',
                      title_color=[0, 0, 0, 1],
                      title_font= 'Roboto-Bold',
                      title_size = '20sp',
                      content=layout_plan,
                      size_hint=(None, None),
                      size=(300, 300),
                      auto_dismiss= False
                      )
        
        popup.separator_color = [230 / 255., 74 / 255., 25 / 255., 1.]
        popup.separator_height = '4dp'
        popup.background = './asmcnc/apps/shapeCutter_app/img/popup_background.png'
        
        ok_button.bind(on_press=popup.dismiss)
        ok_button.bind(on_press=go_datum)
        back_button.bind(on_press=popup.dismiss)       


        popup.open()

class PopupUSBInfo(Widget):

    def __init__(self, screen_manager, safe_to_remove):
        
        self.sm = screen_manager
        
        if safe_to_remove == 'mounted':
            description = 'USB stick found!\n\nPlease don\'t remove your USB stick until it is safe to do so.'
       
            ok_button = Button(text='[b]Ok[/b]', markup = True)
            ok_button.background_normal = ''
            ok_button.background_color = [230 / 255., 74 / 255., 25 / 255., 1.]
        
        elif safe_to_remove == False:
            description = 'Don\'t remove your USB stick yet.\n\nPlease wait...'
       
            ok_button = Button(text='[b]Ok[/b]', markup = True)
            ok_button.background_normal = ''
            ok_button.background_color = [230 / 255., 74 / 255., 25 / 255., 1.]

        elif safe_to_remove == True:
            description = 'It is now safe to remove your USB stick.'          
            ok_button = Button(text='[b]Ok[/b]', markup = True)
            ok_button.background_normal = ''
            ok_button.background_color = [76 / 255., 175 / 255., 80 / 255., 1.]

        img = Image(source="./asmcnc/apps/shapeCutter_app/img/error_icon.png", allow_stretch=False)
        label = Label(size_hint_y=1, text_size=(360, None), halign='center', valign='middle', text=description, color=[0,0,0,1], padding=[40,20], markup = True)
 
 
       
        btn_layout = BoxLayout(orientation='horizontal', spacing=10, padding=[0,0,0,0])
#         btn_layout.add_widget(back_button)
        btn_layout.add_widget(ok_button)
        
        layout_plan = BoxLayout(orientation='vertical', spacing=10, padding=[40,20,40,20])
        layout_plan.add_widget(img)
        layout_plan.add_widget(label)
        layout_plan.add_widget(btn_layout)
        
        self.popup = Popup(title='Warning!',
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
#         back_button.bind(on_press=popup.dismiss)       

        self.popup.open()