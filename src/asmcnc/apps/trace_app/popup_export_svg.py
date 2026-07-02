"""
Popup for naming an exported SVG trace capture before it is saved.

@author: Benji
"""
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput


class PopupExportSvg(Widget):
    def __init__(self, screen_manager, localization, keyboard, default_name, on_confirm):
        self.sm = screen_manager
        self.l = localization
        self.kb = keyboard
        self.on_confirm = on_confirm

        title_string = self.l.get_str('Export SVG')
        save_string = self.l.get_bold('Save')
        cancel_string = self.l.get_bold('Cancel')

        label = Label(size_hint_y=None, height=40, text=self.l.get_str('Name this trace capture:'),
                      color=[0, 0, 0, 1], markup=True)
        textinput = TextInput(text=default_name, size_hint_y=None, height=60, multiline=False)

        self.kb.setup_text_inputs([textinput])

        def confirm(*args):
            self.on_confirm(textinput.text)

        save_button = Button(text=save_string, markup=True)
        save_button.background_normal = ''
        save_button.background_color = [76 / 255., 175 / 255., 80 / 255., 1.]
        cancel_button = Button(text=cancel_string, markup=True)
        cancel_button.background_normal = ''
        cancel_button.background_color = [230 / 255., 74 / 255., 25 / 255., 1.]

        btn_layout = BoxLayout(orientation='horizontal', spacing=15, padding=[0, 5, 0, 0])
        btn_layout.add_widget(cancel_button)
        btn_layout.add_widget(save_button)

        layout_plan = BoxLayout(orientation='vertical', spacing=10, padding=[30, 20, 30, 20])
        layout_plan.add_widget(label)
        layout_plan.add_widget(textinput)
        layout_plan.add_widget(btn_layout)

        popup = Popup(title=title_string,
                      title_color=[0, 0, 0, 1],
                      title_size='20sp',
                      content=layout_plan,
                      size_hint=(None, None),
                      size=(500, 300),
                      auto_dismiss=False)

        popup.separator_color = [25 / 255., 118 / 255., 210 / 255., 1.]
        popup.separator_height = '4dp'
        popup.background = './asmcnc/apps/shapeCutter_app/img/popup_background.png'

        save_button.bind(on_press=confirm)
        save_button.bind(on_press=popup.dismiss)
        cancel_button.bind(on_press=popup.dismiss)

        popup.open()
