from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import  Button
from kivy.uix.image import Image

class PopupCalibrate(Widget):

    def __init__(self, screen_manager, localization):
        
        self.sm = screen_manager
        self.l = localization

        description = "Remove the belt, then press 'Calibrate' to continue"
        title_string = "Calibration"
        calibrate_string = "Calibrate"
        cancel_string = "Cancel"

        def do_calibrate(*args):
            self.sm.get_screen('mechanics').calibrate_motor()
        
        img = Image(source="./asmcnc/apps/shapeCutter_app/img/info_icon.png", allow_stretch=False)
        label = Label(size_hint_y=1.5, text_size=(480, None), halign='center', valign='middle', text=description, color=[0,0,0,1], padding=[0,0], markup = True)

        ok_button = Button(text=calibrate_string, markup = True)
        ok_button.background_normal = ''
        ok_button.background_color = [76 / 255., 175 / 255., 80 / 255., 1.]
        ok_button.bold = True
        cancel_button = Button(text=cancel_string, markup = True)
        cancel_button.background_normal = ''
        cancel_button.background_color = [230 / 255., 74 / 255., 25 / 255., 1.]
        cancel_button.bold = True

        btn_layout = BoxLayout(orientation='horizontal', spacing=10, padding=[0,10,0,0])
        btn_layout.add_widget(cancel_button)
        btn_layout.add_widget(ok_button)
        
        layout_plan = BoxLayout(orientation='vertical', spacing=10, padding=[20,10,20,10])
        layout_plan.add_widget(img)
        layout_plan.add_widget(label)
        layout_plan.add_widget(btn_layout)
        
        popup = Popup(title=title_string,
                      title_color=[0, 0, 0, 1],
                      title_size = '20sp',
                      content=layout_plan,
                      size_hint=(None, None),
                      size=(540, 400),
                      auto_dismiss= False
                      )

        popup.background = './asmcnc/apps/shapeCutter_app/img/popup_background.png'
        popup.separator_color = [249 / 255., 206 / 255., 29 / 255., 1.]
        popup.separator_height = '4dp'

        ok_button.bind(on_press=do_calibrate)
        ok_button.bind(on_press=popup.dismiss)
        cancel_button.bind(on_press=popup.dismiss)

        popup.open()


class PopupPhaseTwo(Widget):

    def __init__(self, screen_manager, localization):
        
        self.sm = screen_manager
        self.l = localization

        description = "Press 'Continue' to proceed to fast run. Watch and listen for a stall throughout."
        title_string = "Phase Two"
        ok_string = "Continue"

        def proceed_to_phase_two(*args):
            self.sm.get_screen('mechanics').phase_two()
        
        img = Image(source="./asmcnc/apps/shapeCutter_app/img/info_icon.png", allow_stretch=False)
        label = Label(size_hint_y=1.5, text_size=(480, None), halign='center', valign='middle', text=description, color=[0,0,0,1], padding=[0,0], markup = True)

        ok_button = Button(text=ok_string, markup = True)
        ok_button.background_normal = ''
        ok_button.background_color = [76 / 255., 175 / 255., 80 / 255., 1.]
        ok_button.bold = True
        
        layout_plan = BoxLayout(orientation='vertical', spacing=10, padding=[20,10,20,10])
        layout_plan.add_widget(img)
        layout_plan.add_widget(label)
        layout_plan.add_widget(ok_button)
        
        popup = Popup(title=title_string,
                      title_color=[0, 0, 0, 1],
                      title_size = '20sp',
                      content=layout_plan,
                      size_hint=(None, None),
                      size=(540, 400),
                      auto_dismiss= False
                      )

        popup.background = './asmcnc/apps/shapeCutter_app/img/popup_background.png'
        popup.separator_color = [249 / 255., 206 / 255., 29 / 255., 1.]
        popup.separator_height = '4dp'

        ok_button.bind(on_press=proceed_to_phase_two)
        ok_button.bind(on_press=popup.dismiss)

        popup.open()
