'''
@author Letty
Created for info buttons in the shapecutter app
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


class PopupMachineError(Widget):

    def __init__(self, screen_manager):
        
        self.sm = screen_manager
        
        description = "Machine is not Idle.\n\n" \
                    "Please check that SmartBench is clear," \
                    " and then use EasyCut Pro to RESET SmartBench before using Shape Cutter."
        
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
                      title_font= 'Roboto-Bold',
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
        
        
class PopupWait(Widget):

    def __init__(self, screen_manager):
        
        self.sm = screen_manager
        
        description = "Please wait while the machine moves..."
        
        img = Image(source="./asmcnc/apps/shapeCutter_app/img/error_icon.png", allow_stretch=False)
        label = Label(size_hint_y=1, text_size=(360, None), halign='center', valign='middle', text=description, color=[0,0,0,1], padding=[20,20])
        
        ok_button = Button(text='[b]Ok[/b]', markup = True, disabled = True)
        ok_button.background_normal = ''
        ok_button.background_color = [230 / 255., 74 / 255., 25 / 255., 1.]
        
        btn_layout = BoxLayout(orientation='horizontal', spacing=15, padding=[50,25,50,0])
        btn_layout.add_widget(ok_button)
        
        layout_plan = BoxLayout(orientation='vertical', spacing=10, padding=[50,20,50,20])
        layout_plan.add_widget(img)
        layout_plan.add_widget(label)
        layout_plan.add_widget(btn_layout)
        
        self.popup = Popup(title='Warning!',
                      title_color=[0, 0, 0, 1],
                      title_font= 'Roboto-Bold',
                      title_size = '20sp',
                      content=layout_plan,
                      size_hint=(None, None),
                      size=(400, 380),
                      auto_dismiss= False
                      )
        
        self.popup.separator_color = [230 / 255., 74 / 255., 25 / 255., 1.]
        self.popup.separator_height = '4dp'
        self.popup.background = './asmcnc/apps/shapeCutter_app/img/popup_background.png'
        
        ok_button.bind(on_press=self.popup.dismiss)

        self.popup.open()
        