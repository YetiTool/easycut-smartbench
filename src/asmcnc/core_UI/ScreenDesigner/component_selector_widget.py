from kivy.app import App
from kivy.metrics import dp
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from mock.mock import MagicMock

from asmcnc.comms.localization import Localization
from asmcnc.core_UI.components.buttons.button_base import ButtonBase
from asmcnc.core_UI.components.labels.base_label import LabelBase
from asmcnc.core_UI.components.buttons.probe_button import ProbeButton
from asmcnc.core_UI.components.buttons.spindle_button import SpindleButton
from asmcnc.core_UI.components.buttons.vacuum_button import VacuumButton
from asmcnc.skavaUI.widget_xy_move import XYMove


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
        self.counter = 0
        self.sm = App.get_running_app().sm
        self.controller = controller
        self.localization = Localization()
        self.main_layout = FloatLayout(size=self.size, pos=self.pos)
        self.add_widget(self.main_layout)
        # Add label button:
        self.btn_add_label = ButtonBase(size=(70, 50), size_hint=(None, None), pos=(self.x + 10, self.y), id='DESIGNER_1', text='Label')
        self.btn_add_label.bind(on_press=self.add_label_to_selection)
        self.main_layout.add_widget(self.btn_add_label)
        # Add probe button:
        self.btn_probe_button = ButtonBase(size=(70, 50), size_hint=(None, None), pos=(self.x + 10, self.y + 50), id='DESIGNER_1', text='Probe')
        self.btn_probe_button.bind(on_press=self.add_probe_button_to_selection)
        self.main_layout.add_widget(self.btn_probe_button)
        # Add spindle button:
        self.btn_probe_button = ButtonBase(size=(70, 50), size_hint=(None, None), pos=(self.x + 10, self.y + 100), id='DESIGNER_1', text='Spindle')
        self.btn_probe_button.bind(on_press=self.add_spindle_button_to_selection)
        self.main_layout.add_widget(self.btn_probe_button)
        # Add vacuum button:
        self.btn_vacuum_button = ButtonBase(size=(70, 50), size_hint=(None, None), pos=(self.x + 10, self.y + 150), id='DESIGNER_1', text='vacuum')
        self.btn_vacuum_button.bind(on_press=self.add_vacuum_button_to_selection)
        self.main_layout.add_widget(self.btn_vacuum_button)
        # Add xy move button:
        self.btn_xy_move_button = ButtonBase(size=(70, 50), size_hint=(None, None), pos=(self.x + 80, self.y), id='DESIGNER_1', text='xy_move')
        self.btn_xy_move_button.bind(on_press=self.add_xy_move_button_to_selection)
        self.main_layout.add_widget(self.btn_xy_move_button)
        #  save button:
        self.btn_save = ButtonBase(size=(70, 50), size_hint=(None, None), pos=(self.x + 150, self.y), id='DESIGNER_1', text='save')
        self.btn_save.bind(on_press=lambda *args: self.controller.save_to_file())
        self.main_layout.add_widget(self.btn_save)

    def add_label_to_selection(self, *args):
        tmp = LabelBase(text='Inspector Widget was here!',
                        size_hint=(None, None),
                        size=(250, dp(20)),
                        font_size=dp(20),
                        pos=(60, 70),
                        # pos=(w.x + 10, w.y + 10),
                        color=(0.1, 1, 0.1, 1))
        self.controller.get_widget_to_add_to().add_widget(tmp)

    def add_probe_button_to_selection(self, *args):
        btn = ProbeButton(MagicMock(), self.sm, self.localization)
        btn.size_hint = [None, None]
        btn.size = [70, 70]
        btn.disabled = True
        btn.id = 'probe_button_' + str(self.counter)
        self.counter += 1
        self.controller.get_widget_to_add_to().add_widget(btn)

    def add_spindle_button_to_selection(self, *args):
        btn = SpindleButton(MagicMock(), MagicMock(), self.sm)
        btn.size_hint = [None, None]
        btn.size = [71, 72]
        btn.disabled = True
        btn.id = 'spindle_button_' + str(self.counter)
        self.counter += 1
        self.controller.get_widget_to_add_to().add_widget(btn)

    def add_vacuum_button_to_selection(self, *args):
        btn = VacuumButton(MagicMock(), MagicMock())
        btn.size_hint = [None, None]
        btn.size = [71, 72]
        btn.disabled = True
        btn.id = 'vacuum_button_' + str(self.counter)
        self.counter += 1
        self.controller.get_widget_to_add_to().add_widget(btn)

    def add_xy_move_button_to_selection(self, *args):
        btn = XYMove(machine=MagicMock(), screen_manager=MagicMock(), localization=self.localization)
        btn.size_hint = [None, None]
        btn.size = [270.5, 391.6]
        btn.id = 'xy_move_' + str(self.counter)
        self.counter += 1
        self.controller.get_widget_to_add_to().add_widget(btn)


