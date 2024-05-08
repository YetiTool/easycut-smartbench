from kivy.clock import Clock
import sys, os

from kivy.lang import Builder
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen

from asmcnc.apps.drywall_cutter_app import screen_config_filechooser
from asmcnc.apps.drywall_cutter_app import screen_config_filesaver
from asmcnc.apps.drywall_cutter_app import widget_drywall_shape_display
from asmcnc.apps.drywall_cutter_app import widget_xy_move_drywall
from asmcnc.apps.drywall_cutter_app.config import config_loader
from asmcnc.apps.drywall_cutter_app.image_dropdown import ToolSelectionDropDown, ShapeSelectionDropDown, ToolPathSelectionDropDown
from asmcnc.comms.logging_system.logging_system import Logger
from asmcnc.apps.drywall_cutter_app import material_setup_popup
from asmcnc.apps.drywall_cutter_app import job_load_helper
from asmcnc.core_UI import scaling_utils
from asmcnc.core_UI.new_popups.job_validation_popup import JobValidationPopup
from asmcnc.skavaUI import popup_info


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
            ToolSelectionDropDown:
                id: tool_selection
                callback: root.select_tool
                size_hint_x: 7
                allow_stretch: True
            ShapeSelectionDropDown:
                id: shape_selection
                callback: root.select_shape
                size_hint_x: 7
                allow_stretch: True
            ImageButton:
                id: rotate_button
                source: './asmcnc/apps/drywall_cutter_app/img/rotate_button.png'
                allow_stretch: True
                size_hint_x: 7
                text: 'Rotate'
                on_press: root.rotate_shape()
            ToolPathSelectionDropDown:
                id: toolpath_selection
                size_hint_x: 7
                callback: root.select_toolpath
                allow_stretch: True
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
                            rgba: hex('#FFFFFFFF')
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

    pulse_poll = None

    def __init__(self, **kwargs):
        self.name = 'drywall_cutter'
        super(DrywallCutterScreen, self).__init__(**kwargs)
        self.dwt_config = config_loader.DWTConfig(self)
        self.tool_options = self.dwt_config.get_available_cutter_names()

        self.sm = kwargs['screen_manager']
        self.m = kwargs['machine']
        self.l = kwargs['localization']
        self.kb = kwargs['keyboard']
        self.jd = kwargs['job']
        self.pm = kwargs['popup_manager']
        self.cs = self.m.cs

        self.engine = GCodeEngine(self.m, self.dwt_config, self.cs)
        self.simulation_started = False
        self.ignore_state = True

        # XY move widget
        self.xy_move_widget = widget_xy_move_drywall.XYMoveDrywall(machine=self.m,
                                                                   screen_manager=self.sm,
                                                                   localization=self.l,
                                                                   coordinate_system=self.cs)
        self.xy_move_container.add_widget(self.xy_move_widget)

        self.materials_popup = material_setup_popup.CuttingDepthsPopup(self.l, self.kb, self.dwt_config)
        self.drywall_shape_display_widget = widget_drywall_shape_display.DrywallShapeDisplay(machine=self.m,
                                                                                             screen_manager=self.sm,
                                                                                             dwt_config=self.dwt_config,
                                                                                             engine=self.engine,
                                                                                             kb=self.kb,
                                                                                             localization=self.l,
                                                                                             cs=self.cs,)
        self.shape_display_container.add_widget(self.drywall_shape_display_widget)

        self.dwt_config.show_tool_image()
        self.dwt_config.show_toolpath_image()

        self.bumper_list = [self.drywall_shape_display_widget.bumper_bottom_image,
                            self.drywall_shape_display_widget.bumper_right_image,
                            self.drywall_shape_display_widget.bumper_top_image,
                            self.drywall_shape_display_widget.bumper_left_image]

        self.dwt_config.bind(active_config=self.on_load_config)
        self.m.bind(datum_position=self.set_datum_position)

    def set_datum_position(self, *args):
        if self.sm.current != self.name:
            return

        dx, dy = self.drywall_shape_display_widget.get_current_x_y(self.m.datum_position[0],
                                                                   self.m.datum_position[1], False)

        self.dwt_config.on_parameter_change('datum_position.x', dx)
        self.dwt_config.on_parameter_change('datum_position.y', dy)

    def on_pre_enter(self):
        self.apply_active_config()
        self.materials_popup.on_open()  # to make sure material values are set correctly
        self.pulse_poll = Clock.schedule_interval(self.update_pulse_opacity, 0.04)
        self.kb.set_numeric_pos((scaling_utils.get_scaled_width(565), scaling_utils.get_scaled_height(115)))
        self.drywall_shape_display_widget.check_datum_and_extents()  # update machine value labels

    def on_enter(self):
        self.m.laser_on()

    def on_pre_leave(self):
        self.m.laser_off()
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
        self.dwt_config.select_tool(cutter_file)

    def select_shape(self, shape):
        self.dwt_config.select_shape(shape)

    def rotate_shape(self, swap_lengths=True):
        if self.rotation == 'horizontal':
            self.rotation = 'vertical'
        else:
            self.rotation = 'horizontal'

        self.drywall_shape_display_widget.select_shape(self.dwt_config.active_config.shape_type, self.rotation,
                                                       swap_lengths=swap_lengths)
        self.select_toolpath(self.dwt_config.active_config.toolpath_offset)

        # Need to manually set parameters after internally swapping x and y, because inputs are bound to on_focus
        self.drywall_shape_display_widget.swapping_lengths = True
        self.drywall_shape_display_widget.text_input_change(self.drywall_shape_display_widget.x_input)
        self.drywall_shape_display_widget.text_input_change(self.drywall_shape_display_widget.y_input)
        self.drywall_shape_display_widget.swapping_lengths = False

    def select_toolpath(self, toolpath):
        self.dwt_config.select_toolpath(toolpath)

    def material_setup(self):
        self.materials_popup.open()

    def stop(self):
        popup_info.PopupStop(self.m, self.sm, self.l)

    def quit_to_lobby(self):
        self.set_return_screens()
        self.jd.reset_values()
        self.sm.current = 'lobby'

    def simulate(self):
        self.popup_watchdog = Clock.schedule_interval(lambda dt: self.set_simulation_popup_state(self.m.s.m_state), 1)
        if not self.is_config_valid():
            self.show_validation_popup()
            return

        if not self.simulation_started and self.m.s.m_state.lower() == 'idle':
            self.m.s.bind(m_state=lambda i, value: self.set_simulation_popup_state(value))
            self.pm.show_wait_popup(main_string=self.l.get_str('Preparing for simulation') + '...')
            self.ignore_state = False
            self.simulation_started = False
            self.engine.engine_run(simulate=True)

    def set_simulation_popup_state(self, machine_state):
        machine_state = machine_state.lower()
        if not self.ignore_state:

            if machine_state == 'run':
                # Machine is simulating
                self.sm.pm.close_wait_popup()
                if not self.simulation_started:
                    # If the popup is not already open, open it
                    self.sm.pm.show_simulating_job_popup()
                self.simulation_started = True

            elif (machine_state == 'idle' or self.sm.current != "drywall_cutter") and self.simulation_started:
                # Machine stopped simulating
                self.sm.pm.close_simulating_job_popup()
                Clock.unschedule(self.popup_watchdog)
                self.simulation_started = False
                self.ignore_state = True

        if machine_state not in ['run', 'idle']:
            # Machine is in an unknown state, close all popups
            self.sm.pm.close_wait_popup()
            self.sm.pm.close_simulating_job_popup()
            Clock.unschedule(self.popup_watchdog)
            self.simulation_started = False
            self.ignore_state = True
            
    def save(self):
        if not self.is_config_valid():
            self.show_validation_popup()
            return

        if not self.sm.has_screen('config_filesaver'):
            self.sm.add_widget(screen_config_filesaver.ConfigFileSaver(name='config_filesaver',
                                                                       screen_manager=self.sm,
                                                                       localization=self.l,
                                                                       callback=self.dwt_config.save_config))
        self.sm.current = 'config_filesaver'

    def is_config_valid(self):
        return self.materials_popup.validate_inputs() and self.drywall_shape_display_widget.are_inputs_valid()

    def run(self):
        if self.materials_popup.validate_inputs() and self.drywall_shape_display_widget.are_inputs_valid():
            output_path = self.engine.engine_run()

            job_loader = job_load_helper.JobLoader(screen_manager=self.sm, machine=self.m, job=self.jd,
                                                   localization=self.l)
            self.jd.set_job_filename(self.drywall_shape_display_widget.config_name_label.text)
            job_loader.load_gcode_file(output_path)
            os.remove(output_path)
            self.set_return_screens()
            self.sm.get_screen('go').dwt_config = self.dwt_config
            self.proceed_to_go_screen()

        else:
            self.show_validation_popup()

    def show_validation_popup(self):
        m_popup_steps = self.materials_popup.get_steps_to_validate()
        s_widget_steps = self.drywall_shape_display_widget.get_steps_to_validate()

        m_popup_steps.extend(s_widget_steps)

        steps_to_validate = "\n".join(m_popup_steps)
        popup = JobValidationPopup(steps_to_validate, size_hint=(0.8, 0.8), auto_dismiss=False)
        popup.open()

    def set_return_screens(self):
        self.sm.get_screen('go').return_to_screen = 'drywall_cutter' if self.sm.get_screen(
            'go').return_to_screen == 'home' else 'home'
        self.sm.get_screen('go').cancel_to_screen = 'drywall_cutter' if self.sm.get_screen(
            'go').cancel_to_screen == 'home' else 'home'

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

    def open_filechooser(self):
        if not self.sm.has_screen('config_filechooser'):
            self.sm.add_widget(screen_config_filechooser.ConfigFileChooser(name='config_filechooser',
                                                                           screen_manager=self.sm,
                                                                           localization=self.l,
                                                                           callback=self.dwt_config.load_config))
        self.sm.current = 'config_filechooser'

    def on_load_config(self, instance, value):
        """
        Called by the config_loader module when a config is loaded

        :return: None
        """
        Logger.debug("New config loaded. Applying settings.")

        self.apply_active_config()

        dx, dy = self.drywall_shape_display_widget.get_current_x_y(value.datum_position.x,
                                                                   value.datum_position.y, True)
        self.m.set_datum(x=dx, y=dy, relative=True)

    def apply_active_config(self):
        toolpath_offset = self.dwt_config.active_config.toolpath_offset
        rotation = self.dwt_config.active_config.rotation

        self.select_shape(self.dwt_config.active_config.shape_type)

        #if rotation == 'vertical':
        #    self.rotate_shape(swap_lengths=False)

        self.select_tool(self.dwt_config.active_config.cutter_type)
        self.select_toolpath(toolpath_offset)

        self.drywall_shape_display_widget.d_input.text = str(self.dwt_config.active_config.canvas_shape_dims.d)
        self.drywall_shape_display_widget.l_input.text = str(self.dwt_config.active_config.canvas_shape_dims.l)
        self.drywall_shape_display_widget.r_input.text = str(self.dwt_config.active_config.canvas_shape_dims.r)
        self.drywall_shape_display_widget.x_input.text = str(self.dwt_config.active_config.canvas_shape_dims.x)
        self.drywall_shape_display_widget.y_input.text = str(self.dwt_config.active_config.canvas_shape_dims.y)

        self.drywall_shape_display_widget.unit_switch.active = self.dwt_config.active_config.units == 'mm'

        # Vlad set your text inputs here:

    def on_leave(self, *args):
        self.dwt_config.save_temp_config()
