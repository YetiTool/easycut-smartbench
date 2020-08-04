
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

Builder.load_string("""

<ZHeadDiagnosticsScreen>:

    fw_version_label: fw_version_label
    consoleStatusText: consoleStatusText
    dust_shoe_check: dust_shoe_check
    x_home_check: x_home_check
    x_max_check: x_max_check
    z_home_check: z_home_check
    probe_check: probe_check    

    GridLayout:
        size: self.parent.size
        pos: self.parent.pos
        cols: 3
        rows: 6
        cols_minimum: {0: 250, 1: 200, 2: 350}

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
            cols: 2

            Label: 
            	text: '  7. Dust shoe         switch'
            	color: 1,1,1,1
            	text_size: self.size
	            size: self.parent.size
	            pos: self.parent.pos
	            markup: 'True'
	            halign: 'left'
	            valign: 'middle'       

            Image:
            	id: dust_shoe_check
                source: "./asmcnc/skavaUI/img/checkbox_inactive.png"
                center_x: self.parent.center_x
                y: self.parent.y
                size: self.parent.width, self.parent.height
                allow_stretch: True

        GridLayout:
            size: self.parent.size
            pos: self.parent.pos
            cols: 2

            ToggleButton: 
                id: cycle_test
                text: '13. Z cycle test'

            Button:
                text: '  EXIT'
                text_size: self.size
                size: self.parent.size
                pos: self.parent.pos
                markup: 'True'
                halign: 'left'
                valign: 'middle'
                on_press: root.exit()


# Row 2

	    Button:
	    	text: '  2. Bake GRBL Settings'
        	text_size: self.size
            size: self.parent.size
            pos: self.parent.pos
            markup: 'True'
            halign: 'left'
            valign: 'middle'

        GridLayout:
            size: self.parent.size
            pos: self.parent.pos
            cols: 2

            Label: 
            	text: '  8. X Home'
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

        GridLayout:
            size: self.parent.size
            pos: self.parent.pos
            cols: 2

	        Label: 
	        	text: 'Drive Z to limit switch'
	        	color: 1,1,1,1
            	text_size: self.size
	            size: self.parent.size
	            pos: self.parent.pos
	            markup: 'True'
	            halign: 'left'
	            valign: 'middle'

	        Button: 
	        	text: 'Up'

# Row 3


        GridLayout:
            size: self.parent.size
            pos: self.parent.pos
            cols: 3

            Label: 
            	text: '  3. X motors'
            	color: 1,1,1,1

            Button: 
            	text: 'Up'
            Button: 
            	text: 'Down'

        GridLayout:
            size: self.parent.size
            pos: self.parent.pos
            cols: 2

            Label: 
            	text: '  9. X Max'
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

            Label: 
            	text: 'Z limit'
            	color: 1,1,1,1          

            Image:
            	id: cycle_limit_check
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
            	text: '  4. Z motors'
            	color: 1,1,1,1
	            text_size: self.size
	            size: self.parent.size
	            pos: self.parent.pos
	            markup: 'True'
	            halign: 'left'
	            valign: 'middle'

            Button: 
            	text: 'Up'
            Button: 
            	text: 'Down'

        GridLayout:
            size: self.parent.size
            pos: self.parent.pos
            cols: 2

            Label: 
            	text: '  10. Z Home'
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

        GridLayout:
            size: self.parent.size
            pos: self.parent.pos
            cols: 2
	
	        Label: 
	        	text: 'Drive Z off limit switch'
	        	color: 1,1,1,1
            	text_size: self.size
	            size: self.parent.size
	            pos: self.parent.pos
	            markup: 'True'
	            halign: 'left'
	            valign: 'middle'

	        Button: 
	        	text: 'Down'
# Row 5

        ToggleButton: 
            id: spindle_toggle
            text: '  5. Spindle'
            text_size: self.size
            size: self.parent.size
            pos: self.parent.pos
            markup: 'True'
            halign: 'left'
            valign: 'middle'

        GridLayout:
            size: self.parent.size
            pos: self.parent.pos
            cols: 2

            Label: 
            	text: '  11. Probe'
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

        ToggleButton: 
            id: do_cycle
            text: 'Cycle'

# Row 6

        GridLayout:
            size: self.parent.size
            pos: self.parent.pos
            cols: 4

            Label: 
            	text: '  6. Dust Shoe'
            	color: 1,1,1,1
                text_size: self.size
                size: self.parent.size
                pos: self.parent.pos
                markup: 'True'
                halign: 'center'
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
                
        ToggleButton: 
            id: laser_toggle
            text: '  12. Laser'
        	text_size: self.size
            size: self.parent.size
            pos: self.parent.pos
            markup: 'True'
            halign: 'left'
            valign: 'middle'

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

    def on_enter(self, *args):
        self.scrape_fw_version()
        self.m.s.suppress_error_screens = True
        self.m.s.suppress_alarm_screens = True
        self.m.s.suppress_door_screens = True
        self.poll_for_status = Clock.schedule_interval(self.update_status_text, STATUS_UPDATE_DELAY)      # Poll for status
        self.poll_for_checks = Clock.schedule_interval(self.update_checkboxes, STATUS_UPDATE_DELAY)      # Poll for status


    def on_leave(self, *args):
        Clock.unschedule(self.poll_for_status)
        Clock.unschedule(self.poll_for_checks)
        self.m.s.suppress_error_screens = False
        self.m.s.suppress_alarm_screens = False
        self.m.s.suppress_door_screens = False

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
                    '$21=1',          #Hard limits, boolean <------------------
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

    def x_motor_up(self):
        self.m.s.write_command('G0 X50')

    def x_motor_down(self):
        self.m.s.write_command('G0 X-50')

    def z_motor_up(self):
        pass

    def z_motor_down(self):
        pass

    def set_spindle(self):
        if self.spindle_toggle.state == 'normal': 
            self.m.spindle_off()
        else: 
            self.m.spindle_on()

    def dust_shoe_red(self):
        self.m.set_led_colour('RED')

    def dust_shoe_green(self):
        self.m.set_led_colour('GREEN')

    def dust_shoe_blue(self):
        self.m.set_led_colour('BLUE')

    def update_checkboxes(self, dt):
        self.dust_shoe_switch()
        self.x_home_switch()
        self.x_max_switch()
        self.z_home_switch()
        self.probe()

    def dust_shoe_switch(self):
        if self.m.s.dust_shoe_cover:
            self.dust_shoe_check.source = "./asmcnc/skavaUI/img/file_select_select.png"
        else:
            self.dust_shoe_check.source = "./asmcnc/skavaUI/img/checkbox_inactive.png"

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

    def set_laser(self):
        if self.spindle_toggle.state == 'normal': 
            self.m.laser_off()
        else: 
            self.m.laser_on()

    def cycle_test(self):
        pass

    def exit(self):
        self.sm.current = 'lobby'

    def do_cycle(self):
        pass

    def update_status_text(self, dt):
        self.consoleStatusText.text = self.sm.get_screen('home').gcode_monitor_widget.consoleStatusText.text











