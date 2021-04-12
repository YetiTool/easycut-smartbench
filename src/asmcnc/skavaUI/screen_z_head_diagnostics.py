
'''
Created on 03 August 2020

@author: Letty
'''

import kivy
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from kivy.uix.scrollview import ScrollView
from kivy.properties import StringProperty

from asmcnc.skavaUI import popup_info

Builder.load_string("""

<ZHeadDiagnosticsScreen>:

    fw_version_label : fw_version_label
    consoleStatusText : consoleStatusText
    # dust_shoe_check : dust_shoe_check
    x_home_check : x_home_check
    x_max_check : x_max_check
    z_home_check : z_home_check
    probe_check : probe_check
    temp_voltage_power_check : temp_voltage_power_check
    spindle_toggle : spindle_toggle
    laser_toggle : laser_toggle
    spindle_speed_check : spindle_speed_check

    GridLayout:
        size: self.parent.size
        pos: self.parent.pos
        cols: 3
        rows: 6
        cols_minimum: {0: 250, 1: 250, 2: 300}

# Row 1

        GridLayout:
            size: self.parent.size
            pos: self.parent.pos
            cols: 2
	        Label:
		        text: '  1. FW Version: '
		        color: 1,1,1,1
            	text_size: self.size
	            size: self.parent.size
	            pos: self.parent.pos
	            markup: 'True'
	            halign: 'left'
	            valign: 'middle'

		    Label:
                id: fw_version_label
		        text: 'fw version 1.etc.'
		        color: 1,1,1,1

        GridLayout:
            size: self.parent.size
            pos: self.parent.pos
            cols: 4

            Label: 
                text: '  8. Dust Shoe'
                color: 1,1,1,1
                text_size: self.size
                size: self.parent.size
                pos: self.parent.pos
                markup: 'True'
                halign: 'left'
                valign: 'middle'

            Button: 
                text: 'R'
                on_press: root.dust_shoe_red()

            Button: 
                text: 'G'
                on_press: root.dust_shoe_green()

            Button:
                text: 'B'
                on_press: root.dust_shoe_blue()



        Button:
            text: '  STOP'
            text_size: self.size
            size: self.parent.size
            pos: self.parent.pos
            markup: 'True'
            halign: 'center'
            valign: 'middle'
            on_press: root.stop()
            background_color: [1,0,0,1]
            background_normal: ''


# Row 2


	    Button:
	    	text: '  2. Bake GRBL Settings'
        	text_size: self.size
            size: self.parent.size
            pos: self.parent.pos
            markup: 'True'
            halign: 'left'
            valign: 'middle'
            on_press: root.bake_grbl_settings()

        GridLayout:
            size: self.parent.size
            pos: self.parent.pos
            cols: 2

            Label: 
                text: '  9. X Home'
                color: 1,1,1,1
                text_size: self.size
                size: self.parent.size
                pos: self.parent.pos
                markup: 'True'
                halign: 'left'
                valign: 'middle'        

            Image:
                id: x_home_check
                source: "./asmcnc/skavaUI/img/checkbox_inactive.png"
                center_x: self.parent.center_x
                y: self.parent.y
                size: self.parent.width, self.parent.height
                allow_stretch: True

        # GridLayout:
        #     size: self.parent.size
        #     pos: self.parent.pos
        #     cols: 2

        #     Label: 
        #         text: '  7. Dust shoe         switch'
        #         color: 1,1,1,1
        #         text_size: self.size
        #         size: self.parent.size
        #         pos: self.parent.pos
        #         markup: 'True'
        #         halign: 'left'
        #         valign: 'middle'       

        #     Image:
        #         id: dust_shoe_check
        #         source: "./asmcnc/skavaUI/img/checkbox_inactive.png"
        #         center_x: self.parent.center_x
        #         y: self.parent.y
        #         size: self.parent.width, self.parent.height
        #         allow_stretch: True

        Button: 
            id: do_cycle
            text: '  14. Cycle'
            on_press: root.do_cycle()
            text_size: self.size
            size: self.parent.size
            pos: self.parent.pos
            markup: 'True'
            halign: 'left'
            valign: 'middle'


# Row 3

        Button:
            text: '  3. HOME'
            text_size: self.size
            size: self.parent.size
            pos: self.parent.pos
            markup: 'True'
            halign: 'left'
            valign: 'middle'
            on_press: root.home()

        GridLayout:
            size: self.parent.size
            pos: self.parent.pos
            cols: 2

            Label: 
                text: '  10. X Max'
                color: 1,1,1,1
                text_size: self.size
                size: self.parent.size
                pos: self.parent.pos
                markup: 'True'
                halign: 'left'
                valign: 'middle'       

            Image:
                id: x_max_check
                source: "./asmcnc/skavaUI/img/checkbox_inactive.png"
                center_x: self.parent.center_x
                y: self.parent.y
                size: self.parent.width, self.parent.height
                allow_stretch: True

        GridLayout:
            size: self.parent.size
            pos: self.parent.pos
            cols: 2

            Button: 
                text: '15. Spindle Speed Check (wait 8 seconds)'
                color: 1,1,1,1
                on_press: root.run_spindle_check()
                text_size: self.size
                size: self.parent.size
                pos: self.parent.pos
                markup: 'True'
                halign: 'center'
                valign: 'middle'

            Image:
                id: spindle_speed_check
                source: "./asmcnc/skavaUI/img/checkbox_inactive.png"
                center_x: self.parent.center_x
                y: self.parent.y
                size: self.parent.width, self.parent.height
                allow_stretch: True



# Row 4

        GridLayout:
            size: self.parent.size
            pos: self.parent.pos
            cols: 3

            Label: 
                text: ' 4. X motors'
                color: 1,1,1,1

            Button: 
                text: 'Up'
                on_press: root.x_motor_up()
                on_release: root.quit_jog()
            Button: 
                text: 'Down'
                on_press: root.x_motor_down()
                on_release: root.quit_jog()

        GridLayout:
            size: self.parent.size
            pos: self.parent.pos
            cols: 2

            Label: 
                text: '  11. Z Home'
                color: 1,1,1,1
                text_size: self.size
                size: self.parent.size
                pos: self.parent.pos
                markup: 'True'
                halign: 'left'
                valign: 'middle'      

            Image:
                id: z_home_check
                source: "./asmcnc/skavaUI/img/checkbox_inactive.png"
                center_x: self.parent.center_x
                y: self.parent.y
                size: self.parent.width, self.parent.height
                allow_stretch: True

        Button: 
            id: test_fw_update
            text: '  16. Test FW Update'
            on_press: root.test_fw_update()
            text_size: self.size
            size: self.parent.size
            pos: self.parent.pos
            markup: 'True'
            halign: 'left'
            valign: 'middle'



# Row 5

        GridLayout:
            size: self.parent.size
            pos: self.parent.pos
            cols: 3

            Label: 
                text: ' 5. Z motors'
                color: 1,1,1,1
                text_size: self.size
                size: self.parent.size
                pos: self.parent.pos
                markup: 'True'
                halign: 'left'
                valign: 'middle'

            Button: 
                text: 'Up'
                on_press: root.z_motor_up()
                on_release: root.quit_jog()

            Button: 
                text: 'Down'
                on_press: root.z_motor_down()
                on_release: root.quit_jog()

        GridLayout:
            size: self.parent.size
            pos: self.parent.pos
            cols: 2

            Label: 
                text: '  12. Probe'
                color: 1,1,1,1
                text_size: self.size
                size: self.parent.size
                pos: self.parent.pos
                markup: 'True'
                halign: 'left'
                valign: 'middle'    

            Image:
                id: probe_check
                source: "./asmcnc/skavaUI/img/checkbox_inactive.png"
                center_x: self.parent.center_x
                y: self.parent.y
                size: self.parent.width, self.parent.height
                allow_stretch: True

        Button:
            text: '  17. EXIT'
            text_size: self.size
            size: self.parent.size
            pos: self.parent.pos
            markup: 'True'
            halign: 'left'
            valign: 'middle'
            on_press: root.exit()



# Row 6

        GridLayout:
            size: self.parent.size
            pos: self.parent.pos
            cols: 2

            ToggleButton: 
                id: spindle_toggle
                text: '  6. Spindle'
                text_size: self.size
                size: self.parent.size
                pos: self.parent.pos
                markup: 'True'
                halign: 'left'
                valign: 'middle'
                on_press: root.set_spindle()

            ToggleButton: 
                id: laser_toggle
                text: '  7. Laser'
                text_size: self.size
                size: self.parent.size
                pos: self.parent.pos
                markup: 'True'
                halign: 'left'
                valign: 'middle'
                on_press: root.set_laser()

        GridLayout:
            size: self.parent.size
            pos: self.parent.pos
            cols: 2

            Label: 
                text: '  13. Temp/Power'
                color: 1,1,1,1
                text_size: self.size
                size: self.parent.size
                pos: self.parent.pos
                markup: 'True'
                halign: 'left'
                valign: 'middle'

            Image:
                id: temp_voltage_power_check
                source: "./asmcnc/skavaUI/img/checkbox_inactive.png"
                center_x: self.parent.center_x
                y: self.parent.y
                size: self.parent.width, self.parent.height
                allow_stretch: True

	    ScrollableLabelStatus:
	        size_hint_y: 0.2        
	        id: consoleStatusText
	        text: "status update" 


""")

