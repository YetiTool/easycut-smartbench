from kivy.app import App
from kivy.metrics import dp
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from mock.mock import MagicMock

from asmcnc.comms.localization import Localization
from asmcnc.comms.logging_system.logging_system import Logger
from asmcnc.core_UI.components.buttons.button_base import ButtonBase, ImageButtonBase
from asmcnc.core_UI.components.labels.base_label import LabelBase
from asmcnc.core_UI.components.buttons.probe_button import ProbeButton
from asmcnc.core_UI.components.buttons.spindle_button import SpindleButton
from asmcnc.core_UI.components.buttons.vacuum_button import VacuumButton
from asmcnc.core_UI.components.text_inputs.base_text_input import TextInputBase
from asmcnc.core_UI.hoverable import InspectorSingleton
from asmcnc.skavaUI.widget_xy_move import XYMove
from asmcnc.core_UI import path_utils as pu


class ComponentSelectorWidget(Widget):
    """
    This popup is shown when [w] is pressed.
    It offers various options to add widgets to the current screen.
    saves the screen as python code.
    """
    def __init__(self, controller):
        super(ComponentSelectorWidget, self).__init__(size_hint=(None, None),
                                                     size=(400, 300),
                                                     pos=(800, 0))
        self.sm = App.get_running_app().sm
        self.controller = controller
        self.localization = Localization()
        self.main_layout = FloatLayout(size=self.size, pos=self.pos)
        self.add_widget(self.main_layout)
        # Add label button:
        self.btn_add_label = ButtonBase(size=(70, 50), size_hint=(None, None), pos=(self.x + 10, self.y), id='DESIGNER', text='Label')
        self.btn_add_label.bind(on_press=self.add_label_to_selection)
        self.main_layout.add_widget(self.btn_add_label)
        # Add probe button:
        self.btn_probe_button = ButtonBase(size=(70, 50), size_hint=(None, None), pos=(self.x + 10, self.y + 50), id='DESIGNER', text='Probe')
        self.btn_probe_button.bind(on_press=self.add_probe_button_to_selection)
        self.main_layout.add_widget(self.btn_probe_button)
        # Add spindle button:
        self.btn_probe_button = ButtonBase(size=(70, 50), size_hint=(None, None), pos=(self.x + 10, self.y + 100), id='DESIGNER', text='Spindle')
        self.btn_probe_button.bind(on_press=self.add_spindle_button_to_selection)
        self.main_layout.add_widget(self.btn_probe_button)
        # Add vacuum button:
        self.btn_vacuum_button = ButtonBase(size=(70, 50), size_hint=(None, None), pos=(self.x + 10, self.y + 150), id='DESIGNER', text='vacuum')
        self.btn_vacuum_button.bind(on_press=self.add_vacuum_button_to_selection)
        self.main_layout.add_widget(self.btn_vacuum_button)
        # Add xy move button:
        self.btn_xy_move_button = ButtonBase(size=(70, 50), size_hint=(None, None), pos=(self.x + 80, self.y), id='DESIGNER', text='xy_move')
        self.btn_xy_move_button.bind(on_press=self.add_xy_move_button_to_selection)
        self.main_layout.add_widget(self.btn_xy_move_button)
        # Add text_input button:
        self.btn_text_input = ButtonBase(size=(70, 50), size_hint=(None, None), pos=(self.x + 80, self.y + 50), id='DESIGNER', text='input')
        self.btn_text_input.bind(on_press=self.add_text_input_to_selection)
        self.main_layout.add_widget(self.btn_text_input)
        # Add button button:
        self.btn_button = ButtonBase(size=(70, 50), size_hint=(None, None), pos=(self.x + 80, self.y + 100), id='DESIGNER', text='button')
        self.btn_button.bind(on_press=self.add_button_to_selection)
        self.main_layout.add_widget(self.btn_button)
        #  save button:
        self.btn_save = ButtonBase(size=(70, 50), size_hint=(None, None), pos=(self.x + 290, self.y), id='DESIGNER', text='save')
        self.btn_save.bind(on_press=lambda *args: self.controller.save_to_file())
        self.main_layout.add_widget(self.btn_save)
        # text text_input
        self.label_text = LabelBase(size=(100, 30), size_hint=(None, None), pos=(self.x + 10, self.y + 250), id='DESIGNER', text='text:')
        self.main_layout.add_widget(self.label_text)
        self.text_text_input = TextInputBase(size=(200, 30), size_hint=(None, None), pos=(self.x + 110, self.y + 250), id='DESIGNER', text='text to show')
        self.text_text_input.bind(focus=self.text_input_focus)
        self.main_layout.add_widget(self.text_text_input)
        # source text_input
        self.label_source = LabelBase(size=(100, 30), size_hint=(None, None), pos=(self.x + 10, self.y + 290), id='DESIGNER', text='source:')
        self.main_layout.add_widget(self.label_source)
        self.source_text_input = TextInputBase(size=(200, 30), size_hint=(None, None), pos=(self.x + 110, self.y + 290), id='DESIGNER', text='source filename')
        self.source_text_input.bind(focus=self.text_input_focus)
        self.main_layout.add_widget(self.source_text_input)
        # size text_input
        self.label_size = LabelBase(size=(100, 30), size_hint=(None, None), pos=(self.x + 10, self.y + 330), id='DESIGNER', text='size:')
        self.main_layout.add_widget(self.label_size)
        self.size_text_input = TextInputBase(size=(200, 30), size_hint=(None, None), pos=(self.x + 110, self.y + 330), id='DESIGNER', text='100,100')
        self.size_text_input.bind(focus=self.text_input_focus)
        self.main_layout.add_widget(self.size_text_input)
        # pos text_input
        self.label_pos = LabelBase(size=(100, 30), size_hint=(None, None), pos=(self.x + 10, self.y + 370), id='DESIGNER', text='pos:')
        self.main_layout.add_widget(self.label_pos)
        self.pos_text_input = TextInputBase(size=(200, 30), size_hint=(None, None), pos=(self.x + 110, self.y + 370), id='DESIGNER', text='0,0')
        self.pos_text_input.bind(focus=self.text_input_focus)
        self.main_layout.add_widget(self.pos_text_input)

    def text_input_focus(self, instance, state):
        """
        Is called when a text_input gains or loses focus, to disable inspector key inputs while typing.
        """
        if state:
            InspectorSingleton().disable_key_input()
        else:
            InspectorSingleton().enable_key_input()

    def add_text_input_to_selection(self, *args):
        tmp = TextInputBase(size_hint=(None, None))
        tmp.size = self.controller.convert_to_value_list(self.size_text_input.text)
        tmp.pos = self.controller.convert_to_value_list(self.pos_text_input.text)
        self.controller.get_widget_to_add_to().add_widget(tmp)
        
    def add_button_to_selection(self, *args):
        tmp = ImageButtonBase(text=self.text_text_input.text,
                              size_hint=(None, None))
        tmp.size = self.controller.convert_to_value_list(self.size_text_input.text)
        tmp.pos = self.controller.convert_to_value_list(self.pos_text_input.text)
        tmp.source = self.controller.get_image_path(self.source_text_input.text)
        self.controller.get_widget_to_add_to().add_widget(tmp)

    def add_label_to_selection(self, *args):
        tmp = LabelBase(text=self.text_text_input.text,
                        size_hint=(None, None),
                        font_size=dp(20),
                        color=(1, 1, 1, 1))
        tmp.size = self.controller.convert_to_value_list(self.size_text_input.text)
        tmp.pos = self.controller.convert_to_value_list(self.pos_text_input.text)
        self.controller.get_widget_to_add_to().add_widget(tmp)

    def add_probe_button_to_selection(self, *args):
        btn = ProbeButton(MagicMock(), self.sm, self.localization)
        btn.size_hint = [None, None]
        btn.size = [70, 70]
        btn.disabled = True
        btn.id = 'probe_button_' + str(self.controller.counter)
        self.controller.counter += 1
        self.controller.get_widget_to_add_to().add_widget(btn)

    def add_spindle_button_to_selection(self, *args):
        btn = SpindleButton(MagicMock(), MagicMock(), self.sm)
        btn.size_hint = [None, None]
        btn.size = [71, 72]
        btn.disabled = True
        btn.id = 'spindle_button_' + str(self.controller.counter)
        self.controller.counter += 1
        self.controller.get_widget_to_add_to().add_widget(btn)

    def add_vacuum_button_to_selection(self, *args):
        btn = VacuumButton(MagicMock(), MagicMock())
        btn.size_hint = [None, None]
        btn.size = [71, 72]
        btn.disabled = True
        btn.id = 'vacuum_button_' + str(self.controller.counter)
        self.controller.counter += 1
        self.controller.get_widget_to_add_to().add_widget(btn)

    def add_xy_move_button_to_selection(self, *args):
        btn = XYMove(machine=MagicMock(), screen_manager=MagicMock(), localization=self.localization)
        btn.size_hint = [None, None]
        btn.size = [270.5, 391.6]
        btn.id = 'xy_move_' + str(self.controller.counter)
        self.controller.counter += 1
        self.controller.get_widget_to_add_to().add_widget(btn)


