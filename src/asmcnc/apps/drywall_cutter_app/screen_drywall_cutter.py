from datetime import datetime
import sys, textwrap

from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

from asmcnc.skavaUI import popup_info
from asmcnc.apps.drywall_cutter_app import widget_xy_move_drywall
from asmcnc.apps.drywall_cutter_app import widget_drywall_shape_display
from asmcnc.apps.drywall_cutter_app import material_setup_popup
from asmcnc.apps.drywall_cutter_app.config import config_loader
from asmcnc.apps.drywall_cutter_app import screen_config_filechooser
from asmcnc.apps.drywall_cutter_app import screen_config_filesaver
from asmcnc.apps.drywall_cutter_app import job_load_helper

from engine import GCodeEngine

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
            Button:
                size_hint_x: 7
                text: 'Home'
                on_press: root.home()
            Button:
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
            Button:
                id: rotate_button
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

    def __init__(self, **kwargs):
        super(DrywallCutterScreen, self).__init__(**kwargs)

        self.sm = kwargs['screen_manager']
        self.m = kwargs['machine']
        self.l = kwargs['localization']
        self.kb = kwargs['keyboard']
        self.jd = kwargs['job']

        self.engine = GCodeEngine(self.dwt_config, machine=self.m)

        # XY move widget
        self.xy_move_widget = widget_xy_move_drywall.XYMoveDrywall(machine=self.m, screen_manager=self.sm, localization=self.l)
        self.xy_move_container.add_widget(self.xy_move_widget)

        self.drywall_shape_display_widget = widget_drywall_shape_display.DrywallShapeDisplay(machine=self.m, screen_manager=self.sm, dwt_config=self.dwt_config, engine=self.engine)
        self.shape_display_container.add_widget(self.drywall_shape_display_widget)

        self.shape_selection.text = 'circle'

        self.select_tool()

    def home(self):
        self.m.request_homing_procedure('drywall_cutter', 'drywall_cutter')

    def select_tool(self):
        selected_tool_name = self.tool_selection.text

        self.dwt_config.load_cutter(self.tool_options[selected_tool_name])

        # Convert allowed toolpaths object to dict, then put attributes with True into a list
        self.cut_offset_selection.values = [toolpath for toolpath, allowed in self.dwt_config.active_cutter.allowable_toolpath_offsets.__dict__.items() if allowed]
        # Default to first cutter, so disabled cutter is never selected
        self.cut_offset_selection.text = self.cut_offset_selection.values[0]

    def select_shape(self):
        if self.shape_selection.text in ['line', 'geberit']:
            # Only on line available for these options
            self.cut_offset_selection.text = 'on'
            self.cut_offset_selection.disabled = True
        else:
            # Default to cut inside line (when available)
            self.cut_offset_selection.text = 'inside' if 'inside' in self.cut_offset_selection.values else self.cut_offset_selection.values[0]
            self.cut_offset_selection.disabled = False

        if self.shape_selection.text in ['rectangle', 'line']:
            self.rotate_button.disabled = False
        else:
            self.rotate_button.disabled = True

        self.rotation = 'horizontal'
        self.drywall_shape_display_widget.select_shape(self.shape_selection.text, self.rotation)
        self.select_toolpath()

        if self.drywall_shape_display_widget.rotation_required():
            self.rotate_shape(swap_lengths=False)

        self.dwt_config.on_parameter_change('shape_type', self.shape_selection.text)

    def rotate_shape(self, swap_lengths=True):
        if self.rotation == 'horizontal':
            self.rotation = 'vertical'
        else:
            self.rotation = 'horizontal'
        self.drywall_shape_display_widget.select_shape(self.shape_selection.text, self.rotation, swap_lengths=swap_lengths)
        self.select_toolpath()

    def select_toolpath(self):
        self.drywall_shape_display_widget.select_toolpath(self.shape_selection.text, self.cut_offset_selection.text, self.rotation)

        self.dwt_config.on_parameter_change('toolpath_offset', self.cut_offset_selection.text)

    def material_setup(self):
        material_setup_popup.CuttingDepthsPopup(self.l, self.kb, self.dwt_config)
        pass

    def stop(self):
        popup_info.PopupStop(self.m, self.sm, self.l)

    def quit_to_lobby(self):
        self.set_return_screens()
        self.jd.reset_values()
        self.sm.current = 'lobby'

    def simulate(self):
        self.engine.engine_run(True)

    def save(self):
        if not self.sm.has_screen('config_filesaver'):
            self.sm.add_widget(screen_config_filesaver.ConfigFileSaver(name='config_filesaver',
                                                                       screen_manager=self.sm,
                                                                       localization=self.l,
                                                                       callback=self.save_config))
        self.sm.current = 'config_filesaver'

    def run(self):
        self.engine.engine_run(False)
        job_loader = job_load_helper.JobLoader(screen_manager=self.sm, machine=self.m, job=self.jd,
                                                           localization=self.l)
        output_file = "jobCache/" + self.dwt_config.active_config.shape_type + u".nc"
        self.jd.set_job_filename(output_file)
        job_loader.load_gcode_file(output_file)
        self.set_return_screens()
        self.proceed_to_go_screen()

    def set_return_screens(self):
        self.sm.get_screen('go').return_to_screen = 'drywall_cutter' if self.sm.get_screen('go').return_to_screen == 'home' else 'home'
        self.sm.get_screen('go').cancel_to_screen = 'drywall_cutter' if self.sm.get_screen('go').cancel_to_screen == 'home' else 'home'

    def proceed_to_go_screen(self):

        # NON-OPTIONAL CHECKS (bomb if non-satisfactory)

        # GCode must be loaded.
        # Machine state must be idle.
        # Machine must be homed.
        # Job must be within machine bounds.

        if self.jd.job_gcode == []:
            info = (
                    self.format_command(
                        self.l.get_str('Before running, a file needs to be loaded.')) + '\n\n' + self.format_command(
                self.l.get_str('Tap the file chooser in the first tab (top left) to load a file.'))
            )

            popup_info.PopupInfo(self.sm, self.l, 450, info)

        # elif not self.m.state().startswith('Idle'):
        #     self.sm.current = 'mstate'

        elif self.m.is_machine_homed == False and sys.platform != "win32":
            self.m.request_homing_procedure('drywall_cutter', 'drywall_cutter')

        elif self.sm.get_screen('home').z_datum_reminder_flag and not self.sm.get_screen('home').has_datum_been_reset:

            z_datum_reminder_message = (
                    self.format_command(
                        self.l.get_str(
                            'You may need to set a new Z datum before you start a new job!')) + '\n\n' + self.format_command(
                self.l.get_str('Press Ok to clear this reminder.').replace(self.l.get_str('Ok'), self.l.get_bold('Ok')))
            )

            popup_info.PopupWarning(self.sm, self.l, z_datum_reminder_message)
            self.sm.get_screen('home').z_datum_reminder_flag = False

        else:
            # clear to proceed
            self.jd.screen_to_return_to_after_job = 'drywall_cutter'
            self.jd.screen_to_return_to_after_cancel = 'drywall_cutter'

            # Check if stylus option is enabled
            if self.m.is_stylus_enabled == True:
                # Display tool selection screen
                self.sm.current = 'tool_selection'

            else:
                self.m.stylus_router_choice = 'router'

                # is fw capable of auto Z lift?
                if self.m.fw_can_operate_zUp_on_pause():
                    self.sm.current = 'lift_z_on_pause_or_not'
                else:
                    self.sm.current = 'jobstart_warning'

    def format_command(self, cmd):
        wrapped_cmd = textwrap.fill(cmd, width=50, break_long_words=False)
        return wrapped_cmd

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
        self.shape_selection.text = self.dwt_config.active_config.shape_type
        self.select_shape()

        self.cut_offset_selection.text = toolpath_offset
        self.select_toolpath()

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