STATUS_UPDATE_DELAY = 0.4

class ScrollableLabelStatus(ScrollView):
    text = StringProperty('')

class ZHeadDiagnosticsScreen(Screen):

    def __init__(self, **kwargs):

        super(ZHeadDiagnosticsScreen, self).__init__(**kwargs)
        self.m=kwargs['machine']
        self.sm=kwargs['screen_manager']

        self.z_limit_set = False
        self.spindle_pass_fail = True
        self.string_overload_summary = ''
        self.spindle_test_counter = 0

    def on_enter(self, *args):
        self.string_overload_summary = ''
        self.scrape_fw_version()
        self.m.is_laser_enabled = True
        self.m.s.write_command('$21 = 0')
        self.poll_for_status = Clock.schedule_interval(self.update_status_text, STATUS_UPDATE_DELAY)      # Poll for status
        self.poll_for_limits = Clock.schedule_interval(self.update_checkboxes, STATUS_UPDATE_DELAY)      # Poll for limit switches being triggered
        self.poll_for_temps_power = Clock.schedule_interval(self.temp_power_check, STATUS_UPDATE_DELAY)      # Poll for status

    def on_leave(self, *args):
        Clock.unschedule(self.poll_for_status)
        Clock.unschedule(self.poll_for_limits)
        Clock.unschedule(self.poll_for_temps_power)
        self.m.s.write_command('$21 = 1')

    def scrape_fw_version(self):
        self.fw_version_label.text = str((str(self.m.s.fw_version)).split('; HW')[0])

    def bake_grbl_settings(self):
        grbl_settings = [
                    '$0=10',          #Step pulse, microseconds
                    '$1=255',         #Step idle delay, milliseconds
                    '$2=4',           #Step port invert, mask
                    '$3=1',           #Direction port invert, mask
                    '$4=0',           #Step enable invert, boolean
                    '$5=1',           #Limit pins invert, boolean
                    '$6=0',           #Probe pin invert, boolean
                    '$10=3',          #Status report, mask <----------------------
                    '$11=0.010',      #Junction deviation, mm
                    '$12=0.002',      #Arc tolerance, mm
                    '$13=0',          #Report inches, boolean
                    '$20=1',          #Soft limits, boolean <-------------------
                    # '$21=1',          #Hard limits, boolean <------------------
                    '$22=1',          #Homing cycle, boolean <------------------------
                    '$23=3',          #Homing dir invert, mask
                    '$24=600.0',      #Homing feed, mm/min
                    '$25=3000.0',     #Homing seek, mm/min
                    '$26=250',        #Homing debounce, milliseconds
                    '$27=15.000',     #Homing pull-off, mm
                    '$30=25000.0',    #Max spindle speed, RPM
                    '$31=0.0',        #Min spindle speed, RPM
                    '$32=0',          #Laser mode, boolean
                    # '$100=56.649',    #X steps/mm
                    # '$101=56.665',    #Y steps/mm
                    # '$102=1066.667',  #Z steps/mm
                    '$110=8000.0',    #X Max rate, mm/min
                    '$111=6000.0',    #Y Max rate, mm/min
                    '$112=750.0',     #Z Max rate, mm/min
                    '$120=130.0',     #X Acceleration, mm/sec^2
                    '$121=130.0',     #Y Acceleration, mm/sec^2
                    '$122=200.0',     #Z Acceleration, mm/sec^2
                    '$130=1300.0',    #X Max travel, mm TODO: Link to a settings object
                    '$131=2502.0',    #Y Max travel, mm
                    '$132=150.0',     #Z Max travel, mm
                    '$$',             # Echo grbl settings, which will be read by sw, and internal parameters sync'd
                    '$#'              # Echo grbl parameter info, which will be read by sw, and internal parameters sync'd
            ]

        self.m.s.start_sequential_stream(grbl_settings, reset_grbl_after_stream=True)   # Send any grbl specific parameters

    def home(self):
        self.m.is_machine_completed_the_initial_squaring_decision = True
        self.m.request_homing_procedure('z_head_diagnostics','z_head_diagnostics', False)

    def x_motor_up(self):
        self.m.jog_relative('X', 50, 6000)

    def x_motor_down(self):
        self.m.jog_relative('X', -50, 6000)

    def z_motor_up(self):
        self.m.jog_relative('Z', 20, 750)

    def z_motor_down(self):
        self.m.jog_relative('Z', -20, 750)

    def set_spindle(self):
        if self.spindle_toggle.state == 'normal': 
            self.m.spindle_off()
        else: 
            self.m.spindle_on()

    def set_laser(self):
        if self.laser_toggle.state == 'normal': 
            self.m.laser_off()
        else: 
            self.m.laser_on()

    def dust_shoe_red(self):
        self.m.set_led_colour('RED')

    def dust_shoe_green(self):
        self.m.set_led_colour('GREEN')

    def dust_shoe_blue(self):
        self.m.set_led_colour('BLUE')

    def update_checkboxes(self, dt):
        # self.dust_shoe_switch()
        self.x_home_switch()
        self.x_max_switch()
        self.z_home_switch()
        self.probe()

    # def dust_shoe_switch(self):
    #     if self.m.s.dust_shoe_cover:
    #         self.dust_shoe_check.source = "./asmcnc/skavaUI/img/file_select_select.png"
    #     else:
    #         self.dust_shoe_check.source = "./asmcnc/skavaUI/img/checkbox_inactive.png"

    def x_home_switch(self):
        if self.m.s.limit_x:
            self.x_home_check.source = "./asmcnc/skavaUI/img/file_select_select.png"
        else:
            self.x_home_check.source = "./asmcnc/skavaUI/img/checkbox_inactive.png"

    def x_max_switch(self):
        if self.m.s.limit_X:
            self.x_max_check.source = "./asmcnc/skavaUI/img/file_select_select.png"
        else:
            self.x_max_check.source = "./asmcnc/skavaUI/img/checkbox_inactive.png"

    def z_home_switch(self):
        if self.m.s.limit_z:
            self.z_home_check.source = "./asmcnc/skavaUI/img/file_select_select.png"
        else:
            self.z_home_check.source = "./asmcnc/skavaUI/img/checkbox_inactive.png"

    def probe(self):
        if self.m.s.probe:
            self.probe_check.source = "./asmcnc/skavaUI/img/file_select_select.png"
        else:
            self.probe_check.source = "./asmcnc/skavaUI/img/checkbox_inactive.png"


    def temp_power_check(self, dt):
        # pcb_temp
        # motor_driver_temp
        # microcontroller_mV 
        # LED_mV 
        # PSU_mV
        # ac_loss

        pass_fail = True
        fail_report = []

        # Poll for all the temperatures, voltages, and power loss pin reported from the FW 
        # If one of them fails, polling will stop and report will be triggered.

        if (self.m.s.pcb_temp > 10) and (self.m.s.pcb_temp < 50):
            self.temp_voltage_power_check.source = "./asmcnc/skavaUI/img/file_select_select.png"
            pass_fail = pass_fail*(True)
        else:
            self.temp_voltage_power_check.source = "./asmcnc/skavaUI/img/template_cancel.png"
            pass_fail = pass_fail*(False)
            fail_report.append("PCB Temperature: " + str(self.m.s.pcb_temp) + " degrees C")
            fail_report.append("Should be greater than 10 and less than 50 deg C.")

        if (self.m.s.motor_driver_temp > 10) and (self.m.s.motor_driver_temp < 50):
            self.temp_voltage_power_check.source = "./asmcnc/skavaUI/img/file_select_select.png"
            pass_fail = pass_fail*(True)
        else:
            self.temp_voltage_power_check.source = "./asmcnc/skavaUI/img/template_cancel.png"
            pass_fail = pass_fail*(False)
            fail_report.append("Motor Driver Temperature: " + str(self.m.s.motor_driver_temp) + " degrees C")
            fail_report.append("Should be greater than 10 and less than 50 deg C.")

        if (self.m.s.microcontroller_mV > 4800) and (self.m.s.microcontroller_mV < 5200):
            self.temp_voltage_power_check.source = "./asmcnc/skavaUI/img/file_select_select.png"
            pass_fail = pass_fail*(True)
        else:
            self.temp_voltage_power_check.source = "./asmcnc/skavaUI/img/template_cancel.png"
            pass_fail = pass_fail*(False)
            fail_report.append("Microcontroller voltage: " + str(self.m.s.microcontroller_mV) + " mV")
            fail_report.append("Should be greater than 4800 and less than 5200 mV.")

        if (self.m.s.LED_mV > 4800) and (self.m.s.LED_mV < 5200):
            self.temp_voltage_power_check.source = "./asmcnc/skavaUI/img/file_select_select.png"
            pass_fail = pass_fail*(True)
        else:
            self.temp_voltage_power_check.source = "./asmcnc/skavaUI/img/template_cancel.png"
            pass_fail = pass_fail*(False)
            fail_report.append("LED (dust shoe) voltage: " + str(self.m.s.LED_mV) + " mV")
            fail_report.append("Should be greater than 4800 and less than 5200 mV.")

        if (self.m.s.PSU_mV > 22000) and (self.m.s.PSU_mV < 26000):
            self.temp_voltage_power_check.source = "./asmcnc/skavaUI/img/file_select_select.png"
            pass_fail = pass_fail*(True)
        else:
            self.temp_voltage_power_check.source = "./asmcnc/skavaUI/img/template_cancel.png"
            pass_fail = pass_fail*(False)
            fail_report.append("24V PSU Voltage: " + str(self.m.s.PSU_mV) + " mV")
            fail_report.append("Should be greater than 22000 and less than 26000 mV.")

        if self.m.s.ac_loss == True:
            self.temp_voltage_power_check.source = "./asmcnc/skavaUI/img/file_select_select.png"
            pass_fail = pass_fail*(True)
        else:
            self.temp_voltage_power_check.source = "./asmcnc/skavaUI/img/template_cancel.png"
            pass_fail = pass_fail*(False)
            fail_report.append("AC Loss: " + str(self.m.s.ac_loss))
            fail_report.append("AC should be reported as lost (True) on diagnostics jig.")

        if pass_fail == 0:
            Clock.unschedule(self.poll_for_temps_power)
            fail_report_string = "\n".join(fail_report)
            popup_info.PopupTempPowerDiagnosticsInfo(self.sm, fail_report_string)

    def cycle_limit_switch(self):
        if self.m.s.limit_z:
            self.cycle_limit_check.source = "./asmcnc/skavaUI/img/file_select_select.png"
            self.z_limit_set = True
        else:
            self.cycle_limit_check.source = "./asmcnc/skavaUI/img/checkbox_inactive.png"        

    def stop(self):
        popup_info.PopupStop(self.m, self.sm)

    def quit_jog(self):
        self.m.quit_jog()

    def do_cycle(self):

        self.m.s.write_command('G53 G0 Z-150')
        self.m.s.write_command('G53 G0 Z-1')
        self.m.s.write_command('G53 G0 Z-150')
        self.m.s.write_command('G53 G0 Z-1')
        self.m.s.write_command('G53 G0 Z-150')
        self.m.s.write_command('G53 G0 Z-1')
        self.m.s.write_command('G53 G0 Z-150')
        self.m.s.write_command('G53 G0 Z-1')
        self.m.s.write_command('G53 G0 Z-150')
        self.m.s.write_command('G53 G0 Z-1')
        self.m.s.write_command('G53 G0 Z-150')
        self.m.s.write_command('G53 G0 Z-1')
        self.m.s.write_command('G53 G0 Z-150')
        self.m.s.write_command('G53 G0 Z-1')
        self.m.s.write_command('G53 G0 Z-150')
        self.m.s.write_command('G53 G0 Z-1')
        self.m.s.write_command('G53 G0 Z-150')
        self.m.s.write_command('G53 G0 Z-1')
        self.m.s.write_command('G53 G0 Z-150')
        self.m.s.write_command('G53 G0 Z-1')


    def run_spindle_check(self):
        
        # Send command:
        # 5000 RPM = 1.2 V
        self.spindle_check('M3 S5000', 2000, 2000)

        # 10000 RPM = 3.4 - 3.6 V 
        Clock.schedule_once(lambda dt: self.spindle_check('M3 S10000', 3900, 4000), 2.5)

        # 15000 RPM = 5.6 - 5.8 V
        Clock.schedule_once(lambda dt: self.spindle_check('M3 S15000', 5750, 6000), 5)

        # 20000 RPM = 7.8 V
        Clock.schedule_once(lambda dt: self.spindle_check('M3 S20000', 5750, 8000), 7.5)

        # # 250000 RPM = 10 V
        Clock.schedule_once(lambda dt: self.spindle_check('M3 S25000', 5750, 10000), 10)

        # Spindle off
        Clock.schedule_once(lambda dt: self.m.s.write_command('M5'), 12.5)


        def show_outcome():

            self.spindle_test_counter = 0

            if self.spindle_pass_fail == 0:
                self.spindle_speed_check.source = "./asmcnc/skavaUI/img/template_cancel.png"
                test = self.string_overload_summary.split("**")
                popup_info.PopupSpindleDiagnosticsInfo(self.sm, test[1], test[2], test[3])

            else: 
                self.spindle_speed_check.source = "./asmcnc/skavaUI/img/file_select_select.png"

            print self.spindle_pass_fail

            self.spindle_pass_fail = True


        Clock.schedule_once(lambda dt: show_outcome(), 13)


    def spindle_check(self, M3_command, ld_expected_mV, speed_expected_mV):

        self.spindle_test_counter = 1

        def overload_check(ld_mid_range_mV, speed_mid_range_mV):

            # 5000 RPM = 1.7V - 2.3V
            # 10000 RPM = 3.3V - 4.5V
            # 15000 RPM = 5.0V - 6.5V

            if ld_mid_range_mV == 2000: ld_tolerance = 300
            elif ld_mid_range_mV == 3900: ld_tolerance = 600
            elif ld_mid_range_mV == 5750: ld_tolerance = 750

            speed_V_tolerance = 0.2*speed_mid_range_mV

            if self.spindle_test_counter == 1:
                self.string_overload_summary = self.string_overload_summary + '\n' + 'Ld range: ' + str(ld_mid_range_mV - ld_tolerance) + "-" + str(ld_mid_range_mV + ld_tolerance)
                self.string_overload_summary = self.string_overload_summary + '\n' + 'V range: ' + str(speed_mid_range_mV - speed_V_tolerance) + "-" + str(speed_mid_range_mV + speed_V_tolerance)

            self.string_overload_summary = self.string_overload_summary + '\n' + "Test " + str(self.spindle_test_counter) + ": Ld: " + str(self.m.s.overload_pin_mV) + "|" + " V: " + str(self.m.s.spindle_speed_mV)

            self.is_it_within_tolerance(self.m.s.overload_pin_mV, ld_mid_range_mV, ld_tolerance)
            self.is_it_within_tolerance(self.m.s.spindle_speed_mV, speed_mid_range_mV, speed_V_tolerance)

            self.spindle_test_counter+=1

            # end of inner function

        Clock.schedule_once(lambda dt: self.m.s.write_command(M3_command), 0.1)

        self.string_overload_summary = self.string_overload_summary + "**" + str(M3_command).strip("M3 S") + " RPM"

        overload_check_event = Clock.schedule_interval(lambda dt: overload_check(expected_mV, speed_expected_mV), 0.5)

        Clock.schedule_once(lambda dt: Clock.unschedule(overload_check_event), 1.8)
        
    def is_it_within_tolerance(self, value, expected, tolerance):
        if (value >= expected - tolerance) and (value <= expected + tolerance): self.spindle_pass_fail = self.spindle_pass_fail*(True)
        else: self.spindle_pass_fail = self.spindle_pass_fail*(False)

    def test_fw_update(self):
        pass

    def exit(self):
        self.sm.current = 'lobby'

    def update_status_text(self, dt):
        self.consoleStatusText.text = self.sm.get_screen('home').gcode_monitor_widget.consoleStatusText.text
        
        
        
        
        