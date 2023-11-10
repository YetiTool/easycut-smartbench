from datetime import datetime
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from asmcnc.skavaUI import popup_info
from asmcnc.apps.drywall_cutter_app import widget_xy_move_drywall
from asmcnc.apps.drywall_cutter_app.config import config_loader
from asmcnc.apps.drywall_cutter_app import screen_config_filechooser
Builder.load_string(
    """
<DrywallCutterScreen>:
    xy_move_container:xy_move_container
    tool_selection:tool_selection
    BoxLayout:
        orientation: 'vertical'
        BoxLayout:
            orientation: 'horizontal'
            padding: dp([0.00625*app.width, 0.0104166666667*app.height])
            spacing: dp(0.0125*app.width)
            Button:
                font_size: str(0.01875 * app.width) + 'sp'
                size_hint_x: 7
                text: 'Home'
                on_press: root.home()
            Button:
                font_size: str(0.01875 * app.width) + 'sp'
                size_hint_x: 7
                text: 'File'
                on_press: root.open_filechooser()
            Spinner:
                font_size: str(0.01875 * app.width) + 'sp'
                id: tool_selection
                size_hint_x: 7
                text: root.tool_options.keys()[0]
                values: root.tool_options.keys()
                on_text: root.select_tool()
            Spinner:
                font_size: str(0.01875 * app.width) + 'sp'
                size_hint_x: 7
                text: 'Shape'
                values: root.shape_options
                on_text: root.select_shape()
            Button:
                font_size: str(0.01875 * app.width) + 'sp'
                size_hint_x: 7
                text: 'Rotate'
                on_press: root.rotate_shape()
            Spinner:
                font_size: str(0.01875 * app.width) + 'sp'
                size_hint_x: 7
                text: 'Cut on line'
                text_size: self.size
                halign: 'center'
                valign: 'middle'
                values: root.line_cut_options
            Button:
                font_size: str(0.01875 * app.width) + 'sp'
                size_hint_x: 7
                text: 'Material setup'
                text_size: self.size
                halign: 'center'
                valign: 'middle'
                on_press: root.material_setup()
            Button:
                font_size: str(0.01875 * app.width) + 'sp'
                size_hint_x: 15
                text: 'STOP'
                on_press: root.stop()
            Button:
                font_size: str(0.01875 * app.width) + 'sp'
                size_hint_x: 7
                on_press: root.quit_to_lobby()
                text: 'Quit'
        BoxLayout:
            size_hint_y: 5
            orientation: 'horizontal'
            padding: dp([0.00625*app.width, 0.0104166666667*app.height])
            spacing: dp(0.0125*app.width)
            BoxLayout:
                size_hint_x: 55
                canvas.before:
                    Color:
                        rgba: hex('#E5E5E5FF')
                    Rectangle:
                        size: self.size
                        pos: self.pos
            BoxLayout:
                size_hint_x: 23
                orientation: 'vertical'
                spacing: dp(0.0208333333333*app.height)
                BoxLayout:
                    id: xy_move_container
                    size_hint_y: 31
                    padding:[dp(0), dp(0.0625*app.height)]
                    canvas.before:
                        Color:
                            rgba: hex('#E5E5E5FF')
                        Rectangle:
                            size: self.size
                            pos: self.pos
                BoxLayout:
                    size_hint_y: 7
                    orientation: 'horizontal'
                    spacing: dp(0.0125*app.width)
                    Button:
                        font_size: str(0.01875 * app.width) + 'sp'
                        text: 'Simulate'
                        on_press: root.simulate()
                    Button:
                        font_size: str(0.01875 * app.width) + 'sp'
                        text: 'Save'
                        on_press: root.save()
                    Button:
                        font_size: str(0.01875 * app.width) + 'sp'
                        text: 'Run'
                        on_press: root.run()
"""
    )


def log(message):
    timestamp = datetime.now()
    print timestamp.strftime('%H:%M:%S.%f')[:12] + ' ' + message


class DrywallCutterScreen(Screen):
    shape_options = ['Circle', 'Square', 'Line', 'Geberit']
    line_cut_options = ['Cut on line', 'Cut inside line', 'Cut outside line']
    dwt_config = config_loader.DWTConfig()
    tool_options = config_loader.DWTConfig().get_available_cutter_names()

    def __init__(self, **kwargs):
        super(DrywallCutterScreen, self).__init__(**kwargs)
        self.sm = kwargs['screen_manager']
        self.m = kwargs['machine']
        self.l = kwargs['localization']
        self.xy_move_widget = widget_xy_move_drywall.XYMoveDrywall(machine=
            self.m, screen_manager=self.sm)
        self.xy_move_container.add_widget(self.xy_move_widget)

    def home(self):
        self.m.request_homing_procedure('drywall_cutter', 'drywall_cutter')

    def select_tool(self):
        selected_tool_name = self.tool_selection.text
        self.dwt_config.load_cutter(self.tool_options[selected_tool_name])

    def select_shape(self):
        pass

    def rotate_shape(self):
        pass

    def material_setup(self):
        pass

    def stop(self):
        popup_info.PopupStop(self.m, self.sm, self.l)

    def quit_to_lobby(self):
        self.sm.current = 'lobby'

    def simulate(self):
        pass

    def save(self):
        pass

    def run(self):
        pass

    def open_filechooser(self):
        if not self.sm.has_screen('config_filechooser'):
            self.sm.add_widget(screen_config_filechooser.ConfigFileChooser(
                name='config_filechooser', screen_manager=self.sm,
                localization=self.l, callback=self.load_config))
        self.sm.current = 'config_filechooser'

    def load_config(self, config):
        """
        Used as the callback for the config filechooser screen.

        :param config: The path to the config file, including extension.
        """
        self.dwt_config.load_config(config)
        file_name_no_ext = config.split('/')[-1].split('.')[0]

    def on_leave(self, *args):
        self.dwt_config.save_temp_config()
