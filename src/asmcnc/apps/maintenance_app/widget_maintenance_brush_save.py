'''
Created on 19 August 2020
@author: Letty
widget to hold brush maintenance save and info
'''

import kivy
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget
from kivy.clock import Clock

from asmcnc.apps.maintenance_app import popup_maintenance
from asmcnc.skavaUI import popup_info

Builder.load_string("""

<BrushSaveWidget>

    BoxLayout:
        size_hint: (None, None)
        height: dp(250)
        width: dp(160)
        pos: self.parent.pos
        orientation: 'vertical'

        BoxLayout: 
	        size_hint: (None, None)
	        height: dp(140)
	        width: dp(160)
            padding: [22,20,18,0]
            ToggleButton:
                id: save_button
                on_press: root.save()
                size_hint: (None,None)
                height: dp(120)
                width: dp(120)
                background_color: [0,0,0,0]
                center: self.parent.center
                pos: self.parent.pos
                BoxLayout:
                    size: self.parent.size
                    pos: self.parent.pos
                    Image:
                        id: save_image
                        source: "./asmcnc/apps/maintenance_app/img/save_button_132.png"
                        center_x: self.parent.center_x
                        y: self.parent.y
                        size: self.parent.width, self.parent.height
                        allow_stretch: True

        BoxLayout: 
	        size_hint: (None, None)
	        height: dp(110)
	        width: dp(160)
            padding: [50,0,50,27]
	        Button:
	            background_color: hex('#F4433600')
	            on_press: root.get_info()
	            BoxLayout:
	                size_hint: (None,None)
	                height: dp(60)
	                width: dp(60)
	                pos: self.parent.pos
	                Image:
	                    source: "./asmcnc/apps/shapeCutter_app/img/info_icon.png"
	                    center_x: self.parent.center_x
	                    y: self.parent.y
	                    size: self.parent.width, self.parent.height
	                    allow_stretch: True

""")

class BrushSaveWidget(Widget):

    def __init__(self, **kwargs):
    
        super(BrushSaveWidget, self).__init__(**kwargs)
        self.sm=kwargs['screen_manager']
        self.m=kwargs['machine']
        self.l=kwargs['localization']

    def get_info(self):

        popup_maintenance.PopupBrushInfo(self.sm, self.l)

    def save(self):

        # Machine must be idle if a spindle brush reset is attempted
        if not self.m.state().startswith('Idle'):
            popup_info.PopupError(self.sm, self.l, self.l.get_str("There was a problem saving your settings."))
            return

        # TIME FOR DATA VALIDATION

        # Read from screen
        use_str = self.sm.get_screen('maintenance').brush_use_widget.brush_use.text
        lifetime_str = self.sm.get_screen('maintenance').brush_life_widget.brush_life.text

        try:
            #  Convert hours into seconds
            use = float(use_str) * 3600
            lifetime = float(lifetime_str) * 3600

            # Brush use
            if use >= 0 and use <= 999*3600: pass # all good, carry on
            else: 
                # throw popup, return without saving
                brush_use_validation_error = (
                        self.l.get_str("The number of hours the brushes have been used for should be between 0 and 999.") + \
                        "\n\n" + \
                        self.l.get_str("Please enter a new value.")
                    )

                popup_info.PopupError(self.sm, self.l, brush_use_validation_error)
                return


            # Brush life
            if lifetime >= 100*3600 and lifetime <= 999*3600: pass # all good, carry on
            else: 
                # throw popup, return without saving
                brush_life_validation_error = (
                        self.l.get_str("The maximum brush lifetime should be between 100 and 999 hours.") + \
                        "\n\n" + \
                        self.l.get_str("Please enter a new value.")
                    )

                popup_info.PopupError(self.sm, self.l, brush_life_validation_error)
                return

            # Check use <= lifetime
            if use <= lifetime: pass # all good, carry on
            else: 
                # throw popup, return without saving
                brush_both_validation_error = (
                        self.l.get_str("The brush use hours should be less than or equal to the lifetime!") + \
                        "\n\n" + \
                        self.l.get_str("Please check your values.")
                    )

                popup_info.PopupError(self.sm, self.l, brush_both_validation_error)
                return


            # Store into variable that is accessible from functions called by clock, after reset is performed
            self.use = use
            self.lifetime = lifetime

            try:
                if self.m.s.setting_51 and use == 0:
                    # SC2 should not save spindle brush use, so write old value
                    self.use = self.m.spindle_brush_use_seconds
                    self.reset_brush_time()
                    # New values written after reset if it is successful, so stop here
                    return
            except:
                pass

            # If not SC2, then just write values as is
            self.write_new_values()

        except:
            # throw popup, return without saving
            warning_message = (
                    self.l.get_str("There was a problem saving your settings.") + \
                    "\n\n" + \
                    self.l.get_str("Please check your settings and try again, or if the problem persists please contact the YetiTool support team.")
                )
            popup_info.PopupError(self.sm, self.l, warning_message)
            return

    def write_new_values(self):
    
        # write new values to file
        if self.m.write_spindle_brush_values(self.use, self.lifetime):

            saved_success = self.l.get_str("Settings saved!")
            popup_info.PopupMiniInfo(self.sm, self.l, saved_success)

        else:
            warning_message = (
                    self.l.get_str("There was a problem saving your settings.") + \
                    "\n\n" + \
                    self.l.get_str("Please check your settings and try again, or if the problem persists please contact the YetiTool support team.")
                )
            popup_info.PopupError(self.sm, self.l, warning_message)

        # Update the monitor :)
        self.sm.get_screen('maintenance').brush_monitor_widget.update_percentage()

    def reset_brush_time(self):
        self.wait_popup = popup_info.PopupWait(self.sm, self.l)
        self.m.s.write_command('M3 S0')
        self.brush_reset_test_count = 0
        self.attempt_reset()

    def attempt_reset(self):
        def do_reset(dt):
            self.m.s.write_protocol(self.m.p.ResetDigitalSpindleBrushTime(), "RESET DIGITAL SPINDLE BRUSH TIME")
            Clock.schedule_once(read_info, 3)

        def read_info(dt):
            self.m.s.write_protocol(self.m.p.GetDigitalSpindleInfo(), "GET DIGITAL SPINDLE INFO")
            self.check_info_count = 0
            Clock.schedule_once(wait_for_successful_read, 0.3)

        def wait_for_successful_read(dt):
            self.check_info_count += 1
            # Value of -999 represents disconnected spindle - if detected then stop waiting
            if (self.m.s.digital_spindle_ld_qdA != -999) or (self.check_info_count > 10):
                check_info()
            else: # Keep trying for a few seconds
                Clock.schedule_once(wait_for_successful_read, 0.3)

        def check_info():
            # Value of -999 represents disconnected spindle
            if self.m.s.digital_spindle_ld_qdA == -999:
                self.m.s.write_command('M5')
                self.wait_popup.popup.dismiss()
                popup_info.PopupError(self.sm, self.l, self.l.get_str("Error!"))
            elif self.m.s.spindle_brush_run_time_seconds != 0:
                if self.brush_reset_test_count == 5:
                    self.m.s.write_command('M5')
                    self.wait_popup.popup.dismiss()
                    popup_info.PopupError(self.sm, self.l, self.l.get_str("There was a problem saving your settings."))
                else:
                    self.attempt_reset()
            else:
                self.m.s.write_command('M5')
                self.wait_popup.popup.dismiss()
                self.write_new_values()

        self.brush_reset_test_count += 1

        Clock.schedule_once(do_reset, 0.1)
