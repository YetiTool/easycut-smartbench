"""
Popup for assigning controller buttons/axes to an app's functions.

Works on whatever ControllerInputMap (input_map.py) it is given, so any app
gets the same UI: one row per action/axis showing the current binding, an
Assign button that waits for the next button press / stick push, plus reset
to defaults. Bindings are saved as soon as they're captured.

@author: Benji
"""
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView

from asmcnc.bluetooth_controller import input_map as input_map_module
from asmcnc.bluetooth_controller import sdl_joystick_hotplug

GREEN = [76 / 255., 175 / 255., 80 / 255., 1.]
RED = [230 / 255., 74 / 255., 25 / 255., 1.]
BLUE = [25 / 255., 118 / 255., 210 / 255., 1.]
GREY = [120 / 255., 120 / 255., 120 / 255., 1.]


class PopupInputMapping(Widget):

    def __init__(self, screen_manager, localization, input_map):
        self.sm = screen_manager
        self.l = localization
        self.input_map = input_map

        # Mappings are saved per controller model, so name the pad being configured
        device_name = sdl_joystick_hotplug.get_primary_device_name()
        if device_name:
            device_text = self.l.get_str('Configuring') + ': ' + device_name
        else:
            device_text = self.l.get_str('No controller detected - connect one to assign controls.')
        self.device_label = Label(size_hint_y=None, height=24, markup=True,
                                  color=[0.3, 0.3, 0.3, 1], font_size=14, text=device_text)

        self.status_label = Label(size_hint_y=None, height=30, markup=True,
                                  color=[0, 0, 0, 1], font_size=16,
                                  text=self.l.get_str('Tap Assign, then use the control you want.'))

        self.rows_container = GridLayout(cols=1, spacing=6, size_hint_y=None)
        self.rows_container.bind(minimum_height=self.rows_container.setter('height'))
        scroll = ScrollView(do_scroll_x=False, scroll_type=['content', 'bars'])
        scroll.add_widget(self.rows_container)

        reset_button = Button(text=self.l.get_bold('Reset defaults'), markup=True,
                              background_normal='', background_color=BLUE)
        reset_button.bind(on_press=self.reset_defaults)
        close_button = Button(text=self.l.get_bold('Close'), markup=True,
                              background_normal='', background_color=RED)
        close_button.bind(on_press=self.close)

        button_row = BoxLayout(orientation='horizontal', spacing=15, size_hint_y=None, height=50)
        button_row.add_widget(close_button)
        button_row.add_widget(reset_button)

        layout = BoxLayout(orientation='vertical', spacing=8, padding=[20, 10, 20, 15])
        layout.add_widget(self.device_label)
        layout.add_widget(self.status_label)
        layout.add_widget(scroll)
        layout.add_widget(button_row)

        self.popup = Popup(title=self.l.get_str('Controller buttons'),
                           title_color=[0, 0, 0, 1],
                           title_size='20sp',
                           content=layout,
                           size_hint=(None, None),
                           size=(560, 420),
                           auto_dismiss=False)
        self.popup.separator_color = BLUE
        self.popup.separator_height = '4dp'
        self.popup.background = './asmcnc/apps/shapeCutter_app/img/popup_background.png'

        self.rebuild_rows()
        self.popup.open()

    def close(self, *args):
        self.input_map.cancel_capture()
        self.popup.dismiss()

    def reset_defaults(self, *args):
        self.input_map.cancel_capture()
        self.input_map.reset_to_defaults()
        self.set_status(self.l.get_str('Defaults restored.'), GREY)
        self.rebuild_rows()

    # --- Rows -----------------------------------------------------------------

    def rebuild_rows(self):
        self.rows_container.clear_widgets()
        for action_id, display_name, _default, _callback in self.input_map.actions:
            self.rows_container.add_widget(self.build_row(
                display_name,
                self.input_map.describe_action_binding(action_id),
                input_map_module.BUTTON, action_id))
        for axis_name, display_name, _default in self.input_map.axes:
            self.rows_container.add_widget(self.build_row(
                display_name,
                self.input_map.describe_axis_binding(axis_name),
                input_map_module.AXIS, axis_name))

    def build_row(self, display_name, binding_description, kind, target_id):
        row = BoxLayout(orientation='horizontal', spacing=6, size_hint_y=None, height=44)

        name_label = Label(text=display_name, markup=True, halign='left', valign='middle',
                           color=[0, 0, 0, 1], font_size=16, size_hint_x=0.45)
        name_label.bind(size=name_label.setter('text_size'))

        binding_label = Label(text=self.l.get_str(binding_description), markup=True,
                              halign='left', valign='middle',
                              color=[0.25, 0.25, 0.25, 1], font_size=15, size_hint_x=0.3)
        binding_label.bind(size=binding_label.setter('text_size'))

        assign_button = Button(text=self.l.get_str('Assign'), size_hint_x=0.25,
                               background_normal='', background_color=BLUE)
        assign_button.bind(on_press=self.get_assign_func(kind, target_id, display_name))

        row.add_widget(name_label)
        row.add_widget(binding_label)
        row.add_widget(assign_button)
        return row

    # --- Capture ------------------------------------------------------------------

    def get_assign_func(self, kind, target_id, display_name):
        def assign(*args):
            if kind == input_map_module.BUTTON:
                prompt = self.l.get_str('Press the button to use for') + ' ' + display_name + '...'
            else:
                prompt = (self.l.get_str('Push the stick to use for') + ' ' + display_name
                          + ' ' + self.l.get_str('(right/up for normal direction)') + '...')
            self.set_status(prompt, GREEN)
            self.input_map.start_capture(kind, target_id, self.on_captured)
        return assign

    def on_captured(self, binding):
        self.set_status(self.l.get_str('Saved.'), GREY)
        self.rebuild_rows()

    def set_status(self, text, color):
        self.status_label.color = color
        self.status_label.text = text
