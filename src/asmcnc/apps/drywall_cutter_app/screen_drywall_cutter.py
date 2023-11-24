from datetime import datetime

from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

from asmcnc.skavaUI import popup_info
from asmcnc.apps.drywall_cutter_app import widget_xy_move_drywall
from asmcnc.apps.drywall_cutter_app import widget_drywall_shape_display
from asmcnc.apps.drywall_cutter_app import material_setup_popup
from asmcnc.apps.drywall_cutter_app.config import config_loader
from asmcnc.apps.drywall_cutter_app import screen_config_filechooser
from asmcnc.apps.drywall_cutter_app import screen_config_filesaver
from asmcnc.apps.drywall_cutter_app.image_dropdown import ImageDropDownButton

from engine import GCodeEngine

Builder.load_string("""
<DrywallCutterScreen>:
    tool_selection:tool_selection
    shape_selection:shape_selection
    rotate_button:rotate_button
    toolpath_selection:toolpath_selection
    shape_display_container:shape_display_container
    xy_move_container:xy_move_container
    BoxLayout:
        orientation: 'vertical'
        BoxLayout:
            orientation: 'horizontal'
            padding: dp(5)
            spacing: dp(10)
            Button:
                size_hint_x: 7
                text: 'Home'
                on_press: root.home()
            Button:
                size_hint_x: 7
                text: 'File'
                on_press: root.open_filechooser()
            ImageDropDownButton:
                id: tool_selection
                callback: root.select_tool
                key_name: 'cutter_path'
                image_dict: root.tool_options
                size_hint_x: 7
                allow_stretch: True
                source: './asmcnc/apps/drywall_cutter_app/config/cutters/images/tool_6mm.png'
            ImageDropDownButton:
                id: shape_selection
                callback: root.select_shape
                image_dict: root.shape_options_dict
                key_name: 'key'
                size_hint_x: 7
                allow_stretch: True
                source: './asmcnc/apps/drywall_cutter_app/img/square_shape_button.png'
            Button:
                id: rotate_button
                size_hint_x: 7
                text: 'Rotate'
                on_press: root.rotate_shape()
            ImageDropDownButton:
                id: toolpath_selection
                size_hint_x: 7
                callback: root.select_toolpath
                key_name: 'key'
                image_dict: root.toolpath_offset_options_dict
                allow_stretch: True
                source: './asmcnc/apps/drywall_cutter_app/img/toolpath_offset_inside_button.png'
            Button:
                size_hint_x: 7
                text: 'Material setup'
                text_size: self.size
                halign: 'center'
                valign: 'middle'
                on_press: root.material_setup()
            Button:
                size_hint_x: 15
                text: 'STOP'
                on_press: root.stop()
            Button:
                size_hint_x: 7
                on_press: root.quit_to_lobby()
                text: 'Quit'
        BoxLayout:
            size_hint_y: 5
            orientation: 'horizontal'
            padding: dp(5)
            spacing: dp(10)
            BoxLayout:
                id: shape_display_container
                size_hint_x: 55
            BoxLayout:
                size_hint_x: 23
                orientation: 'vertical'
                spacing: dp(10)
                BoxLayout:
                    id: xy_move_container
                    size_hint_y: 31
                    padding: [dp(0), dp(30)]
                    canvas.before:
                        Color:
                            rgba: hex('#E5E5E5FF')
                        Rectangle:
                            size: self.size
                            pos: self.pos
                BoxLayout:
                    size_hint_y: 7
                    orientation: 'horizontal'
                    spacing: dp(10)
                    Button:
                        text: 'Simulate'
                        on_press: root.simulate()
                    Button:
                        text: 'Save'
                        on_press: root.save()
                    Button:
                        text: 'Run'
                        on_press: root.run()
""")


def log(message):
    timestamp = datetime.now()
    print (timestamp.strftime('%H:%M:%S.%f')[:12] + ' ' + message)


