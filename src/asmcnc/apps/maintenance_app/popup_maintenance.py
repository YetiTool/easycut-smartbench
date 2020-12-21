import kivy

from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.properties import StringProperty  # @UnresolvedImport
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import  Button
from kivy.uix.image import Image


class PopupResetOffset(Widget):

    def __init__(self, screen_manager):
        
        self.sm = screen_manager
        
        description = "You are resetting the laser datum offset.\n\nPlease confirm that this is where you have made a reference mark with the spindle."

        def reset_laser_datum_offset(*args):
            self.sm.get_screen('maintenance').laser_datum_buttons_widget.reset_laser_offset()
        
        img = Image(source="./asmcnc/apps/shapeCutter_app/img/info_icon.png", allow_stretch=False)
        label = Label(size_hint_y=1.4, text_size=(360, None), halign='center', valign='middle', text=description, color=[0,0,0,1], padding=[20,20], markup = True)
        
        ok_button = Button(text='[b]Yes, set reference[/b]', markup = True)
        ok_button.background_normal = ''
        ok_button.background_color = [76 / 255., 175 / 255., 80 / 255., 1.]
        back_button = Button(text='[b]No, go back[/b]', markup = True)
        back_button.background_normal = ''
        back_button.background_color = [230 / 255., 74 / 255., 25 / 255., 1.]

       
        btn_layout = BoxLayout(orientation='horizontal', spacing=10, padding=[0,0,0,0])
        btn_layout.add_widget(back_button)
        btn_layout.add_widget(ok_button)
        
        layout_plan = BoxLayout(orientation='vertical', spacing=10, padding=[10,20,10,20])
        layout_plan.add_widget(img)
        layout_plan.add_widget(label)
        layout_plan.add_widget(btn_layout)
        

        popup = Popup(title='Reset laser datum offset',
                      title_color=[0, 0, 0, 1],
                      title_font= 'Roboto-Bold',
                      title_size = '20sp',
                      content=layout_plan,
                      size_hint=(None, None),
                      size=(400, 360),
                      auto_dismiss= False
                      )
        
        popup.separator_color = [249 / 255., 206 / 255., 29 / 255., 1.]
        popup.separator_height = '4dp'
        popup.background = './asmcnc/apps/shapeCutter_app/img/popup_background.png'
        
        ok_button.bind(on_press=popup.dismiss)
        ok_button.bind(on_press=reset_laser_datum_offset)
        back_button.bind(on_press=popup.dismiss)       

        popup.open() 

class PopupSaveOffset(Widget):

    def __init__(self, screen_manager):
        
        self.sm = screen_manager
        
        description = "You are saving the laser datum offset.\n\nPlease confirm that the laser crosshair lines up with the centre of your refernce mark."

        def save_laser_datum_offset(*args):
            self.sm.get_screen('maintenance').laser_datum_buttons_widget.save_laser_offset()
        
        img = Image(source="./asmcnc/apps/shapeCutter_app/img/info_icon.png", allow_stretch=False)
        label = Label(size_hint_y=1.4, text_size=(360, None), halign='center', valign='middle', text=description, color=[0,0,0,1], padding=[20,20], markup = True)
        
        ok_button = Button(text='[b]Yes, set offset[/b]', markup = True)
        ok_button.background_normal = ''
        ok_button.background_color = [76 / 255., 175 / 255., 80 / 255., 1.]
        back_button = Button(text='[b]No, go back[/b]', markup = True)
        back_button.background_normal = ''
        back_button.background_color = [230 / 255., 74 / 255., 25 / 255., 1.]

       
        btn_layout = BoxLayout(orientation='horizontal', spacing=10, padding=[0,0,0,0])
        btn_layout.add_widget(back_button)
        btn_layout.add_widget(ok_button)
        
        layout_plan = BoxLayout(orientation='vertical', spacing=10, padding=[10,20,10,20])
        layout_plan.add_widget(img)
        layout_plan.add_widget(label)
        layout_plan.add_widget(btn_layout)
        

        popup = Popup(title='Save laser datum offset',
                      title_color=[0, 0, 0, 1],
                      title_font= 'Roboto-Bold',
                      title_size = '20sp',
                      content=layout_plan,
                      size_hint=(None, None),
                      size=(400, 360),
                      auto_dismiss= False
                      )
        
        popup.separator_color = [249 / 255., 206 / 255., 29 / 255., 1.]
        popup.separator_height = '4dp'
        popup.background = './asmcnc/apps/shapeCutter_app/img/popup_background.png'
        
        ok_button.bind(on_press=popup.dismiss)
        ok_button.bind(on_press=save_laser_datum_offset)
        back_button.bind(on_press=popup.dismiss)       

        popup.open()


