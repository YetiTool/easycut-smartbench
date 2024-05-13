"""
Created on 10 June 2020
@author: Letty
widget to hold laser datum setting buttons
"""
from kivy.lang import Builder
from kivy.uix.widget import Widget

from asmcnc.core_UI import scaling_utils
from asmcnc.core_UI.components.buttons.spindle_button import SpindleButton
from asmcnc.core_UI.components.buttons.vacuum_button import VacuumButton
from asmcnc.core_UI.popups import InfoPopup
from asmcnc.apps.maintenance_app import popup_maintenance

Builder.load_string(
    """

<LaserDatumButtons>
    
    vacuum_button_container:vacuum_button_container
    spindle_button_container: spindle_button_container
    reset_button: reset_button
    save_button: save_button
    save_button_image: save_button_image
    
    BoxLayout:
    
        size: self.parent.size
        pos: self.parent.pos
        orientation: 'vertical'
        padding:[dp(0.0125)*app.width, dp(0.0208333333333)*app.height]
        spacing:0.0208333333333*app.height
        
        GridLayout:
            cols: 2
            rows: 2
            spacing: 0
            size_hint_y: None
            height: self.width

            BoxLayout: 
                size: self.parent.size
                pos: self.parent.pos 
                id: vacuum_button_container
                padding: [dp(app.get_scaled_width(10)), dp(app.get_scaled_height(10))]

            BoxLayout: 
                size: self.parent.size
                pos: self.parent.pos 
                id: spindle_button_container
                padding: [dp(app.get_scaled_width(10)), dp(app.get_scaled_height(10))]

            BoxLayout: 
                size: self.parent.size
                pos: self.parent.pos 
                Button:
                    font_size: str(0.01875 * app.width) + 'sp'
                    id: reset_button
                    size_hint: (None,None)
                    height: dp(0.28125*app.height)
                    width: dp(0.165*app.width)
                    background_color: color_provider.get_rgba("transparent")
                    center: self.parent.center
                    pos: self.parent.pos
                    on_press: root.reset_button_press()
                    BoxLayout:
                        padding: 0
                        size: self.parent.size
                        pos: self.parent.pos
                        Image:
                            source: "./asmcnc/apps/maintenance_app/img/reset_button_132.png"
                            center_x: self.parent.center_x
                            y: self.parent.y
                            size: self.parent.width, self.parent.height
                            allow_stretch: True

            BoxLayout: 
                size: self.parent.size
                pos: self.parent.pos 
                Button:
                    font_size: str(0.01875 * app.width) + 'sp'
                    id: save_button
                    size_hint: (None,None)
                    height: dp(0.28125*app.height)
                    width: dp(0.165*app.width)
                    background_color: color_provider.get_rgba("transparent")
                    center: self.parent.center
                    pos: self.parent.pos
                    on_press: root.save_button_press()
                    disabled: True
                    BoxLayout:
                        padding: 0
                        size: self.parent.size
                        pos: self.parent.pos
                        Image:
                            id: save_button_image
                            source: "./asmcnc/apps/maintenance_app/img/save_button_132_greyscale.png"
                            center_x: self.parent.center_x
                            y: self.parent.y
                            size: self.parent.width, self.parent.height
                            allow_stretch: True


"""
)


class LaserDatumButtons(Widget):
    def __init__(self, **kwargs):
        super(LaserDatumButtons, self).__init__(**kwargs)
        self.m = kwargs["machine"]
        self.sm = kwargs["screen_manager"]
        self.l = kwargs["localization"]
        self.add_buttons()

    spindle_button = None
    vacuum_button = None

    def add_buttons(self):
        self.vacuum_button = VacuumButton(self.m, self.m.s, size_hint=(None, None),
                                          size=(scaling_utils.get_scaled_dp_width(120),
                                                scaling_utils.get_scaled_dp_height(120)),
                                          pos_hint={"center_x": 0.5, "center_y": 0.5})
        self.vacuum_button_container.add_widget(self.vacuum_button)

        self.spindle_button = SpindleButton(self.m, self.m.s, self.sm,
                                            size_hint=(None, None),
                                            size=(scaling_utils.get_scaled_dp_width(120),
                                                  scaling_utils.get_scaled_dp_height(122)),
                                            pos_hint={"center_x": 0.5, "center_y": 0.5})
        self.spindle_button_container.add_widget(self.spindle_button)

    def reset_button_press(self):
        popup_maintenance.PopupResetOffset(self.sm, self.l)

    def save_button_press(self):
        if self.m.is_laser_enabled == True:
            popup_maintenance.PopupSaveOffset(self.sm, self.l)

        else:
            main_string = (
                    self.l.get_str("Could not save laser crosshair offset!")
                    + "\n\n"
                    + self.l.get_str(
                "You need to line up the laser crosshair with the mark you made with the spindle (press (i) for help)."
            ).replace("(i)", "[b](i)[/b]")
                    + "\n\n"
                    + self.l.get_str("Please enable laser to set offset.")
            )
            self.sm.pm.show_error_popup(main_string)

    def reset_laser_offset(self):
        self.sm.get_screen(
            "maintenance"
        ).laser_datum_reset_coordinate_x = self.m.mpos_x()
        self.sm.get_screen(
            "maintenance"
        ).laser_datum_reset_coordinate_y = self.m.mpos_y()
        self.save_button_image.source = (
            "./asmcnc/apps/maintenance_app/img/save_button_132.png"
        )
        self.save_button.disabled = False

    def save_laser_offset(self):
        self.m.laser_offset_x_value = (
                self.sm.get_screen("maintenance").laser_datum_reset_coordinate_x
                - self.m.mpos_x()
        )
        self.m.laser_offset_y_value = (
                self.sm.get_screen("maintenance").laser_datum_reset_coordinate_y
                - self.m.mpos_y()
        )
        if self.m.write_z_head_laser_offset_values(
                "True", self.m.laser_offset_x_value, self.m.laser_offset_y_value
        ):
            saved_success = self.l.get_str("Settings saved!")
            self.sm.pm.show_mini_info_popup(saved_success)
            self.save_button_image.source = (
                "./asmcnc/apps/maintenance_app/img/save_button_132_greyscale.png"
            )
            self.save_button.disabled = True
        else:
            main_string = (
                    self.l.get_str("There was a problem saving your settings.")
                    + "\n\n"
                    + self.l.get_str(
                "Please check your settings and try again, or if the problem persists please contact the YetiTool support team."
            )
            )
            self.sm.pm.show_error_popup(main_string)
