import os
from datetime import datetime
import sys, textwrap

from kivy.lang import Builder
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock

from asmcnc.skavaUI import popup_info
from asmcnc.apps.drywall_cutter_app import widget_xy_move_drywall
from asmcnc.apps.drywall_cutter_app import widget_drywall_shape_display
from asmcnc.apps.drywall_cutter_app import material_setup_popup
from asmcnc.apps.drywall_cutter_app.config import config_loader
from asmcnc.apps.drywall_cutter_app import screen_config_filechooser
from asmcnc.apps.drywall_cutter_app import screen_config_filesaver
from asmcnc.apps.drywall_cutter_app.image_dropdown import ImageDropDownButton
from asmcnc.apps.drywall_cutter_app import job_load_helper

from engine import GCodeEngine


class ImageButton(ButtonBehavior, Image):
    pass


Builder.load_string("""
<DrywallCutterScreen>:
    tool_selection:tool_selection
    shape_selection:shape_selection
    rotate_button:rotate_button
    simulate_button:simulate_button
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
                        id: simulate_button
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
        self.jd = kwargs['job']

        self.engine = GCodeEngine(self.dwt_config, machine=self.m)

        # XY move widget
        self.xy_move_widget = widget_xy_move_drywall.XYMoveDrywall(machine=self.m, screen_manager=self.sm, localization=self.l)
        self.xy_move_container.add_widget(self.xy_move_widget)

        self.drywall_shape_display_widget = widget_drywall_shape_display.DrywallShapeDisplay(machine=self.m, screen_manager=self.sm, dwt_config=self.dwt_config, engine=self.engine, keyboard = self.kb)
        self.shape_display_container.add_widget(self.drywall_shape_display_widget)

        self.show_tool_image()
        self.show_toolpath_image()

        self.materials_popup = material_setup_popup.CuttingDepthsPopup(self.l, self.kb, self.dwt_config)

    def on_pre_enter(self):
        self.apply_active_config()

    def home(self):
        self.m.request_homing_procedure('drywall_cutter', 'drywall_cutter')

    def select_tool(self, cutter_file, *args):

        self.dwt_config.load_cutter(cutter_file)
        self.show_tool_image()

        # Save active cutter information to a text file
        self.save_active_cutter_info()
        # Convert allowed toolpaths object to dict, then put attributes with True into a list
        allowed_toolpaths = [toolpath for toolpath, allowed in self.dwt_config.active_cutter.allowable_toolpath_offsets.__dict__.items() if allowed]
        # Use allowed toolpath list to create a dict of only allowed toolpaths
        allowed_toolpath_dict = dict([(k, self.toolpath_offset_options_dict[k]) for k in allowed_toolpaths if k in self.toolpath_offset_options_dict])
        # Then update dropdown to only show allowed toolpaths
        self.toolpath_selection.image_dict = allowed_toolpath_dict
        # Default to first toolpath, so disabled toolpath is never selected
        self.select_toolpath(allowed_toolpaths[0])

    def save_active_cutter_info(self):
        active_cutter_info = self.dwt_config.active_cutter.diameter,self.dwt_config.active_cutter.cutter_description
        print("active_cutter_info: {}".format(active_cutter_info))
        with open("active_cutter_info.txt", "w+") as file:
            file.write(active_cutter_info)

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
        self.materials_popup.open()

    def select_toolpath(self, toolpath):
        self.dwt_config.on_parameter_change('toolpath_offset', toolpath)

        self.drywall_shape_display_widget.select_toolpath(self.dwt_config.active_config.shape_type, toolpath, self.rotation)

        self.show_toolpath_image()

    def show_toolpath_image(self):
        self.toolpath_selection.source = self.toolpath_offset_options_dict[self.dwt_config.active_config.toolpath_offset]['image_path']

    def stop(self):
        popup_info.PopupStop(self.m, self.sm, self.l)

    def quit_to_lobby(self):
        self.set_return_screens()
        self.jd.reset_values()
        self.sm.current = 'lobby'

    def simulate(self):        
        if self.are_inputs_valid():
            self.simulate_button.disabled = True
            self.engine.engine_run(simulate=True)
            sim_popup = popup_info.PopupWait(self.sm, self.l, "Preparing for simulation")
            Clock.schedule_once(
                                lambda dt: self.dismiss_popup(sim_popup), 2)
            Clock.schedule_once(
                            lambda dt: self.enable_simulation_button(), 5)
        else:
            popup_info.PopupError(self.sm, self.l, "Please check your inputs are valid, and not too small.")

    def save(self):
        if not self.sm.has_screen('config_filesaver'):
            self.sm.add_widget(screen_config_filesaver.ConfigFileSaver(name='config_filesaver',
                                                                       screen_manager=self.sm,
                                                                       localization=self.l,
                                                                       callback=self.save_config,
                                                                       keyboard=self.kb))
        self.sm.current = 'config_filesaver'

    def run(self):
        if self.are_inputs_valid():
            self.engine.engine_run(False)
            job_loader = job_load_helper.JobLoader(screen_manager=self.sm, machine=self.m, job=self.jd,
                                                            localization=self.l)
            output_file = "jobCache/" + self.dwt_config.active_config.shape_type + u".nc"
            self.jd.set_job_filename(output_file)
            job_loader.load_gcode_file(output_file)
            self.set_return_screens()
            self.proceed_to_go_screen()
        else:
            popup_info.PopupError(self.sm, self.l, "Please check your inputs are valid, and not too small.")

    def are_inputs_valid(self):
        return self.drywall_shape_display_widget.are_inputs_valid() and self.materials_popup.validate_inputs()

    def set_return_screens(self):
        self.sm.get_screen('go').return_to_screen = 'drywall_cutter' if self.sm.get_screen('go').return_to_screen == 'home' else 'home'
        self.sm.get_screen('go').cancel_to_screen = 'drywall_cutter' if self.sm.get_screen('go').cancel_to_screen == 'home' else 'home'

    def enable_simulation_button(self):
        self.simulate_button.disabled = False

    def dismiss_popup(self, popup):
        popup.popup.dismiss()

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

        # Show config name
        file_name = config.rsplit(os.sep, 1)[-1]
        self.drywall_shape_display_widget.config_name_label.text = file_name

        # Set datum when loading a new config
        self.m.set_datum(x=self.dwt_config.active_config.datum_position.x, y=self.dwt_config.active_config.datum_position.y, relative=True)

        self.apply_active_config()

    def apply_active_config(self):
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

    def on_enter(self):
        self.m.laser_on()

    def on_leave(self, *args):
        self.dwt_config.save_temp_config()
        self.m.laser_off()
