from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.clock import Clock
from datetime import datetime
from asmcnc.skavaUI import popup_info
import traceback

from asmcnc.apps.systemTools_app.screens.calibration import widget_sg_status_bar

Builder.load_string("""
<CalibrationTesting>:

    y_axis_fw_range : y_axis_fw_range
    y1_fw_range : y1_fw_range
    y2_fw_range : y2_fw_range
    x_fw_range : x_fw_range
    z_fw_range : z_fw_range
    y_axis_bw_range : y_axis_bw_range
    y1_bw_range : y1_bw_range
    y2_bw_range : y2_bw_range
    x_bw_range : x_bw_range
    z_bw_range : z_bw_range

    y_peak_posve : y_peak_posve
    y1_peak_posve : y1_peak_posve
    y2_peak_posve : y2_peak_posve
    x_peak_posve : x_peak_posve
    z_peak_posve : z_peak_posve

    y_peak_negve : y_peak_negve
    y1_peak_negve : y1_peak_negve
    y2_peak_negve : y2_peak_negve
    x_peak_negve : x_peak_negve
    z_peak_negve : z_peak_negve

    x_test_check:x_test_check
    y_test_check:y_test_check
    z_test_check:z_test_check
    unweighted_test_check:unweighted_test_check
    sent_data_check:sent_data_check

    unweighted_test_button : unweighted_test_button
    x_load_button : x_load_button
    y_load_button : y_load_button
    z_load_button : z_load_button

    data_send_button : data_send_button

    home_button : home_button
    x0y0_jog_button : x0y0_jog_button
    x7y0_jog_button : x7y0_jog_button
    z0_jog_button : z0_jog_button

    y_peak_checkbox : y_peak_checkbox
    y1_peak_checkbox : y1_peak_checkbox
    y2_peak_checkbox : y2_peak_checkbox
    x_peak_checkbox : x_peak_checkbox
    z_peak_checkbox : z_peak_checkbox

    y_peak_posve_weighted : y_peak_posve_weighted
    y1_peak_posve_weighted : y1_peak_posve_weighted
    y2_peak_posve_weighted : y2_peak_posve_weighted
    x_peak_posve_weighted : x_peak_posve_weighted
    z_peak_posve_weighted : z_peak_posve_weighted

    y_peak_negve_weighted : y_peak_negve_weighted
    y1_peak_negve_weighted : y1_peak_negve_weighted
    y2_peak_negve_weighted : y2_peak_negve_weighted
    x_peak_negve_weighted : x_peak_negve_weighted
    z_peak_negve_weighted : z_peak_negve_weighted

    y_axis_fw_range_weighted : y_axis_fw_range_weighted
    y_axis_bw_range_weighted : y_axis_bw_range_weighted
    y_peak_checkbox_weighted : y_peak_checkbox_weighted
    y1_fw_range_weighted : y1_fw_range_weighted
    y1_bw_range_weighted : y1_bw_range_weighted
    y1_peak_checkbox_weighted : y1_peak_checkbox_weighted
    y2_fw_range_weighted : y2_fw_range_weighted
    y2_bw_range_weighted : y2_bw_range_weighted
    y2_peak_checkbox_weighted : y2_peak_checkbox_weighted
    x_fw_range_weighted : x_fw_range_weighted
    x_bw_range_weighted : x_bw_range_weighted
    x_peak_checkbox_weighted : x_peak_checkbox_weighted
    z_fw_range_weighted : z_fw_range_weighted
    z_bw_range_weighted : z_bw_range_weighted
    z_peak_checkbox_weighted : z_peak_checkbox_weighted

    status_container : status_container

    BoxLayout:
        orientation: 'vertical'

        BoxLayout:
            size_hint_y: 0.92
            orientation: 'vertical'


            BoxLayout:
                orientation: "horizontal"
                size_hint_y: 0.3

                BoxLayout:
                    orientation: "horizontal"
                    size_hint_x: 0.7

                    Button:
                        text: 'Back'
                        on_press: root.back_to_fac_settings()

                    Button:
                        id: home_button
                        text: 'Home'
                        on_press: root.home()

                    Button:
                        id: x0y0_jog_button
                        text: 'X0Y0'
                        on_press: root.zero_x_and_y()

                    Button:
                        id: x7y0_jog_button
                        text: 'X-700Y0'
                        on_press: root.mid_x_and_zero_y()

                    Button:
                        id: z0_jog_button
                        text: 'Z0'
                        on_press: root.zero_Z()

                Button:
                    text: 'STOP'
                    background_color: [1,0,0,1]
                    on_press: root.stop()
                    size_hint_x: 0.3


            GridLayout: 
                cols: 3
                size_hint_y: 0.6

                GridLayout:
                    cols: 2

                    Button:
                        id: unweighted_test_button
                        text: 'Run XYZ 0kg'
                        on_press: root.run_unweighted_test()

                    Image:
                        id: unweighted_test_check
                        source: "./asmcnc/skavaUI/img/checkbox_inactive.png"
                        center_x: self.parent.center_x
                        y: self.parent.y
                        size: self.parent.width, self.parent.height
                        allow_stretch: True

                GridLayout:
                    cols: 2

                    Button:
                        id: x_load_button
                        text: 'Run X (7.5kg)'
                        on_press: root.run_x_procedure(None)

                    Image:
                        id: x_test_check
                        source: "./asmcnc/skavaUI/img/checkbox_inactive.png"
                        center_x: self.parent.center_x
                        y: self.parent.y
                        size: self.parent.width, self.parent.height
                        allow_stretch: True

                GridLayout:
                    cols: 2

                    Button:
                        id: y_load_button
                        text: 'Run Y (7.5kg)'
                        on_press: root.run_y_procedure(None)
                    
                    Image:
                        id: y_test_check
                        source: "./asmcnc/skavaUI/img/checkbox_inactive.png"
                        center_x: self.parent.center_x
                        y: self.parent.y
                        size: self.parent.width, self.parent.height
                        allow_stretch: True

                GridLayout:
                    cols: 2

                    Button:
                        id: z_load_button
                        text: 'Run Z (2kg)'
                        on_press: root.run_z_procedure(None)

                    Image:
                        id: z_test_check
                        source: "./asmcnc/skavaUI/img/checkbox_inactive.png"
                        center_x: self.parent.center_x
                        y: self.parent.y
                        size: self.parent.width, self.parent.height
                        allow_stretch: True

                Button:
                    id: data_send_button
                    text: 'Send data to database'
                    on_press: root.send_data()
                    disabled: True

                GridLayout:
                    cols: 2

                    Label:
                        text: 'Sent data?'
                    
                    Image:
                        id: sent_data_check
                        source: "./asmcnc/skavaUI/img/checkbox_inactive.png"
                        center_x: self.parent.center_x
                        y: self.parent.y
                        size: self.parent.width, self.parent.height
                        allow_stretch: True

            BoxLayout:
                orientation: 'horizontal'
                size_hint_y: 0.1

                Label:
                    text: 'Unweighted'

                Label:
                    text: 'Weighted'

            BoxLayout:
                orientation: 'horizontal'
                size_hint_y: 1

                GridLayout: 
                    cols: 7
                    rows: 5
                    # cols_minimum: {0: 30, 1: 40, 2: 110, 3: 110, 4: 110}

                    ## Y axis

                    Label:
                        text: 'Y+: '
                        halign: 'right'
                        markup: True
                        valign: 'middle'
                        text_size: self.size

                    Label:
                        id: y_peak_posve
                        text: 'yyy'
                        halign: 'left'
                        markup: True
                        valign: 'middle'
                        text_size: self.size

                    Label:
                        id: y_axis_fw_range
                        text: 'yyy - yyy'
                        markup: True
                        valign: 'middle'
                        text_size: self.size
                        halign: 'center'

                    Label:
                        text: 'Y-: '
                        halign: 'right'
                        markup: True
                        valign: 'middle'
                        text_size: self.size

                    Label:
                        id: y_peak_negve
                        text: 'yyy'
                        halign: 'left'
                        markup: True
                        valign: 'middle'
                        text_size: self.size


                    Label:
                        id: y_axis_bw_range
                        text: 'yyy - yyy'
                        markup: True
                        valign: 'middle'
                        text_size: self.size
                        halign: 'center'


                    Image:
                        id: y_peak_checkbox
                        source: "./asmcnc/skavaUI/img/checkbox_inactive.png"
                        center_x: self.parent.center_x
                        y: self.parent.y
                        size: self.parent.width, self.parent.height
                        allow_stretch: True

                    ## Y1 axis

                    Label:
                        text: 'Y1+:'
                        halign: 'right'
                        markup: True
                        valign: 'middle'
                        text_size: self.size

                    Label:
                        id: y1_peak_posve
                        text: 'yyy'
                        halign: 'left'
                        markup: True
                        valign: 'middle'
                        text_size: self.size

                    Label:
                        id: y1_fw_range
                        text: 'yyy - yyy'
                        markup: True
                        valign: 'middle'
                        text_size: self.size
                        halign: 'center'

                    Label:
                        text: 'Y1-:'
                        halign: 'right'
                        markup: True
                        valign: 'middle'
                        text_size: self.size

                    Label:
                        id: y1_peak_negve
                        text: 'yyy'
                        halign: 'left'
                        markup: True
                        valign: 'middle'
                        text_size: self.size

                    Label:
                        id: y1_bw_range
                        text: 'yyy - yyy'
                        markup: True
                        valign: 'middle'
                        text_size: self.size
                        halign: 'center'

                    Image:
                        id: y1_peak_checkbox
                        source: "./asmcnc/skavaUI/img/checkbox_inactive.png"
                        center_x: self.parent.center_x
                        y: self.parent.y
                        size: self.parent.width, self.parent.height
                        allow_stretch: True

                    ## Y2 axis

                    Label:
                        text: 'Y2+:'
                        halign: 'right'
                        markup: True
                        valign: 'middle'
                        text_size: self.size

                    Label:
                        id: y2_peak_posve
                        text: 'yyy'
                        halign: 'left'
                        markup: True
                        valign: 'middle'
                        text_size: self.size

                    Label:
                        id: y2_fw_range
                        text: 'yyy - yyy'
                        markup: True
                        valign: 'middle'
                        text_size: self.size
                        halign: 'center'

                    Label:
                        text: 'Y2-:'
                        halign: 'right'
                        markup: True
                        valign: 'middle'
                        text_size: self.size

                    Label:
                        id: y2_peak_negve
                        text: 'yyy'
                        halign: 'left'
                        markup: True
                        valign: 'middle'
                        text_size: self.size

                    Label:
                        id: y2_bw_range
                        text: 'yyy - yyy'
                        markup: True
                        valign: 'middle'
                        text_size: self.size
                        halign: 'center'

                    Image:
                        id: y2_peak_checkbox
                        source: "./asmcnc/skavaUI/img/checkbox_inactive.png"
                        center_x: self.parent.center_x
                        y: self.parent.y
                        size: self.parent.width, self.parent.height
                        allow_stretch: True

                    ## X axis

                    Label:
                        text: 'X+:'
                        halign: 'right'
                        markup: True
                        valign: 'middle'
                        text_size: self.size

                    Label:
                        id: x_peak_posve
                        text: 'xxx'
                        halign: 'left'
                        markup: True
                        valign: 'middle'
                        text_size: self.size

                    Label:
                        id: x_fw_range
                        text: 'xxx - xxx'
                        markup: True
                        valign: 'middle'
                        text_size: self.size
                        halign: 'center'

                    Label:
                        text: 'X-:'
                        halign: 'right'
                        markup: True
                        valign: 'middle'
                        text_size: self.size

                    Label:
                        id: x_peak_negve
                        text: 'xxx'
                        halign: 'left'
                        markup: True
                        valign: 'middle'
                        text_size: self.size

                    Label:
                        id: x_bw_range
                        text: 'xxx - xxx'
                        markup: True
                        valign: 'middle'
                        text_size: self.size
                        halign: 'center'

                    Image:
                        id: x_peak_checkbox
                        source: "./asmcnc/skavaUI/img/checkbox_inactive.png"
                        center_x: self.parent.center_x
                        y: self.parent.y
                        size: self.parent.width, self.parent.height
                        allow_stretch: True


                    ## Z axis

                    Label:
                        text: 'Z-:'
                        halign: 'right'
                        markup: True
                        valign: 'middle'
                        text_size: self.size

                    Label:
                        id: z_peak_negve
                        text: 'zzz'
                        halign: 'left'
                        markup: True
                        valign: 'middle'
                        text_size: self.size

                    Label:
                        id: z_fw_range
                        text: 'zzz - zzz'
                        markup: True
                        valign: 'middle'
                        text_size: self.size
                        halign: 'center'

                    Label:
                        text: 'Z+:'
                        halign: 'right'
                        markup: True
                        valign: 'middle'
                        text_size: self.size

                    Label:
                        id: z_peak_posve
                        text: 'zzz'
                        halign: 'left'
                        markup: True
                        valign: 'middle'
                        text_size: self.size

                    Label:
                        id: z_bw_range
                        text: 'zzz - zzz'
                        markup: True
                        valign: 'middle'
                        text_size: self.size
                        halign: 'center'

                    Image:
                        id: z_peak_checkbox
                        source: "./asmcnc/skavaUI/img/checkbox_inactive.png"
                        center_x: self.parent.center_x
                        y: self.parent.y
                        size: self.parent.width, self.parent.height
                        allow_stretch: True


                GridLayout: 
                    cols: 7
                    rows: 5
                    # cols_minimum: {0: 30, 1: 40, 2: 110, 3: 110, 4: 110}

                    ## Y axis

                    Label:
                        text: 'Y+:'
                        halign: 'right'
                        markup: True
                        valign: 'middle'
                        text_size: self.size

                    Label:
                        id: y_peak_posve_weighted
                        text: 'yyy'
                        halign: 'left'
                        markup: True
                        valign: 'middle'
                        text_size: self.size

                    Label:
                        id: y_axis_fw_range_weighted
                        text: 'yyy - yyy'
                        markup: True
                        valign: 'middle'
                        text_size: self.size
                        halign: 'center'

                    Label:
                        text: 'Y-:'
                        halign: 'right'
                        markup: True
                        valign: 'middle'
                        text_size: self.size

                    Label:
                        id: y_peak_negve_weighted
                        text: 'yyy'
                        halign: 'left'
                        markup: True
                        valign: 'middle'
                        text_size: self.size

                    Label:
                        id: y_axis_bw_range_weighted
                        text: 'yyy - yyy'
                        markup: True
                        valign: 'middle'
                        text_size: self.size
                        halign: 'center'

                    Image:
                        id: y_peak_checkbox_weighted
                        source: "./asmcnc/skavaUI/img/checkbox_inactive.png"
                        center_x: self.parent.center_x
                        y: self.parent.y
                        size: self.parent.width, self.parent.height
                        allow_stretch: True

                    ## Y1 axis

                    Label:
                        text: 'Y1+:'
                        halign: 'right'
                        markup: True
                        valign: 'middle'
                        text_size: self.size

                    Label:
                        id: y1_peak_posve_weighted
                        text: 'yyy'
                        halign: 'left'
                        markup: True
                        valign: 'middle'
                        text_size: self.size

                    Label:
                        id: y1_fw_range_weighted
                        text: 'yyy - yyy'
                        markup: True
                        valign: 'middle'
                        text_size: self.size
                        halign: 'center'

                    Label:
                        text: 'Y1-:'
                        halign: 'right'
                        markup: True
                        valign: 'middle'
                        text_size: self.size

                    Label:
                        id: y1_peak_negve_weighted
                        text: 'yyy'
                        halign: 'left'
                        markup: True
                        valign: 'middle'
                        text_size: self.size

                    Label:
                        id: y1_bw_range_weighted
                        text: 'yyy - yyy'
                        markup: True
                        valign: 'middle'
                        text_size: self.size
                        halign: 'center'

                    Image:
                        id: y1_peak_checkbox_weighted
                        source: "./asmcnc/skavaUI/img/checkbox_inactive.png"
                        center_x: self.parent.center_x
                        y: self.parent.y
                        size: self.parent.width, self.parent.height
                        allow_stretch: True

                    ## Y2 axis

                    Label:
                        text: 'Y2+:'
                        halign: 'right'
                        markup: True
                        valign: 'middle'
                        text_size: self.size

                    Label:
                        id: y2_peak_posve_weighted
                        text: 'yyy'
                        halign: 'left'
                        markup: True
                        valign: 'middle'
                        text_size: self.size

                    Label:
                        id: y2_fw_range_weighted
                        text: 'yyy - yyy'
                        markup: True
                        valign: 'middle'
                        text_size: self.size
                        halign: 'center'

                    Label:
                        text: 'Y2-:'
                        halign: 'right'
                        markup: True
                        valign: 'middle'
                        text_size: self.size

                    Label:
                        id: y2_peak_negve_weighted
                        text: 'yyy'
                        halign: 'left'
                        markup: True
                        valign: 'middle'
                        text_size: self.size

                    Label:
                        id: y2_bw_range_weighted
                        text: 'yyy - yyy'
                        markup: True
                        valign: 'middle'
                        text_size: self.size
                        halign: 'center'

                    Image:
                        id: y2_peak_checkbox_weighted
                        source: "./asmcnc/skavaUI/img/checkbox_inactive.png"
                        center_x: self.parent.center_x
                        y: self.parent.y
                        size: self.parent.width, self.parent.height
                        allow_stretch: True

                    ## X axis

                    Label:
                        text: 'X+:'
                        halign: 'right'
                        markup: True
                        valign: 'middle'
                        text_size: self.size

                    Label:
                        id: x_peak_posve_weighted
                        text: 'xxx'
                        halign: 'left'
                        markup: True
                        valign: 'middle'
                        text_size: self.size

                    Label:
                        id: x_fw_range_weighted
                        text: 'xxx - xxx'
                        markup: True
                        valign: 'middle'
                        text_size: self.size
                        halign: 'center'

                    Label:
                        text: 'X-:'
                        halign: 'right'
                        markup: True
                        valign: 'middle'
                        text_size: self.size

                    Label:
                        id: x_peak_negve_weighted
                        text: 'xxx'
                        halign: 'left'
                        markup: True
                        valign: 'middle'
                        text_size: self.size

                    Label:
                        id: x_bw_range_weighted
                        text: 'xxx - xxx'
                        markup: True
                        valign: 'middle'
                        text_size: self.size
                        halign: 'center'

                    Image:
                        id: x_peak_checkbox_weighted
                        source: "./asmcnc/skavaUI/img/checkbox_inactive.png"
                        center_x: self.parent.center_x
                        y: self.parent.y
                        size: self.parent.width, self.parent.height
                        allow_stretch: True


                    ## Z axis

                    Label:
                        text: 'Z-:'
                        halign: 'right'
                        markup: True
                        valign: 'middle'
                        text_size: self.size

                    Label:
                        id: z_peak_negve_weighted
                        text: 'zzz'
                        halign: 'left'
                        markup: True
                        valign: 'middle'
                        text_size: self.size

                    Label:
                        id: z_fw_range_weighted
                        text: 'zzz - zzz'
                        markup: True
                        valign: 'middle'
                        text_size: self.size
                        halign: 'center'

                    Label:
                        text: 'Z+:'
                        halign: 'right'
                        markup: True
                        valign: 'middle'
                        text_size: self.size

                    Label:
                        id: z_peak_posve_weighted
                        text: 'zzz'
                        halign: 'left'
                        markup: True
                        valign: 'middle'
                        text_size: self.size

                    Label:
                        id: z_bw_range_weighted
                        text: 'zzz - zzz'
                        markup: True
                        valign: 'middle'
                        text_size: self.size
                        halign: 'center'

                    Image:
                        id: z_peak_checkbox_weighted
                        source: "./asmcnc/skavaUI/img/checkbox_inactive.png"
                        center_x: self.parent.center_x
                        y: self.parent.y
                        size: self.parent.width, self.parent.height
                        allow_stretch: True

        BoxLayout:
            size_hint_y: 0.08
            id: status_container
""")

