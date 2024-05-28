from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from asmcnc.apps.systemTools_app.screens.calibration.widget_current_adjustment import (
    CurrentAdjustmentWidget,
)
from asmcnc.apps.systemTools_app.screens import widget_final_test_xy_move
from asmcnc.comms.yeti_grbl_protocol.c_defines import *
from asmcnc.apps.systemTools_app.screens.popup_system import (
    PopupConfirmStoreCurrentValues,
)
from asmcnc.skavaUI.popup_info import PopupWait, PopupWarning
from asmcnc.apps.systemTools_app.screens.calibration import widget_sg_status_bar
from kivy.clock import Clock

Builder.load_string(
    """
<CurrentAdjustment>:

    xy_move_container:xy_move_container
    current_adjustment_container:current_adjustment_container
    
    rt_x_sg:rt_x_sg
    rt_x1_sg:rt_x1_sg
    rt_x2_sg:rt_x2_sg
    rt_y1_sg:rt_y1_sg
    rt_y2_sg:rt_y2_sg
    rt_z_sg:rt_z_sg
    
    peak_x_sg:peak_x_sg
    peak_x1_sg:peak_x1_sg
    peak_x2_sg:peak_x2_sg
    peak_y1_sg:peak_y1_sg
    peak_y2_sg:peak_y2_sg
    peak_z_sg:peak_z_sg

    raw_sg_toggle_button : raw_sg_toggle_button
    protocol_status : protocol_status

    status_container : status_container

    on_touch_down: root.on_touch()

    BoxLayout:
        orientation: 'vertical'

        BoxLayout:
            size_hint_y: 0.92
            orientation: 'horizontal'

            GridLayout:
                cols: 2
        
                GridLayout:
                    rows: 2
                    size_hint_x: 0.5
        
                    BoxLayout:
                        id: xy_move_container
                        pos_hint: {'center_x': .5, 'center_y': .5}
                        size_hint: (None,None)
                        height: dp(0.75*app.height)
                        width: dp(0.3375*app.width)
        
                    BoxLayout:
                        size_hint_y: 0.1
                        padding:[0, dp(0.0625)*app.height, dp(0.1875)*app.width, 0]
        
                        Button:
                            font_size: str(0.01875 * app.width) + 'sp'
                            text: 'Factory Settings'
                            on_press: root.back_to_fac_settings()
        
                GridLayout:
                    rows: 2
        
                    GridLayout:
                        cols: 2
        
                        GridLayout:
                            rows:2
        
                            Label:
                                font_size: str(0.01875 * app.width) + 'sp'
                                size_hint_y: 0.2
                                text: 'Active Current Adjustment'
        
                            BoxLayout:
                                id: current_adjustment_container
        
                        BoxLayout:
                            size_hint_x: 0.3
                            # padding: [0, dp(25), 0, dp(25)]
                            orientation: 'vertical'
        
                            Button:
                                font_size: str(0.01875 * app.width) + 'sp'
                                text: 'Home'
                                on_press: root.home()
        
                            Button:
                                font_size: str(0.01875 * app.width) + 'sp'
                                text: 'Reset Currents'
                                on_press: root.reset_currents()

                            Button:
                                font_size: str(0.01875 * app.width) + 'sp'
                                text: 'GRBL Reset'
                                on_press: root.grbl_reset()

                            Label: 
                                font_size: str(0.01875 * app.width) + 'sp'
                                id: protocol_status
                                text: ""

        
                    GridLayout:
                        cols: 2
        
                        # SG value status box
                        GridLayout:
                            rows: 3
                            cols: 7
        
                            Label
        
                            Label:
                                font_size: str(0.01875 * app.width) + 'sp'
                                text: 'SG X'
        
                            Label:
                                font_size: str(0.01875 * app.width) + 'sp'
                                text: 'SG X1'
        
                            Label:
                                font_size: str(0.01875 * app.width) + 'sp'
                                text: 'SG X2'
        
                            Label:
                                font_size: str(0.01875 * app.width) + 'sp'
                                text: 'SG Y1'
        
                            Label:
                                font_size: str(0.01875 * app.width) + 'sp'
                                text: 'SG Y2'
        
                            Label:
                                font_size: str(0.01875 * app.width) + 'sp'
                                text: 'SG Z'
        
                            Label:
                                font_size: str(0.01875 * app.width) + 'sp'
                                text: 'Realtime'
        
                            Label:
                                id: rt_x_sg
                                font_size: str(0.01875 * app.width) + 'sp'
                                text: '-'
        
                            Label:
                                id: rt_x1_sg
                                font_size: str(0.01875 * app.width) + 'sp'
                                text: '-'
        
                            Label:
                                id: rt_x2_sg
                                font_size: str(0.01875 * app.width) + 'sp'
                                text: '-'
        
                            Label:
                                id: rt_y1_sg
                                font_size: str(0.01875 * app.width) + 'sp'
                                text: '-'
        
                            Label:
                                id: rt_y2_sg
                                font_size: str(0.01875 * app.width) + 'sp'
                                text: '-'
        
                            Label:
                                id: rt_z_sg
                                font_size: str(0.01875 * app.width) + 'sp'
                                text: '-'
        
                            Label:
                                font_size: str(0.01875 * app.width) + 'sp'
                                text: 'Peak'
        
                            Label:
                                id: peak_x_sg
                                font_size: str(0.01875 * app.width) + 'sp'
                                text: '-'
        
                            Label:
                                id: peak_x1_sg
                                font_size: str(0.01875 * app.width) + 'sp'
                                text: '-'
        
                            Label:
                                id: peak_x2_sg
                                font_size: str(0.01875 * app.width) + 'sp'
                                text: '-'
        
                            Label:
                                id: peak_y1_sg
                                font_size: str(0.01875 * app.width) + 'sp'
                                text: '-'
        
                            Label:
                                id: peak_y2_sg
                                font_size: str(0.01875 * app.width) + 'sp'
                                text: '-'
        
                            Label:
                                id: peak_z_sg
                                font_size: str(0.01875 * app.width) + 'sp'
                                text: '-'
        
                        BoxLayout:
                            orientation: 'vertical'
                            size_hint_x: 0.3
                            padding:[0, dp(0.0520833333333)*app.height, 0, dp(0.0520833333333)*app.height]
        
                            Button:
                                font_size: str(0.01875 * app.width) + 'sp'
                                text: 'Clear'
                                on_press: root.clear_sg_vals()
        
                            ToggleButton:
                                id: raw_sg_toggle_button
                                font_size: str(0.01875 * app.width) + 'sp'
                                text: 'Show raw'
                                on_press: root.toggle_raw_sg_values()
        
                            Button:
                                font_size: str(0.01875 * app.width) + 'sp'
                                text: 'STORE PARAMS'
                                on_press: root.confirm_store_values()

        BoxLayout:
            id: status_container    
            size_hint_y: 0.08


"""
)


