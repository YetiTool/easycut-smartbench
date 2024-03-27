import os
from datetime import datetime

from kivy.lang import Builder
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock

from asmcnc.skavaUI import popup_info
from asmcnc.apps.drywall_cutter_app import widget_xy_move_drywall
from asmcnc.apps.drywall_cutter_app import widget_drywall_shape_display
from asmcnc.apps.drywall_cutter_app.config import config_loader
from asmcnc.apps.drywall_cutter_app import screen_config_filechooser
from asmcnc.apps.drywall_cutter_app import screen_config_filesaver
from asmcnc.apps.drywall_cutter_app.image_dropdown import ImageDropDownButton
from asmcnc.apps.drywall_cutter_app import material_setup_popup

from asmcnc.core_UI import scaling_utils


class ImageButton(ButtonBehavior, Image):
    pass


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
            ImageButton:
                source: './asmcnc/apps/drywall_cutter_app/img/home_button.png'
                allow_stretch: True
                size_hint_x: 7
                on_press: root.home()
            ImageButton:
                source: './asmcnc/apps/drywall_cutter_app/img/open_button.png'
                allow_stretch: True
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
            ImageButton:
                id: rotate_button
                source: './asmcnc/apps/drywall_cutter_app/img/rotate_button.png'
                allow_stretch: True
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
            ImageButton:
                source: './asmcnc/apps/drywall_cutter_app/img/cutting_depths_button.png'
                allow_stretch: True
                size_hint_x: 7
                text: 'Material setup'
                text_size: self.size
                halign: 'center'
                valign: 'middle'
                on_press: root.material_setup()
            ImageButton:
                source: './asmcnc/apps/drywall_cutter_app/img/stop_button.png'
                allow_stretch: True
                size_hint_x: 15
                text: 'STOP'
                on_press: root.stop()
            ImageButton:
                source: './asmcnc/apps/drywall_cutter_app/img/exit_button.png'
                allow_stretch: True
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
                    ImageButton:
                        source: './asmcnc/apps/drywall_cutter_app/img/simulate_button.png'
                        allow_stretch: True
                        text: 'Simulate'
                        on_press: root.simulate()
                    ImageButton:
                        source: './asmcnc/apps/drywall_cutter_app/img/save_button.png'
                        allow_stretch: True
                        text: 'Save'
                        on_press: root.save()
                    ImageButton:
                        source: './asmcnc/apps/drywall_cutter_app/img/start_job_button.png'
                        allow_stretch: True
                        text: 'Run'
                        on_press: root.run()
