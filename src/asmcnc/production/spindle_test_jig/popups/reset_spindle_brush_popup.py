from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from kivy.clock import Clock

class ResetSpindleBrushPopup(Widget):
    def __init__(self, m, sm):
        self.m = m
        self.sm = sm

        description = "Would you like to reset the spindle's internal brush timer?"
        title_string = "Reset Spindle Brush"
        ok_string = "Yes"
        back_string = "No"

        img = Image(source="./asmcnc/apps/shapeCutter_app/img/error_icon.png", allow_stretch=False)
        label = Label(size_hint_y=2, text_size=(320, None), halign='center', valign='middle', text=description,
                      color=[0, 0, 0, 1], padding=[0, 0], markup=True)

        ok_button = Button(text=ok_string, markup=True)
        ok_button.background_normal = ''
        ok_button.background_color = [76 / 255., 175 / 255., 80 / 255., 1.]
        back_button = Button(text=back_string, markup=True)
        back_button.background_normal = ''
        back_button.background_color = [230 / 255., 74 / 255., 25 / 255., 1.]

        btn_layout = BoxLayout(orientation='horizontal', spacing=15, padding=[0, 5, 0, 0])
        btn_layout.add_widget(back_button)
        btn_layout.add_widget(ok_button)

        layout_plan = BoxLayout(orientation='vertical', spacing=10, padding=[30, 20, 30, 0])
        layout_plan.add_widget(img)
        layout_plan.add_widget(label)
        layout_plan.add_widget(btn_layout)

        popup = Popup(title=title_string,
                      title_color=[0, 0, 0, 1],
                      title_font='Roboto-Bold',
                      title_size='20sp',
                      content=layout_plan,
                      size_hint=(None, None),
                      size=(360, 360),
                      auto_dismiss=False
                      )

        popup.separator_color = [230 / 255., 74 / 255., 25 / 255., 1.]
        popup.separator_height = '4dp'
        popup.background = './asmcnc/apps/shapeCutter_app/img/popup_background.png'

        ok_button.bind(on_press=popup.dismiss)
        ok_button.bind(on_press=self.reset_spindle_brush_timer)
        back_button.bind(on_press=popup.dismiss)

        popup.open()

    def reset_spindle_brush_timer(self, *args):
        Clock.schedule_once(lambda dt: self.m.s.write_protocol(self.m.p.ResetDigitalSpindleBrushTime(), "RESET BRUSH TIMER"),
                            1)

        if self.sm.has_screen('spindle_test_1'):
            Clock.schedule_once(lambda dt: self.sm.get_screen('spindle_test_1').get_spindle_info(),
                                2)