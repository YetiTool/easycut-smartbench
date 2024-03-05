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
from asmcnc.apps.drywall_cutter_app import material_setup_popup

from asmcnc.core_UI import scaling_utils


class ImageButton(ButtonBehavior, Image):
    pass


Builder.load_string("""
<DrywallCutterScreen>:
    tool_selection:tool_selection
    shape_selection:shape_selection
    rotate_button:rotate_button
    cut_offset_selection:cut_offset_selection
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
            Spinner:
                id: tool_selection
                size_hint_x: 7
                text: root.tool_options.keys()[0]
                values: root.tool_options.keys()
                on_text: root.select_tool()
                text_size: self.size
                halign: 'center'
                valign: 'middle'
            Spinner:
                id: shape_selection
                size_hint_x: 7
                text: 'Shape'
                values: root.shape_options
                on_text: root.select_shape()
            ImageButton:
                id: rotate_button
                source: './asmcnc/apps/drywall_cutter_app/img/rotate_button.png'
                allow_stretch: True
                size_hint_x: 7
                text: 'Rotate'
                on_press: root.rotate_shape()
            Spinner:
                id: cut_offset_selection
                size_hint_x: 7
                text: 'Cut on line'
                text_size: self.size
                halign: 'center'
                valign: 'middle'
                values: root.line_cut_options
                on_text: root.select_toolpath()
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


def log(message):
    timestamp = datetime.now()
    print (timestamp.strftime('%H:%M:%S.%f')[:12] + ' ' + message)


class DrywallCutterScreen(Screen):
    shape_options = ['circle', 'square', 'rectangle', 'line', 'geberit']
    line_cut_options = ['inside', 'on', 'outside']
    rotation = 'horizontal'

    pulse_poll = None

    def __init__(self, **kwargs):
        self.dwt_config = config_loader.DWTConfig(self)
        self.tool_options = self.dwt_config.get_available_cutter_names()

        super(DrywallCutterScreen, self).__init__(**kwargs)

        self.sm = kwargs['screen_manager']
        self.m = kwargs['machine']
        self.l = kwargs['localization']
        self.kb = kwargs['keyboard']

        # XY move widget
        self.xy_move_widget = widget_xy_move_drywall.XYMoveDrywall(machine=self.m, screen_manager=self.sm, localization=self.l)
        self.xy_move_container.add_widget(self.xy_move_widget)

        self.materials_popup = material_setup_popup.CuttingDepthsPopup(self.l, self.kb, self.dwt_config)
        self.drywall_shape_display_widget = widget_drywall_shape_display.DrywallShapeDisplay(machine=self.m,
                                                                                             screen_manager=self.sm,
                                                                                             dwt_config=self.dwt_config,
                                                                                             kb=self.kb)
        self.shape_display_container.add_widget(self.drywall_shape_display_widget)

        self.select_tool()

    def on_pre_enter(self):
        self.apply_active_config()
        self.pulse_poll = Clock.schedule_interval(self.xy_move_widget.check_zh_at_datum, 0.04)
        self.kb.set_numeric_pos((scaling_utils.get_scaled_width(565), scaling_utils.get_scaled_height(85)))

    def on_pre_leave(self):
        if self.pulse_poll:
            Clock.unschedule(self.pulse_poll)
        self.kb.set_numeric_pos(None)

    def home(self):
        self.m.request_homing_procedure('drywall_cutter', 'drywall_cutter')

    def select_tool(self):
        selected_tool_name = self.tool_selection.text

        self.dwt_config.load_cutter(self.tool_options[selected_tool_name])

        # Convert allowed toolpaths object to dict, then put attributes with True into a list
        self.cut_offset_selection.values = [toolpath for toolpath, allowed in
                                            self.dwt_config.active_cutter.allowable_toolpath_offsets.__dict__.items() if
                                            allowed]
        # Default to first cutter, so disabled cutter is never selected
        self.cut_offset_selection.text = self.cut_offset_selection.values[0]

    def select_shape(self):
        if self.shape_selection.text in ['line', 'geberit']:
            # Only on line available for these options
            self.cut_offset_selection.text = 'on'
            self.cut_offset_selection.disabled = True
        else:
            # Default to cut inside line (when available)
            self.cut_offset_selection.text = 'inside' if 'inside' in self.cut_offset_selection.values else \
            self.cut_offset_selection.values[0]
            self.cut_offset_selection.disabled = False

        if self.shape_selection.text in ['rectangle', 'line']:
            self.rotate_button.disabled = False
        else:
            self.rotate_button.disabled = True

        self.rotation = 'horizontal'
        self.drywall_shape_display_widget.select_shape(self.shape_selection.text, self.rotation)
        self.select_toolpath()

        self.dwt_config.on_parameter_change('shape_type', self.shape_selection.text)

    def rotate_shape(self, swap_lengths=True):
        if self.rotation == 'horizontal':
            self.rotation = 'vertical'
        else:
            self.rotation = 'horizontal'
        self.drywall_shape_display_widget.select_shape(self.shape_selection.text, self.rotation,
                                                       swap_lengths=swap_lengths)
        self.select_toolpath()
        # Need to manually set parameters after internally swapping x and y, because inputs are bound to on_focus
        self.drywall_shape_display_widget.swapping_lengths = True
        self.drywall_shape_display_widget.text_input_change(self.drywall_shape_display_widget.x_input)
        self.drywall_shape_display_widget.text_input_change(self.drywall_shape_display_widget.y_input)
        self.drywall_shape_display_widget.swapping_lengths = False

    def select_toolpath(self):
        self.drywall_shape_display_widget.select_toolpath(self.shape_selection.text, self.cut_offset_selection.text,
                                                          self.rotation)

        self.dwt_config.on_parameter_change('toolpath_offset', self.cut_offset_selection.text)

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
        pass

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

        # Show config name
        file_name = config.rsplit(os.sep, 1)[-1]
        self.drywall_shape_display_widget.config_name_label.text = file_name

        # Set datum when loading a new config
        self.m.set_datum(x=self.dwt_config.active_config.datum_position.x, y=self.dwt_config.active_config.datum_position.y, relative=True)

        self.apply_active_config()

    def apply_active_config(self):
        toolpath_offset = self.dwt_config.active_config.toolpath_offset
        rotation = self.dwt_config.active_config.rotation
        self.shape_selection.text = self.dwt_config.active_config.shape_type
        self.select_shape()

        if rotation == 'vertical':
            self.rotate_shape(swap_lengths=False)

        self.cut_offset_selection.text = toolpath_offset
        self.select_toolpath()

        self.drywall_shape_display_widget.d_input.text = str(self.dwt_config.active_config.canvas_shape_dims.d)
        self.drywall_shape_display_widget.l_input.text = str(self.dwt_config.active_config.canvas_shape_dims.l)
        self.drywall_shape_display_widget.r_input.text = str(self.dwt_config.active_config.canvas_shape_dims.r)
        self.drywall_shape_display_widget.x_input.text = str(self.dwt_config.active_config.canvas_shape_dims.x)
        self.drywall_shape_display_widget.y_input.text = str(self.dwt_config.active_config.canvas_shape_dims.y)

        self.drywall_shape_display_widget.unit_switch.active = True if self.dwt_config.active_config.units == 'mm' else False

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