""")


class DrywallCutterScreen(Screen):
    shape_options = ['circle', 'square', 'rectangle', 'line', 'geberit']
    line_cut_options = ['inside', 'on', 'outside']
    rotation = 'horizontal'

    current_pulse_opacity = 1
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

    pulse_poll = None

    def __init__(self, **kwargs):
        self.dwt_config = config_loader.DWTConfig(self)
        self.tool_options = self.dwt_config.get_available_cutter_names()

        super(DrywallCutterScreen, self).__init__(**kwargs)

        self.sm = kwargs['screen_manager']
        self.m = kwargs['machine']
        self.l = kwargs['localization']
        self.kb = kwargs['keyboard']

        self.engine = GCodeEngine(self.dwt_config)

        # XY move widget
        self.xy_move_widget = widget_xy_move_drywall.XYMoveDrywall(machine=self.m, screen_manager=self.sm, localization=self.l)
        self.xy_move_container.add_widget(self.xy_move_widget)

        self.materials_popup = material_setup_popup.CuttingDepthsPopup(self.l, self.kb, self.dwt_config)
        self.drywall_shape_display_widget = widget_drywall_shape_display.DrywallShapeDisplay(machine=self.m,
                                                                                             screen_manager=self.sm,
                                                                                             dwt_config=self.dwt_config,
                                                                                             engine=self.engine,
                                                                                             kb=self.kb)
        self.shape_display_container.add_widget(self.drywall_shape_display_widget)

        self.show_tool_image()
        self.show_toolpath_image()

        self.bumper_list = [self.drywall_shape_display_widget.bumper_bottom_image,
                            self.drywall_shape_display_widget.bumper_right_image,
                            self.drywall_shape_display_widget.bumper_top_image,
                            self.drywall_shape_display_widget.bumper_left_image]

    def on_pre_enter(self):
        self.apply_active_config()
        self.pulse_poll = Clock.schedule_interval(self.update_pulse_opacity, 0.04)
        self.kb.set_numeric_pos((scaling_utils.get_scaled_width(565), scaling_utils.get_scaled_height(85)))

    def on_pre_leave(self):
        if self.pulse_poll:
            Clock.unschedule(self.pulse_poll)
        self.kb.set_numeric_pos(None)

    def update_pulse_opacity(self, dt):
        # Pulse overlay by smoothly alternating between 0 and 1 opacity
        # Hacky way to track pulsing on or off without a variable by storing that information in the opacity value
        if self.current_pulse_opacity <= 0:
            self.current_pulse_opacity = 0.01
        elif self.current_pulse_opacity >= 1:
            self.current_pulse_opacity = 0.98
        # Check if second decimal place is even or odd
        elif int(("%.2f" % self.current_pulse_opacity)[-1]) % 2 == 1:
            self.current_pulse_opacity += 0.1
        else:
            self.current_pulse_opacity -= 0.1

        # Pulse bumpers
        for bumper in self.bumper_list:
            if "red" in bumper.source:
                bumper.opacity = self.current_pulse_opacity
            else:
                bumper.opacity = 1

        # Pulse go to datum button
        self.xy_move_widget.check_zh_at_datum(self.current_pulse_opacity)

    def home(self):
        self.m.request_homing_procedure('drywall_cutter', 'drywall_cutter')

    def select_tool(self, cutter_file, *args):
        self.dwt_config.load_cutter(cutter_file)

        # Convert allowed toolpaths object to dict, then put attributes with True into a list
        allowed_toolpaths = [toolpath for toolpath, allowed in self.dwt_config.active_cutter.allowable_toolpath_offsets.__dict__.items() if allowed]
        # Use allowed toolpath list to create a dict of only allowed toolpaths
        allowed_toolpath_dict = dict([(k, self.toolpath_offset_options_dict[k]) for k in allowed_toolpaths if k in self.toolpath_offset_options_dict])
        # Then update dropdown to only show allowed toolpaths
        self.toolpath_selection.image_dict = allowed_toolpath_dict
        # Default to first toolpath, so disabled toolpath is never selected
        self.select_toolpath(allowed_toolpaths[0])

        self.show_tool_image()
        self.dwt_config.on_parameter_change('cutter_type', cutter_file)

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

        if shape in ['rectangle', 'line', 'geberit']:
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

        # Need to manually set parameters after internally swapping x and y, because inputs are bound to on_focus
        self.drywall_shape_display_widget.swapping_lengths = True
        self.drywall_shape_display_widget.text_input_change(self.drywall_shape_display_widget.x_input)
        self.drywall_shape_display_widget.text_input_change(self.drywall_shape_display_widget.y_input)
        self.drywall_shape_display_widget.swapping_lengths = False

    def select_toolpath(self, toolpath):
        self.dwt_config.on_parameter_change('toolpath_offset', toolpath)

        self.drywall_shape_display_widget.select_toolpath(self.dwt_config.active_config.shape_type, toolpath, self.rotation)

        self.show_toolpath_image()

    def show_toolpath_image(self):
        self.toolpath_selection.source = self.toolpath_offset_options_dict[self.dwt_config.active_config.toolpath_offset]['image_path']

    def material_setup(self):
        self.materials_popup.open()

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

    def load_config(self, config_path):
        # type: (str) -> None
        """
        Used as the callback for the config filechooser screen.

        :param config_path: The path to the config file, including extension (if present).
        """
        self.dwt_config.load_config(config_path)
        self.apply_active_config()

        # Set datum when loading a new config
        dx, dy = self.drywall_shape_display_widget.get_current_x_y(self.dwt_config.active_config.datum_position.x,
                                                                   self.dwt_config.active_config.datum_position.y, True)
        self.m.set_datum(x=dx, y=dy, relative=True)

    def apply_active_config(self):
        toolpath_offset = self.dwt_config.active_config.toolpath_offset
        rotation = self.dwt_config.active_config.rotation

        self.select_shape(self.dwt_config.active_config.shape_type)

        if rotation == 'vertical':
            self.rotate_shape(swap_lengths=False)

        self.select_tool(self.dwt_config.active_config.cutter_type)
        self.select_toolpath(toolpath_offset)

        self.drywall_shape_display_widget.d_input.text = str(self.dwt_config.active_config.canvas_shape_dims.d)
        self.drywall_shape_display_widget.l_input.text = str(self.dwt_config.active_config.canvas_shape_dims.l)
        self.drywall_shape_display_widget.r_input.text = str(self.dwt_config.active_config.canvas_shape_dims.r)
        self.drywall_shape_display_widget.x_input.text = str(self.dwt_config.active_config.canvas_shape_dims.x)
        self.drywall_shape_display_widget.y_input.text = str(self.dwt_config.active_config.canvas_shape_dims.y)

        self.drywall_shape_display_widget.unit_switch.active = self.dwt_config.active_config.units == 'mm'

        # Vlad set your text inputs here:

    def save_config(self, file_name):
        # type: (str) -> None
        """
        Saves the active configuration to the configurations directory.

        :param file_name: The name of to save the configuration file as.
        """

        self.dwt_config.save_config(file_name)

    def on_leave(self, *args):
        self.dwt_config.save_temp_config()
