from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from kivy.uix.scrollview import ScrollView

from asmcnc.production.spindle_test_jig.popups.reset_spindle_brush_popup import ResetSpindleBrushPopup


class PostTestSummaryPopup(Widget):
    def __init__(self, m, sm, fail_reasons):
        self.m = m
        self.sm = sm

        pass_test = len(fail_reasons) == 0

        description = ""

        if pass_test:
            description = "Spindle test passed!"
        else:
            description = "Spindle test failed. Following issues were found:\n"

            for fail_reason in fail_reasons:
                description += str(fail_reason) + "\n"

        title_string = "Spindle Test Result: " + "passed" if pass_test else "fail"
        ok_string = "OK"

        img = Image(source="./asmcnc/apps/shapeCutter_app/img/error_icon.png", allow_stretch=False)
        label = Label(size_hint_y=2, text_size=(320, None), halign='center', valign='middle', text=description,
                      color=[0, 0, 0, 1], padding=[0, 0], markup=True)

        ok_button = Button(text=ok_string, markup=True)
        ok_button.background_normal = ''
        ok_button.background_color = [76 / 255., 175 / 255., 80 / 255., 1.]

        btn_layout = BoxLayout(orientation='horizontal', spacing=15, padding=[0, 5, 0, 0])
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
        ok_button.bind(on_press=self.open_spindle_brush_popup)
        popup.open()

    def open_spindle_brush_popup(self, *args):
        ResetSpindleBrushPopup(self.m, self.sm)