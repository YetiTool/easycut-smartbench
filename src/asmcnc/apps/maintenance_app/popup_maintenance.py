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

        # do this as a grid layout instead
        description_top = (
            self.l.get_bold("Brush use:") + "\n" + \
            "  " + self.l.get_bold("Value:") + " " + self.l.get_str("The running hours of the brushes.") + "\n" + \
            "  " + self.l.get_bold("Restore:") + " " + self.l.get_str("Return to the hours previously logged.") + "\n" + \
            "  " + self.l.get_bold("Reset:") + " " + self.l.get_str("Set the running hours to zero.")
            )
        

        # description_bottom = "[b]Brush reminder:[/b]\n" + \
        # "   [b]Value:[/b] Set to the hours the brushes are expected to last.\n" + \
        # "               This will vary depending on heavy use (~approx 120 hours) or light use (~approx 500\n               hours)." + \
        # " It is best to set to worst case, inspect the brushes, and update as necessary.\n" + \
        # "   [b]Restore:[/b] Return the brush reminder to the hours previously set.\n" + \
        # "   [b]Reset:[/b] Sets to the brush reminder to 120 hours."

        description_bottom = (
                self.l.get_bold("Brush reminder:") + "\n" + \
                "  " + self.l.get_bold("Value:") + " " + self.l.get_str("Set to the hours the brushes are expected to last.") + "\n" + \
                "  " + self.l.get_str("This will vary depending on heavy use (~120 hours) or light use (~500 hours).") + "\n" + \
                "  " + self.l.get_str("It is best to set to worst case, inspect the brushes, and update as necessary.") + "\n" + \
                "  " + self.l.get_bold("Restore:") + " " + self.l.get_str("Return the brush reminder to the hours previously set.") + "\n" + \
                "  " + self.l.get_bold("Reset:") + " " + self.l.get_str("Sets the brush reminder to 120 hours.")
            )

        
        img = Image(source="./asmcnc/apps/shapeCutter_app/img/info_icon.png", allow_stretch=False)
        label_top = Label(size_hint_y=1, text_size=(476, self.height), markup=True, halign='left', valign='bottom', text=description_top, color=[0,0,0,1], padding=[0,0], width=476)
        label_blank = Label(size_hint_y=0.1, text_size=(476, self.height), markup=True, halign='left', valign='bottom', text='', color=[0,0,0,1], padding=[0,0], width=476)
        label_bottom = Label(text_size=(760, None), markup=True, halign='left', valign='top', text=description_bottom, color=[0,0,0,1], padding=[0,0], width=760)

        img_full_brush = Image(source="./asmcnc/apps/maintenance_app/img/brush_long_img.png", allow_stretch=False, size=(68,99))
        label_full_brush_top = Label(text=self.l.get_bold("NEW"), text_size=(68, self.height), size_hint_y=0.1, font_size='12sp', markup=True, halign='left', valign='middle', color=[0,0,0,1], padding=[0,0], width=img_full_brush.width)
        label_full_brush_length = Label(text="[b]16mm[/b]", text_size=(68, self.height),  size_hint_y=0.1, font_size='12sp', markup=True, halign='left', valign='middle', color=[0,0,0,1], padding=[0,0], width=img_full_brush.width)
        label_full_brush_tolerance = Label(text="[b](+/-0.2mm)[/b]", text_size=(68, self.height), size_hint_y=0.1, font_size='12sp', markup=True, halign='left', valign='middle', color=[0,0,0,1], padding=[0,0], width=img_full_brush.width)

        example_full_length = BoxLayout(orientation = 'vertical', padding = 0, spacing = 5, size_hint_x = None, width=68)
        example_full_length.add_widget(label_full_brush_top)
        example_full_length.add_widget(img_full_brush)
        example_full_length.add_widget(label_full_brush_length)
        example_full_length.add_widget(label_full_brush_tolerance)

        img_med_brush = Image(source="./asmcnc/apps/maintenance_app/img/brush_med_img.png", allow_stretch=False, size=(68,99))
        label_med_brush_top = Label(text=self.l.get_bold("LOW"), text_size=(68, self.height), size_hint_y=0.1, font_size='12sp', markup=True, halign='left', valign='middle', color=[0,0,0,1], padding=[0,0], width=68)
        label_med_brush_length = Label(text="[b]10mm[/b]", text_size=(68, self.height), size_hint_y=0.1, font_size='12sp', markup=True, halign='left', valign='middle', color=[0,0,0,1], padding=[0,0], width=68)
        label_med_brush_tolerance = Label(text="[b](+/-0.2mm)[/b]", text_size=(68, self.height), size_hint_y=0.1, font_size='12sp', markup=True, halign='left', valign='middle', color=[0,0,0,1], padding=[0,0], width=68)

        example_med_length = BoxLayout(orientation = 'vertical', padding = 0, spacing = 5, size_hint_x = None, width=68)
        example_med_length.add_widget(label_med_brush_top)
        example_med_length.add_widget(img_med_brush)
        example_med_length.add_widget(label_med_brush_length)
        example_med_length.add_widget(label_med_brush_tolerance)

        img_short_brush = Image(source="./asmcnc/apps/maintenance_app/img/brush_short_img.png", allow_stretch=False, size=(68,99))
        label_short_brush_top = Label(text=self.l.get_bold("SHUT-OFF"), text_size=(78, self.height), size_hint_y=0.1, font_size='12sp', markup=True, halign='left', valign='middle', color=[0,0,0,1], padding=[0,0], width=78)
        label_short_brush_length = Label(text="[b]9.5mm[/b]", text_size=(68, self.height), size_hint_y=0.1, font_size='12sp', markup=True, halign='left', valign='middle', color=[0,0,0,1], padding=[0,0], width=68)
        label_short_brush_tolerance = Label(text="[b](+/-0.2mm)[/b]", text_size=(68, self.height), size_hint_y=0.1, font_size='12sp', markup=True, halign='left', valign='middle', color=[0,0,0,1], padding=[0,0], width=68)

        example_short_length = BoxLayout(orientation = 'vertical', padding = 0, spacing = 5, size_hint_x = None, width=78)
        example_short_length.add_widget(label_short_brush_top)
        example_short_length.add_widget(img_short_brush)
        example_short_length.add_widget(label_short_brush_length)
        example_short_length.add_widget(label_short_brush_tolerance)

        ok_button = Button(text='[b]Ok[/b]', markup = True)
        ok_button.background_normal = ''
        ok_button.background_color = [76 / 255., 175 / 255., 80 / 255., 1.]

        examples_layout = BoxLayout(orientation='horizontal', padding=[0, 0, 30, 0], spacing=20, size_hint_x = None, width=284)
        examples_layout.add_widget(example_full_length)
        examples_layout.add_widget(example_med_length)
        examples_layout.add_widget(example_short_length)

        label_cheat = BoxLayout(orientation='vertical', padding=0, spacing=5, size_hint_x = None, width=476)
        label_cheat.add_widget(label_blank)
        label_cheat.add_widget(label_top)

        btn_layout = BoxLayout(orientation='horizontal', padding=[150,0,150,0], size_hint_y = 0.9)
        btn_layout.add_widget(ok_button)

        use_layout = BoxLayout(orientation='horizontal', spacing=0, padding=0, size_hint_y = 2, size_hint_x = None, width=760)
        use_layout.add_widget(label_cheat)
        use_layout.add_widget(examples_layout)

        reminder_layout = BoxLayout(orientation='horizontal', spacing=0, padding=0, size_hint_y = 2.1, size_hint_x = None, width=760)
        reminder_layout.add_widget(label_bottom)

        layout_plan = BoxLayout(orientation='vertical', spacing=0, padding=[0,0,0,0], width=780)
        layout_plan.add_widget(img)
        layout_plan.add_widget(use_layout)
        layout_plan.add_widget(reminder_layout)
        layout_plan.add_widget(btn_layout)
        
        popup = Popup(title='Information',
                      title_color=[0, 0, 0, 1],
                      title_font= 'Roboto-Bold',
                      title_size = '20sp',
                      content=layout_plan,
                      size_hint=(None, None),
                      size=(780, 460),
                      auto_dismiss= False
                      )

        popup.background = './asmcnc/apps/shapeCutter_app/img/popup_background.png'
        popup.separator_color = [249 / 255., 206 / 255., 29 / 255., 1.]
        popup.separator_height = '4dp'

        ok_button.bind(on_press=popup.dismiss)

        popup.open()
