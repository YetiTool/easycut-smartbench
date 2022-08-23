from kivy.uix.screenmanager import Screen
from kivy.lang import Builder

from asmcnc.apps.systemTools_app.screens.popup_system import PopupConfirmStoreCurrentValues

Builder.load_string("""
<SetThresholdsScreen>:

    x_threshold_input:x_threshold_input
    y_threshold_input:y_threshold_input
    z_threshold_input:z_threshold_input

    BoxLayout:
        orientation: 'vertical'

        BoxLayout:
            size_hint_y: 5
            orientation: 'vertical'
            padding: dp(30)
            spacing: dp(30)

            GridLayout:
                size_hint_y: 1.5
                cols: 3
                rows: 3
                spacing: dp(10)

                Label:
                    text: 'X:'

                TextInput:
                    id: x_threshold_input
                    input_filter: 'int'
                    multiline: False

                Button:
                    text: 'Set'
                    on_press: root.set_threshold('X', x_threshold_input.text)

                Label:
                    text: 'Y:'

                TextInput:
                    id: y_threshold_input
                    input_filter: 'int'
                    multiline: False

                Button:
                    text: 'Set'
                    on_press: root.set_threshold('Y', y_threshold_input.text)

                Label:
                    text: 'Z:'

                TextInput:
                    id: z_threshold_input
                    input_filter: 'int'
                    multiline: False

                Button:
                    text: 'Set'
                    on_press: root.set_threshold('Z', z_threshold_input.text)

            BoxLayout:
                orientation: 'vertical'

                Button:
                    text: 'Store params'
                    on_press: root.store_parameters()

        Button:
            text: 'Factory settings'
            on_press: root.back_to_fac_settings()

""")

class SetThresholdsScreen(Screen):

    def __init__(self, **kwargs):
        super(SetThresholdsScreen, self).__init__(**kwargs)

        self.systemtools_sm = kwargs['systemtools']
        self.m = kwargs['m']
        self.l = kwargs['l']

    def set_threshold(self, axis, value):
        self.m.set_threshold_for_axis(axis, int(value))

    def store_parameters(self):
        PopupConfirmStoreCurrentValues(self.m, self.systemtools_sm.sm, self.l)

    def back_to_fac_settings(self):
        self.systemtools_sm.open_factory_settings_screen()
