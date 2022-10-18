from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.clock import Clock
from asmcnc.comms.yeti_grbl_protocol.c_defines import *
from datetime import datetime

from asmcnc.skavaUI import widget_status_bar

Builder.load_string("""
<ZHeadPCBSetUpOutcome>:

    status_container : status_container
    fw_update_image : fw_update_image
    fw_update_label : fw_update_label
    fw_version_image : fw_version_image
    fw_version_label : fw_version_label
    z_current_image : z_current_image
    z_current_label : z_current_label
    x_current_image : x_current_image
    x_current_label : x_current_label
    thermal_coefficients_image : thermal_coefficients_image
    thermal_coefficients_label : thermal_coefficients_label


    BoxLayout:
        orientation: 'vertical'

        BoxLayout:
            orientation: 'vertical'
            size_hint_y: 0.92

            BoxLayout:
                orientation: 'horizontal'
                size_hint_y: 0.2

                Button:
                    text: '<<< Back'
                    text_size: self.size
                    markup: 'True'
                    halign: 'left'
                    valign: 'middle'
                    padding: [dp(10),0]
                    on_press: root.go_back_to_pcb_setup()


                BoxLayout: 
                    orientation: 'horizontal'

            GridLayout: 
                size_hint_y: 0.6
                cols: 2
                rows: 5
                cols_minimum: {0: dp(200), 1: dp(600)}

                Image:
                    id: fw_update_image
                    source: "./asmcnc/skavaUI/img/checkbox_inactive.png"
                    center_x: self.parent.center_x
                    y: self.parent.y
                    size: self.parent.width, self.parent.height
                    allow_stretch: True

                Label:
                    id: fw_update_label
                    text: "FW update successful"
                    text_size: self.size
                    markup: 'True'
                    halign: 'left'
                    valign: 'middle'

                Image:
                    id: fw_version_image
                    source: "./asmcnc/skavaUI/img/checkbox_inactive.png"
                    center_x: self.parent.center_x
                    y: self.parent.y
                    size: self.parent.width, self.parent.height
                    allow_stretch: True

                Label:
                    id: fw_version_label
                    text: "FW update successful"
                    text_size: self.size
                    markup: 'True'
                    halign: 'left'
                    valign: 'middle'

                Image:
                    id: z_current_image
                    source: "./asmcnc/skavaUI/img/file_select_select.png"
                    center_x: self.parent.center_x
                    y: self.parent.y
                    size: self.parent.width, self.parent.height
                    allow_stretch: True

                Label:
                    id: z_current_label
                    text: "FW update successful"
                    text_size: self.size
                    markup: 'True'
                    halign: 'left'
                    valign: 'middle'

                Image:
                    id: x_current_image
                    source: "./asmcnc/skavaUI/img/checkbox_inactive.png"
                    center_x: self.parent.center_x
                    y: self.parent.y
                    size: self.parent.width, self.parent.height
                    allow_stretch: True

                Label:
                    id: x_current_label
                    text: "FW update successful"
                    text_size: self.size
                    markup: 'True'
                    halign: 'left'
                    valign: 'middle'

                Image:
                    id: thermal_coefficients_image
                    source: "./asmcnc/skavaUI/img/checkbox_inactive.png"
                    center_x: self.parent.center_x
                    y: self.parent.y
                    size: self.parent.width, self.parent.height
                    allow_stretch: True

                Label:
                    id: thermal_coefficients_label
                    text: "FW update successful"
                    text_size: self.size
                    markup: 'True'
                    halign: 'left'
                    valign: 'middle'

            Button:
                on_press: 
                text: 'OK'
                font_size: dp(30)
                size_hint_y: 0.2
                on_press: root.go_to_qc_home()

        BoxLayout:
            size_hint_y: 0.08
            id: status_container 
            pos: self.pos
""")

def log(message):
    timestamp = datetime.now()
    print ('Z Head Connecting Screen: ' + timestamp.strftime('%H:%M:%S.%f' )[:12] + ' ' + str(message))

class ZHeadPCBSetUpOutcome(Screen):

    undetermined_image = "./asmcnc/skavaUI/img/checkbox_inactive.png"
    success_image = "./asmcnc/skavaUI/img/file_select_select.png"
    fail_image = "./asmcnc/skavaUI/img/template_cancel.png"

    fw_update_success = True
    fw_version_correct = True
    z_current_correct = True
    x_current_correct = True
    thermal_coefficients_correct = True

    def __init__(self, **kwargs):

        super(ZHeadPCBSetUpOutcome, self).__init__(**kwargs)

        self.sm = kwargs['sm']
        self.m = kwargs['m']

        # Green status bar
        self.status_bar_widget = widget_status_bar.StatusBar(machine=self.m, screen_manager=self.sm)
        self.status_container.add_widget(self.status_bar_widget)

    def go_to_qc_home(self):
        self.sm.current = "qchome"

    def go_back_to_pcb_setup(self):
        self.sm.current = "qcpcbsetup"

    def on_enter(self):

        if self.fw_update_success:
            self.fw_update_image.source = self.success_image

        if self.fw_version_correct: 
            self.fw_version_image.source = self.success_image

        if self.z_current_correct:
            self.z_current_image.source = self.success_image

        if self.x_current_correct:
            self.x_current_image.source = self.success_image

        if self.thermal_coefficients_correct:
            self.thermal_coefficients_image.source = self.success_image



    # fw_update_image
    # fw_update_label
    # fw_version_image
    # fw_version_label
    # z_current_image
    # z_current_label
    # x_current_image
    # x_current_label
    # thermal_coefficients_image
    # thermal_coefficients_label
