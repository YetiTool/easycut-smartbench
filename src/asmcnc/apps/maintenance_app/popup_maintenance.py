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

    def __init__(self, screen_manager, localization):
        
        self.sm = screen_manager
        self.l = localization
        
        description = (
                self.l.get_str("You are resetting the laser datum offset.") + \
                "\n\n" + \
                self.l.get_str("Please confirm that this is where you have made a reference mark with the spindle.")
            )

        reset_laser_datum_offset_string = self.l.get_str('Reset laser datum offset')
        yes_string = self.l.get_bold("Yes, set reference")
        no_string = self.l.get_bold("No, go back")

        def reset_laser_datum_offset(*args):
            self.sm.get_screen('maintenance').laser_datum_buttons_widget.reset_laser_offset()
        
        img = Image(source="./asmcnc/apps/shapeCutter_app/img/info_icon.png", allow_stretch=False)
        label = Label(size_hint_y=1.4, text_size=(460, None), halign='center', valign='middle', text=description, color=[0,0,0,1], padding=[20,20], markup = True)
        
        ok_button = Button(text=yes_string, markup = True)
        ok_button.background_normal = ''
        ok_button.background_color = [76 / 255., 175 / 255., 80 / 255., 1.]
        back_button = Button(text=no_string, markup = True)
        back_button.background_normal = ''
        back_button.background_color = [230 / 255., 74 / 255., 25 / 255., 1.]

       
        btn_layout = BoxLayout(orientation='horizontal', spacing=10, padding=[0,0,0,0])
        btn_layout.add_widget(back_button)
        btn_layout.add_widget(ok_button)
        
        layout_plan = BoxLayout(orientation='vertical', spacing=10, padding=[10,20,10,20])
        layout_plan.add_widget(img)
        layout_plan.add_widget(label)
        layout_plan.add_widget(btn_layout)
        

        popup = Popup(title=reset_laser_datum_offset_string,
                      title_color=[0, 0, 0, 1],
                      title_font= 'Roboto-Bold',
                      title_size = '20sp',
                      content=layout_plan,
                      size_hint=(None, None),
                      size=(500, 360),
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

    def __init__(self, screen_manager, localization):
        
        self.sm = screen_manager
        self.l = localization
        
        description = (
                self.l.get_str("You are saving the laser datum offset.") + \
                "\n\n" + \
                self.l.get_str("Please confirm that the laser crosshair lines up with the centre of your reference mark.")
            )

        save_laser_datum_offset_string = self.l.get_str('Save laser datum offset')
        yes_string = self.l.get_bold("Yes, set offset")
        no_string = self.l.get_bold("No, go back")

        def save_laser_datum_offset(*args):
            self.sm.get_screen('maintenance').laser_datum_buttons_widget.save_laser_offset()
        
        img = Image(source="./asmcnc/apps/shapeCutter_app/img/info_icon.png", allow_stretch=False)
        label = Label(size_hint_y=1.4, text_size=(460, None), halign='center', valign='middle', text=description, color=[0,0,0,1], padding=[20,20], markup = True)
        
        ok_button = Button(text=yes_string, markup = True)
        ok_button.background_normal = ''
        ok_button.background_color = [76 / 255., 175 / 255., 80 / 255., 1.]
        back_button = Button(text=no_string, markup = True)
        back_button.background_normal = ''
        back_button.background_color = [230 / 255., 74 / 255., 25 / 255., 1.]

       
        btn_layout = BoxLayout(orientation='horizontal', spacing=10, padding=[0,0,0,0])
        btn_layout.add_widget(back_button)
        btn_layout.add_widget(ok_button)
        
        layout_plan = BoxLayout(orientation='vertical', spacing=10, padding=[10,20,10,20])
        layout_plan.add_widget(img)
        layout_plan.add_widget(label)
        layout_plan.add_widget(btn_layout)
        

        popup = Popup(title=save_laser_datum_offset_string,
                      title_color=[0, 0, 0, 1],
                      title_font= 'Roboto-Bold',
                      title_size = '20sp',
                      content=layout_plan,
                      size_hint=(None, None),
                      size=(500, 360),
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

    def __init__(self, screen_manager, localization):
        
        self.sm = screen_manager
        self.l = localization

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
        description_examples_bottom = '[b]16mm               10mm                  9.5mm[/b]         '
        description_examples_tolerances = '[b]        (+/-0.2mm)      (+/-0.2mm)         (+/-0.2mm)[/b]         '
        
        img = Image(source="./asmcnc/apps/shapeCutter_app/img/info_icon.png", allow_stretch=False)
        label_top = Label(size_hint_y=2.1, text_size=(None, None), markup=True, halign='left', valign='middle', text=description_top, color=[0,0,0,1], padding=[0,0])
        label_blank = Label(size_hint_y=0.01, text_size=(None, None), markup=True, halign='left', valign='bottom', text='', color=[0,0,0,1], padding=[0,0])
        label_bottom = Label(size_hint_y=1.5, text_size=(None, None), markup=True, halign='left', valign='middle', text=description_bottom, color=[0,0,0,1], padding=[0,0])
        # examples_label_top = Label(size_hint_y=0.1, text_size=(None, None), markup=True, font_size='12sp', halign='left', valign='top', text=description_examples_top, color=[0,0,0,1], padding=[0,0])
        # examples_label_bottom = Label(size_hint_y=0.1, text_size=(None, None), markup=True, font_size='12sp', halign='left', valign='bottom', text=description_examples_bottom, color=[0,0,0,1], padding=[0,0])        
        # examples_label_tolerances = Label(size_hint_y=0.1, text_size=(None, None), markup=True, font_size='12sp', halign='left', valign='bottom', text=description_examples_tolerances, color=[0,0,0,1], padding=[0,0])

        # img_brushes = Image(source="./asmcnc/apps/maintenance_app/img/brush_examples.png", allow_stretch=False)


        img_full_brush = Image(source="./asmcnc/apps/maintenance_app/img/brush_long_img.png", allow_stretch=False)
        label_full_brush_top = Label(text="NEW", text_size=(None, None), markup=True, halign='left', valign='middle', color=[0,0,0,1], padding=[0,0])
        label_full_brush_length = Label(text="16mm", text_size=(None, None), markup=True, halign='left', valign='middle', color=[0,0,0,1], padding=[0,0])
        label_full_brush_tolerance = Label(text="(+/-0.2mm)", text_size=(None, None), markup=True, halign='left', valign='middle', color=[0,0,0,1], padding=[0,0])

        example_full_length = BoxLayout(orientation = 'vertical', padding = 0, spacing = 5)
        example_full_length.add_widget(label_full_brush_top)
        example_full_length.add_widget(img_full_brush)
        example_full_length.add_widget(label_full_brush_length)
        example_full_length.add_widget(label_full_brush_tolerance)

        img_med_brush = Image(source="./asmcnc/apps/maintenance_app/img/brush_med_img.png", allow_stretch=False)
        label_med_brush_top = Label(text="LOW", text_size=(None, None), markup=True, halign='left', valign='middle', color=[0,0,0,1], padding=[0,0])
        label_med_brush_length = Label(text="10mm", text_size=(None, None), markup=True, halign='left', valign='middle', color=[0,0,0,1], padding=[0,0])
        label_med_brush_tolerance = Label(text="(+/-0.2mm)", text_size=(None, None), markup=True, halign='left', valign='middle', color=[0,0,0,1], padding=[0,0])

        example_med_length = BoxLayout(orientation = 'vertical', padding = 0, spacing = 5)
        example_med_length.add_widget(label_med_brush_top)
        example_med_length.add_widget(img_med_brush)
        example_med_length.add_widget(label_med_brush_length)
        example_med_length.add_widget(label_med_brush_tolerance)

        img_short_brush = Image(source="./asmcnc/apps/maintenance_app/img/brush_short_img.png", allow_stretch=False)
        label_short_brush_top = Label(text="SHUT-OFF", text_size=(None, None), markup=True, halign='left', valign='middle', color=[0,0,0,1], padding=[0,0])
        label_short_brush_length = Label(text="9.5mm", text_size=(None, None), markup=True, halign='left', valign='middle', color=[0,0,0,1], padding=[0,0])
        label_short_brush_tolerance = Label(text="(+/-0.2mm)", text_size=(None, None), markup=True, halign='left', valign='middle', color=[0,0,0,1], padding=[0,0])

        example_short_length = BoxLayout(orientation = 'vertical', padding = 0, spacing = 5)
        example_short_length.add_widget(label_short_brush_top)
        example_short_length.add_widget(img_short_brush)
        example_short_length.add_widget(label_short_brush_length)
        example_short_length.add_widget(label_short_brush_tolerance)

        ok_button = Button(text='[b]Ok[/b]', markup = True)
        ok_button.background_normal = ''
        ok_button.background_color = [76 / 255., 175 / 255., 80 / 255., 1.]

        # examples_layout = BoxLayout(orientation='vertical', padding=0, spacing=5)
        # examples_layout.add_widget(examples_label_top)  
        # examples_layout.add_widget(img_brushes)
        # examples_layout.add_widget(examples_label_bottom)
        # examples_layout.add_widget(examples_label_tolerances)

        examples_layout = BoxLayout(orientation='horizontal', padding=0, spacing=0)
        examples_layout.add_widget(example_full_length)
        examples_layout.add_widget(example_med_length)
        examples_layout.add_widget(example_short_length)

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
