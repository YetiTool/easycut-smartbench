from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from asmcnc.apps.maintenance_app.widget_maintenance_xy_move import MaintenanceXYMove
from asmcnc.apps.systemTools_app.screens.calibration.widget_current_adjustment import CurrentAdjustmentWidget
from asmcnc.comms.yeti_grbl_protocol.c_defines import *

Builder.load_string("""
<CurrentAdjustment>:

    xy_move_container:xy_move_container
    current_adjustment_container:current_adjustment_container

    rt_x_sg:rt_x_sg
    rt_y1_sg:rt_y1_sg
    rt_y2_sg:rt_y2_sg
    peak_x_sg:peak_x_sg
    peak_y1_sg:peak_y1_sg
    peak_y2_sg:peak_y2_sg

    raw_sg_toggle_button : raw_sg_toggle_button

    GridLayout:
        cols: 2

        GridLayout:
            rows: 2
            size_hint_x: 0.5

            BoxLayout:
                id: xy_move_container
                pos_hint: {'center_x': .5, 'center_y': .5}
                size_hint: (None,None)
                height: dp(360)
                width: dp(270)

            BoxLayout:
                size_hint_y: 0.1
                padding: [0, dp(30), dp(150), 0]

                Button:
                    text: 'Factory Settings'
                    on_press: root.back_to_fac_settings()

        GridLayout:
            rows: 2

            GridLayout:
                cols: 2

                GridLayout:
                    rows:2

                    Label:
                        size_hint_y: 0.2
                        text: 'Active Current Adjustment'

                    BoxLayout:
                        id: current_adjustment_container

                BoxLayout:
                    size_hint_x: 0.3
                    padding: [0, dp(75), 0, dp(75)]

                    Button:
                        text: 'Reset'
                        on_press: root.reset_currents()

            GridLayout:
                cols: 2

                # SG value status box
                GridLayout:
                    rows: 3
                    cols: 4

                    Label

                    Label:
                        text: 'SG X'

                    Label:
                        text: 'SG Y1'

                    Label:
                        text: 'SG Y2'

                    Label:
                        text: 'Realtime'

                    Label:
                        id: rt_x_sg
                        text: '-'

                    Label:
                        id: rt_y1_sg
                        text: '-'

                    Label:
                        id: rt_y2_sg
                        text: '-'

                    Label:
                        text: 'Peak'

                    Label:
                        id: peak_x_sg
                        text: '-'

                    Label:
                        id: peak_y1_sg
                        text: '-'

                    Label:
                        id: peak_y2_sg
                        text: '-'

                BoxLayout:
                    orientation: 'vertical'
                    size_hint_x: 0.3
                    padding: [0, dp(25), 0, dp(25)]

                    Button:
                        text: 'Clear'
                        on_press: root.clear_sg_vals()

                    ToggleButton:
                        id: raw_sg_toggle_button
                        text: 'Show raw'
                        on_press: root.toggle_raw_sg_values()


""")

class CurrentAdjustment(Screen):

    def __init__(self, **kwargs):
        super(CurrentAdjustment, self).__init__(**kwargs)

        self.m = kwargs['m']
        self.systemtools_sm = kwargs['systemtools']
        self.l = kwargs['l']

        # Movement widget
        self.xy_move_widget = MaintenanceXYMove(machine=self.m, screen_manager=self.systemtools_sm, localization=self.l)
        self.xy_move_container.add_widget(self.xy_move_widget)

        # Current adjustment widgets
        self.x_current_adjustment_widget = CurrentAdjustmentWidget(m=self.m, motor=TMC_X1, localization=self.l, systemtools=self.systemtools_sm)
        self.current_adjustment_container.add_widget(self.x_current_adjustment_widget)

        self.y1_current_adjustment_widget = CurrentAdjustmentWidget(m=self.m, motor=TMC_Y1, localization=self.l, systemtools=self.systemtools_sm)
        self.current_adjustment_container.add_widget(self.y1_current_adjustment_widget)

        self.y2_current_adjustment_widget = CurrentAdjustmentWidget(m=self.m, motor=TMC_Y2, localization=self.l, systemtools=self.systemtools_sm)
        self.current_adjustment_container.add_widget(self.y2_current_adjustment_widget)

        self.clear_sg_vals()

    def on_enter(self):
        self.m.s.FINAL_TEST = True

    def on_leave(self):
        self.m.s.FINAL_TEST = False
        self.reset_currents()
        self.m.send_command_to_motor("REPORT RAW SG UNSET", command=REPORT_RAW_SG, value=0)

    def back_to_fac_settings(self):
        self.systemtools_sm.open_factory_settings_screen()

    def measure(self):
        if self.m.s.sg_x_motor_axis != -999:
            self.x_vals.append(self.m.s.sg_x_motor_axis)
            self.rt_x_sg.text = str(self.m.s.sg_x_motor_axis)
            self.peak_x_sg.text = str(max(self.x_vals, key=abs))

        if self.m.s.sg_y1_motor != -999:
            self.y1_vals.append(self.m.s.sg_y1_motor)
            self.rt_y1_sg.text = str(self.m.s.sg_y1_motor)
            self.peak_y1_sg.text = str(max(self.y1_vals, key=abs))

        if self.m.s.sg_y2_motor != -999:
            self.y2_vals.append(self.m.s.sg_y2_motor)
            self.rt_y2_sg.text = str(self.m.s.sg_y2_motor)
            self.peak_y2_sg.text = str(max(self.y2_vals, key=abs))

    def clear_sg_vals(self):
        self.x_vals = []
        self.y1_vals = []
        self.y2_vals = []

        self.rt_x_sg.text = '-'
        self.rt_y1_sg.text = '-'
        self.rt_y2_sg.text = '-'
        self.peak_x_sg.text = '-'
        self.peak_y1_sg.text = '-'
        self.peak_y2_sg.text = '-'

    def reset_currents(self):
        self.x_current_adjustment_widget.reset_current()
        self.y1_current_adjustment_widget.reset_current()
        self.y2_current_adjustment_widget.reset_current()

    def toggle_raw_sg_values(self):
        
        if self.raw_sg_toggle_button.state == 'normal':
            self.m.send_command_to_motor("REPORT RAW SG UNSET", command=REPORT_RAW_SG, value=0)
        
        else:
            self.m.send_command_to_motor("REPORT RAW SG SET", command=REPORT_RAW_SG, value=1)