class CurrentAdjustment(Screen):
    wait_popup_for_tmc_read_in = None
    update_protocol_status_label_event = None

    def __init__(self, **kwargs):
        self.m = kwargs.pop("m")
        self.systemtools_sm = kwargs.pop("systemtools")
        self.l = kwargs.pop("l")
        self.kb = kwargs.pop("keyboard")
        super(CurrentAdjustment, self).__init__(**kwargs)
        self.xy_move_container.add_widget(
            widget_final_test_xy_move.FinalTestXYMove(
                machine=self.m, screen_manager=self.systemtools_sm.sm
            )
        )
        self.x1_current_adjustment_widget = CurrentAdjustmentWidget(
            m=self.m, motor=TMC_X1, localization=self.l, systemtools=self.systemtools_sm
        )
        self.current_adjustment_container.add_widget(self.x1_current_adjustment_widget)
        self.x2_current_adjustment_widget = CurrentAdjustmentWidget(
            m=self.m, motor=TMC_X2, localization=self.l, systemtools=self.systemtools_sm
        )
        self.current_adjustment_container.add_widget(self.x2_current_adjustment_widget)
        self.y1_current_adjustment_widget = CurrentAdjustmentWidget(
            m=self.m, motor=TMC_Y1, localization=self.l, systemtools=self.systemtools_sm
        )
        self.current_adjustment_container.add_widget(self.y1_current_adjustment_widget)
        self.y2_current_adjustment_widget = CurrentAdjustmentWidget(
            m=self.m, motor=TMC_Y2, localization=self.l, systemtools=self.systemtools_sm
        )
        self.current_adjustment_container.add_widget(self.y2_current_adjustment_widget)
        self.z_current_adjustment_widget = CurrentAdjustmentWidget(
            m=self.m, motor=TMC_Z, localization=self.l, systemtools=self.systemtools_sm
        )
        self.current_adjustment_container.add_widget(self.z_current_adjustment_widget)
        self.clear_sg_vals()
        self.status_container.add_widget(
            widget_sg_status_bar.SGStatusBar(
                machine=self.m, screen_manager=self.systemtools_sm.sm
            )
        )
        self.text_inputs = [
            self.x1_current_adjustment_widget.current_current_label,
            self.x2_current_adjustment_widget.current_current_label,
            self.y1_current_adjustment_widget.current_current_label,
            self.y2_current_adjustment_widget.current_current_label,
            self.z_current_adjustment_widget.current_current_label,
        ]

    def on_enter(self):
        self.kb.setup_text_inputs(self.text_inputs)
        self.m.s.FINAL_TEST = True
        self.update_protocol_status_label_event = Clock.schedule_interval(
            self.update_protocol_status_label, 0.1
        )

    def on_leave(self):
        self.m.s.FINAL_TEST = False
        if self.update_protocol_status_label_event:
            Clock.unschedule(self.update_protocol_status_label_event)

    def on_touch(self):
        for text_input in self.text_inputs:
            text_input.focus = False

    def back_to_fac_settings(self):
        if not self.m.state().startswith("Idle"):
            PopupWarning(
                self.systemtools_sm.sm, self.l, "SB not Idle!! Can't reset currents!"
            )
            return
        self.raw_sg_toggle_button.state = "normal"
        self.toggle_raw_sg_values()
        self.reset_currents()
        self.systemtools_sm.open_factory_settings_screen()

    def home(self):
        self.m.is_machine_completed_the_initial_squaring_decision = True
        self.m.is_squaring_XY_needed_after_homing = False
        self.m.request_homing_procedure("current_adjustment", "current_adjustment")

    def measure(self):
        if self.m.s.sg_x_motor_axis != -999:
            self.x_vals.append(self.m.s.sg_x_motor_axis)
            self.rt_x_sg.text = str(self.m.s.sg_x_motor_axis)
            self.peak_x_sg.text = str(max(self.x_vals))
        if self.m.s.sg_x1_motor not in [-999, None]:
            self.x1_vals.append(self.m.s.sg_x1_motor)
            self.rt_x1_sg.text = str(self.m.s.sg_x1_motor)
            self.peak_x1_sg.text = str(max(self.x1_vals))
        if self.m.s.sg_x2_motor not in [-999, None]:
            self.x2_vals.append(self.m.s.sg_x2_motor)
            self.rt_x2_sg.text = str(self.m.s.sg_x2_motor)
            self.peak_x2_sg.text = str(max(self.x2_vals))
        if self.m.s.sg_y1_motor != -999:
            self.y1_vals.append(self.m.s.sg_y1_motor)
            self.rt_y1_sg.text = str(self.m.s.sg_y1_motor)
            self.peak_y1_sg.text = str(max(self.y1_vals))
        if self.m.s.sg_y2_motor != -999:
            self.y2_vals.append(self.m.s.sg_y2_motor)
            self.rt_y2_sg.text = str(self.m.s.sg_y2_motor)
            self.peak_y2_sg.text = str(max(self.y2_vals))
        if self.m.s.sg_z_motor_axis != -999:
            self.z_vals.append(self.m.s.sg_z_motor_axis)
            self.rt_z_sg.text = str(self.m.s.sg_z_motor_axis)
            self.peak_z_sg.text = str(max(self.z_vals))

    def clear_sg_vals(self):
        self.x_vals = []
        self.x1_vals = []
        self.x2_vals = []
        self.y1_vals = []
        self.y2_vals = []
        self.z_vals = []
        self.rt_x_sg.text = "-"
        self.rt_x1_sg.text = "-"
        self.rt_x2_sg.text = "-"
        self.rt_y1_sg.text = "-"
        self.rt_y2_sg.text = "-"
        self.rt_z_sg.text = "-"
        self.peak_x_sg.text = "-"
        self.peak_x1_sg.text = "-"
        self.peak_x2_sg.text = "-"
        self.peak_y1_sg.text = "-"
        self.peak_y2_sg.text = "-"
        self.peak_z_sg.text = "-"

    def reset_currents(self):
        if not self.m.state().startswith("Idle"):
            PopupWarning(
                self.systemtools_sm.sm, self.l, "SB not Idle!! Can't reset currents!"
            )
            return False
        self.wait_popup_for_reset_currents = PopupWait(self.systemtools_sm.sm, self.l)
        if (
            not self.x1_current_adjustment_widget.reset_current()
            or not self.x2_current_adjustment_widget.reset_current()
            or not self.y1_current_adjustment_widget.reset_current()
            or not self.y2_current_adjustment_widget.reset_current()
            or not self.z_current_adjustment_widget.reset_current()
        ):
            PopupWarning(self.systemtools_sm.sm, self.l, "Issue resetting currents!")
        self.wait_while_currents_reset()

    def wait_while_currents_reset(self, dt=0):
        if self.m.s.write_protocol_buffer:
            Clock.schedule_once(self.wait_while_currents_reset, 0.2)
        else:
            Clock.schedule_once(
                lambda dt: self.wait_popup_for_reset_currents.popup.dismiss(), 0.1
            )

    def toggle_raw_sg_values(self):
        if self.raw_sg_toggle_button.state == "normal":
            self.m.send_command_to_motor(
                "REPORT RAW SG UNSET", command=REPORT_RAW_SG, value=0
            )
        else:
            self.m.send_command_to_motor(
                "REPORT RAW SG SET", command=REPORT_RAW_SG, value=1
            )

    def confirm_store_values(self):
        if self.m.state().startswith("Idle"):
            PopupConfirmStoreCurrentValues(self.m, self.systemtools_sm.sm, self.l, self)
        else:
            PopupWarning(self.systemtools_sm.sm, self.l, "SB not Idle!! Can't store")

    def store_values_and_wait_for_handshake(self):
        self.wait_popup_for_tmc_read_in = PopupWait(self.systemtools_sm.sm, self.l)
        Clock.schedule_once(self.do_tmc_value_store, 0.2)

    def do_tmc_value_store(self, dt=0):
        self.m.store_tmc_params_in_eeprom_and_handshake()
        self.wait_while_values_stored_and_read_back_in()

    def wait_while_values_stored_and_read_back_in(self, dt=0):
        if self.m.TMC_registers_have_been_read_in():
            self.wait_popup_for_tmc_read_in.popup.dismiss()
            self.wait_popup_for_tmc_read_in = None
        else:
            Clock.schedule_once(self.wait_while_values_stored_and_read_back_in, 0.2)

    def update_protocol_status_label(self, dt=0):
        if self.m.s.write_protocol_buffer:
            self.protocol_status.text = "Writing..."
        else:
            self.protocol_status.text = ""

    def grbl_reset(self):
        self.m.resume_from_alarm()
