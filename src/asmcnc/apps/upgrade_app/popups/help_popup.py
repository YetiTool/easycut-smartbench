from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget


class HelpPopup(Widget):
    def __init__(self):
        title_string = "Info"
        ok_string = "Ok"

        step_one = "1. Insert your SC2 spindle motor"
        step_two = "2. Type in your unlock code into the box"
        step_three = "3. Press 'enter' on the keyboard"

        label_step_one = Label(size_hint_y=2, text_size=(320, None), halign='center', valign='middle', text=step_one,
                      color=[0, 0, 0, 1], padding=[0, 0], markup=True)
        label_step_two = Label(size_hint_y=2, text_size=(320, None), halign='center', valign='middle', text=step_two,
                               color=[0, 0, 0, 1], padding=[0, 0], markup=True)
        label_step_three = Label(size_hint_y=2, text_size=(320, None), halign='center', valign='middle', text=step_three,
                               color=[0, 0, 0, 1], padding=[0, 0], markup=True)

        ok_button = Button(text=ok_string, markup=True)
        ok_button.background_normal = ''
        ok_button.background_color = [76 / 255., 175 / 255., 80 / 255., 1.]

        btn_layout = BoxLayout(orientation='horizontal', spacing=15, padding=[0, 5, 0, 0])
        btn_layout.add_widget(ok_button)

        layout_plan = BoxLayout(orientation='vertical', spacing=10, padding=[30, 20, 30, 0])
        layout_plan.add_widget(label_step_one)
        layout_plan.add_widget(label_step_two)
        layout_plan.add_widget(label_step_three)
        layout_plan.add_widget(btn_layout)

        popup = Popup(title=title_string,
                      title_color=[0, 0, 0, 1],
                      title_font='Roboto-Bold',
                      title_size='20sp',
                      content=layout_plan,
                      size_hint=(None, None),
                      size=(480, 360),
                      auto_dismiss=False
                      )

        popup.separator_color = [230 / 255., 74 / 255., 25 / 255., 1.]
        popup.separator_height = '4dp'
        popup.background = './asmcnc/apps/shapeCutter_app/img/popup_background.png'

        ok_button.bind(on_press=popup.dismiss)

        popup.open()