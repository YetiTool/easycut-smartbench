'''
@author Letty
Created for info buttons in the shapecutter app
'''

import kivy

from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.properties import StringProperty  
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget

from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import  Button
from kivy.uix.image import Image
from kivy.uix.rst import RstDocument
from kivy.uix.scrollview import ScrollView

from kivy.clock import Clock

from asmcnc.core_UI import scaling_utils as utils

class PopupInfo(Widget):

    def __init__(self, screen_manager, description):
        
        self.shapecutter_sm = screen_manager
        
#         description = "If this is your first time using the app, please go to the tutorial.\n\n" \
#                             "If you need help or support, please visit customer support at www.yetitool.com/support"
        
        img = Image(source="./asmcnc/apps/shapeCutter_app/img/info_icon.png", allow_stretch=False)
        label = Label(size_hint_y=2, text_size=(360, None), markup=True, halign='left', valign='middle', text=description, color=[0,0,0,1], padding=[10,10])

        
        ok_button = Button(text='[b]Ok[/b]', markup = True)
        ok_button.background_normal = ''
        ok_button.background_color = [76 / 255., 175 / 255., 80 / 255., 1.]
        
        btn_layout = BoxLayout(orientation='horizontal', spacing=15, padding=[150,20,150,0])
        btn_layout.add_widget(ok_button)
        
        layout_plan = BoxLayout(orientation='vertical', spacing=10, padding=[10,10,10,10])
        layout_plan.add_widget(img)
        layout_plan.add_widget(label)
        layout_plan.add_widget(btn_layout)
        
        popup = Popup(title='Information',
#                       title_color=[0.141, 0.596, 0.957, 1],
                      title_color=[0, 0, 0, 1],
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
        
    def go_tutorial(self, *args):
        self.shapecutter_sm.tutorial()
        
class PopupTutorial(Widget):

    def __init__(self, screen_manager):
        
        self.shapecutter_sm = screen_manager
        
        description = "If this is your first time using the app, please go to the tutorial.\n\n" \
                            "If you need help or support, please visit customer support at www.yetitool.com/support"
        
        img = Image(source="./asmcnc/apps/shapeCutter_app/img/info_bigger.png", allow_stretch=False)
        label = Label(size_hint_y=1, text_size=(360, None), halign='left', valign='middle', text=description, color=[0,0,0,1], padding=[20,20])
        tutorial_button = Button(text='[b]Tutorial[/b]', markup = True)
        tutorial_button.background_normal = ''
        tutorial_button.background_color = [0.141, 0.596, 0.957, 1]
        
        ok_button = Button(text='[b]Ok[/b]', markup = True)
        ok_button.background_normal = ''
        ok_button.background_color = [76 / 255., 175 / 255., 80 / 255., 1.]
        
        btn_layout = BoxLayout(orientation='horizontal', spacing=15, padding=[50,20,50,0])
        btn_layout.add_widget(tutorial_button)
        btn_layout.add_widget(ok_button)
        
        layout_plan = BoxLayout(orientation='vertical', spacing=10, padding=[50,20,50,20])
        layout_plan.add_widget(img)
        layout_plan.add_widget(label)
        layout_plan.add_widget(btn_layout)
        
        popup = Popup(title='Information',
                      title_color=[0, 0, 0, 1],
                      title_size = '20sp',
                      content=layout_plan,
                      size_hint=(None, None),
                      size=(400, 380),
                      auto_dismiss= False
                      )
        
        popup.separator_color = [249 / 255., 206 / 255., 29 / 255., 1.]
        popup.separator_height = '4dp'
        popup.background = './asmcnc/apps/shapeCutter_app/img/popup_background.png'
        
        ok_button.bind(on_press=popup.dismiss)
        tutorial_button.bind(on_press=self.go_tutorial)
        tutorial_button.bind(on_press=popup.dismiss)

        popup.open()
        
    def go_tutorial(self, *args):
        self.shapecutter_sm.tutorial()

class PopupFeedsAndSpeedsLookupTable(Widget):

    def __init__(self, screen_manager):
        
        self.shapecutter_sm = screen_manager
        
        ok_button = Button(text='[b]Ok[/b]', markup = True, font_size=utils.get_scaled_sp("15sp"))
        ok_button.background_normal = ''
        ok_button.background_color = [76 / 255., 175 / 255., 80 / 255., 1.]
        
        btn_layout = BoxLayout(orientation='horizontal', spacing=utils.get_scaled_tuple(15, orientation="horizontal"), padding=utils.get_scaled_tuple([150,0,150,0]), size_hint_y = 0.2)
        btn_layout.add_widget(ok_button)
        
        rst_doc = RstDocument(source = './asmcnc/apps/shapeCutter_app/feeds_and_speeds_table.rst', background_color = [1,1,1,1], base_font_size = utils.get_scaled_width(26), underline_color = '000000')

        rst_layout = ScrollView(do_scroll_x = True, do_scroll_y = True, scroll_type = ['content'], size_hint_y = 0.8)
        rst_layout.add_widget(rst_doc)

        layout_plan = BoxLayout(orientation='vertical', spacing=utils.get_scaled_tuple(10, orientation="vertical"), padding=utils.get_scaled_tuple([10,10,10,10]))
        layout_plan.add_widget(rst_layout)
        layout_plan.add_widget(btn_layout)
        
        popup = Popup(title='Information',
#                       title_color=[0.141, 0.596, 0.957, 1],
                      title_color=[0, 0, 0, 1],
                      title_size = utils.get_scaled_sp("20sp"),
                      content=layout_plan,
                      size_hint=(None, None),
                      size=(utils.get_scaled_width(700), utils.get_scaled_height(400)),
                      auto_dismiss= False
                      )

        popup.background = './asmcnc/apps/shapeCutter_app/img/popup_background.png'
        popup.separator_color = [249 / 255., 206 / 255., 29 / 255., 1.]
        popup.separator_height = str(utils.get_scaled_width(4)) + "dp"

        ok_button.bind(on_press=popup.dismiss)
        popup.open()

class PopupWait(Widget):  

    def __init__(self, screen_manager, message):
        
        self.sm = screen_manager
        
        description = "Please wait" + message
        
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
        
        popup = Popup(title='Please Wait...',
                      title_color=[0, 0, 0, 1],
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
        Clock.schedule_once(lambda dt: popup.dismiss(), 2.5)
        popup.open()

        