class DrywallCutterScreen(Screen):
    tool_options = ['6mm', '8mm', 'V groove']
    shape_options = ['circle', 'square', 'rectangle', 'line', 'geberit']
    line_cut_options = ['inside', 'on', 'outside']
    rotation = 'horizontal'
    dwt_config = config_loader.DWTConfig()
    tool_options = dwt_config.get_available_cutter_names()
    shape_options_dict = {
        'circle': {
            'image_path': './asmcnc/apps/drywall_cutter_app/img/circle_shape_button.png',
        },
        'square': {
            'image_path': './asmcnc/apps/drywall_cutter_app/img/square_shape_button.png',
        },
        'line': {
            'image_path': './asmcnc/apps/drywall_cutter_app/img/line_shape_button.png',
        },
        'geberit': {
            'image_path': './asmcnc/apps/drywall_cutter_app/img/geberit_shape_button.png',
        },
        'rectangle': {
            'image_path': './asmcnc/apps/drywall_cutter_app/img/rectangle_shape_button.png',
        },
    }
    toolpath_offset_options_dict = {
        'inside': {
            'image_path': './asmcnc/apps/drywall_cutter_app/img/toolpath_offset_inside_button.png',
        },
        'outside': {
            'image_path': './asmcnc/apps/drywall_cutter_app/img/toolpath_offset_outside_button.png',
        },
        'on': {
            'image_path': './asmcnc/apps/drywall_cutter_app/img/toolpath_offset_on_button.png',
        },
    }

    def __init__(self, **kwargs):
        super(DrywallCutterScreen, self).__init__(**kwargs)

        self.sm = kwargs['screen_manager']
        self.m = kwargs['machine']
        self.l = kwargs['localization']
        self.kb = kwargs['keyboard']

        self.engine = GCodeEngine(self.dwt_config)

        # XY move widget
        self.xy_move_widget = widget_xy_move_drywall.XYMoveDrywall(machine=self.m, screen_manager=self.sm, localization=self.l)
        self.xy_move_container.add_widget(self.xy_move_widget)

        self.drywall_shape_display_widget = widget_drywall_shape_display.DrywallShapeDisplay(machine=self.m, screen_manager=self.sm, dwt_config=self.dwt_config, engine=self.engine)
        self.shape_display_container.add_widget(self.drywall_shape_display_widget)

        self.select_shape('circle')

        self.show_tool_image()
        self.show_toolpath_image()

    def home(self):
        self.m.request_homing_procedure('drywall_cutter', 'drywall_cutter')

    def select_tool(self, cutter_file, *args):
        self.dwt_config.load_cutter(cutter_file)
        self.show_tool_image()

    def show_tool_image(self):
        self.tool_selection.source = self.dwt_config.active_cutter.image_path

    def select_shape(self, shape):
        self.dwt_config.on_parameter_change('shape_type', shape.lower())

        self.shape_selection.source = self.shape_options_dict[shape.lower()]['image_path']

        if shape in ['line', 'geberit']:
            # Only on line available for these options
            new_toolpath = 'on'
            self.toolpath_selection.disabled = True
        else:
            # Default to cut inside line
            new_toolpath = 'inside'
            self.toolpath_selection.disabled = False

        if shape in ['rectangle', 'line']:
            self.rotate_button.disabled = False
        else:
            self.rotate_button.disabled = True

        self.rotation = 'horizontal'
        self.drywall_shape_display_widget.select_shape(shape, self.rotation)
        self.select_toolpath(new_toolpath)

        if self.drywall_shape_display_widget.rotation_required():
            self.rotate_shape(swap_lengths=False)

    def rotate_shape(self, swap_lengths=True):
        if self.rotation == 'horizontal':
            self.rotation = 'vertical'
        else:
            self.rotation = 'horizontal'
        self.drywall_shape_display_widget.select_shape(self.dwt_config.active_config.shape_type, self.rotation, swap_lengths=swap_lengths)
        self.select_toolpath(self.dwt_config.active_config.toolpath_offset)

    def material_setup(self):
        material_setup_popup.CuttingDepthsPopup(self.l, self.kb, self.dwt_config)

    def select_toolpath(self, toolpath):
        self.dwt_config.on_parameter_change('toolpath_offset', toolpath)

        self.drywall_shape_display_widget.select_toolpath(self.dwt_config.active_config.shape_type, toolpath, self.rotation)

        self.show_toolpath_image()

    def show_toolpath_image(self):
        self.toolpath_selection.source = self.toolpath_offset_options_dict[self.dwt_config.active_config.toolpath_offset]['image_path']

    def stop(self):
        popup_info.PopupStop(self.m, self.sm, self.l)

    def quit_to_lobby(self):
        self.sm.current = 'lobby'

    def simulate(self):
        pass

    def save(self):
        if not self.sm.has_screen('config_filesaver'):
            self.sm.add_widget(screen_config_filesaver.ConfigFileSaver(name='config_filesaver',
                                                                       screen_manager=self.sm,
                                                                       localization=self.l,
                                                                       callback=self.save_config))
        self.sm.current = 'config_filesaver'

    def run(self):
        self.engine.engine_run()

    def open_filechooser(self):
        if not self.sm.has_screen('config_filechooser'):
            self.sm.add_widget(screen_config_filechooser.ConfigFileChooser(name='config_filechooser',
                                                                           screen_manager=self.sm,
                                                                           localization=self.l,
                                                                           callback=self.load_config))
        self.sm.current = 'config_filechooser'

    def load_config(self, config):
        # type: (str) -> None
        """
        Used as the callback for the config filechooser screen.

        :param config: The path to the config file, including extension.
        """
        self.dwt_config.load_config(config)

        file_name_no_ext = config.split('/')[-1].split('.')[0]
        # set the label on the screen to the name of the config file below

        toolpath_offset = self.dwt_config.active_config.toolpath_offset
        self.select_shape(self.dwt_config.active_config.shape_type)

        self.select_toolpath(toolpath_offset)

        self.drywall_shape_display_widget.d_input.text = str(self.dwt_config.active_config.canvas_shape_dims.d)
        self.drywall_shape_display_widget.l_input.text = str(self.dwt_config.active_config.canvas_shape_dims.l)
        self.drywall_shape_display_widget.r_input.text = str(self.dwt_config.active_config.canvas_shape_dims.r)
        # Shape rotation is automatically set when these inputs are changed
        self.drywall_shape_display_widget.x_input.text = str(self.dwt_config.active_config.canvas_shape_dims.x)
        self.drywall_shape_display_widget.y_input.text = str(self.dwt_config.active_config.canvas_shape_dims.y)

    def save_config(self, name):
        # type: (str) -> None
        """
        Saves the active configuration to the configurations directory.

        :param name: The name of to save the configuration file as.
        """
        file_name = name + ('.json' if not name.endswith('.json') else '')

        self.dwt_config.save_config(file_name)

    def on_leave(self, *args):
        self.dwt_config.save_temp_config()
