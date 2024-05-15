from asmcnc.comms.logging_system.logging_system import Logger
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.clock import Clock
from datetime import datetime
from asmcnc.skavaUI import popup_info
import traceback
from asmcnc.apps.systemTools_app.screens.calibration import widget_sg_status_bar
from asmcnc.comms.logging import log_exporter

Builder.load_string(
    """
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
    # z_test_check:z_test_check
    unweighted_test_check:unweighted_test_check
    sent_data_check:sent_data_check

    unweighted_test_button : unweighted_test_button
    x_load_button : x_load_button
    y_load_button : y_load_button
    # z_load_button : z_load_button

    data_send_button : data_send_button
    data_send_label : data_send_label

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
    # z_peak_posve_weighted : z_peak_posve_weighted

    y_peak_negve_weighted : y_peak_negve_weighted
    y1_peak_negve_weighted : y1_peak_negve_weighted
    y2_peak_negve_weighted : y2_peak_negve_weighted
    x_peak_negve_weighted : x_peak_negve_weighted
    # z_peak_negve_weighted : z_peak_negve_weighted

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
    # z_fw_range_weighted : z_fw_range_weighted
    # z_bw_range_weighted : z_bw_range_weighted
    # z_peak_checkbox_weighted : z_peak_checkbox_weighted

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
                        font_size: app.get_scaled_sp('15.0sp')
                        text: 'Back'
                        on_press: root.back_to_fac_settings()

                    Button:
                        font_size: app.get_scaled_sp('15.0sp')
                        id: home_button
                        text: 'Home'
                        on_press: root.home()

                    Button:
                        font_size: app.get_scaled_sp('15.0sp')
                        id: x0y0_jog_button
                        text: 'X0Y0'
                        on_press: root.zero_x_and_y()

                    Button:
                        font_size: app.get_scaled_sp('15.0sp')
                        id: x7y0_jog_button
                        text: 'X-700Y0'
                        on_press: root.mid_x_and_zero_y()

                    Button:
                        font_size: app.get_scaled_sp('15.0sp')
                        id: z0_jog_button
                        text: 'Z0'
                        on_press: root.zero_Z()

                Button:
                    font_size: app.get_scaled_sp('15.0sp')
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
                        font_size: app.get_scaled_sp('15.0sp')
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
                        font_size: app.get_scaled_sp('15.0sp')
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
                        font_size: app.get_scaled_sp('15.0sp')
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

                    Label:
                        font_size: app.get_scaled_sp('15.0sp')
                        text: ''

                    Label:
                        font_size: app.get_scaled_sp('15.0sp')
                        text: ''

                    # Button:
                    #     id: z_load_button
                    #     text: 'Run Z (2kg)'
                    #     on_press: root.run_z_procedure(None)

                    # Image:
                    #     id: z_test_check
                    #     source: "./asmcnc/skavaUI/img/checkbox_inactive.png"
                    #     center_x: self.parent.center_x
                    #     y: self.parent.y
                    #     size: self.parent.width, self.parent.height
                    #     allow_stretch: True

                Button:
                    font_size: app.get_scaled_sp('15.0sp')
                    id: data_send_button
                    text: 'Send data to database'
                    on_press: root.send_all_data()
                    disabled: True

                GridLayout:
                    cols: 2

                    Label:
                        font_size: app.get_scaled_sp('15.0sp')
                        id: data_send_label
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
                    font_size: app.get_scaled_sp('15.0sp')
                    text: 'Unweighted'

                Label:
                    font_size: app.get_scaled_sp('15.0sp')
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
                        font_size: app.get_scaled_sp('15.0sp')
                        text: 'Y+: '
                        halign: 'right'
                        markup: True
                        valign: 'middle'
                        text_size: self.size

                    Label:
                        id: y_peak_posve
                        font_size: app.get_scaled_sp('15.0sp')
                        text: 'yyy'
                        halign: 'left'
                        markup: True
                        valign: 'middle'
                        text_size: self.size

                    Label:
                        id: y_axis_fw_range
                        font_size: app.get_scaled_sp('15.0sp')
                        text: 'yyy - yyy'
                        markup: True
                        valign: 'middle'
                        text_size: self.size
                        halign: 'center'

                    Label:
                        font_size: app.get_scaled_sp('15.0sp')
                        text: 'Y-: '
                        halign: 'right'
                        markup: True
                        valign: 'middle'
                        text_size: self.size

                    Label:
                        id: y_peak_negve
                        font_size: app.get_scaled_sp('15.0sp')
                        text: 'yyy'
                        halign: 'left'
                        markup: True
                        valign: 'middle'
                        text_size: self.size


                    Label:
                        id: y_axis_bw_range
                        font_size: app.get_scaled_sp('15.0sp')
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
                        font_size: app.get_scaled_sp('15.0sp')
                        text: 'Y1+:'
                        halign: 'right'
                        markup: True
                        valign: 'middle'
                        text_size: self.size

                    Label:
                        id: y1_peak_posve
                        font_size: app.get_scaled_sp('15.0sp')
                        text: 'yyy'
                        halign: 'left'
                        markup: True
                        valign: 'middle'
                        text_size: self.size

                    Label:
                        id: y1_fw_range
                        font_size: app.get_scaled_sp('15.0sp')
                        text: 'yyy - yyy'
                        markup: True
                        valign: 'middle'
                        text_size: self.size
                        halign: 'center'

                    Label:
                        font_size: app.get_scaled_sp('15.0sp')
                        text: 'Y1-:'
                        halign: 'right'
                        markup: True
                        valign: 'middle'
                        text_size: self.size

                    Label:
                        id: y1_peak_negve
                        font_size: app.get_scaled_sp('15.0sp')
                        text: 'yyy'
                        halign: 'left'
                        markup: True
                        valign: 'middle'
                        text_size: self.size

                    Label:
                        id: y1_bw_range
                        font_size: app.get_scaled_sp('15.0sp')
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
                        font_size: app.get_scaled_sp('15.0sp')
                        text: 'Y2+:'
                        halign: 'right'
                        markup: True
                        valign: 'middle'
                        text_size: self.size

                    Label:
                        id: y2_peak_posve
                        font_size: app.get_scaled_sp('15.0sp')
                        text: 'yyy'
                        halign: 'left'
                        markup: True
                        valign: 'middle'
                        text_size: self.size

                    Label:
                        id: y2_fw_range
                        font_size: app.get_scaled_sp('15.0sp')
                        text: 'yyy - yyy'
                        markup: True
                        valign: 'middle'
                        text_size: self.size
                        halign: 'center'

                    Label:
                        font_size: app.get_scaled_sp('15.0sp')
                        text: 'Y2-:'
                        halign: 'right'
                        markup: True
                        valign: 'middle'
                        text_size: self.size

                    Label:
                        id: y2_peak_negve
                        font_size: app.get_scaled_sp('15.0sp')
                        text: 'yyy'
                        halign: 'left'
                        markup: True
                        valign: 'middle'
                        text_size: self.size

                    Label:
                        id: y2_bw_range
                        font_size: app.get_scaled_sp('15.0sp')
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
                        font_size: app.get_scaled_sp('15.0sp')
                        text: 'X+:'
                        halign: 'right'
                        markup: True
                        valign: 'middle'
                        text_size: self.size

                    Label:
                        id: x_peak_posve
                        font_size: app.get_scaled_sp('15.0sp')
                        text: 'xxx'
                        halign: 'left'
                        markup: True
                        valign: 'middle'
                        text_size: self.size

                    Label:
                        id: x_fw_range
                        font_size: app.get_scaled_sp('15.0sp')
                        text: 'xxx - xxx'
                        markup: True
                        valign: 'middle'
                        text_size: self.size
                        halign: 'center'

                    Label:
                        font_size: app.get_scaled_sp('15.0sp')
                        text: 'X-:'
                        halign: 'right'
                        markup: True
                        valign: 'middle'
                        text_size: self.size

                    Label:
                        id: x_peak_negve
                        font_size: app.get_scaled_sp('15.0sp')
                        text: 'xxx'
                        halign: 'left'
                        markup: True
                        valign: 'middle'
                        text_size: self.size

                    Label:
                        id: x_bw_range
                        font_size: app.get_scaled_sp('15.0sp')
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
                        font_size: app.get_scaled_sp('15.0sp')
                        text: 'Z-:'
                        halign: 'right'
                        markup: True
                        valign: 'middle'
                        text_size: self.size

                    Label:
                        id: z_peak_negve
                        font_size: app.get_scaled_sp('15.0sp')
                        text: 'zzz'
                        halign: 'left'
                        markup: True
                        valign: 'middle'
                        text_size: self.size

                    Label:
                        id: z_fw_range
                        font_size: app.get_scaled_sp('15.0sp')
                        text: 'zzz - zzz'
                        markup: True
                        valign: 'middle'
                        text_size: self.size
                        halign: 'center'

                    Label:
                        font_size: app.get_scaled_sp('15.0sp')
                        text: 'Z+:'
                        halign: 'right'
                        markup: True
                        valign: 'middle'
                        text_size: self.size

                    Label:
                        id: z_peak_posve
                        font_size: app.get_scaled_sp('15.0sp')
                        text: 'zzz'
                        halign: 'left'
                        markup: True
                        valign: 'middle'
                        text_size: self.size

                    Label:
                        id: z_bw_range
                        font_size: app.get_scaled_sp('15.0sp')
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
                        font_size: app.get_scaled_sp('15.0sp')
                        text: 'Y+:'
                        halign: 'right'
                        markup: True
                        valign: 'middle'
                        text_size: self.size

                    Label:
                        id: y_peak_posve_weighted
                        font_size: app.get_scaled_sp('15.0sp')
                        text: 'yyy'
                        halign: 'left'
                        markup: True
                        valign: 'middle'
                        text_size: self.size

                    Label:
                        id: y_axis_fw_range_weighted
                        font_size: app.get_scaled_sp('15.0sp')
                        text: 'yyy - yyy'
                        markup: True
                        valign: 'middle'
                        text_size: self.size
                        halign: 'center'

                    Label:
                        font_size: app.get_scaled_sp('15.0sp')
                        text: 'Y-:'
                        halign: 'right'
                        markup: True
                        valign: 'middle'
                        text_size: self.size

                    Label:
                        id: y_peak_negve_weighted
                        font_size: app.get_scaled_sp('15.0sp')
                        text: 'yyy'
                        halign: 'left'
                        markup: True
                        valign: 'middle'
                        text_size: self.size

                    Label:
                        id: y_axis_bw_range_weighted
                        font_size: app.get_scaled_sp('15.0sp')
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
                        font_size: app.get_scaled_sp('15.0sp')
                        text: 'Y1+:'
                        halign: 'right'
                        markup: True
                        valign: 'middle'
                        text_size: self.size

                    Label:
                        id: y1_peak_posve_weighted
                        font_size: app.get_scaled_sp('15.0sp')
                        text: 'yyy'
                        halign: 'left'
                        markup: True
                        valign: 'middle'
                        text_size: self.size

                    Label:
                        id: y1_fw_range_weighted
                        font_size: app.get_scaled_sp('15.0sp')
                        text: 'yyy - yyy'
                        markup: True
                        valign: 'middle'
                        text_size: self.size
                        halign: 'center'

                    Label:
                        font_size: app.get_scaled_sp('15.0sp')
                        text: 'Y1-:'
                        halign: 'right'
                        markup: True
                        valign: 'middle'
                        text_size: self.size

                    Label:
                        id: y1_peak_negve_weighted
                        font_size: app.get_scaled_sp('15.0sp')
                        text: 'yyy'
                        halign: 'left'
                        markup: True
                        valign: 'middle'
                        text_size: self.size

                    Label:
                        id: y1_bw_range_weighted
                        font_size: app.get_scaled_sp('15.0sp')
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
                        font_size: app.get_scaled_sp('15.0sp')
                        text: 'Y2+:'
                        halign: 'right'
                        markup: True
                        valign: 'middle'
                        text_size: self.size

                    Label:
                        id: y2_peak_posve_weighted
                        font_size: app.get_scaled_sp('15.0sp')
                        text: 'yyy'
                        halign: 'left'
                        markup: True
                        valign: 'middle'
                        text_size: self.size

                    Label:
                        id: y2_fw_range_weighted
                        font_size: app.get_scaled_sp('15.0sp')
                        text: 'yyy - yyy'
                        markup: True
                        valign: 'middle'
                        text_size: self.size
                        halign: 'center'

                    Label:
                        font_size: app.get_scaled_sp('15.0sp')
                        text: 'Y2-:'
                        halign: 'right'
                        markup: True
                        valign: 'middle'
                        text_size: self.size

                    Label:
                        id: y2_peak_negve_weighted
                        font_size: app.get_scaled_sp('15.0sp')
                        text: 'yyy'
                        halign: 'left'
                        markup: True
                        valign: 'middle'
                        text_size: self.size

                    Label:
                        id: y2_bw_range_weighted
                        font_size: app.get_scaled_sp('15.0sp')
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
                        font_size: app.get_scaled_sp('15.0sp')
                        text: 'X+:'
                        halign: 'right'
                        markup: True
                        valign: 'middle'
                        text_size: self.size

                    Label:
                        id: x_peak_posve_weighted
                        font_size: app.get_scaled_sp('15.0sp')
                        text: 'xxx'
                        halign: 'left'
                        markup: True
                        valign: 'middle'
                        text_size: self.size

                    Label:
                        id: x_fw_range_weighted
                        font_size: app.get_scaled_sp('15.0sp')
                        text: 'xxx - xxx'
                        markup: True
                        valign: 'middle'
                        text_size: self.size
                        halign: 'center'

                    Label:
                        font_size: app.get_scaled_sp('15.0sp')
                        text: 'X-:'
                        halign: 'right'
                        markup: True
                        valign: 'middle'
                        text_size: self.size

                    Label:
                        id: x_peak_negve_weighted
                        font_size: app.get_scaled_sp('15.0sp')
                        text: 'xxx'
                        halign: 'left'
                        markup: True
                        valign: 'middle'
                        text_size: self.size

                    Label:
                        id: x_bw_range_weighted
                        font_size: app.get_scaled_sp('15.0sp')
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
                        font_size: app.get_scaled_sp('15.0sp')
                        text: ''

                    Label: 
                        font_size: app.get_scaled_sp('15.0sp')
                        text: ''

                    Label: 
                        font_size: app.get_scaled_sp('15.0sp')
                        text: ''

                    # Label:
                    #     text: 'Z-:'
                    #     halign: 'right'
                    #     markup: True
                    #     valign: 'middle'
                    #     text_size: self.size

                    # Label:
                    #     id: z_peak_negve_weighted
                    #     text: 'zzz'
                    #     halign: 'left'
                    #     markup: True
                    #     valign: 'middle'
                    #     text_size: self.size

                    # Label:
                    #     id: z_fw_range_weighted
                    #     text: 'zzz - zzz'
                    #     markup: True
                    #     valign: 'middle'
                    #     text_size: self.size
                    #     halign: 'center'

                    Label: 
                        font_size: app.get_scaled_sp('15.0sp')
                        text: ''

                    Label: 
                        font_size: app.get_scaled_sp('15.0sp')
                        text: ''

                    Label: 
                        font_size: app.get_scaled_sp('15.0sp')
                        text: ''

                    Label: 
                        font_size: app.get_scaled_sp('15.0sp')
                        text: ''

                    # Label:
                    #     text: 'Z+:'
                    #     halign: 'right'
                    #     markup: True
                    #     valign: 'middle'
                    #     text_size: self.size

                    # Label:
                    #     id: z_peak_posve_weighted
                    #     text: 'zzz'
                    #     halign: 'left'
                    #     markup: True
                    #     valign: 'middle'
                    #     text_size: self.size

                    # Label:
                    #     id: z_bw_range_weighted
                    #     text: 'zzz - zzz'
                    #     markup: True
                    #     valign: 'middle'
                    #     text_size: self.size
                    #     halign: 'center'

                    # Image:
                    #     id: z_peak_checkbox_weighted
                    #     source: "./asmcnc/skavaUI/img/checkbox_inactive.png"
                    #     center_x: self.parent.center_x
                    #     y: self.parent.y
                    #     size: self.parent.width, self.parent.height
                    #     allow_stretch: True

        BoxLayout:
            size_hint_y: 0.08
            id: status_container
"""
)
MAX_XY_SPEED = 2400.0
MAX_Z_SPEED = 150.0


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
    mini_run_dev_mode = False

    def __init__(self, **kwargs):
        super(CalibrationTesting, self).__init__(**kwargs)
        self.m = kwargs["m"]
        self.systemtools_sm = kwargs["systemtools"]
        self.calibration_db = kwargs["calibration_db"]
        self.sm = kwargs["sm"]
        self.l = kwargs["l"]

        # used to only measure axis in motion
        self.x_running = False
        self.y_running = False
        self.z_running = False
        self.stage = ""
        self.stage_id = 0
        self.statuses = []
        self.x_weight = 0
        self.y_weight = 0
        self.z_weight = 2
        self.status_data_dict = {"UnweightedFT": [], "WeightedFT": []}
        self.statistics_data_dict = {"UnweightedFT": [], "WeightedFT": []}
        self.raw_x_pos_vals = {"UnweightedFT": [], "WeightedFT": []}
        self.raw_y_pos_vals = {"UnweightedFT": [], "WeightedFT": []}
        self.raw_y1_pos_vals = {"UnweightedFT": [], "WeightedFT": []}
        self.raw_y2_pos_vals = {"UnweightedFT": [], "WeightedFT": []}
        self.raw_z_pos_vals = {"UnweightedFT": [], "WeightedFT": []}
        self.raw_x_neg_vals = {"UnweightedFT": [], "WeightedFT": []}
        self.raw_y_neg_vals = {"UnweightedFT": [], "WeightedFT": []}
        self.raw_y1_neg_vals = {"UnweightedFT": [], "WeightedFT": []}
        self.raw_y2_neg_vals = {"UnweightedFT": [], "WeightedFT": []}
        self.raw_z_neg_vals = {"UnweightedFT": [], "WeightedFT": []}
        self.setup_arrays("UnweightedFT")
        self.setup_arrays("WeightedFT")
        self.status_container.add_widget(
            widget_sg_status_bar.SGStatusBar(
                machine=self.m, screen_manager=self.systemtools_sm.sm
            )
        )
        if self.mini_run_dev_mode:
            self.sn_for_db = "YS6test"

    def setup_arrays(self, stage):
        self.raw_x_pos_vals[stage] = []
        self.raw_y_pos_vals[stage] = []
        self.raw_y1_pos_vals[stage] = []
        self.raw_y2_pos_vals[stage] = []
        self.raw_z_pos_vals[stage] = []
        self.raw_x_neg_vals[stage] = []
        self.raw_y_neg_vals[stage] = []
        self.raw_y1_neg_vals[stage] = []
        self.raw_y2_neg_vals[stage] = []
        self.raw_z_neg_vals[stage] = []

    # Stage is used to detect which part of the operation overnight test is in, both in screen functions & data
    def set_stage(self, stage):
        self.stage = stage
        self.stage_id = self.calibration_db.get_stage_id_by_description(self.stage)
        self.status_data_dict[self.stage] = []
        Logger.info("Overnight test, stage: " + str(self.stage))

    def stop(self):
        self.x_running = False
        self.y_running = False
        self.z_running = False
        if self.next_run_event != None:
            Clock.unschedule(self.next_run_event)
        if self.confirm_event != None:
            Clock.unschedule(self.confirm_event)
        popup_info.PopupStop(self.m, self.sm, self.l)
        self.enable_run_buttons()

    def on_enter(self):
        self.sn_for_db = "ys6" + str(self.m.serial_number()).split(".")[0]
        self.m.s.FINAL_TEST = True
        if self.next_run_event != None:
            Clock.unschedule(self.next_run_event)
        if self.confirm_event != None:
            Clock.unschedule(self.confirm_event)
        self.enable_run_buttons()

    def on_leave(self):
        self.m.s.FINAL_TEST = False
        if self.next_run_event != None:
            Clock.unschedule(self.next_run_event)
        if self.confirm_event != None:
            Clock.unschedule(self.confirm_event)
        self.enable_run_buttons()

    def back_to_fac_settings(self):
        self.systemtools_sm.open_factory_settings_screen()

    def home(self):
        self.m.is_machine_completed_the_initial_squaring_decision = True
        self.m.is_squaring_XY_needed_after_homing = False
        self.m.request_homing_procedure("calibration_testing", "calibration_testing")

    def reset(self):
        if self.next_run_event != None:
            Clock.unschedule(self.next_run_event)
        if self.confirm_event != None:
            Clock.unschedule(self.confirm_event)
        self.m.resume_from_alarm()
        self.enable_run_buttons()

    def zero_x_and_y(self):
        self.m.jog_absolute_xy(
            self.m.x_min_jog_abs_limit, self.m.y_min_jog_abs_limit, 6000
        )

    def mid_x_and_zero_y(self):
        self.m.jog_absolute_xy(-700, self.m.y_min_jog_abs_limit, 6000)

    def zero_Z(self):
        self.m.jog_absolute_single_axis("Z", self.m.z_max_jog_abs_limit, 750)

    def disable_x_measurement(self, dt):
        self.x_running = False

    def disable_z_measurement(self, dt):
        self.z_running = False

    def disable_y_measurement(self, dt):
        self.y_running = False

    def enable_run_buttons(self):
        self.x_load_button.disabled = False
        self.y_load_button.disabled = False
        # self.z_load_button.disabled = False
        self.unweighted_test_button.disabled = False
        self.home_button.disabled = False
        self.x0y0_jog_button.disabled = False
        self.x7y0_jog_button.disabled = False
        self.z0_jog_button.disabled = False
        if all(
            [
                self.is_step_ticked(self.unweighted_test_check),
                self.is_step_ticked(self.x_test_check),
                self.is_step_ticked(self.y_test_check),
            ]
        ):
            self.data_send_button.disabled = False
        else:
            self.data_send_button.disabled = True

    def disable_run_buttons(self):
        self.x_load_button.disabled = True
        self.y_load_button.disabled = True
        self.unweighted_test_button.disabled = True
        self.home_button.disabled = True
        self.x0y0_jog_button.disabled = True
        self.x7y0_jog_button.disabled = True
        self.z0_jog_button.disabled = True
        self.data_send_button.disabled = True

    def measure(self):
        if (
            not (self.x_running and self.m.feed_rate() < MAX_XY_SPEED * 1.1)
            and not (self.y_running and self.m.feed_rate() < MAX_XY_SPEED * 1.1)
            and not (self.z_running and self.m.feed_rate() < MAX_Z_SPEED * 1.1)
        ):
            return
        
        # GET DIRECTIONS

        # -1    BACKWARDS/UP (TOWARDS HOME)
        # 0     NOT MOVING
        # 1     FORWARDS/DOWN (AWAY FROM HOME)

        # NOTE Z LIFTS WEIGHT WHEN IT IS

        if len(self.status_data_dict[self.stage]) > 0:
            if (
                self.status_data_dict[self.stage][
                    len(self.status_data_dict[self.stage]) - 1
                ][1]
                < self.m.mpos_x()
            ):
                x_dir = -1
            elif (
                self.status_data_dict[self.stage][
                    len(self.status_data_dict[self.stage]) - 1
                ][1]
                > self.m.mpos_x()
            ):
                x_dir = 1
            else:
                x_dir = 0
            if (
                self.status_data_dict[self.stage][
                    len(self.status_data_dict[self.stage]) - 1
                ][2]
                < self.m.mpos_y()
            ):
                y_dir = -1
            elif (
                self.status_data_dict[self.stage][
                    len(self.status_data_dict[self.stage]) - 1
                ][2]
                > self.m.mpos_y()
            ):
                y_dir = 1
            else:
                y_dir = 0
            if (
                self.status_data_dict[self.stage][
                    len(self.status_data_dict[self.stage]) - 1
                ][3]
                < self.m.mpos_z()
            ):
                z_dir = 1
            elif (
                self.status_data_dict[self.stage][
                    len(self.status_data_dict[self.stage]) - 1
                ][3]
                > self.m.mpos_z()
            ):
                z_dir = -1
            else:
                z_dir = 0
        else:
            x_dir = 0
            y_dir = 0
            z_dir = 0

        # XCoordinate, YCoordinate, ZCoordinate, XDirection, YDirection, ZDirection, XSG, YSG, Y1SG, Y2SG, ZSG, TMCTemperature, PCBTemperature, MOTTemperature, Timestamp, Feedrate
        
        status = (
            int(self.sn_for_db[2:] + str(self.stage_id)),
            self.m.mpos_x(),
            self.m.mpos_y(),
            self.m.mpos_z(),
            x_dir,
            y_dir,
            z_dir,
            int(self.m.s.sg_x_motor_axis),
            int(self.m.s.sg_y_axis),
            int(self.m.s.sg_y1_motor),
            int(self.m.s.sg_y2_motor),
            int(self.m.s.sg_z_motor_axis),
            int(self.m.s.motor_driver_temp),
            int(self.m.s.pcb_temp),
            int(self.m.s.transistor_heatsink_temp),
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            self.m.feed_rate(),
            self.x_weight,
            self.y_weight,
            self.z_weight,
        )
        self.status_data_dict[self.stage].append(status)

        # Record raw values for statistics calculations
        if -999 < self.m.s.sg_x_motor_axis < 1023:
            if x_dir > 0:
                self.raw_x_pos_vals[self.stage].append(self.m.s.sg_x_motor_axis)
            if x_dir < 0:
                self.raw_x_neg_vals[self.stage].append(self.m.s.sg_x_motor_axis)
        if -999 < self.m.s.sg_y_axis < 1023:
            if y_dir > 0:
                self.raw_y_pos_vals[self.stage].append(self.m.s.sg_y_axis)
            if y_dir < 0:
                self.raw_y_neg_vals[self.stage].append(self.m.s.sg_y_axis)
        if -999 < self.m.s.sg_y1_motor < 1023:
            if y_dir > 0:
                self.raw_y1_pos_vals[self.stage].append(self.m.s.sg_y1_motor)
            if y_dir < 0:
                self.raw_y1_neg_vals[self.stage].append(self.m.s.sg_y1_motor)
        if -999 < self.m.s.sg_y2_motor < 1023:
            if y_dir > 0:
                self.raw_y2_pos_vals[self.stage].append(self.m.s.sg_y2_motor)
            if y_dir < 0:
                self.raw_y2_neg_vals[self.stage].append(self.m.s.sg_y2_motor)
        if -999 < self.m.s.sg_z_motor_axis < 1023:
            if z_dir < 0:
                self.raw_z_pos_vals[self.stage].append(self.m.s.sg_z_motor_axis)
            if z_dir > 0:
                self.raw_z_neg_vals[self.stage].append(self.m.s.sg_z_motor_axis)
        self.update_peaks()

    def update_peaks(self):
        if self.stage == "UnweightedFT":
            self.get_peak_as_string(self.x_peak_posve, self.raw_x_pos_vals[self.stage])
            self.get_peak_as_string(self.y_peak_posve, self.raw_y_pos_vals[self.stage])
            self.get_peak_as_string(
                self.y1_peak_posve, self.raw_y1_pos_vals[self.stage]
            )
            self.get_peak_as_string(
                self.y2_peak_posve, self.raw_y2_pos_vals[self.stage]
            )
            self.get_peak_as_string(self.z_peak_posve, self.raw_z_pos_vals[self.stage])
            self.get_peak_as_string(self.x_peak_negve, self.raw_x_neg_vals[self.stage])
            self.get_peak_as_string(self.y_peak_negve, self.raw_y_neg_vals[self.stage])
            self.get_peak_as_string(
                self.y1_peak_negve, self.raw_y1_neg_vals[self.stage]
            )
            self.get_peak_as_string(
                self.y2_peak_negve, self.raw_y2_neg_vals[self.stage]
            )
            self.get_peak_as_string(self.z_peak_negve, self.raw_z_neg_vals[self.stage])
            return
        if self.stage == "WeightedFT":
            self.get_peak_as_string(
                self.x_peak_posve_weighted, self.raw_x_pos_vals[self.stage]
            )
            self.get_peak_as_string(
                self.y_peak_posve_weighted, self.raw_y_pos_vals[self.stage]
            )
            self.get_peak_as_string(
                self.y1_peak_posve_weighted, self.raw_y1_pos_vals[self.stage]
            )
            self.get_peak_as_string(
                self.y2_peak_posve_weighted, self.raw_y2_pos_vals[self.stage]
            )
            #self.get_peak_as_string(
            #    self.z_peak_posve_weighted, self.raw_z_pos_vals[self.stage]
            #)
            self.get_peak_as_string(
                self.x_peak_negve_weighted, self.raw_x_neg_vals[self.stage]
            )
            self.get_peak_as_string(
                self.y_peak_negve_weighted, self.raw_y_neg_vals[self.stage]
            )
            self.get_peak_as_string(
                self.y1_peak_negve_weighted, self.raw_y1_neg_vals[self.stage]
            )
            self.get_peak_as_string(
                self.y2_peak_negve_weighted, self.raw_y2_neg_vals[self.stage]
            )
            #self.get_peak_as_string(
            #    self.z_peak_negve_weighted, self.raw_z_neg_vals[self.stage]
            #)
            return

    def get_peak_as_string(self, label_id, raw_vals):
        try:
            label_id.text = str(max(raw_vals))
        except:
            pass

    def read_out_peaks(self, stage):
        if stage == "UnweightedFT":
            peak_list = [
                int(self.x_peak_posve.text),
                int(self.x_peak_negve.text),
                int(self.y_peak_posve.text),
                int(self.y_peak_negve.text),
                int(self.y1_peak_posve.text),
                int(self.y1_peak_negve.text),
                int(self.y2_peak_posve.text),
                int(self.y2_peak_negve.text),
                int(self.z_peak_negve.text),
                int(self.z_peak_posve.text),
                # int(self.z_peak_negve_weighted.text),
                # int(self.z_peak_posve_weighted.text)
            ]
            return peak_list
        if stage == "WeightedFT":
            peak_list = [
                int(self.x_peak_posve_weighted.text),
                int(self.x_peak_negve_weighted.text),
                int(self.y_peak_posve_weighted.text),
                int(self.y_peak_negve_weighted.text),
                int(self.y1_peak_posve_weighted.text),
                int(self.y1_peak_negve_weighted.text),
                int(self.y2_peak_posve_weighted.text),
                int(self.y2_peak_negve_weighted.text),
            ]
            return peak_list

    def get_statistics(self, stage):

        # x_forw_peak, x_backw_peak, y_forw_peak, y_backw_peak, y1_forw_peak, y1_backw_peak, y2_forw_peak, y2_backw_peak, z_forw_peak, z_backw_peak 

        peak_list = self.read_out_peaks(stage)
        if stage == "UnweightedFT":
            self.statistics_data_dict[stage] = [
                sum(self.raw_x_pos_vals[stage]) / len(self.raw_x_pos_vals[stage]),
                peak_list[0],
                sum(self.raw_x_neg_vals[stage]) / len(self.raw_x_neg_vals[stage]),
                peak_list[1],
                sum(self.raw_y_pos_vals[stage]) / len(self.raw_y_pos_vals[stage]),
                peak_list[2],
                sum(self.raw_y_neg_vals[stage]) / len(self.raw_y_neg_vals[stage]),
                peak_list[3],
                sum(self.raw_y1_pos_vals[stage]) / len(self.raw_y1_pos_vals[stage]),
                peak_list[4],
                sum(self.raw_y1_neg_vals[stage]) / len(self.raw_y1_neg_vals[stage]),
                peak_list[5],
                sum(self.raw_y2_pos_vals[stage]) / len(self.raw_y2_pos_vals[stage]),
                peak_list[6],
                sum(self.raw_y2_neg_vals[stage]) / len(self.raw_y2_neg_vals[stage]),
                peak_list[7],
                sum(self.raw_z_pos_vals[stage]) / len(self.raw_z_pos_vals[stage]),
                peak_list[8],
                sum(self.raw_z_neg_vals[stage]) / len(self.raw_z_neg_vals[stage]),
                peak_list[9],
            ]
        if stage == "WeightedFT":
            self.statistics_data_dict[stage] = [
                sum(self.raw_x_pos_vals[stage]) / len(self.raw_x_pos_vals[stage]),
                peak_list[0],
                sum(self.raw_x_neg_vals[stage]) / len(self.raw_x_neg_vals[stage]),
                peak_list[1],
                sum(self.raw_y_pos_vals[stage]) / len(self.raw_y_pos_vals[stage]),
                peak_list[2],
                sum(self.raw_y_neg_vals[stage]) / len(self.raw_y_neg_vals[stage]),
                peak_list[3],
                sum(self.raw_y1_pos_vals[stage]) / len(self.raw_y1_pos_vals[stage]),
                peak_list[4],
                sum(self.raw_y1_neg_vals[stage]) / len(self.raw_y1_neg_vals[stage]),
                peak_list[5],
                sum(self.raw_y2_pos_vals[stage]) / len(self.raw_y2_pos_vals[stage]),
                peak_list[6],
                sum(self.raw_y2_neg_vals[stage]) / len(self.raw_y2_neg_vals[stage]),
                peak_list[7],
                0,
                0,
                0,
                0,
                # sum(self.raw_z_pos_vals[stage])/len(self.raw_z_pos_vals[stage]),
                # peak_list[8],
                # sum(self.raw_z_neg_vals[stage])/len(self.raw_z_neg_vals[stage]),
                # peak_list[9]
            ]

    # def run_z_procedure(self, dt):

    #     # start run, run all the way down and then all the way back up. 

    #     if self.m.mpos_z() != self.m.z_max_jog_abs_limit:
    #         popup_info.PopupError(self.sm, self.l, "Move Z to Z0 first!")
    #         return

    #     self.disable_run_buttons()

    #     self.raw_z_pos_vals["WeightedFT"] = []
    #     self.raw_z_neg_vals["WeightedFT"] = []

    #     if self.stage != "WeightedFT":
    #         self.set_stage("WeightedFT")
        
    #     self.x_weight = 0
    #     self.y_weight = 0

    #     self.set_weighted_z_range()

    #     self.z_running = True

    #     self.m.send_any_gcode_command('G91 G1 Z-149 F' + str(MAX_Z_SPEED))
    #     self.m.send_any_gcode_command('G91 G1 Z149 F' + str(MAX_Z_SPEED))

    #     # poll to see when run is done
    #     self.confirm_event = Clock.schedule_interval(self.confirm_z, 5)


    # def confirm_z(self, dt):
    #     if self.m.state().startswith('Idle'):
    #         self.z_running = False
    #         self.enable_run_buttons()
    #         self.z_test_check.source = "./asmcnc/skavaUI/img/file_select_select.png"
    #         self.tick_checkbox(self.z_peak_checkbox_weighted, self.check_in_range(self.z_peak_posve_weighted))


    def run_y_procedure(self, dt):

        # start run, run all the way down and then all the way back up. 
        self.disable_run_buttons()
        self.raw_y_pos_vals["WeightedFT"] = []
        self.raw_y_neg_vals["WeightedFT"] = []
        self.raw_y1_pos_vals["WeightedFT"] = []
        self.raw_y1_neg_vals["WeightedFT"] = []
        self.raw_y2_pos_vals["WeightedFT"] = []
        self.raw_y2_neg_vals["WeightedFT"] = []
        if self.stage != "WeightedFT":
            self.set_stage("WeightedFT")
        self.x_weight = 0
        self.y_weight = 7.5
        self.set_weighted_y_range()
        self.y_running = True
        self.m.send_any_gcode_command(
            "G53 G1 Y" + str(self.m.y_max_jog_abs_limit) + " F" + str(MAX_XY_SPEED)
        )
        self.m.send_any_gcode_command(
            "G53 G1 Y" + str(self.m.y_min_jog_abs_limit) + " F" + str(MAX_XY_SPEED)
        )

        # poll to see when run is done
        self.confirm_event = Clock.schedule_interval(self.confirm_y, 5)

    def confirm_y(self, dt):
        if self.m.state().startswith("Idle"):
            self.y_running = False
            self.enable_run_buttons()
            self.y_test_check.source = "./asmcnc/skavaUI/img/file_select_select.png"
            self.tick_checkbox(
                self.y_peak_checkbox_weighted,
                self.check_in_range(self.y_peak_posve_weighted),
            )
            self.tick_checkbox(
                self.y1_peak_checkbox_weighted,
                self.check_in_range(self.y1_peak_posve_weighted),
            )
            self.tick_checkbox(
                self.y2_peak_checkbox_weighted,
                self.check_in_range(self.y2_peak_posve_weighted),
            )

    def run_x_procedure(self, dt):

        # start run, run all the way down and then all the way back up. 
        self.disable_run_buttons()
        self.raw_x_pos_vals["WeightedFT"] = []
        self.raw_x_neg_vals["WeightedFT"] = []
        if self.stage != "WeightedFT":
            self.set_stage("WeightedFT")
        self.x_weight = 7.5
        self.y_weight = 0
        self.set_weighted_x_range()
        self.x_running = True
        self.m.send_any_gcode_command(
            "G53 G1 X" + str(self.m.x_max_jog_abs_limit) + " F" + str(MAX_XY_SPEED)
        )
        self.m.send_any_gcode_command(
            "G53 G1 X" + str(self.m.x_min_jog_abs_limit) + " F" + str(MAX_XY_SPEED)
        )

        # poll to see when run is done
        self.confirm_event = Clock.schedule_interval(self.confirm_x, 5)

    def confirm_x(self, dt):
        if self.m.state().startswith("Idle"):
            self.x_running = False
            self.enable_run_buttons()
            self.x_test_check.source = "./asmcnc/skavaUI/img/file_select_select.png"
            self.tick_checkbox(
                self.x_peak_checkbox_weighted,
                self.check_in_range(self.x_peak_posve_weighted),
            )

    def run_unweighted_test(self):
        if self.m.state().startswith("Idle"):
            self.disable_run_buttons()
            self.set_stage("UnweightedFT")
            self.x_weight = 0
            self.y_weight = 0
            self.zero_x_and_y()
            self.zero_Z()
            self.next_run_event = Clock.schedule_once(self.part_1_unweighted_x, 3)
        else:
            popup_info.PopupError(self.sm, self.l, "SB not Idle! Check status")

    def part_1_unweighted_x(self, dt):
        if self.m.state().startswith("Idle"):
            self.setup_arrays("UnweightedFT")
            self.set_unweighted_x_range()
            self.x_running = True
            self.m.send_any_gcode_command(
                "G53 G1 X" + str(self.m.x_max_jog_abs_limit) + " F" + str(MAX_XY_SPEED)
            )
            self.m.send_any_gcode_command(
                "G53 G1 X" + str(self.m.x_min_jog_abs_limit) + " F" + str(MAX_XY_SPEED)
            )
            self.next_run_event = Clock.schedule_once(self.part_2_unweighted_y, 20)
        else:
            self.next_run_event = Clock.schedule_once(self.part_1_unweighted_x, 3)

    def part_2_unweighted_y(self, dt):
        if self.m.state().startswith("Idle"):
            self.set_unweighted_y_range()
            self.x_running = False
            self.y_running = True
            self.m.send_any_gcode_command(
                "G53 G1 Y" + str(self.m.y_max_jog_abs_limit) + " F" + str(MAX_XY_SPEED)
            )
            self.m.send_any_gcode_command(
                "G53 G1 Y" + str(self.m.y_min_jog_abs_limit) + " F" + str(MAX_XY_SPEED)
            )
            self.next_run_event = Clock.schedule_once(self.part_3_unweighted_z, 20)
        else:
            self.next_run_event = Clock.schedule_once(self.part_2_unweighted_y, 3)

    def part_3_unweighted_z(self, dt):
        if self.m.state().startswith("Idle"):
            self.set_unweighted_z_range()
            self.y_running = False
            self.z_running = True
            self.m.send_any_gcode_command(
                "G53 G1 Z" + str(self.m.z_min_jog_abs_limit) + " F" + str(MAX_Z_SPEED)
            )
            self.m.send_any_gcode_command(
                "G53 G1 Z" + str(self.m.z_max_jog_abs_limit) + " F" + str(MAX_Z_SPEED)
            )
            self.confirm_event = Clock.schedule_once(self.confirm_unweighted, 20)
        else:
            self.next_run_event = Clock.schedule_once(self.part_3_unweighted_z, 3)

    def confirm_unweighted(self, dt):
        if self.m.state().startswith("Idle"):
            self.z_running = False
            self.enable_run_buttons()
            # self.data_send_button.disabled = False
            self.unweighted_test_check.source = self.green_tick
            self.pass_or_fail_unweighted_peak_loads()
        else:
            self.confirm_event = Clock.schedule_once(self.confirm_unweighted, 3)

    ## SET TICKS
    def tick_checkbox(self, checkbox_id, tick):
        if tick:
            checkbox_id.source = self.green_tick
        else:
            checkbox_id.source = self.red_cross

    def is_step_ticked(self, checkbox_id):
        if checkbox_id.source == self.green_tick:
            return True
        else:
            return False

    def check_in_range(self, peak_id):
        within_plus_minus = 400
        try:
            if -1 * within_plus_minus < int(peak_id.text) < within_plus_minus:
                return True
            else:
                return False
        except:
            return False

    def pass_or_fail_unweighted_peak_loads(self):
        within_plus_minus = 400
        self.tick_checkbox(self.y_peak_checkbox, self.check_in_range(self.y_peak_posve))
        self.tick_checkbox(
            self.y1_peak_checkbox, self.check_in_range(self.y1_peak_posve)
        )
        self.tick_checkbox(
            self.y2_peak_checkbox, self.check_in_range(self.y2_peak_posve)
        )
        self.tick_checkbox(self.x_peak_checkbox, self.check_in_range(self.x_peak_posve))
        self.tick_checkbox(self.z_peak_checkbox, self.check_in_range(self.z_peak_posve))

    def up_range(self, friction, load):
        expected_min = (friction + float(load)) * (1.0 - self.tolerance)
        expected_max = (friction + float(load)) * (1.0 + self.tolerance)
        return expected_min, expected_max

    def down_range(self, friction, load):
        expected_min = (friction - float(load)) * (1.0 - self.tolerance)
        expected_max = (friction - float(load)) * (1.0 + self.tolerance)
        return expected_min, expected_max

    def get_range_text(self, friction, load, scaling):
        fw_expected_min, fw_expected_max = self.up_range(friction, load)
        bw_expected_min, bw_expected_max = self.down_range(friction, load)
        fw_range_text = (
            str(fw_expected_min * scaling) + " - " + str(fw_expected_max * scaling)
        )
        bw_range_text = (
            str(bw_expected_min * scaling) + " - " + str(bw_expected_max * scaling)
        )
        return fw_range_text, bw_range_text

    def set_unweighted_x_range(self):
        x_fw_range_text, x_bw_range_text = self.get_range_text(
            self.xy_friction, 0, self.X_SG_to_kg_scaling
        )
        self.x_fw_range.text = x_fw_range_text
        self.x_bw_range.text = x_bw_range_text

    def set_weighted_x_range(self):
        x_fw_range_text, x_bw_range_text = self.get_range_text(
            self.xy_friction, 7.5, self.X_SG_to_kg_scaling
        )
        self.x_fw_range_weighted.text = x_fw_range_text
        self.x_bw_range_weighted.text = x_bw_range_text

    def set_unweighted_y_range(self):
        y_fw_range_text, y_bw_range_text = self.get_range_text(
            self.xy_friction, 0, self.Y_SG_to_kg_scaling
        )
        self.y_axis_fw_range.text = y_fw_range_text
        self.y1_fw_range.text = y_fw_range_text
        self.y2_fw_range.text = y_fw_range_text
        self.y_axis_bw_range.text = y_bw_range_text
        self.y1_bw_range.text = y_bw_range_text
        self.y2_bw_range.text = y_bw_range_text

    def set_weighted_y_range(self):
        y_fw_range_text, y_bw_range_text = self.get_range_text(
            self.xy_friction, 7.5, self.Y_SG_to_kg_scaling
        )
        self.y_axis_fw_range_weighted.text = y_fw_range_text
        self.y1_fw_range_weighted.text = y_fw_range_text
        self.y2_fw_range_weighted.text = y_fw_range_text
        self.y_axis_bw_range_weighted.text = y_bw_range_text
        self.y1_bw_range_weighted.text = y_bw_range_text
        self.y2_bw_range_weighted.text = y_bw_range_text

    def set_unweighted_z_range(self):
        z_fw_range_text, z_bw_range_text = self.get_range_text(
            self.z_friction, 2, self.Z_SG_to_kg_scaling
        )
        self.z_fw_range.text = z_fw_range_text
        self.z_bw_range.text = z_bw_range_text

    # def set_weighted_z_range(self):

    #     z_fw_range_text, z_bw_range_text = self.get_range_text(self.z_friction, 2, self.Z_SG_to_kg_scaling)

    #     self.z_fw_range_weighted.text = z_fw_range_text
    #     self.z_bw_range_weighted.text = z_bw_range_text   
        
    def send_all_data(self):
        self.calibration_db.set_up_connection()
        self.data_send_button.disabled = True
        self.data_send_label.text = "Sending..."
        self.sent_data_check.source = self.checkbox_inactive
        Clock.schedule_once(self.do_data_send, 0.2)

    def do_data_send(self, dt):
        success = True
        try:
            if self.is_step_ticked(self.unweighted_test_check):
                self.get_statistics("UnweightedFT")
                success = success * self.send_data_for_each_stage("UnweightedFT")
            if all(
                [
                    self.is_step_ticked(self.x_test_check),
                    self.is_step_ticked(self.y_test_check),
                ]
            ):
                self.get_statistics("WeightedFT")
                success = success * self.send_data_for_each_stage("WeightedFT")
            if success:
                self.sent_data_check.source = self.green_tick
            else:
                self.sent_data_check.source = self.red_cross
        except:
            self.sent_data_check.source = self.red_cross
            Logger.exception("Failed to do data send")
        self.data_send_label.text = "Sent data?"
        self.data_send_button.disabled = False
        log_exporter.create_and_send_logs(self.sn_for_db)

    def send_data_for_each_stage(self, stage):
        try:
            try:
                stage_id = self.calibration_db.get_stage_id_by_description(stage)
                self.insert_stage_into_database(stage_id)
                self.calibration_db.insert_final_test_statuses(
                    self.status_data_dict[stage]
                )
                statistics = [self.sn_for_db, stage_id]
                statistics.extend(self.statistics_data_dict[stage])
                self.calibration_db.insert_final_test_statistics(*statistics)
                return True
            except:
                Logger.exception("Failed to send data")
                return False
        finally:
            log_exporter.create_and_send_logs(self.sn_for_db)

    def insert_stage_into_database(self, stage_id):
        try:
            self.calibration_db.insert_final_test_stage(self.sn_for_db, stage_id)
        except:
            Logger.exception("Could not insert final test stage into DB!!")
            message = "Issue contacting database - if you continue data send may fail!"
            popup_info.PopupError(self.sm, self.l, message)
