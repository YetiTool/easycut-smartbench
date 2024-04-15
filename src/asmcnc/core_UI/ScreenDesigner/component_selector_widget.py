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
from asmcnc.core_UI.hoverable import InspectorSingleton
import asmcnc.core_UI.ScreenDesigner.string_builder as sb
import asmcnc.core_UI.path_utils as pu
from asmcnc.skavaUI.widget_xy_move import XYMove

GENERATED_FILES_FOLDER = pu.get_path('generated_screens')


class ComponentSelectorWidget(Widget):
    """
    This popup is shown when [w] is pressed.
    It offers various options to add widgets to the current screen.
    saves the screen as python code.
    """
    def __init__(self):
        super(ComponentSelectorWidget, self).__init__(size_hint=(None, None),
                                                     size=(400, 300),
                                                     pos=(800, 0))
        self.counter = 0
        self.is_opened = False
        self.sm = App.get_running_app().sm
        self.localization = Localization()
        self.inspector = InspectorSingleton()
        self.widget_to_add_to = None
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
        # Add back button:
        self.btn_back_button = ButtonBase(size=(70, 50), size_hint=(None, None), pos=(self.x + 220, self.y), id='DESIGNER_1', text='back')
        self.btn_back_button.bind(on_press=self.back_to_main_screen)
        self.main_layout.add_widget(self.btn_back_button)
        #  save button:
        self.btn_save = ButtonBase(size=(70, 50), size_hint=(None, None), pos=(self.x + 150, self.y), id='DESIGNER_1', text='save')
        self.btn_save.bind(on_press=self.save)
        self.main_layout.add_widget(self.btn_save)

    def back_to_main_screen(self, *args):
        self.sm.current = 'ScreenDesigner'

    def save(self, *args):
        """
        Takes generated python code from the StringBuilder and saves it to a file.
        The filename is converted from CamelCase to snake_case.
        """
        s = sb.get_python_code_from_screen(self.widget_to_add_to)
        # e.g. turn "MyFirstScreen" into "my_first_screen":
        filename = App.get_running_app().screenname_to_filename(sb.get_screen(self.widget_to_add_to).name)
        path = pu.join(GENERATED_FILES_FOLDER, filename + '.py')
        with open(path, 'w') as f:
            f.write(s)

    def add_label_to_selection(self, *args):
        w = self.widget_to_add_to  # if self.widget_to_add_to else self.inspector.widget
        tmp = LabelBase(text='Inspector Widget was here!',
                        size_hint=(None, None),
                        size=(250, dp(20)),
                        font_size=dp(20),
                        pos=(60, 70),
                        # pos=(w.x + 10, w.y + 10),
                        color=(0.1, 1, 0.1, 1))
        w.add_widget(tmp)

    def add_probe_button_to_selection(self, *args):
        w = self.widget_to_add_to  # if self.widget_to_add_to else self.inspector.widget
        btn = ProbeButton(MagicMock(), self.sm, self.localization)
        btn.size_hint = [None, None]
        btn.size = [70, 70]
        btn.disabled = True
        btn.id = 'probe_button_' + str(self.counter)
        self.counter += 1
        w.add_widget(btn)

    def add_spindle_button_to_selection(self, *args):
        w = self.widget_to_add_to  # if self.widget_to_add_to else self.inspector.widget
        btn = SpindleButton(MagicMock(), MagicMock(), self.sm)
        btn.size_hint = [None, None]
        btn.size = [71, 72]
        btn.disabled = True
        btn.id = 'spindle_button_' + str(self.counter)
        self.counter += 1
        w.add_widget(btn)

    def add_vacuum_button_to_selection(self, *args):
        w = self.widget_to_add_to  # if self.widget_to_add_to else self.inspector.widget
        btn = VacuumButton(MagicMock(), MagicMock())
        btn.size_hint = [None, None]
        btn.size = [71, 72]
        btn.disabled = True
        btn.id = 'vacuum_button_' + str(self.counter)
        self.counter += 1
        w.add_widget(btn)

    def add_xy_move_button_to_selection(self, *args):
        w = self.widget_to_add_to  # if self.widget_to_add_to else self.inspector.widget
        btn = XYMove(machine=MagicMock(), screen_manager=MagicMock(), localization=self.localization)
        btn.size_hint = [None, None]
        btn.size = [270.5, 391.6]
        btn.id = 'xy_move_' + str(self.counter)
        self.counter += 1
        w.add_widget(btn)


