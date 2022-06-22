from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.clock import Clock
from datetime import datetime
from asmcnc.skavaUI import popup_info
import math
import traceback
from time import sleep
import threading
from datetime import datetime
from asmcnc.production.database.payload_publisher import Publisher

from asmcnc.apps.systemTools_app.screens.calibration import widget_sg_status_bar

from asmcnc.apps.systemTools_app.screens.popup_system import PopupStopOvernightTest
from asmcnc.skavaUI import popup_info

Builder.load_string("""
<OvernightTesting>:

    back_button : back_button
    home_button : home_button
    overnight_test_button : overnight_test_button
    stop_button : stop_button

    six_hour_wear_in_button : six_hour_wear_in_button
    six_hour_wear_in_checkbox : six_hour_wear_in_checkbox
    recalibration_button : recalibration_button
    recalibration_checkbox : recalibration_checkbox
    fully_calibrated_run_button : fully_calibrated_run_button
    fully_calibrated_run_checkbox : fully_calibrated_run_checkbox
    retry_six_hour_wear_in_data_send : retry_six_hour_wear_in_data_send
    sent_six_hour_wear_in_data : sent_six_hour_wear_in_data
    retry_recalibration_data_send : retry_recalibration_data_send
    sent_recalibration_data : sent_recalibration_data
    retry_fully_calibrated_run_data_send : retry_fully_calibrated_run_data_send
    sent_fully_recalibrated_run_data : sent_fully_recalibrated_run_data

    y_wear_in_peak_pos : y_wear_in_peak_pos
    y1_wear_in_peak_pos : y1_wear_in_peak_pos
    y2_wear_in_peak_pos : y2_wear_in_peak_pos
    x_wear_in_peak_pos : x_wear_in_peak_pos
    z_wear_in_peak_pos : z_wear_in_peak_pos

    y_wear_in_peak_neg : y_wear_in_peak_neg
    y1_wear_in_peak_neg : y1_wear_in_peak_neg
    y2_wear_in_peak_neg : y2_wear_in_peak_neg
    x_wear_in_peak_neg : x_wear_in_peak_neg
    z_wear_in_peak_neg : z_wear_in_peak_neg

    y_wear_in_checkbox : y_wear_in_checkbox
    y1_wear_in_checkbox : y1_wear_in_checkbox
    y2_wear_in_checkbox : y2_wear_in_checkbox
    x_wear_in_checkbox : x_wear_in_checkbox
    z_wear_in_checkbox : z_wear_in_checkbox

    y_fully_calibrated_peak_pos : y_fully_calibrated_peak_pos
    y1_fully_calibrated_peak_pos : y1_fully_calibrated_peak_pos
    y2_fully_calibrated_peak_pos : y2_fully_calibrated_peak_pos
    x_fully_calibrated_peak_pos : x_fully_calibrated_peak_pos
    z_fully_calibrated_peak_pos : z_fully_calibrated_peak_pos

    y_fully_calibrated_peak_neg : y_fully_calibrated_peak_neg
    y1_fully_calibrated_peak_neg : y1_fully_calibrated_peak_neg
    y2_fully_calibrated_peak_neg : y2_fully_calibrated_peak_neg
    x_fully_calibrated_peak_neg : x_fully_calibrated_peak_neg
    z_fully_calibrated_peak_neg : z_fully_calibrated_peak_neg

    y_fully_calibrated_checkbox : y_fully_calibrated_checkbox
    y1_fully_calibrated_checkbox : y1_fully_calibrated_checkbox
    y2_fully_calibrated_checkbox : y2_fully_calibrated_checkbox
    x_fully_calibrated_checkbox : x_fully_calibrated_checkbox
    z_fully_calibrated_checkbox : z_fully_calibrated_checkbox

    status_container : status_container

    BoxLayout:
        orientation: 'vertical'

        BoxLayout:
            size_hint_y: 0.92
            orientation: 'vertical'

            BoxLayout:
                orientation: 'vertical'
                size_hint_y: 0.5   

                BoxLayout: 
                    orientation: 'horizontal'
                    size_hint_y: 0.26

                    Button:
                        id: back_button
                        text: 'Back'
                        on_press: root.back_to_fac_settings()

                    Button:
                        id: home_button
                        text: 'Home'
                        on_press: root.home()
                        background_color: [0,0,1,1]

                    Button:
                        id: overnight_test_button
                        text: 'START'
                        on_press: root.start_full_overnight_test()
                        background_color: [0,1,0,1]

                    Button:
                        id: stop_button
                        text: 'STOP'
                        background_color: [1,0,0,1]
                        on_press: root.stop()
                        background_normal: ''

                Label: 
                    text: "Overnight test stages"
                    markup: True
                    text_size: self.size
                    halign: "center"
                    size_hint_y: 0.11

                BoxLayout: 
                    orientation: 'horizontal'
                    size_hint_y: 0.26

                    BoxLayout: 
                        orientation: 'horizontal'

                        Button:
                            id: six_hour_wear_in_button
                            text: '6 hour wear-in'
                            size_hint_x: 0.7
                            on_press: root.start_six_hour_wear_in()



                        BoxLayout:
                            size_hint_x: 0.3

                            Image:
                                id: six_hour_wear_in_checkbox
                                source: "./asmcnc/skavaUI/img/checkbox_inactive.png"
                                center_x: self.parent.center_x
                                y: self.parent.y
                                size: self.parent.width, self.parent.height
                                allow_stretch: True

                    BoxLayout: 
                        orientation: 'horizontal'

                        Button:
                            id: recalibration_button
                            text: 're-calibration'
                            size_hint_x: 0.7
                            on_press: root.start_recalibration()


                        BoxLayout:
                            size_hint_x: 0.3

                            Image:
                                id: recalibration_checkbox
                                source: "./asmcnc/skavaUI/img/checkbox_inactive.png"
                                center_x: self.parent.center_x
                                y: self.parent.y
                                size: self.parent.width, self.parent.height
                                allow_stretch: True
                    BoxLayout: 
                        orientation: 'horizontal'

                        Button:
                            id: fully_calibrated_run_button
                            text: 'post-calibration run'
                            size_hint_x: 0.7
                            on_press: root.start_fully_calibrated_final_run()


                        BoxLayout:
                            size_hint_x: 0.3

                            Image:
                                id: fully_calibrated_run_checkbox
                                source: "./asmcnc/skavaUI/img/checkbox_inactive.png"
                                center_x: self.parent.center_x
                                y: self.parent.y
                                size: self.parent.width, self.parent.height
                                allow_stretch: True

                Label: 
                    text: "Data sends"
                    markup: True
                    text_size: self.size
                    halign: "center"
                    size_hint_y: 0.11

                BoxLayout: 
                    orientation: 'horizontal'
                    size_hint_y: 0.26

                    BoxLayout: 
                        orientation: 'horizontal'

                        Button:
                            id: retry_six_hour_wear_in_data_send
                            text: 'Retry'
                            size_hint_x: 0.7
                            on_press: root.send_six_hour_wear_in_data()


                        BoxLayout:
                            size_hint_x: 0.3

                            Image:
                                id: sent_six_hour_wear_in_data
                                source: "./asmcnc/skavaUI/img/checkbox_inactive.png"
                                center_x: self.parent.center_x
                                y: self.parent.y
                                size: self.parent.width, self.parent.height
                                allow_stretch: True

                    BoxLayout: 
                        orientation: 'horizontal'

                        Button:
                            id: retry_recalibration_data_send
                            text: 'Retry'
                            size_hint_x: 0.7
                            on_press: root.send_recalibration_data()


                        BoxLayout:
                            size_hint_x: 0.3

                            Image:
                                id: sent_recalibration_data
                                source: "./asmcnc/skavaUI/img/checkbox_inactive.png"
                                center_x: self.parent.center_x
                                y: self.parent.y
                                size: self.parent.width, self.parent.height
                                allow_stretch: True
                    BoxLayout: 
                        orientation: 'horizontal'

                        Button:
                            id: retry_fully_calibrated_run_data_send
                            text: 'Retry'
                            size_hint_x: 0.7
                            on_press: root.send_fully_calibrated_final_run_data()


                        BoxLayout:
                            size_hint_x: 0.3

                            Image:
                                id: sent_fully_recalibrated_run_data
                                source: "./asmcnc/skavaUI/img/checkbox_inactive.png"
                                center_x: self.parent.center_x
                                y: self.parent.y
                                size: self.parent.width, self.parent.height
                                allow_stretch: True

            BoxLayout: 
                orientation: 'vertical'
                size_hint_y: 0.5

                Label: 
                    text: 'Peak testing'
                    size_hint_y: 0.11

                GridLayout:
                    cols: 3
                    size_hint_y: 0.89

                    ## SIX HOUR WEAR IN PEAKS

                    GridLayout:
                        cols: 5
                        rows: 5
                        size_hint_y: 0.5
                        spacing: [5,0]

                        Label:
                            text: 'Y+:  '
                            halign: 'right'
                            markup: True
                            valign: 'middle'
                            text_size: self.size

                        Label:
                            id: y_wear_in_peak_pos
                            text: 'yyy'
                            halign: 'left'
                            markup: True
                            valign: 'middle'
                            text_size: self.size

                        Label:
                            text: 'Y-:  '
                            halign: 'right'
                            markup: True
                            valign: 'middle'
                            text_size: self.size

                        Label:
                            id: y_wear_in_peak_neg
                            text: 'yyy'
                            halign: 'left'
                            markup: True
                            valign: 'middle'
                            text_size: self.size

                        Image:
                            id: y_wear_in_checkbox
                            source: "./asmcnc/skavaUI/img/checkbox_inactive.png"
                            center_x: self.parent.center_x
                            y: self.parent.y
                            size: self.parent.width, self.parent.height
                            allow_stretch: True

                        Label:
                            text: 'Y1+:  '
                            halign: 'right'
                            markup: True
                            valign: 'middle'
                            text_size: self.size

                        Label:
                            id: y1_wear_in_peak_pos
                            text: 'yyy'
                            halign: 'left'
                            markup: True
                            valign: 'middle'
                            text_size: self.size

                        Label:
                            text: 'Y1-:  '
                            halign: 'right'
                            markup: True
                            valign: 'middle'
                            text_size: self.size

                        Label:
                            id: y1_wear_in_peak_neg
                            text: 'yyy'
                            halign: 'left'
                            markup: True
                            valign: 'middle'
                            text_size: self.size

                        Image:
                            id: y1_wear_in_checkbox
                            source: "./asmcnc/skavaUI/img/checkbox_inactive.png"
                            center_x: self.parent.center_x
                            y: self.parent.y
                            size: self.parent.width, self.parent.height
                            allow_stretch: True


                        Label:
                            text: 'Y2+:  '
                            halign: 'right'
                            markup: True
                            valign: 'middle'
                            text_size: self.size

                        Label:
                            id: y2_wear_in_peak_pos
                            text: 'yyy'
                            halign: 'left'
                            markup: True
                            valign: 'middle'
                            text_size: self.size

                        Label:
                            text: 'Y2-:  '
                            halign: 'right'
                            markup: True
                            valign: 'middle'
                            text_size: self.size

                        Label:
                            id: y2_wear_in_peak_neg
                            text: 'yyy'
                            halign: 'left'
                            markup: True
                            valign: 'middle'
                            text_size: self.size

                        Image:
                            id: y2_wear_in_checkbox
                            source: "./asmcnc/skavaUI/img/checkbox_inactive.png"
                            center_x: self.parent.center_x
                            y: self.parent.y
                            size: self.parent.width, self.parent.height
                            allow_stretch: True

                        Label:
                            text: 'X+:  '
                            halign: 'right'
                            markup: True
                            valign: 'middle'
                            text_size: self.size

                        Label:
                            id: x_wear_in_peak_pos
                            text: 'xxx'
                            halign: 'left'
                            markup: True
                            valign: 'middle'
                            text_size: self.size

                        Label:
                            text: 'X-:  '
                            halign: 'right'
                            markup: True
                            valign: 'middle'
                            text_size: self.size

                        Label:
                            id: x_wear_in_peak_neg
                            text: 'xxx'
                            halign: 'left'
                            markup: True
                            valign: 'middle'
                            text_size: self.size


                        Image:
                            id: x_wear_in_checkbox
                            source: "./asmcnc/skavaUI/img/checkbox_inactive.png"
                            center_x: self.parent.center_x
                            y: self.parent.y
                            size: self.parent.width, self.parent.height
                            allow_stretch: True

                        Label:
                            text: 'Z-:  '
                            halign: 'right'
                            markup: True
                            valign: 'middle'
                            text_size: self.size

                        Label:
                            id: z_wear_in_peak_neg
                            text: 'zzz'
                            halign: 'left'
                            markup: True
                            valign: 'middle'
                            text_size: self.size

                        Label:
                            text: 'Z+:  '
                            halign: 'right'
                            markup: True
                            valign: 'middle'
                            text_size: self.size

                        Label:
                            id: z_wear_in_peak_pos
                            text: 'zzz'
                            halign: 'left'
                            markup: True
                            valign: 'middle'
                            text_size: self.size

                        Image:
                            id: z_wear_in_checkbox
                            source: "./asmcnc/skavaUI/img/checkbox_inactive.png"
                            center_x: self.parent.center_x
                            y: self.parent.y
                            size: self.parent.width, self.parent.height
                            allow_stretch: True

                    ## RECALIBRATION PEAKS

                    # Placeholding
                    BoxLayout:
                        orientation: 'vertical'


                    ## FULLY CALIBRATED PEAKS

                    GridLayout:
                        cols: 5
                        rows: 5
                        size_hint_y: 0.5
                        spacing: [5,0]

                        Label:
                            text: 'Y+:  '
                            halign: 'right'
                            markup: True
                            valign: 'middle'
                            text_size: self.size

                        Label:
                            id: y_fully_calibrated_peak_pos
                            text: 'yyy'
                            halign: 'left'
                            markup: True
                            valign: 'middle'
                            text_size: self.size

                        Label:
                            text: 'Y-:  '
                            halign: 'right'
                            markup: True
                            valign: 'middle'
                            text_size: self.size

                        Label:
                            id: y_fully_calibrated_peak_neg
                            text: 'yyy'
                            halign: 'left'
                            markup: True
                            valign: 'middle'
                            text_size: self.size

                        Image:
                            id: y_fully_calibrated_checkbox
                            source: "./asmcnc/skavaUI/img/checkbox_inactive.png"
                            center_x: self.parent.center_x
                            y: self.parent.y
                            size: self.parent.width, self.parent.height
                            allow_stretch: True


                        Label:
                            text: 'Y1+:  '
                            halign: 'right'
                            markup: True
                            valign: 'middle'
                            text_size: self.size

                        Label:
                            id: y1_fully_calibrated_peak_pos
                            text: 'yyy'
                            halign: 'left'
                            markup: True
                            valign: 'middle'
                            text_size: self.size


                        Label:
                            text: 'Y1-:  '
                            halign: 'right'
                            markup: True
                            valign: 'middle'
                            text_size: self.size

                        Label:
                            id: y1_fully_calibrated_peak_neg
                            text: 'yyy'
                            halign: 'left'
                            markup: True
                            valign: 'middle'
                            text_size: self.size

                        Image:
                            id: y1_fully_calibrated_checkbox
                            source: "./asmcnc/skavaUI/img/checkbox_inactive.png"
                            center_x: self.parent.center_x
                            y: self.parent.y
                            size: self.parent.width, self.parent.height
                            allow_stretch: True


                        Label:
                            text: 'Y2+:  '
                            halign: 'right'
                            markup: True
                            valign: 'middle'
                            text_size: self.size

                        Label:
                            id: y2_fully_calibrated_peak_pos
                            text: 'yyy'
                            halign: 'left'
                            markup: True
                            valign: 'middle'
                            text_size: self.size

                        Label:
                            text: 'Y2-:  '
                            halign: 'right'
                            markup: True
                            valign: 'middle'
                            text_size: self.size

                        Label:
                            id: y2_fully_calibrated_peak_neg
                            text: 'yyy'
                            halign: 'left'
                            markup: True
                            valign: 'middle'
                            text_size: self.size

                        Image:
                            id: y2_fully_calibrated_checkbox
                            source: "./asmcnc/skavaUI/img/checkbox_inactive.png"
                            center_x: self.parent.center_x
                            y: self.parent.y
                            size: self.parent.width, self.parent.height
                            allow_stretch: True

                        Label:
                            text: 'X+:  '
                            halign: 'right'
                            markup: True
                            valign: 'middle'
                            text_size: self.size

                        Label:
                            id: x_fully_calibrated_peak_pos
                            text: 'xxx'
                            halign: 'left'
                            markup: True
                            valign: 'middle'
                            text_size: self.size

                        Label:
                            text: 'X-:  '
                            halign: 'right'
                            markup: True
                            valign: 'middle'
                            text_size: self.size

                        Label:
                            id: x_fully_calibrated_peak_neg
                            text: 'xxx'
                            halign: 'left'
                            markup: True
                            valign: 'middle'
                            text_size: self.size

                        Image:
                            id: x_fully_calibrated_checkbox
                            source: "./asmcnc/skavaUI/img/checkbox_inactive.png"
                            center_x: self.parent.center_x
                            y: self.parent.y
                            size: self.parent.width, self.parent.height
                            allow_stretch: True

                        Label:
                            text: 'Z-:  '
                            halign: 'right'
                            markup: True
                            valign: 'middle'
                            text_size: self.size

                        Label:
                            id: z_fully_calibrated_peak_neg
                            text: 'zzz'
                            halign: 'left'
                            markup: True
                            valign: 'middle'
                            text_size: self.size

                        Label:
                            text: 'Z+:  '
                            halign: 'right'
                            markup: True
                            valign: 'middle'
                            text_size: self.size

                        Label:
                            id: z_fully_calibrated_peak_pos
                            text: 'zzz'
                            halign: 'left'
                            markup: True
                            valign: 'middle'
                            text_size: self.size

                        Image:
                            id: z_fully_calibrated_checkbox
                            source: "./asmcnc/skavaUI/img/checkbox_inactive.png"
                            center_x: self.parent.center_x
                            y: self.parent.y
                            size: self.parent.width, self.parent.height
                            allow_stretch: True
        BoxLayout:
            size_hint_y: 0.08
            id: status_container

""")

