'''
@author Letty
Info pop-up for SW Update app
'''

import kivy

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
from kivy.graphics import Color, Rectangle

class PopupBetaUpdate(Widget):   
    def __init__(self, screen_manager, wifi_or_usb):
        
        self.sm = screen_manager
        
        description = "The update you are trying to install is a beta release.\n" + \
        "This is a version of the software that allows our developers and product testers to " + \
        "try out new features and identify any bugs before the next customer release.\n\n" + \
        "This release might not be stable, and it is recommended that you wait until the full " + \
        "update..\n\nIf you do update to a beta release, and you have any issues, please contact Yeti Tool support.\n\n" + \
        "Do you want to continue? "
        
        def do_update(*args):
            if wifi_or_usb == 'wifi':
            	self.sm.get_screen('update').get_sw_update_over_wifi()
            elif wifi_or_usb == 'usb':
            	self.sm.get_screen('update').get_sw_update_over_usb()

        img = Image(source="./asmcnc/apps/shapeCutter_app/img/error_icon.png", allow_stretch=False)
        label = Label(size_hint_y=2, text_size=(620, None), halign='center', valign='middle', text=description, color=[0,0,0,1], padding=[0,0], markup = True)
        
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
                      size=(700, 440),
                      auto_dismiss= False
                      )
        
        popup.separator_color = [230 / 255., 74 / 255., 25 / 255., 1.]
        popup.separator_height = '4dp'
        popup.background = './asmcnc/apps/shapeCutter_app/img/popup_background.png'
        
        ok_button.bind(on_press=popup.dismiss)
        ok_button.bind(on_press=do_update)
        back_button.bind(on_press=popup.dismiss)       


        popup.open()