from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.clock import Clock


class PopupSendData(Widget):
    def __init__(self, machine):
        self.m = machine

        total_rows = 0

        if self.m.s.yp:
            total_rows = len(self.m.s.yp.logger.logs)

        if total_rows == 0:
            return

        description = "Would you like to export data to GSheets?\nThere are currently " + str(total_rows) + " rows of data."
        title_string = 'Export?'
        ok_string = 'Yes'
        back_string = 'No (deletes data)'

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

        def on_send_button(*args):
            if self.m.s.yp:
                label.text = 'Exporting...'
                Clock.schedule_once(lambda dt: self.m.s.yp.logger.export_to_gsheet(), 1)
            popup.dismiss()

        def on_cancel_button(*args):
            if self.m.s.yp:
                self.m.s.yp.reset()
            popup.dismiss()

        ok_button.bind(on_press=on_send_button)
        back_button.bind(on_press=on_cancel_button)

        popup.open()