MAX_XY_SPEED = 6000
MAX_Z_SPEED = 750

MAX_Z_DISTANCE = 149
MAX_X_DISTANCE = 1299
MAX_Y_DISTANCE = 2501


def log(message):
    timestamp = datetime.now()
    print (timestamp.strftime('%H:%M:%S.%f')[:12] + ' ' + str(message))


class OvernightTesting(Screen):
    # STAGES ARE:
    # "CalibrationQC"
    # "CalibrationCheckQC"
    # "UnweightedFT"
    # "WeightedFT"
    # "OvernightWearIn"
    # "CalibrationOT"
    # "CalibrationCheckOT" (obsolete, but still a DB stage)
    # "FullyCalibratedTest"

    poll_for_recalibration_stage = None
    poll_for_fully_calibrated_final_run_stage = None
    poll_end_of_six_hour_wear_in = None
    poll_for_recalibration_completion = None
    poll_for_recalibration_check_completion = None
    poll_end_of_fully_calibrated_final_run = None
    poll_for_tuning_completion = None
    start_six_hour_wear_in_event = None
    start_recalibration_event = None
    start_fully_calibrated_final_run_event = None
    poll_for_completion_of_overnight_test = None
    start_calibration_check_event = None
    poll_end_of_spiral = None
    start_last_rectangle = None
    run_event_after_datum_set = None
    start_tuning_event = None

    checkbox_inactive = "./asmcnc/skavaUI/img/checkbox_inactive.png"
    red_cross = "./asmcnc/skavaUI/img/template_cancel.png"
    green_tick = "./asmcnc/skavaUI/img/file_select_select.png"

    mini_run_dev_mode = False

    sn_for_db = ''

    x_wear_in_min_pos = None
    y_wear_in_min_pos = None
    y1_wear_in_min_pos = None
    y2_wear_in_min_pos = None
    z_wear_in_min_pos = None
    x_wear_in_min_neg = None
    y_wear_in_min_neg = None
    y1_wear_in_min_neg = None
    y2_wear_in_min_neg = None
    z_wear_in_min_neg = None
    x_recalibration_min_pos = None
    y_recalibration_min_pos = None
    y1_recalibration_min_pos = None
    y2_recalibration_min_pos = None
    z_recalibration_min_pos = None
    x_recalibration_min_neg = None
    y_recalibration_min_neg = None
    y1_recalibration_min_neg = None
    y2_recalibration_min_neg = None
    z_recalibration_min_neg = None
    x_fully_calibrated_min_pos = None
    y_fully_calibrated_min_pos = None
    y1_fully_calibrated_min_pos = None
    y2_fully_calibrated_min_pos = None
    z_fully_calibrated_min_pos = None
    x_fully_calibrated_min_neg = None
    y_fully_calibrated_min_neg = None
    y1_fully_calibrated_min_neg = None
    y2_fully_calibrated_min_neg = None
    z_fully_calibrated_min_neg = None

    def __init__(self, **kwargs):
        super(OvernightTesting, self).__init__(**kwargs)

        self.m = kwargs['m']
        self.systemtools_sm = kwargs['systemtools']
        self.calibration_db = kwargs['calibration_db']
        self.sm = kwargs['sm']
        self.l = kwargs['l']

        self.setup_arrays()
        self.overnight_running = False

        self.statuses = []
        self.stage = "OvernightWearIn"
        self.stage_id = 0

        self.status_container.add_widget(
            widget_sg_status_bar.SGStatusBar(machine=self.m, screen_manager=self.systemtools_sm.sm))

        self.status_data_dict = {
            "OvernightWearIn": {
                "Table": "FinalTestStatuses",
                "Statuses": []
            },
            "FullyCalibratedTest": {
                "Table": "FinalTestStatuses",
                "Statuses": []
            }

        }

        self.statistics_data_dict = {

            "OvernightWearIn": [],
            "FullyCalibratedTest": []

        }

        self.calibration_stage_id = self.calibration_db.get_stage_id_by_description("CalibrationOT")

    # Set up and clear/reset arrays for storing SG/measurement data

    def setup_arrays(self):

        self.raw_x_pos_vals = []
        self.raw_y_pos_vals = []
        self.raw_y1_pos_vals = []
        self.raw_y2_pos_vals = []
        self.raw_z_pos_vals = []
        self.raw_x_neg_vals = []
        self.raw_y_neg_vals = []
        self.raw_y1_neg_vals = []
        self.raw_y2_neg_vals = []
        self.raw_z_neg_vals = []

    def on_enter(self):
        self.get_sub_serials_from_database()
        self.m.s.FINAL_TEST = True
        self.stop_button.disabled = False

        for i in range(0, 200000):
            self.measure()

        self.send_data("OvernightWearIn")

    def on_leave(self):
        self.m.s.FINAL_TEST = False
        self.cancel_active_polls()
        self.stop_button.disabled = False
        self.buttons_disabled(False)

    def get_sub_serials_from_database(self):

        try:
            # Get serial numbers
            self.sn_for_db = 'ys6' + str(self.m.serial_number()).split('.')[0]
            [self.zh_serial, self.xl_serial] = self.calibration_db.get_serials_by_machine_serial(self.sn_for_db)

        except:
            message = "Can't get subassembly serials from database, have you entered serial numbers yet?" + \
                      "\n" + \
                      "Check connection and serial number entry, and don't continue unless absolutely necessary."
            popup_info.PopupInfo(self.systemtools_sm.sm, self.l, 500, message)
            # self.back_to_fac_settings() # uncommented bc if database down, may block final test.

    # Stage is used to detect which part of the operation overnight test is in, both in screen functions & data
    def set_stage(self, stage):

        self.stage = stage
        self.stage_id = self.calibration_db.get_stage_id_by_description(self.stage)

        try:
            self.calibration_db.insert_final_test_stage(self.sn_for_db, self.stage_id)

        except:
            log("Could not insert final test stage into DB!!")
            print(traceback.format_exc())

        self.status_data_dict[self.stage] = []
        log("Overnight test, stage: " + str(self.stage))

        # Function called from serial comms to record SG values

    def measure(self):
        if not self.overnight_running:
            return

        if self.m.is_machine_paused:
            return

        # GET DIRECTIONS

        # -1    BACKWARDS/UP (TOWARDS HOME)
        # 0     NOT MOVING
        # 1     FORWARDS/DOWN (AWAY FROM HOME)

        # NOTE Z LIFTS WEIGHT WHEN IT IS 

        if len(self.status_data_dict[self.stage]) > 0:

            if self.status_data_dict[self.stage][len(self.status_data_dict[self.stage]) - 1][1] < self.m.mpos_x():
                x_dir = -1
            elif self.status_data_dict[self.stage][len(self.status_data_dict[self.stage]) - 1][1] > self.m.mpos_x():
                x_dir = 1
            else:
                x_dir = 0

            if self.status_data_dict[self.stage][len(self.status_data_dict[self.stage]) - 1][2] < self.m.mpos_y():
                y_dir = -1
            elif self.status_data_dict[self.stage][len(self.status_data_dict[self.stage]) - 1][2] > self.m.mpos_y():
                y_dir = 1
            else:
                y_dir = 0

            if self.status_data_dict[self.stage][len(self.status_data_dict[self.stage]) - 1][3] < self.m.mpos_z():
                z_dir = 1
            elif self.status_data_dict[self.stage][len(self.status_data_dict[self.stage]) - 1][3] > self.m.mpos_z():
                z_dir = -1
            else:
                z_dir = 0

        else:
            x_dir = 0
            y_dir = 0
            z_dir = 0

        # XCoordinate, YCoordinate, ZCoordinate, XDirection, YDirection, ZDirection, XSG, YSG, Y1SG, Y2SG, ZSG, TMCTemperature, PCBTemperature, MOTTemperature, Timestamp, Feedrate

        status = {
            "Id": "",
            "FTID": int(self.sn_for_db[2:] + str(self.stage_id)),
            "XCoordinate": self.m.mpos_x(),
            "YCoordinate": self.m.mpos_y(),
            "ZCoordinate": self.m.mpos_z(),
            "XDirection": x_dir,
            "YDirection": y_dir,
            "ZDirection": z_dir,
            "XSG": int(self.m.s.sg_x_motor_axis),
            "YSG": int(self.m.s.sg_y_axis),
            "Y1SG": int(self.m.s.sg_y1_motor),
            "Y2SG": int(self.m.s.sg_y2_motor),
            "ZSG": int(self.m.s.sg_z_motor_axis),
            "TMCTemperature": int(self.m.s.motor_driver_temp),
            "PCBTemperature": int(self.m.s.pcb_temp),
            "MOTTemperature": int(self.m.s.transistor_heatsink_temp),
            "Timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "Feedrate": self.m.feed_rate(),
            "XWeight": 0,
            "YWeight": 0,
            "ZWeight": 2
        }

        self.status_data_dict[self.stage]["Statuses"].append(status)

        # Record raw values for statistics calculations

        if -999 < self.m.s.sg_x_motor_axis < 1023:
            if x_dir > 0: self.raw_x_pos_vals.append(self.m.s.sg_x_motor_axis)
            if x_dir < 0: self.raw_x_neg_vals.append(self.m.s.sg_x_motor_axis)

        if -999 < self.m.s.sg_y_axis < 1023:
            if y_dir > 0: self.raw_y_pos_vals.append(self.m.s.sg_y_axis)
            if y_dir < 0: self.raw_y_neg_vals.append(self.m.s.sg_y_axis)

        if -999 < self.m.s.sg_y1_motor < 1023:
            if y_dir > 0: self.raw_y1_pos_vals.append(self.m.s.sg_y1_motor)
            if y_dir < 0: self.raw_y1_neg_vals.append(self.m.s.sg_y1_motor)

        if -999 < self.m.s.sg_y2_motor < 1023:
            if y_dir > 0: self.raw_y2_pos_vals.append(self.m.s.sg_y2_motor)
            if y_dir < 0: self.raw_y2_neg_vals.append(self.m.s.sg_y2_motor)

        if -999 < self.m.s.sg_z_motor_axis < 1023:
            if z_dir < 0: self.raw_z_pos_vals.append(self.m.s.sg_z_motor_axis)
            if z_dir > 0: self.raw_z_neg_vals.append(self.m.s.sg_z_motor_axis)

        self.update_peaks()

    def update_peaks(self):

        if self.stage == "OvernightWearIn":
            self.get_peak_as_string(self.x_wear_in_peak_pos, self.raw_x_pos_vals)
            self.get_peak_as_string(self.y_wear_in_peak_pos, self.raw_y_pos_vals)
            self.get_peak_as_string(self.y1_wear_in_peak_pos, self.raw_y1_pos_vals)
            self.get_peak_as_string(self.y2_wear_in_peak_pos, self.raw_y2_pos_vals)
            self.get_peak_as_string(self.z_wear_in_peak_pos, self.raw_z_pos_vals)

            self.get_peak_as_string(self.x_wear_in_peak_neg, self.raw_x_neg_vals)
            self.get_peak_as_string(self.y_wear_in_peak_neg, self.raw_y_neg_vals)
            self.get_peak_as_string(self.y1_wear_in_peak_neg, self.raw_y1_neg_vals)
            self.get_peak_as_string(self.y2_wear_in_peak_neg, self.raw_y2_neg_vals)
            self.get_peak_as_string(self.z_wear_in_peak_neg, self.raw_z_neg_vals)
            return

        if self.stage == "FullyCalibratedTest":
            self.get_peak_as_string(self.x_fully_calibrated_peak_pos, self.raw_x_pos_vals)
            self.get_peak_as_string(self.y_fully_calibrated_peak_pos, self.raw_y_pos_vals)
            self.get_peak_as_string(self.y1_fully_calibrated_peak_pos, self.raw_y1_pos_vals)
            self.get_peak_as_string(self.y2_fully_calibrated_peak_pos, self.raw_y2_pos_vals)
            self.get_peak_as_string(self.z_fully_calibrated_peak_pos, self.raw_z_pos_vals)

            self.get_peak_as_string(self.x_fully_calibrated_peak_neg, self.raw_x_neg_vals)
            self.get_peak_as_string(self.y_fully_calibrated_peak_neg, self.raw_y_neg_vals)
            self.get_peak_as_string(self.y1_fully_calibrated_peak_neg, self.raw_y1_neg_vals)
            self.get_peak_as_string(self.y2_fully_calibrated_peak_neg, self.raw_y2_neg_vals)
            self.get_peak_as_string(self.z_fully_calibrated_peak_neg, self.raw_z_neg_vals)
            return

    def get_peak_as_string(self, label_id, raw_vals):

        try:
            label_id.text = str(max(raw_vals))
        except:
            pass

    def record_min_peaks(self):

        if self.stage == "OvernightWearIn":
            self.x_wear_in_min_pos = self.get_min_peak(self.raw_x_pos_vals)
            self.y_wear_in_min_pos = self.get_min_peak(self.raw_y_pos_vals)
            self.y1_wear_in_min_pos = self.get_min_peak(self.raw_y1_pos_vals)
            self.y2_wear_in_min_pos = self.get_min_peak(self.raw_y2_pos_vals)
            self.z_wear_in_min_pos = self.get_min_peak(self.raw_z_pos_vals)

            self.x_wear_in_min_neg = self.get_min_peak(self.raw_x_neg_vals)
            self.y_wear_in_min_neg = self.get_min_peak(self.raw_y_neg_vals)
            self.y1_wear_in_min_neg = self.get_min_peak(self.raw_y1_neg_vals)
            self.y2_wear_in_min_neg = self.get_min_peak(self.raw_y2_neg_vals)
            self.z_wear_in_min_neg = self.get_min_peak(self.raw_z_neg_vals)
            return

        if self.stage == "FullyCalibratedTest":
            self.x_fully_calibrated_min_pos = self.get_min_peak(self.raw_x_pos_vals)
            self.y_fully_calibrated_min_pos = self.get_min_peak(self.raw_y_pos_vals)
            self.y1_fully_calibrated_min_pos = self.get_min_peak(self.raw_y1_pos_vals)
            self.y2_fully_calibrated_min_pos = self.get_min_peak(self.raw_y2_pos_vals)
            self.z_fully_calibrated_min_pos = self.get_min_peak(self.raw_z_pos_vals)

            self.x_fully_calibrated_min_neg = self.get_min_peak(self.raw_x_neg_vals)
            self.y_fully_calibrated_min_neg = self.get_min_peak(self.raw_y_neg_vals)
            self.y1_fully_calibrated_min_neg = self.get_min_peak(self.raw_y1_neg_vals)
            self.y2_fully_calibrated_min_neg = self.get_min_peak(self.raw_y2_neg_vals)
            self.z_fully_calibrated_min_neg = self.get_min_peak(self.raw_z_neg_vals)
            return

    def get_min_peak(self, raw_vals):
        try:
            return (min(raw_vals))
        except:
            print("Min peak error:")
            print(traceback.format_exc())
            return None

    def read_out_peaks(self, stage):

        if stage == "OvernightWearIn":
            peak_list = [
                int(self.x_wear_in_peak_pos.text),
                int(self.x_wear_in_peak_neg.text),
                int(self.y_wear_in_peak_pos.text),
                int(self.y_wear_in_peak_neg.text),
                int(self.y1_wear_in_peak_pos.text),
                int(self.y1_wear_in_peak_neg.text),
                int(self.y2_wear_in_peak_pos.text),
                int(self.y2_wear_in_peak_neg.text),
                int(self.z_wear_in_peak_neg.text),
                int(self.z_wear_in_peak_pos.text)
            ]

            return peak_list

        if stage == "FullyCalibratedTest":
            peak_list = [
                int(self.x_fully_calibrated_peak_pos.text),
                int(self.x_fully_calibrated_peak_neg.text),
                int(self.y_fully_calibrated_peak_pos.text),
                int(self.y_fully_calibrated_peak_neg.text),
                int(self.y1_fully_calibrated_peak_pos.text),
                int(self.y1_fully_calibrated_peak_neg.text),
                int(self.y2_fully_calibrated_peak_pos.text),
                int(self.y2_fully_calibrated_peak_neg.text),
                int(self.z_fully_calibrated_peak_neg.text),
                int(self.z_fully_calibrated_peak_pos.text)
            ]

            return peak_list

    def get_statistics(self):

        log("Getting statistics...")

        try:

            # x_forw_peak, x_backw_peak, y_forw_peak, y_backw_peak, y1_forw_peak, y1_backw_peak, y2_forw_peak, y2_backw_peak, z_forw_peak, z_backw_peak
            peak_list = self.read_out_peaks(self.stage)

            self.statistics_data_dict[self.stage] = [

                sum(self.raw_x_pos_vals) / len(self.raw_x_pos_vals),
                peak_list[0],
                sum(self.raw_x_neg_vals) / len(self.raw_x_neg_vals),
                peak_list[1],
                sum(self.raw_y_pos_vals) / len(self.raw_y_pos_vals),
                peak_list[2],
                sum(self.raw_y_neg_vals) / len(self.raw_y_neg_vals),
                peak_list[3],
                sum(self.raw_y1_pos_vals) / len(self.raw_y1_pos_vals),
                peak_list[4],
                sum(self.raw_y1_neg_vals) / len(self.raw_y1_neg_vals),
                peak_list[5],
                sum(self.raw_y2_pos_vals) / len(self.raw_y2_pos_vals),
                peak_list[6],
                sum(self.raw_y2_neg_vals) / len(self.raw_y2_neg_vals),
                peak_list[7],
                sum(self.raw_z_pos_vals) / len(self.raw_z_pos_vals),
                peak_list[8],
                sum(self.raw_z_neg_vals) / len(self.raw_z_neg_vals),
                peak_list[9]

            ]

        except:
            print(traceback.format_exc())

    def back_to_fac_settings(self):
        self.systemtools_sm.open_factory_settings_screen()

    def home(self):
        self.m.is_machine_completed_the_initial_squaring_decision = True
        self.m.is_squaring_XY_needed_after_homing = False
        self.m.request_homing_procedure('overnight_testing', 'overnight_testing')

    def stop(self):
        PopupStopOvernightTest(self.m, self.sm, self.l, self)

    # Poll/start events are scheduled to detect when one operation has finished and then start the next
    # If STOP button is pressed, or a stage fails, any active polls need to be cancelled

    def cancel_active_polls(self):

        # put all of the polls here, and check if not none. call this on job cancel, and on_leave. 
        self._unschedule_event(self.poll_for_recalibration_stage)
        self._unschedule_event(self.poll_for_fully_calibrated_final_run_stage)
        self._unschedule_event(self.poll_for_completion_of_overnight_test)
        self._unschedule_event(self.poll_end_of_six_hour_wear_in)
        self._unschedule_event(self.poll_for_recalibration_completion)
        self._unschedule_event(self.poll_for_recalibration_check_completion)
        self._unschedule_event(self.poll_end_of_fully_calibrated_final_run)
        self._unschedule_event(self.start_six_hour_wear_in_event)
        self._unschedule_event(self.start_recalibration_event)
        self._unschedule_event(self.start_fully_calibrated_final_run_event)
        self._unschedule_event(self.start_calibration_check_event)
        self._unschedule_event(self.poll_end_of_spiral)
        self._unschedule_event(self.start_last_rectangle)
        self._unschedule_event(self.run_event_after_datum_set)
        self._unschedule_event(self.poll_for_tuning_completion)

        # also stop measurement running
        self.overnight_running = False

    def _unschedule_event(self, poll_to_unschedule):

        if poll_to_unschedule != None: Clock.unschedule(poll_to_unschedule)

    # Disable any buttons other than STOP while other tests are running

    def buttons_disabled(self, status):

        self.back_button.disabled = status
        self.home_button.disabled = status
        self.overnight_test_button.disabled = status
        self.six_hour_wear_in_button.disabled = status
        self.recalibration_button.disabled = status
        self.fully_calibrated_run_button.disabled = status
        self.retry_six_hour_wear_in_data_send.disabled = status
        self.retry_recalibration_data_send.disabled = status
        self.retry_fully_calibrated_run_data_send.disabled = status

    ## OVERNIGHT TEST CONTROL
    def start_full_overnight_test(self):

        self.buttons_disabled(True)
        self.setup_arrays()

        log("Start full overnight test")

        # Schedule stages #2 and #3, and then run the first stage (6 hour wear in)
        self.poll_for_recalibration_stage = Clock.schedule_interval(self.ready_for_recalibration, 10)
        self.poll_for_fully_calibrated_final_run_stage = Clock.schedule_interval(
            self.ready_for_fully_calibrated_final_run, 10)
        self.poll_for_completion_of_overnight_test = Clock.schedule_interval(self.overnight_test_completed, 120)
        self.start_six_hour_wear_in()

    ## RUNNING FUNCTIONS - THESE ARE ALL PARTS OF "OVERNIGHT TEST" -------------------------------------------------------------------

    # These functions also set the Stage, so each bit of sent data knows what it's for

    # Each function in each stage automatically calL the next one in sequence, so that each stage (six hour, recalibration, one-hour post recal) can also be run individually if needed.
    # The start full overnight test function sets up polls for each stage to start after the next one.

    ## SIX HOUR WEAR IN

    # This should start, stream the 6 hour wear-in file, and then do any post 6 hour wear-in
    def start_six_hour_wear_in(self):

        self.buttons_disabled(True)
        self.reset_checkbox(self.six_hour_wear_in_checkbox)
        self.reset_checkbox(self.y_wear_in_checkbox)
        self.reset_checkbox(self.y1_wear_in_checkbox)
        self.reset_checkbox(self.y2_wear_in_checkbox)
        self.reset_checkbox(self.x_wear_in_checkbox)
        self.reset_checkbox(self.z_wear_in_checkbox)
        self.reset_checkbox(self.sent_six_hour_wear_in_data)

        self.setup_arrays()

        log("Start 6 hour wear-in")

        self.m.jog_absolute_xy(self.m.x_min_jog_abs_limit, self.m.y_min_jog_abs_limit, 6000)
        self.m.jog_absolute_single_axis('Z', self.m.z_max_jog_abs_limit, 750)

        self.start_six_hour_wear_in_event = Clock.schedule_once(self.run_six_hour_wear_in, 5)

    def run_six_hour_wear_in(self, dt):

        if self._not_ready_to_stream():
            self.start_six_hour_wear_in_event = Clock.schedule_once(self.run_six_hour_wear_in, 3)
            return

        self.set_stage("OvernightWearIn")
        self._stream_overnight_file('three_hour_rectangle')
        self.poll_end_of_six_hour_wear_in = Clock.schedule_interval(self.post_six_hour_wear_in, 60)

        log("Running six hour wear-in...")

    def post_six_hour_wear_in(self,
                              dt):  # This should also trigger the payload data send for any data that did not succeed in sending

        if self._not_finished_streaming(self.poll_end_of_six_hour_wear_in):
            return

        log("Six hour wear-in completed")

        self.pass_or_fail_peak_loads()
        self.tick_checkbox(self.six_hour_wear_in_checkbox, True)
        self.get_statistics()
        self.send_six_hour_wear_in_data()
        self.setup_arrays()

        if self.poll_for_completion_of_overnight_test is None:
            self.buttons_disabled(False)

    ## RECALIBRATION

    def ready_for_recalibration(self, dt):

        if self.is_step_ticked(self.six_hour_wear_in_checkbox) and self.is_step_complete(
                self.sent_six_hour_wear_in_data):

            if self.poll_for_recalibration_stage != None: Clock.unschedule(self.poll_for_recalibration_stage)
            log("Start recalibration...")
            self.start_recalibration()

    def start_recalibration(self):

        self.buttons_disabled(True)
        self.reset_checkbox(self.recalibration_checkbox)
        self.reset_checkbox(self.sent_recalibration_data)

        if self._not_ready_to_stream():
            self.start_recalibration_event = Clock.schedule_once(lambda dt: self.start_recalibration(), 3)
            return

        log("Starting recalibration...")

        self.setup_arrays()
        self.overnight_running = False
        self.stage = ""
        self.m.send_any_gcode_command('M3 S20000')
        self.m.jog_absolute_xy(self.m.x_min_jog_abs_limit + 10, self.m.y_min_jog_abs_limit + 10, 6000)
        self.m.jog_absolute_single_axis('Z', self.m.z_max_jog_abs_limit - 10, 750)
        self.stop_button.disabled = True
        self.start_tuning_event = Clock.schedule_once(self.do_tuning, 2)

    def do_tuning(self, dt):

        if self._not_ready_to_stream():
            self.start_tuning_event = Clock.schedule_once(self.do_tuning, 2)
            return

        if not self.m.run_calibration and not self.m.tuning_in_progress:
            self.m.tune_X_Y_Z_for_calibration()
            self.poll_for_tuning_completion = Clock.schedule_interval(self.do_calibration, 5)

    def do_calibration(self, dt):

        if not self.m.tuning_in_progress:
            Clock.unschedule(self.poll_for_tuning_completion)

            if not self.m.calibration_tuning_fail_info:
                self.m.calibrate_X_Y_and_Z()
                self.poll_for_recalibration_completion = Clock.schedule_interval(self.post_recalibration, 5)

            else:
                # Tuning has failed, so no point running future tests
                self.cancel_active_polls()
                self.tick_checkbox(self.recalibration_checkbox, False)
                self.buttons_disabled(False)

    def post_recalibration(self, dt):

        if self.m.run_calibration:
            return

        if self.poll_for_recalibration_completion != None: Clock.unschedule(self.poll_for_recalibration_completion)
        self.overnight_running = False
        self.m.send_any_gcode_command('M5')

        if not self.m.calibration_tuning_fail_info:

            self.tick_checkbox(self.recalibration_checkbox, True)
            self.send_recalibration_data()
            self.setup_arrays()
            self.stop_button.disabled = False
            log("Recalibration complete...")

        else:
            self.tick_checkbox(self.recalibration_checkbox, False)
            self.setup_arrays()
            self.cancel_active_polls()
            self.buttons_disabled(False)

            log("Recalibration did not complete, cancelling further tests")

        if self.poll_for_completion_of_overnight_test is None:
            self.buttons_disabled(False)

    ## ONE HOUR RUN (SAME RECTANGLE AS IS REPEATED FOR SIX HOUR), TO RUN AFTER SB HAS BEEN FULLY CALIBRATED

    # This should run the post-calibration 1 hour file to harvest SG values/run data when machine is fully calibrated. 

    def ready_for_fully_calibrated_final_run(self, dt):

        if self.is_step_ticked(self.recalibration_checkbox) and self.is_step_complete(self.sent_recalibration_data):

            if self.poll_for_fully_calibrated_final_run_stage != None: Clock.unschedule(
                self.poll_for_fully_calibrated_final_run_stage)
            log("Start fully calibrated final run...")
            self.start_fully_calibrated_final_run()

    def start_fully_calibrated_final_run(self):

        self.buttons_disabled(True)
        self.reset_checkbox(self.fully_calibrated_run_checkbox)
        self.reset_checkbox(self.y_fully_calibrated_checkbox)
        self.reset_checkbox(self.y1_fully_calibrated_checkbox)
        self.reset_checkbox(self.y2_fully_calibrated_checkbox)
        self.reset_checkbox(self.x_fully_calibrated_checkbox)
        self.reset_checkbox(self.z_fully_calibrated_checkbox)
        self.reset_checkbox(self.sent_fully_recalibrated_run_data)

        log("SB fully calibrated, start final run")

        self.m.jog_absolute_xy(-1298, -2500, 6000)
        self.m.jog_absolute_single_axis('Z', -32, 750)

        self.start_fully_calibrated_final_run_event = Clock.schedule_once(self.run_spiral_file, 5)

    def run_spiral_file(self, dt):

        if self._not_ready_to_stream():
            self.start_fully_calibrated_final_run_event = Clock.schedule_once(self.run_spiral_file, 3)
            return

        self.setup_arrays()
        self.m.set_workzone_to_pos_xy()
        self.m.set_jobstart_z()
        self.set_stage("FullyCalibratedTest")
        self.run_event_after_datum_set = Clock.schedule_once(lambda dt: self._stream_overnight_file('spiral_file'), 3)
        log("Running fully calibrated final run...")
        log("Running spiral file...")

        self.poll_end_of_spiral = Clock.schedule_interval(self.finish_spiral_file_reset_for_rectangle, 60)

    def finish_spiral_file_reset_for_rectangle(self, dt):

        if self._not_finished_streaming(self.poll_end_of_spiral):
            return

        self.m.jog_absolute_xy(self.m.x_min_jog_abs_limit, self.m.y_min_jog_abs_limit, 6000)
        self.m.jog_absolute_single_axis('Z', self.m.z_max_jog_abs_limit, 750)

        self.start_last_rectangle = Clock.schedule_once(self.run_last_rectangle, 5)

    def run_last_rectangle(self, dt):

        if self._not_ready_to_stream():
            self.start_last_rectangle = Clock.schedule_once(self.run_last_rectangle, 3)
            return

        self.m.set_workzone_to_pos_xy()
        self.m.set_jobstart_z()
        self.run_event_after_datum_set = Clock.schedule_once(lambda dt: self._stream_overnight_file('five_rectangles'),
                                                             3)
        log("Running last rectangle")
        self.poll_end_of_fully_calibrated_final_run = Clock.schedule_interval(self.post_fully_calibrated_final_run, 60)

    def post_fully_calibrated_final_run(self, dt):

        if self._not_finished_streaming(self.poll_end_of_fully_calibrated_final_run):
            return

        log("Fully calibrated final run complete")

        self.pass_or_fail_peak_loads()
        self.tick_checkbox(self.fully_calibrated_run_checkbox, True)
        self.get_statistics()
        self.send_fully_calibrated_final_run_data()
        self.setup_arrays()

        if self.poll_for_completion_of_overnight_test is None:
            self.buttons_disabled(False)

    ## This function only runs if full suite of overnight tests is carried out together (i.e. by pressing START) and completed
    def overnight_test_completed(self, dt):

        if self._not_ready_to_stream():
            return

        if not self.is_step_complete(self.six_hour_wear_in_checkbox):
            return

        if not self.is_step_complete(self.recalibration_checkbox):
            return

        if not self.is_step_complete(self.fully_calibrated_run_checkbox):
            return

        log("Overnight test completed")

        self._unschedule_event(self.poll_for_completion_of_overnight_test)
        self.cancel_active_polls()
        self.setup_arrays()
        self.stage = ""
        self.buttons_disabled(False)

    # FILE STREAMING FUNCTIONS

    def _not_ready_to_stream(self):
        if self.m.state().startswith('Idle') and not self.overnight_running:
            return False

        else:
            return True

    def _stream_overnight_file(self, filename_end):

        self.overnight_running = True

        if self.mini_run_dev_mode: filename_end = 'super_mini_run'

        filename = './asmcnc/apps/systemTools_app/files/' + filename_end + '.gc'

        with open(filename) as f:
            gcode_prescrubbed = f.readlines()

        gcode = [self.m.quick_scrub(line) for line in gcode_prescrubbed]

        self.m.s.run_skeleton_buffer_stuffer(gcode)

    def _not_finished_streaming(self, poll_to_unschedule):

        if not self.m.state().startswith('Idle'):
            return True

        if self.m.s.NOT_SKELETON_STUFF and not self.m.s.is_job_streaming and not self.m.s.is_stream_lines_remaining and not self.m.is_machine_paused:
            self._unschedule_event(poll_to_unschedule)
            self.overnight_running = False

            return False

        return True

    ## DATA SEND FUNCTIONS

    # These actually only need to send any data that hasn't already been sent - for completion, check when arrays are empty

    # Add all statuses to same array - and then for each function/check, see if any of the stages are in the lists. 

    def send_six_hour_wear_in_data(self):
        log("Sending six hour wear-in data")
        self._has_data_been_sent("OvernightWearIn", self.sent_six_hour_wear_in_data)

    def send_recalibration_data(self):
        if self.send_all_calibration_coefficients():
            self.tick_checkbox(self.sent_recalibration_data, True)
        else:
            self.tick_checkbox(self.sent_recalibration_data, False)

    def send_fully_calibrated_final_run_data(self):
        self._has_data_been_sent("FullyCalibratedTest", self.sent_fully_recalibrated_run_data)

    def _has_data_been_sent(self, stage, checkbox_id):

        if self.send_data(stage):
            self.tick_checkbox(checkbox_id, True)
        else:
            self.tick_checkbox(checkbox_id, False)

    def send_data(self, stage):

        try:
            log("Doing data send...")
            stage_id = self.calibration_db.get_stage_id_by_description(stage)

            self.calibration_db.insert_final_test_stage(
                self.sn_for_db,
                stage_id
            )

            publisher = Publisher()

            j_obj = self.status_data_dict[stage]

            response = publisher.publish(j_obj)

            if response == b'Done':
                log("Successful")  # add more verbose output to user & update consumer's response

            log("Received %s from consumer" % response)

            # self.calibration_db.insert_final_test_statuses(self.status_data_dict[stage])
            statistics = [self.sn_for_db, stage_id]
            statistics.extend(self.statistics_data_dict[stage])
            self.calibration_db.insert_final_test_statistics(*statistics)
            log("Finish data send")
            return True

        except:
            log("Failed to send data to DB!!")
            print(traceback.format_exc())
            return False

    def send_all_calibration_coefficients(self):

        try:

            self.send_calibration_coefficients_for_one_motor(self.zh_serial, 0)
            self.send_calibration_coefficients_for_one_motor(self.zh_serial, 1)
            self.send_calibration_coefficients_for_one_motor(self.xl_serial, 2)
            self.send_calibration_coefficients_for_one_motor(self.xl_serial, 3)
            self.send_calibration_coefficients_for_one_motor(self.zh_serial, 4)
            return True

        except:
            log("Failed to send calibration coefficients to DB!!")
            print(traceback.format_exc())
            return False

    def send_calibration_coefficients_for_one_motor(self, sub_serial, motor_index):

        all_coefficients = []
        all_coefficients.extend(self.m.TMC_motor[motor_index].calibration_dataset_SG_values)
        all_coefficients.extend([

            self.m.TMC_motor[motor_index].calibrated_at_current_setting,
            self.m.TMC_motor[motor_index].calibrated_at_sgt_setting,
            self.m.TMC_motor[motor_index].calibrated_at_toff_setting,
            self.m.TMC_motor[motor_index].calibrated_at_temperature

        ])

        if sub_serial.startswith("zh"): self.calibration_db.setup_z_head_coefficients(sub_serial, motor_index,
                                                                                      self.calibration_stage_id)
        if sub_serial.startswith("xl"): self.calibration_db.setup_lower_beam_coefficients(sub_serial, motor_index,
                                                                                          self.calibration_stage_id)
        self.calibration_db.insert_calibration_coefficients(sub_serial, motor_index, self.calibration_stage_id,
                                                            all_coefficients)

    ## SET TICKS
    def tick_checkbox(self, checkbox_id, tick):

        if tick:
            checkbox_id.source = self.green_tick

        else:
            checkbox_id.source = self.red_cross

    ## GET TICKS
    def is_step_complete(self, checkbox_id):

        if not checkbox_id.source == self.checkbox_inactive:
            return True

        else:
            return False

    def is_step_ticked(self, checkbox_id):

        if checkbox_id.source == self.green_tick:
            return True

        else:
            return False

    ## RESET CHECKBOXES WHEN RUNS RESTART
    def reset_checkbox(self, checkbox_id):
        checkbox_id.source = self.checkbox_inactive

    ## CHECK THAT SG VALUES ARE WITHIN EXPECTED RANGES

    def pass_or_fail_peak_loads(self):

        self.record_min_peaks()

        if self.stage == "OvernightWearIn":
            within_plus_minus = 400

            self.tick_checkbox(self.y_wear_in_checkbox, \
                               self.check_in_range(self.y_wear_in_peak_pos, self.y_wear_in_peak_neg,
                                                   self.y_wear_in_min_pos, self.y_wear_in_min_neg, within_plus_minus) \
                               )
            self.tick_checkbox(self.y1_wear_in_checkbox, \
                               self.check_in_range(self.y1_wear_in_peak_pos, self.y1_wear_in_peak_neg,
                                                   self.y1_wear_in_min_pos, self.y1_wear_in_min_neg, 500) \
                               )
            self.tick_checkbox(self.y2_wear_in_checkbox, \
                               self.check_in_range(self.y2_wear_in_peak_pos, self.y2_wear_in_peak_neg,
                                                   self.y2_wear_in_min_pos, self.y2_wear_in_min_neg, 500) \
                               )
            self.tick_checkbox(self.x_wear_in_checkbox, \
                               self.check_in_range(self.x_wear_in_peak_pos, self.x_wear_in_peak_neg,
                                                   self.x_wear_in_min_pos, self.x_wear_in_min_neg, within_plus_minus) \
                               )
            self.tick_checkbox(self.z_wear_in_checkbox, \
                               self.check_in_range(self.z_wear_in_peak_pos, self.z_wear_in_peak_neg,
                                                   self.z_wear_in_min_pos, self.z_wear_in_min_neg, within_plus_minus) \
                               )
            return

        if self.stage == "FullyCalibratedTest":
            within_plus_minus = 100

            self.tick_checkbox(self.y_fully_calibrated_checkbox, \
                               self.check_in_range(self.y_fully_calibrated_peak_pos, self.y_fully_calibrated_peak_neg,
                                                   self.y_fully_calibrated_min_pos, self.y_fully_calibrated_min_neg,
                                                   150)
                               )
            self.tick_checkbox(self.y1_fully_calibrated_checkbox, \
                               self.check_in_range(self.y1_fully_calibrated_peak_pos, self.y1_fully_calibrated_peak_neg,
                                                   self.y1_fully_calibrated_min_pos, self.y1_fully_calibrated_min_neg,
                                                   500)
                               )
            self.tick_checkbox(self.y2_fully_calibrated_checkbox, \
                               self.check_in_range(self.y2_fully_calibrated_peak_pos, self.y2_fully_calibrated_peak_neg,
                                                   self.y2_fully_calibrated_min_pos, self.y2_fully_calibrated_min_neg,
                                                   500)
                               )
            self.tick_checkbox(self.x_fully_calibrated_checkbox, \
                               self.check_in_range(self.x_fully_calibrated_peak_pos, self.x_fully_calibrated_peak_neg,
                                                   self.x_fully_calibrated_min_pos, self.x_fully_calibrated_min_neg,
                                                   200)
                               )
            self.tick_checkbox(self.z_fully_calibrated_checkbox, \
                               self.check_in_range(self.z_fully_calibrated_peak_pos, self.z_fully_calibrated_peak_neg,
                                                   self.z_fully_calibrated_min_pos, self.z_fully_calibrated_min_neg,
                                                   150)
                               )
            return

    def check_in_range(self, peak_id_pos, peak_id_neg, min_pos, min_neg, within_plus_minus):

        print("Lower bound: " + str((-1 * within_plus_minus)))
        print("Upper bound: " + str(within_plus_minus))
        print ("Peak pos: " + str(peak_id_pos.text))
        print ("Peak neg: " + str(peak_id_neg.text))
        print ("Min pos: " + str(min_pos))
        print ("Min neg: " + str(min_neg))

        try:
            if not (-1 * within_plus_minus) < int(peak_id_pos.text) < within_plus_minus: return False
            if not (-1 * within_plus_minus) < int(peak_id_neg.text) < within_plus_minus: return False
            if not (-1 * within_plus_minus) < int(min_pos) < within_plus_minus: return False
            if not (-1 * within_plus_minus) < int(min_neg) < within_plus_minus: return False
            return True

        except:
            print(traceback.format_exc())
            return False