class PopupBrushInfo(Widget):

# This is not elegant.

    def __init__(self, screen_manager):
        
        self.sm = screen_manager
        label_width = 660

        description_top = "[b]Brush use:[/b]\n" + \
        "   [b]Value:[/b] The running hours of the brushes.\n" + \
        "   [b]Restore:[/b] Return to the hours previously logged.\n" + \
        "   [b]Reset:[/b] Set the running hours to zero."
        

        description_bottom = "[b]Brush reminder:[/b]\n" + \
        "   [b]Value:[/b] Set to the hours the brushes are expected to last.\n" + \
        "               This will vary depending on heavy use (~approx 120 hours) or light use (~approx 500\n               hours)." + \
        " It is best to set to worst case, inspect the brushes, and update as necessary.\n" + \
        "   [b]Restore:[/b] Return the brush reminder to the hours previously set.\n" + \
        "   [b]Reset:[/b] Sets to the brush reminder to 120 hours.\n"

        description_examples_top = '[b]     NEW                    LOW                  SHUT-OFF[/b]'
        description_examples_bottom = '[b]          16mm              10mm              9.5mm[/b]    '
        description_examples_tolerances = '[b]                  (+/-0.2mm)     (+/-0.2mm)     (+/-0.2mm)[/b]    '
        
        img = Image(source="./asmcnc/apps/shapeCutter_app/img/info_icon.png", allow_stretch=False)
        label_top = Label(size_hint_y=2.1, text_size=(None, None), markup=True, halign='left', valign='middle', text=description_top, color=[0,0,0,1], padding=[0,0])
        label_blank = Label(size_hint_y=0.01, text_size=(None, None), markup=True, halign='left', valign='bottom', text='', color=[0,0,0,1], padding=[0,0])
        label_bottom = Label(size_hint_y=1.5, text_size=(None, None), markup=True, halign='left', valign='middle', text=description_bottom, color=[0,0,0,1], padding=[0,0])
        examples_label_top = Label(size_hint_y=0.1, text_size=(None, None), markup=True, font_size='12sp', halign='left', valign='top', text=description_examples_top, color=[0,0,0,1], padding=[0,0])
        examples_label_bottom = Label(size_hint_y=0.1, text_size=(None, None), markup=True, font_size='12sp', halign='left', valign='bottom', text=description_examples_bottom, color=[0,0,0,1], padding=[0,0])        
        examples_label_tolerances = Label(size_hint_y=0.1, text_size=(None, None), markup=True, font_size='12sp', halign='left', valign='bottom', text=description_examples_tolerances, color=[0,0,0,1], padding=[0,0])

        img_brushes = Image(source="./asmcnc/apps/maintenance_app/img/brush_examples.png", allow_stretch=False)

        ok_button = Button(text='[b]Ok[/b]', markup = True)
        ok_button.background_normal = ''
        ok_button.background_color = [76 / 255., 175 / 255., 80 / 255., 1.]

        examples_layout = BoxLayout(orientation='vertical', padding=0, spacing=5)
        examples_layout.add_widget(examples_label_top)  
        examples_layout.add_widget(img_brushes)
        examples_layout.add_widget(examples_label_bottom)
        examples_layout.add_widget(examples_label_tolerances)

        label_cheat = BoxLayout(orientation='vertical', padding=0, spacing=5)
        label_cheat.add_widget(label_blank)
        label_cheat.add_widget(label_top)

        btn_layout = BoxLayout(orientation='horizontal', padding=[150,10,150,0], size_hint_y = 0.8)
        btn_layout.add_widget(ok_button)

        use_layout = BoxLayout(orientation='horizontal', spacing=0, padding=0, size_hint_y = 2.2)
        use_layout.add_widget(label_cheat)
        use_layout.add_widget(examples_layout)
        
        layout_plan = BoxLayout(orientation='vertical', spacing=5, padding=[40,10,40,10])
        layout_plan.add_widget(img)
        layout_plan.add_widget(use_layout)
        layout_plan.add_widget(label_bottom)
        layout_plan.add_widget(btn_layout)
        
        popup = Popup(title='Information',
                      title_color=[0, 0, 0, 1],
                      title_font= 'Roboto-Bold',
                      title_size = '20sp',
                      content=layout_plan,
                      size_hint=(None, None),
                      size=(700, 440),
                      auto_dismiss= False
                      )

        popup.background = './asmcnc/apps/shapeCutter_app/img/popup_background.png'
        popup.separator_color = [249 / 255., 206 / 255., 29 / 255., 1.]
        popup.separator_height = '4dp'

        ok_button.bind(on_press=popup.dismiss)

        popup.open()