MAX_XY_SPEED = 1186.0
MAX_Z_SPEED = 75.0


def log(message):
    timestamp = datetime.now()
    print (timestamp.strftime('%H:%M:%S.%f' )[:12] + ' ' + str(message))

class CalibrationTesting(Screen):

    next_run_event = None
    confirm_event = None

    checkbox_inactive = "./asmcnc/skavaUI/img/checkbox_inactive.png"
    red_cross = "./asmcnc/skavaUI/img/template_cancel.png"
    green_tick = "./asmcnc/skavaUI/img/file_select_select.png"

    X_SG_to_kg_scaling = 13.7
    Y_SG_to_kg_scaling = 11.5
    Z_SG_to_kg_scaling = 5.0

    xy_friction = 5.0
    z_friction = 3.0

    tolerance = 0.8

    def __init__(self, **kwargs):
        super(CalibrationTesting, self).__init__(**kwargs)
        self.setup_arrays()

        self.m = kwargs['m']
        self.systemtools_sm = kwargs['systemtools']
        self.calibration_db = kwargs['calibration_db']
        self.sm = kwargs['sm']
        self.l = kwargs['l']

        # used to only measure axis in motion
        self.x_running = False
        self.y_running = False
        self.z_running = False

        self.stage = ''
        self.statuses = []

        self.status_container.add_widget(widget_sg_status_bar.SGStatusBar(machine=self.m, screen_manager=self.systemtools_sm.sm))

    def setup_arrays(self):
        #x loads with vector & pos
        self.x_vals = []
        #raw x loads
        self.raw_x_vals = []

        #z loads with vector & pos
        self.z_vals = []
        #raw z loads
        self.raw_z_vals = []

        #y_motor loads with vector & pos
        self.y_vals = []
        #raw y_motor loads
        self.raw_y_vals = []

        #y1_motor loads with vector & pos
        self.y1_vals = []
        #raw y1 loads
        self.raw_y1_vals = []

        #y2_motor loads with vector & pos
        self.y2_vals = []
        #raw y2 vals
        self.raw_y2_vals = []

        self.unweighted_data = []

    # Stage is used to detect which part of the operation overnight test is in, both in screen functions & data
    def set_stage(self, stage):

        self.stage = stage
        stage_id = self.calibration_db.get_stage_id_by_description(self.stage)
        self.calibration_db.insert_final_test_stage(self.sn_for_db, stage_id)
        self.status_data_dict[self.stage] = []
        log("Overnight test, stage: " + str(self.stage))


    def send_data(self):

        pass
        # try:
        #     serial = self.calibration_db.get_serial_number()
        #     self.calibration_db.send_final_test_calibration(serial, self.unweighted_data[0], self.unweighted_data[1], self.unweighted_data[2], self.x_vals, self.y_vals, self.z_vals)
        #     self.sent_data_check.source = "./asmcnc/skavaUI/img/file_select_select.png"
        # except:
        #     self.sent_data_check.source = "./asmcnc/skavaUI/img/template_cancel.png"
        #     print(traceback.format_exc())


    def stop(self):
        self.x_running = False
        self.y_running = False
        self.z_running = False
        if self.next_run_event != None: Clock.unschedule(self.next_run_event)
        if self.confirm_event != None: Clock.unschedule(self.confirm_event)
        popup_info.PopupStop(self.m, self.sm, self.l)
        self.enable_run_buttons()


    def on_enter(self):
        self.m.s.FINAL_TEST = True
        if self.next_run_event != None: Clock.unschedule(self.next_run_event)
        if self.confirm_event != None: Clock.unschedule(self.confirm_event)
        self.enable_run_buttons()


    def on_leave(self):
        self.m.s.FINAL_TEST = False
        if self.next_run_event != None: Clock.unschedule(self.next_run_event)
        if self.confirm_event != None: Clock.unschedule(self.confirm_event)
        self.enable_run_buttons()


    def back_to_fac_settings(self):
        self.systemtools_sm.open_factory_settings_screen()


    def home(self):
        self.m.is_machine_completed_the_initial_squaring_decision = True
        self.m.is_squaring_XY_needed_after_homing = False
        self.m.request_homing_procedure('calibration_testing','calibration_testing')


    def reset(self):
        if self.next_run_event != None: Clock.unschedule(self.next_run_event)
        if self.confirm_event != None: Clock.unschedule(self.confirm_event)

        self.m.resume_from_alarm()
        self.enable_run_buttons()


    def zero_x_and_y(self):
        self.m.jog_absolute_xy(self.m.x_min_jog_abs_limit, self.m.y_min_jog_abs_limit, 6000)


    def mid_x_and_zero_y(self):
        self.m.jog_absolute_xy(-700, self.m.y_min_jog_abs_limit, 6000)


    def zero_Z(self):
        self.m.jog_absolute_single_axis('Z', self.m.z_max_jog_abs_limit, 750)


    def disable_x_measurement(self, dt):
        self.x_running = False


    def disable_z_measurement(self, dt):
        self.z_running = False


    def disable_y_measurement(self, dt):
        self.y_running = False


    def enable_run_buttons(self):
        self.x_load_button.disabled = False
        self.y_load_button.disabled = False
        self.z_load_button.disabled = False
        self.unweighted_test_button.disabled = False
        self.home_button.disabled = False
        self.x0y0_jog_button.disabled = False
        self.x7y0_jog_button.disabled = False
        self.z0_jog_button.disabled = False        


    def disable_run_buttons(self):
        self.x_load_button.disabled = True
        self.y_load_button.disabled = True
        self.z_load_button.disabled = True
        self.unweighted_test_button.disabled = True
        self.home_button.disabled = True
        self.x0y0_jog_button.disabled = True
        self.x7y0_jog_button.disabled = True
        self.z0_jog_button.disabled = True

    
    def measure(self):

        if not (self.x_running and self.m.feed_rate() < 1200) and not (self.y_running and self.m.feed_rate() < 1200) and not (self.z_running and self.m.feed_rate() < 80):
            return

        cur_pos_x = self.m.mpos_x()
        cur_pos_y = self.m.mpos_y()
        cur_pos_z = self.m.mpos_z()

        x_dir = 0 if len(self.x_vals) > 0 and self.x_vals[len(self.x_vals - 1)][1] < cur_pos_x else 1
        y_dir = 0 if len(self.y_vals) > 0 and self.y_vals[len(self.y_vals - 1)][1] < cur_pos_y else 1
        z_dir = 1 if len(self.z_vals) > 0 and self.z_vals[len(self.z_vals - 1)][1] < cur_pos_z else 0

        x_sg = self.m.s.sg_x_motor_axis
        y_sg = self.m.s.sg_y_axis
        y1_sg = self.m.s.sg_y1_motor
        y2_sg = self.m.s.sg_y2_motor
        z_sg = self.m.s.sg_z_motor_axis

        tmc_temp = self.m.s.motor_driver_temp
        pcb_temp = self.m.s.pcb_temp
        mot_temp = self.m.s.transistor_heatsink_temp

        if -999 < x_sg < 1023: self.raw_x_vals.append(x_sg)
        if -999 < y_sg < 1023: self.raw_y_vals.append(y_sg)
        if -999 < y1_sg < 1023: self.raw_y1_vals.append(y1_sg)
        if -999 < y2_sg < 1023: self.raw_y2_vals.append(y2_sg)
        if -999 < z_sg < 1023: self.raw_z_vals.append(z_sg)

        self.update_peaks()

        timestamp = datetime.now()

        status = [self.stage, cur_pos_x, cur_pos_y, cur_pos_z, x_dir, y_dir, z_dir, x_sg, y_sg, y1_sg, y2_sg, z_sg, tmc_temp, pcb_temp, mot_temp, timestamp]

        self.statuses.append(status)


    def update_peaks(self):

        if self.stage == "Unweighted":

            self.get_peak_as_string(self.x_peak_posve, self.raw_x_vals)
            self.get_peak_as_string(self.y_peak_posve, self.raw_y_vals)
            self.get_peak_as_string(self.y1_peak_posve, self.raw_y1_vals)
            self.get_peak_as_string(self.y2_peak_posve, self.raw_y2_vals)
            self.get_peak_as_string(self.z_peak_posve, self.raw_z_vals)
            return

        if self.stage == "Weighted":

            self.get_peak_as_string(self.x_peak_posve_weighted, self.raw_x_vals)
            self.get_peak_as_string(self.y_peak_posve_weighted, self.raw_y_vals)
            self.get_peak_as_string(self.y1_peak_posve_weighted, self.raw_y1_vals)
            self.get_peak_as_string(self.y2_peak_posve_weighted, self.raw_y2_vals)
            self.get_peak_as_string(self.z_peak_posve_weighted, self.raw_z_vals)
            return


    def get_peak_as_string(self, label_id, raw_vals):

        try: label_id.text = str(max(raw_vals))
        except: pass


    def run_z_procedure(self, dt):

        # start run, run all the way down and then all the way back up. 

        if self.m.mpos_z() != self.m.z_max_jog_abs_limit:
            popup_info.PopupError(self.sm, self.l, "Move Z to Z0 first!")
            return

        self.disable_run_buttons()

        self.setup_arrays()

        if self.stage != "WeightedFT":
            self.set_stage("WeightedFT")

        self.set_weighted_z_range()

        self.z_running = True

        self.m.send_any_gcode_command('G91 G1 Z-149 F75')
        self.m.send_any_gcode_command('G91 G1 Z149 F75')

        # poll to see when run is done
        self.confirm_event = Clock.schedule_interval(self.confirm_z, 5)


    def confirm_z(self, dt):
        if self.m.state().startswith('Idle'):
            self.z_running = False
            self.enable_run_buttons()
            self.z_test_check.source = "./asmcnc/skavaUI/img/file_select_select.png"
            self.tick_checkbox(self.z_peak_checkbox_weighted, self.check_in_range(self.z_peak_posve_weighted))


    def run_y_procedure(self, dt):

        # start run, run all the way down and then all the way back up. 

        self.disable_run_buttons()

        self.setup_arrays()

        if self.stage != "WeightedFT":
            self.set_stage("WeightedFT")

        self.set_weighted_y_range()

        self.y_running = True

        self.m.send_any_gcode_command('G91 G1 Y2500 F1186')
        self.m.send_any_gcode_command('G91 G1 Y-2500 F1186')

        # poll to see when run is done
        self.confirm_event = Clock.schedule_interval(self.confirm_y, 5)


    def confirm_y(self, dt):
        if self.m.state().startswith('Idle'):
            self.y_running = False
            self.enable_run_buttons()
            self.y_test_check.source = "./asmcnc/skavaUI/img/file_select_select.png"
            self.tick_checkbox(self.y_peak_checkbox_weighted, self.check_in_range(self.y_peak_posve_weighted))
            self.tick_checkbox(self.y1_peak_checkbox_weighted, self.check_in_range(self.y1_peak_posve_weighted))
            self.tick_checkbox(self.y2_peak_checkbox_weighted, self.check_in_range(self.y2_peak_posve_weighted))


    def run_x_procedure(self, dt):

        # start run, run all the way down and then all the way back up. 

        self.disable_run_buttons()

        self.setup_arrays()

        if self.stage != "WeightedFT":
            self.set_stage("WeightedFT")

        self.set_weighted_x_range()

        self.x_running = True

        self.m.send_any_gcode_command('G91 G1 x1298 F1186')
        self.m.send_any_gcode_command('G91 G1 x-1298 F1186')

        # poll to see when run is done
        self.confirm_event = Clock.schedule_interval(self.confirm_x, 5)


    def confirm_x(self, dt):

        if self.m.state().startswith('Idle'):

            self.x_running = False
            self.enable_run_buttons()
            self.x_test_check.source = "./asmcnc/skavaUI/img/file_select_select.png"
            self.tick_checkbox(self.x_peak_checkbox_weighted, self.check_in_range(self.x_peak_posve_weighted))


    def run_unweighted_test(self):
        
        if self.m.state().startswith('Idle'):

            self.disable_run_buttons()

            self.set_stage("UnweightedFT")

            self.zero_x_and_y()
            self.zero_Z()


            self.next_run_event = Clock.schedule_once(self.part_1_unweighted_x, 3)

        else:

            popup_info.PopupError(self.sm, self.l, "SB not Idle! Check status")


    def part_1_unweighted_x(self, dt):

        if self.m.state().startswith('Idle'):

            self.setup_arrays()
            self.set_unweighted_x_range()
            self.x_running = True
            self.m.send_any_gcode_command('G91 G1 x1298 F1186')
            self.m.send_any_gcode_command('G91 G1 x-1298 F1186')
            self.next_run_event = Clock.schedule_once(self.part_2_unweighted_y, 20)

        else:
            self.next_run_event = Clock.schedule_once(self.part_1_unweighted_x, 3)

    def part_2_unweighted_y(self, dt):

        if self.m.state().startswith('Idle'):

            self.set_unweighted_y_range()
            self.x_running = False
            self.y_running = True
            self.m.send_any_gcode_command('G91 G1 Y2500 F1186')
            self.m.send_any_gcode_command('G91 G1 Y-2500 F1186')
            self.next_run_event = Clock.schedule_once(self.part_3_unweighted_z, 20)

        else:
            self.next_run_event = Clock.schedule_once(self.part_2_unweighted_y, 3)


    def part_3_unweighted_z(self, dt):

        if self.m.state().startswith('Idle'):

            self.set_unweighted_z_range()
            self.y_running = False
            self.z_running = True
            self.m.send_any_gcode_command('G91 G1 Z-149 F75')
            self.m.send_any_gcode_command('G91 G1 Z149 F75')
            self.confirm_event = Clock.schedule_once(self.confirm_unweighted, 20)


        else:
            self.next_run_event = Clock.schedule_once(self.part_3_unweighted_z, 3)


    def confirm_unweighted(self, dt):

        if self.m.state().startswith('Idle'):

            self.z_running = False
            self.unweighted_data.append(self.x_vals)
            self.unweighted_data.append(self.y_vals)
            self.unweighted_data.append(self.z_vals)
            self.enable_run_buttons()
            self.data_send_button.disabled = False
            self.unweighted_test_check.source = "./asmcnc/skavaUI/img/file_select_select.png"
            self.pass_or_fail_unweighted_peak_loads()


        else: 
            self.confirm_event = Clock.schedule_once(self.confirm_unweighted, 3)


    ## SET TICKS
    def tick_checkbox(self, checkbox_id, tick):

        if tick: 
            checkbox_id.source = self.green_tick

        else: 
            checkbox_id.source = self.red_cross


    def check_in_range(self, peak_id):

        within_plus_minus = 400

        try: 
            if (-1*within_plus_minus) < int(peak_id.text) < within_plus_minus: return True
            else: return False

        except:
            return False


    def pass_or_fail_unweighted_peak_loads(self):

        within_plus_minus = 400

        self.tick_checkbox(self.y_peak_checkbox, self.check_in_range(self.y_peak_posve))
        self.tick_checkbox(self.y1_peak_checkbox, self.check_in_range(self.y1_peak_posve))
        self.tick_checkbox(self.y2_peak_checkbox, self.check_in_range(self.y2_peak_posve))
        self.tick_checkbox(self.x_peak_checkbox, self.check_in_range(self.x_peak_posve))
        self.tick_checkbox(self.z_peak_checkbox, self.check_in_range(self.z_peak_posve))


    def up_range(self, friction, load):

        expected_min = (friction + float(load))*(1.0 - self.tolerance)
        expected_max = (friction + float(load))*(1.0 + self.tolerance)

        return expected_min, expected_max

    def down_range(self, friction, load):

        expected_min = (friction - float(load))*(1.0 - self.tolerance)
        expected_max = (friction - float(load))*(1.0 + self.tolerance)

        return expected_min, expected_max


    def get_range_text(self, friction, load, scaling):

        fw_expected_min, fw_expected_max = self.up_range(friction, load)
        bw_expected_min, bw_expected_max = self.down_range(friction, load)

        fw_range_text = str(fw_expected_min*scaling) + " - " + str(fw_expected_max*scaling)
        bw_range_text = str(bw_expected_min*scaling) + " - " + str(bw_expected_max*scaling)

        return fw_range_text, bw_range_text


    def set_unweighted_x_range(self):

        x_fw_range_text, x_bw_range_text = self.get_range_text(self.xy_friction, 0, self.X_SG_to_kg_scaling)

        self.x_fw_range.text = x_fw_range_text
        self.x_bw_range.text = x_bw_range_text


    def set_weighted_x_range(self):

        x_fw_range_text, x_bw_range_text = self.get_range_text(self.xy_friction, 7.5, self.X_SG_to_kg_scaling)

        self.x_fw_range_weighted.text = x_fw_range_text
        self.x_bw_range_weighted.text = x_bw_range_text


    def set_unweighted_y_range(self):

        y_fw_range_text, y_bw_range_text = self.get_range_text(self.xy_friction, 0, self.Y_SG_to_kg_scaling)

        self.y_axis_fw_range.text = y_fw_range_text
        self.y1_fw_range.text = y_fw_range_text
        self.y2_fw_range.text = y_fw_range_text

        self.y_axis_bw_range.text = y_bw_range_text
        self.y1_bw_range.text = y_bw_range_text
        self.y2_bw_range.text = y_bw_range_text


    def set_weighted_y_range(self):

        y_fw_range_text, y_bw_range_text = self.get_range_text(self.xy_friction, 7.5, self.Y_SG_to_kg_scaling)

        self.y_axis_fw_range_weighted.text = y_fw_range_text
        self.y1_fw_range_weighted.text = y_fw_range_text
        self.y2_fw_range_weighted.text = y_fw_range_text

        self.y_axis_bw_range_weighted.text = y_bw_range_text
        self.y1_bw_range_weighted.text = y_bw_range_text
        self.y2_bw_range_weighted.text = y_bw_range_text


    def set_unweighted_z_range(self):

        z_fw_range_text, z_bw_range_text = self.get_range_text(self.z_friction, 0, self.Z_SG_to_kg_scaling)

        self.z_fw_range.text = z_fw_range_text
        self.z_bw_range.text = z_bw_range_text

    def set_weighted_z_range(self):

        z_fw_range_text, z_bw_range_text = self.get_range_text(self.z_friction, 2, self.Z_SG_to_kg_scaling)

        self.z_fw_range_weighted.text = z_fw_range_text
        self.z_bw_range_weighted.text = z_bw_range_text

