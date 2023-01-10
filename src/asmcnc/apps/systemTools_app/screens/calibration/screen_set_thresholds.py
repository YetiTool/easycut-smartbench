from kivy.uix.screenmanager import Screen
from kivy.lang import Builder

from asmcnc.apps.systemTools_app.screens.popup_system import PopupConfirmStoreCurrentValues
from asmcnc.skavaUI.popup_info import PopupWait
from kivy.clock import Clock

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
        PopupConfirmStoreCurrentValues(self.m, self.systemtools_sm.sm, self.l, self)

    def back_to_fac_settings(self):
        self.systemtools_sm.open_factory_settings_screen()

    def store_values_and_wait_for_handshake(self):
        self.wait_popup_for_tmc_read_in = PopupWait(self.systemtools_sm.sm,  self.l)
        Clock.schedule_once(self.do_tmc_value_store, 0.2)

    def do_tmc_value_store(self, dt=0):
        self.m.store_tmc_params_in_eeprom_and_handshake()
        self.wait_while_values_stored_and_read_back_in()

    def wait_while_values_stored_and_read_back_in(self, dt=0):
        if self.m.TMC_registers_have_been_read_in(): 
            self.wait_popup_for_tmc_read_in.popup.dismiss()
            self.wait_popup_for_tmc_read_in = None
        else: 
            Clock.schedule_once(self.wait_while_values_stored_and_read_back_in, 0.2)
