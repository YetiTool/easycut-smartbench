from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import  Button
from kivy.uix.image import Image

from asmcnc.core_UI.utils import color_provider

class PopupSC2Decision(Widget):

    def __init__(self, screen_manager, localization, description):
        
        self.sm = screen_manager
        self.l = localization

        title_string = "SC2 compatability"
        ok_string = "Continue"
        cancel_string = "Cancel"

        def toggle_sc2_compatability(*args):
            self.sm.get_screen('factory_settings').toggle_sc2_compatability()

        def undo_toggle(*args):
            self.sm.get_screen('factory_settings').undo_toggle()
        
        img = Image(source="./asmcnc/apps/shapeCutter_app/img/info_icon.png", allow_stretch=False)
        label = Label(size_hint_y=1.5, text_size=(480, None), halign='center', valign='middle', text=description, color=color_provider.get_rgba("black"), padding=[0,0], markup = True)

        ok_button = Button(text=ok_string, markup = True)
        ok_button.background_normal = ''
        ok_button.background_color = color_provider.get_rgba("green")
        ok_button.bold = True
        cancel_button = Button(text=cancel_string, markup = True)
        cancel_button.background_normal = ''
        cancel_button.background_color = color_provider.get_rgba("red")
        cancel_button.bold = True

        btn_layout = BoxLayout(orientation='horizontal', spacing=10, padding=[0,10,0,0])
        btn_layout.add_widget(cancel_button)
        btn_layout.add_widget(ok_button)
        
        layout_plan = BoxLayout(orientation='vertical', spacing=10, padding=[20,10,20,10])
        layout_plan.add_widget(img)
        layout_plan.add_widget(label)
        layout_plan.add_widget(btn_layout)
        
        popup = Popup(title=title_string,
                      title_color=color_provider.get_rgba("black"),
                      title_size = '20sp',
                      content=layout_plan,
                      size_hint=(None, None),
                      size=(540, 400),
                      auto_dismiss= False
                      )

        popup.background = './asmcnc/apps/shapeCutter_app/img/popup_background.png'
        popup.separator_color = color_provider.get_rgba("yellow")
        popup.separator_height = '4dp'

        ok_button.bind(on_press=toggle_sc2_compatability)
        ok_button.bind(on_press=popup.dismiss)
        cancel_button.bind(on_press=undo_toggle)
        cancel_button.bind(on_press=popup.dismiss)

        popup.open()
