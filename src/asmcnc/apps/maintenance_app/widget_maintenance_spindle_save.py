'''
Created on 19 August 2020
@author: Letty
widget to hold brush maintenance save and info
'''

import kivy
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget

from asmcnc.apps.maintenance_app import popup_maintenance
from asmcnc.skavaUI import popup_info

Builder.load_string("""

<SpindleSaveWidget>

    BoxLayout:
        pos: self.parent.pos
        size: self.parent.size
        orientation: 'vertical'

        BoxLayout:
            padding: [dp(50), dp(30)]
	        Button:
	            on_press: root.get_info()
	            background_color: [0,0,0,0]
	            BoxLayout:
                    size: self.parent.size
	                pos: self.parent.pos
	                Image:
	                    source: "./asmcnc/apps/shapeCutter_app/img/info_icon.png"
	                    center_x: self.parent.center_x
	                    y: self.parent.y
	                    size: self.parent.width, self.parent.height
	                    allow_stretch: True

        BoxLayout:
            size_hint_y: 1.2
            padding: [dp(20), dp(10)]
            Button:
                on_press: root.save()
                background_color: [0,0,0,0]
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

""")

class SpindleSaveWidget(Widget):

    def __init__(self, **kwargs):
    
        super(SpindleSaveWidget, self).__init__(**kwargs)
        self.sm=kwargs['screen_manager']
        self.m=kwargs['machine']
        self.l=kwargs['localization']

    def get_info(self):
        popup_maintenance.PopupSpindleSettingsInfo(self.sm, self.l)

    def save(self):

        try: 
            [brand, digital, voltage] = (self.sm.get_screen('maintenance').spindle_settings_widget.spindle_brand.text).rsplit(' ', 2)

            brand = brand[1:]
            voltage = voltage.strip('V')

            if 'digital' in digital: digital = True
            elif 'manual' in digital: digital = False
            else:
                brand_validation_error = (
                        self.l.get_str("Please select a valid spindle brand from the drop down.") + \
                        "\n\n" + \
                        self.l.get_str("If you can't find what you're looking for, please enter the version with a voltage and digital/manual option that matches what you have.")
                    )

                popup_info.PopupError(self.sm, self.l, brand_validation_error)
                return

        except:
            brand_validation_error = (
                    self.l.get_str("Please select a valid spindle brand from the drop down.") + \
                    "\n\n" + \
                    self.l.get_str("If you can't find what you're looking for, please enter the version with a voltage and digital/manual option that matches what you have.")
                )

            popup_info.PopupError(self.sm, self.l, brand_validation_error)
            return               




        try: 

            time = int(self.sm.get_screen('maintenance').spindle_settings_widget.cooldown_time_slider.value)

            if (time >= 1 and time <= 60):
                pass

            else:
                time_validation_error = (
                        self.l.get_str("The spindle cooldown time should be between 1 and 60 seconds.") + \
                        "\n\n" + \
                        self.l.get_str("Please enter a new value.")
                    )

                popup_info.PopupError(self.sm, self.l, time_validation_error)
                return

        except: 

            time_validation_error = (
                    self.l.get_str("The spindle cooldown time should be a number between 1 and 60 seconds.") + \
                    "\n\n" + \
                    self.l.get_str("Please enter a new value.")
                )

            popup_info.PopupError(self.sm, self.l, time_validation_error)
            return



        try: 

            speed = int(self.sm.get_screen('maintenance').spindle_settings_widget.cooldown_speed_slider.value)

            if (speed >= 10000 and speed <= 20000):
                pass

            else:
                speed_validation_error = (
                        self.l.get_str("The spindle cooldown speed should be between 10,000 and 20,000 RPM.") + \
                        "\n\n" + \
                        self.l.get_str("Please enter a new value.")
                    )

                popup_info.PopupError(self.sm, self.l, speed_validation_error)
                return

        except:
            speed_validation_error = (
                    self.l.get_str("The spindle cooldown speed should be a number between 10,000 and 20,000 RPM.") + \
                    "\n\n" + \
                    self.l.get_str("Please enter a new value.")
                )

            popup_info.PopupError(self.sm, self.l, speed_validation_error)
            return

        if self.m.write_spindle_cooldown_rpm_override_settings(self.sm.current_screen.spindle_settings_widget.rpm_override) and \
            self.m.write_spindle_cooldown_settings(brand, voltage, digital, time, speed) and \
            self.m.write_stylus_settings(self.sm.current_screen.spindle_settings_widget.stylus_switch.active):

            if self.m.is_machines_fw_version_equal_to_or_greater_than_version('2.2.8', 'Set $51 based on selected spindle'):
                if "SC2" in brand:
                    self.m.write_dollar_setting(51, 1)
                    self.sm.current_screen.spindle_settings_widget.show_spindle_data_container()
                else:
                    self.m.write_dollar_setting(51, 0)
                    self.sm.current_screen.spindle_settings_widget.hide_spindle_data_container()

            saved_success = self.l.get_str("Settings saved!")
            popup_info.PopupMiniInfo(self.sm, self.l, saved_success)

        else:
            warning_message = (
                    self.l.get_str("There was a problem saving your settings.") + \
                    "\n\n" + \
                    self.l.get_str("Please check your settings and try again, or if the problem persists please contact the YetiTool support team.")
                )

            popup_info.PopupError(self.sm, self.l, warning_message)

        if voltage == '110': # localize me!
            spindle_voltage_info = (
                    self.l.get_str("When using a 110V spindle as part of your SmartBench, please be aware of the following:") + \
                    "\n\n" + \
                    self.l.get_str("110V spindles have a minimum speed of ~10,000 RPM.") + \
                    "\n\n" + \
                    self.l.get_str("SmartBench electronics are set up to work with a 230V spindle, so our software does a smart conversion to make sure the machine code we send is adjusted to control a 110V spindle.") + \
                    "\n\n" + \
                    self.l.get_str("The 5% spindle speed adjustments in the Job Screen cannot be converted for a 110V spindle, so they will not be able to adjust the speed by exactly 5%.") + \
                    " " + \
                    self.l.get_str("You will still be able to use the real time spindle speed feedback feature to assist your adjustment.")
                )
            
            popup_info.PopupInfo(self.sm, self.l, 780, spindle_voltage_info)

        # brands = ['YETI digital 230V', 'YETI digital 110V', 'AMB digital 230V', 'AMB manual 230V', 'AMB manual 110V']


    # spindle_brand = 'YETI' # String to hold brand name
    # spindle_voltage = 230 # Options are 230V or 110V
    # spindle_digital = False #spindle can be manual or digital
    # spindle_cooldown_time_seconds = 10 # YETI value is 10 seconds
    # spindle_cooldown_rpm = 12000 # YETI value was 20k, but has been lowered to 12k


# Mafell (YETI) - digital or manual; each one of those 110 or 230V - 4 variants total.

# AMB - 110V or 230V manual, 230V digital


















