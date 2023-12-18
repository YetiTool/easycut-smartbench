"""
Popups that aren't covered by the default popup system.
"""
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.carousel import Carousel
from kivy.uix.checkbox import CheckBox
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget

from asmcnc.core_UI.scaling_utils import (
    get_scaled_height,
    get_scaled_width,
    get_scaled_sp,
    get_scaled_tuple,
)


class PopupBrushInfo(Widget):
    # This is not elegant.

    def __init__(self, screen_manager, localization, **kwargs):
        super(PopupBrushInfo, self).__init__(**kwargs)
        self.sm = screen_manager
        self.l = localization

        _12_sp = get_scaled_sp("12sp")
        default_font_size = get_scaled_sp("15sp")

        # do this as a grid layout instead
        description_top = (
                self.l.get_bold("Brush use:")
                + "\n"
                + "  "
                + self.l.get_bold("Value:")
                + " "
                + self.l.get_str("The running hours of the brushes.")
                + "\n"
                + "  "
                + self.l.get_bold("Restore:")
                + " "
                + self.l.get_str("Return to the hours previously logged.")
                + "\n"
                + "  "
                + self.l.get_bold("Reset:")
                + " "
                + self.l.get_str("Set the running hours to zero.")
        )

        description_bottom = (
                self.l.get_bold("Brush reminder:")
                + "\n"
                + "  "
                + self.l.get_bold("Value:")
                + " "
                + self.l.get_str("Set to the hours the brushes are expected to last.")
                + "\n"
                + "  "
                + self.l.get_str(
            "This will vary depending on heavy use (~120 hours) or light use (~500 hours)."
        )
                + "\n"
                + "  "
                + self.l.get_str(
            "It is best to set to worst case, inspect the brushes, and update as necessary."
        )
                + "\n"
                + "  "
                + self.l.get_bold("Restore:")
                + " "
                + self.l.get_str("Return the brush reminder to the hours previously set.")
                + "\n"
                + "  "
                + self.l.get_bold("Reset:")
                + " "
                + self.l.get_str("Sets the brush reminder to 120 hours.")
        )

        title_string = self.l.get_str("Information")
        img = Image(
            source="./asmcnc/apps/shapeCutter_app/img/info_icon.png",
            allow_stretch=False,
        )
        label_top = Label(
            size_hint_y=1,
            text_size=(get_scaled_width(476), get_scaled_height(self.height)),
            markup=True,
            halign="left",
            valign="bottom",
            text=description_top,
            color=[0, 0, 0, 1],
            padding=[0, 0],
            width=get_scaled_width(476),
            font_size=default_font_size,
        )
        label_blank = Label(
            size_hint_y=0.1,
            text_size=(get_scaled_width(476), get_scaled_height(self.height)),
            markup=True,
            halign="left",
            valign="bottom",
            text="",
            color=[0, 0, 0, 1],
            padding=[0, 0],
            width=get_scaled_width(476),
            font_size=default_font_size,
        )
        label_bottom = Label(
            text_size=(get_scaled_width(760), None),
            markup=True,
            halign="left",
            valign="top",
            text=description_bottom,
            color=[0, 0, 0, 1],
            padding=[0, 0],
            width=get_scaled_width(760),
            font_size=default_font_size,
        )

        img_full_brush = Image(
            source="./asmcnc/apps/maintenance_app/img/brush_long_img.png",
            allow_stretch=False,
            size=(get_scaled_width(68), get_scaled_height(99)),
        )
        label_full_brush_top = Label(
            text=self.l.get_bold("NEW"),
            text_size=(get_scaled_width(68), get_scaled_height(self.height)),
            size_hint_y=0.1,
            font_size=_12_sp,
            markup=True,
            halign="left",
            valign="middle",
            color=[0, 0, 0, 1],
            padding=[0, 0],
            width=img_full_brush.width,
        )
        label_full_brush_length = Label(
            text="[b]16mm[/b]",
            text_size=(get_scaled_width(70), get_scaled_height(self.height)),
            size_hint_y=0.1,
            font_size=_12_sp,
            markup=True,
            halign="left",
            valign="middle",
            color=[0, 0, 0, 1],
            padding=[0, 0],
            width=img_full_brush.width,
        )
        label_full_brush_tolerance = Label(
            text="[b](+/-0.2mm)[/b]",
            text_size=(get_scaled_width(70), get_scaled_height(self.height)),
            size_hint_y=0.1,
            font_size=_12_sp,
            markup=True,
            halign="left",
            valign="middle",
            color=[0, 0, 0, 1],
            padding=[0, 0],
            width=img_full_brush.width,
        )

        example_full_length = BoxLayout(
            orientation="vertical",
            padding=0,
            spacing=get_scaled_tuple((5, 5)),
            size_hint_x=None,
            width=get_scaled_width(68),
        )
        example_full_length.add_widget(label_full_brush_top)
        example_full_length.add_widget(img_full_brush)
        example_full_length.add_widget(label_full_brush_length)
        example_full_length.add_widget(label_full_brush_tolerance)

        img_med_brush = Image(
            source="./asmcnc/apps/maintenance_app/img/brush_med_img.png",
            allow_stretch=False,
            size=(get_scaled_width(68), get_scaled_height(99)),
        )
        label_med_brush_top = Label(
            text=self.l.get_bold("LOW"),
            text_size=(get_scaled_width(68), get_scaled_height(self.height)),
            size_hint_y=0.1,
            font_size=_12_sp,
            markup=True,
            halign="left",
            valign="middle",
            color=[0, 0, 0, 1],
            padding=[0, 0],
            width=get_scaled_width(68),
        )
        label_med_brush_length = Label(
            text="[b]10mm[/b]",
            text_size=(get_scaled_width(70), get_scaled_height(self.height)),
            size_hint_y=0.1,
            font_size=_12_sp,
            markup=True,
            halign="left",
            valign="middle",
            color=[0, 0, 0, 1],
            padding=[0, 0],
            width=get_scaled_width(68),
        )
        label_med_brush_tolerance = Label(
            text="[b](+/-0.2mm)[/b]",
            text_size=(get_scaled_width(70), get_scaled_height(self.height)),
            size_hint_y=0.1,
            font_size=_12_sp,
            markup=True,
            halign="left",
            valign="middle",
            color=[0, 0, 0, 1],
            padding=[0, 0],
            width=get_scaled_width(68),
        )

        example_med_length = BoxLayout(
            orientation="vertical",
            padding=0,
            spacing=get_scaled_tuple((5, 5)),
            size_hint_x=None,
            width=get_scaled_width(68),
        )
        example_med_length.add_widget(label_med_brush_top)
        example_med_length.add_widget(img_med_brush)
        example_med_length.add_widget(label_med_brush_length)
        example_med_length.add_widget(label_med_brush_tolerance)

        img_short_brush = Image(
            source="./asmcnc/apps/maintenance_app/img/brush_short_img.png",
            allow_stretch=False,
            size=(get_scaled_width(68), get_scaled_height(99)),
        )
        label_short_brush_top = Label(
            text=self.l.get_bold("SHUT-OFF"),
            text_size=(get_scaled_width(88), get_scaled_height(self.height)),
            size_hint_y=0.1,
            font_size=_12_sp,
            markup=True,
            halign="left",
            valign="middle",
            color=[0, 0, 0, 1],
            padding=[0, 0],
            width=get_scaled_width(88),
        )
        label_short_brush_length = Label(
            text="[b]9.5mm[/b]",
            text_size=(get_scaled_width(70), get_scaled_height(self.height)),
            size_hint_y=0.1,
            font_size=_12_sp,
            markup=True,
            halign="left",
            valign="middle",
            color=[0, 0, 0, 1],
            padding=[0, 0],
            width=get_scaled_width(68),
        )
        label_short_brush_tolerance = Label(
            text="[b](+/-0.2mm)[/b]",
            text_size=(get_scaled_width(70), get_scaled_height(self.height)),
            size_hint_y=0.1,
            font_size=_12_sp,
            markup=True,
            halign="left",
            valign="middle",
            color=[0, 0, 0, 1],
            padding=[0, 0],
            width=get_scaled_width(68),
        )

        example_short_length = BoxLayout(
            orientation="vertical",
            padding=0,
            spacing=get_scaled_tuple((5, 5)),
            size_hint_x=None,
            width=get_scaled_width(80),
        )
        example_short_length.add_widget(label_short_brush_top)
        example_short_length.add_widget(img_short_brush)
        example_short_length.add_widget(label_short_brush_length)
        example_short_length.add_widget(label_short_brush_tolerance)

        ok_button = Button(text="[b]Ok[/b]", markup=True, font_size=default_font_size)
        ok_button.background_normal = ""
        ok_button.background_color = [76 / 255.0, 175 / 255.0, 80 / 255.0, 1.0]

        examples_layout = BoxLayout(
            orientation="horizontal",
            padding=get_scaled_tuple((0, 0, 20, 0)),
            spacing=get_scaled_tuple((20, 20)),
            size_hint_x=None,
            width=get_scaled_width(284),
        )
        examples_layout.add_widget(example_full_length)
        examples_layout.add_widget(example_med_length)
        examples_layout.add_widget(example_short_length)

        label_cheat = BoxLayout(
            orientation="vertical",
            padding=0,
            spacing=get_scaled_tuple((5, 5)),
            size_hint_x=None,
            width=get_scaled_width(476),
        )
        label_cheat.add_widget(label_blank)
        label_cheat.add_widget(label_top)

        btn_layout = BoxLayout(
            orientation="horizontal",
            padding=get_scaled_tuple((150, 0, 150, 0)),
            size_hint_y=0.9,
        )
        btn_layout.add_widget(ok_button)

        use_layout = BoxLayout(
            orientation="horizontal",
            spacing=0,
            padding=0,
            size_hint_y=2,
            size_hint_x=None,
            width=get_scaled_width(760),
        )
        use_layout.add_widget(label_cheat)
        use_layout.add_widget(examples_layout)

        reminder_layout = BoxLayout(
            orientation="horizontal",
            spacing=0,
            padding=0,
            size_hint_y=2.5,
            size_hint_x=None,
            width=get_scaled_width(760),
        )
        reminder_layout.add_widget(label_bottom)

        layout_plan = BoxLayout(
            orientation="vertical",
            spacing=0,
            padding=[0, 0, 0, 0],
            width=get_scaled_width(780),
        )
        layout_plan.add_widget(img)
        layout_plan.add_widget(use_layout)
        layout_plan.add_widget(reminder_layout)
        layout_plan.add_widget(btn_layout)

        popup = Popup(
            title=title_string,
            title_color=[0, 0, 0, 1],
            title_size=get_scaled_sp("20sp"),
            content=layout_plan,
            size_hint=(None, None),
            size=get_scaled_tuple((780, 460)),
            auto_dismiss=False,
        )

        popup.background = "./asmcnc/apps/shapeCutter_app/img/popup_background.png"
        popup.separator_color = [249 / 255.0, 206 / 255.0, 29 / 255.0, 1.0]
        popup.separator_height = str(get_scaled_height(4)) + "dp"

        ok_button.bind(on_press=popup.dismiss)

        popup.open()


class PopupDisplaySpindleData(Widget):
    def __init__(self, screen_manager, localization, serial, **kwargs):
        super(PopupDisplaySpindleData, self).__init__(**kwargs)
        self.sm = screen_manager
        self.l = localization
        self.s = serial
        default_font_size = get_scaled_sp("15sp")

        category_string = (
                self.l.get_str("Spindle serial number")
                + "\n\n"
                + self.l.get_str("Production year")
                + "\n\n"
                + self.l.get_str("Production week")
                + "\n\n"
                + self.l.get_str("Firmware version")
                + "\n\n"
                + self.l.get_str("Total runtime")
                + "\n\n"
                + self.l.get_str("Brush runtime since last reset")
                + "\n\n"
                + self.l.get_str("Mains frequency")
        )

        value_string = (
                str(self.s.spindle_serial_number)
                + "\n\n"
                + str(self.s.spindle_production_year)
                + "\n\n"
                + str(self.s.spindle_production_week)
                + "\n\n"
                + str(self.s.spindle_firmware_version)
                + "\n\n"
                + str(self.s.spindle_total_run_time_seconds / 3600)
                + " "
                + self.l.get_str("hours")
                + "\n\n"
                + str(self.s.spindle_brush_run_time_seconds / 3600)
                + " "
                + self.l.get_str("hours")
                + "\n\n"
                + str(self.s.spindle_mains_frequency_hertz)
        )

        title_string = self.l.get_str("SC2 Spindle data")
        ok_string = self.l.get_bold("Ok")

        img = Image(
            size_hint_y=0.5,
            source="./asmcnc/apps/shapeCutter_app/img/info_icon.png",
            allow_stretch=False,
        )

        category_label = Label(
            text_size=get_scaled_tuple((250, None)),
            halign="left",
            valign="middle",
            text=category_string,
            color=(0, 0, 0, 1),
            padding=(0, 0),
            markup=True,
            bold=True,
            font_size=default_font_size
        )
        value_label = Label(
            text_size=get_scaled_tuple((250, None)),
            halign="right",
            valign="middle",
            text=value_string,
            color=(0, 0, 0, 1),
            padding=(0, 0),
            markup=True,
            font_size=default_font_size
        )

        label_layout = BoxLayout(
            orientation="horizontal", size_hint_y=2, padding=get_scaled_tuple((75, 0))
        )
        label_layout.add_widget(category_label)
        label_layout.add_widget(value_label)

        ok_button = Button(text=ok_string, markup=True, font_size=default_font_size)
        ok_button.background_normal = ""
        ok_button.background_color = [76 / 255.0, 175 / 255.0, 80 / 255.0, 1.0]

        btn_layout = BoxLayout(
            orientation="horizontal",
            spacing=get_scaled_tuple((100, 100)),
            padding=get_scaled_tuple((200, 10, 200, 0)),
            size_hint_y=0.6,
        )
        btn_layout.add_widget(ok_button)

        layout_plan = BoxLayout(
            orientation="vertical",
            spacing=get_scaled_tuple((10, 10)),
            padding=get_scaled_tuple((10, 20, 10, 10)),
        )
        layout_plan.add_widget(img)
        layout_plan.add_widget(label_layout)
        layout_plan.add_widget(btn_layout)

        popup = Popup(
            title=title_string,
            title_color=[0, 0, 0, 1],
            title_size=get_scaled_sp("20sp"),
            content=layout_plan,
            size_hint=(None, None),
            size=get_scaled_tuple((700, 460)),
            auto_dismiss=False,
        )

        popup.separator_color = [249 / 255.0, 206 / 255.0, 29 / 255.0, 1.0]
        popup.separator_height = str(get_scaled_height(4)) + "dp"
        popup.background = "./asmcnc/apps/shapeCutter_app/img/popup_background.png"

        ok_button.bind(on_press=popup.dismiss)

        popup.open()


class PopupSpindleSettingsInfo(Widget):
    def __init__(self, screen_manager, localization, **kwargs):
        super(PopupSpindleSettingsInfo, self).__init__(**kwargs)
        self.sm = screen_manager
        self.l = localization

        popup_width = get_scaled_width(750)
        label_width = popup_width - get_scaled_width(230)
        default_font_size = get_scaled_sp("15sp")

        model_info = (
                self.l.get_bold("Spindle motor model:")
                + "\n"
                + self.l.get_str(
            "SmartBench will operate slightly differently depending on the type of spindle motor you are using."
        )
                + " "
                + self.l.get_str(
            "It is important that you choose the option that matches the voltage and digital/manual specifications of your spindle motor."
        )
        )

        cooldown_info = (
                self.l.get_bold("Spindle motor cooldown:")
                + "\n"
                + self.l.get_str(
            "The spindle motor needs to cool down after a job to prevent it from overheating, and to extend its lifetime."
        )
                + " "
                + self.l.get_str("We recommend the following cooldown settings:")
                + "\n"
                + "       "
                + self.l.get_str("Yeti SC1/2: 12,000 RPM; 10 seconds")
                + "\n"
                + "       "
                + self.l.get_str("AMB: 10,000 RPM; 30 seconds")
        )

        stylus_info = (
                self.l.get_bold("CNC Stylus switch")
                + "[b]:[/b]\n"
                + self.l.get_str(
            "When enabled, you will always be asked if you are using CNC Stylus or a Router at the start of every job."
        )
        )

        get_data_info = (
                self.l.get_bold("SC2 Spindle motor data:")
                + "\n"
                + self.l.get_str("This button gets data from your spindle motor.")
                + " "
                + self.l.get_str("This is only available when an SC2 model is selected.")
        )

        title_string = self.l.get_str("Information")
        ok_string = self.l.get_bold("Ok")

        img = Image(
            source="./asmcnc/apps/shapeCutter_app/img/info_icon.png",
            allow_stretch=False,
        )

        model_info_image = Image(
            size_hint_x=0.2,
            source="./asmcnc/apps/maintenance_app/img/spindle_small.png",
            allow_stretch=False,
        )
        model_info_label = Label(
            text_size=(label_width, None),
            markup=True,
            halign="left",
            valign="middle",
            text=model_info,
            color=[0, 0, 0, 1],
            font_size=default_font_size,
            background_color=[0.95, 0.95, 0.95, 1],
        )
        model_info_container = BoxLayout(orientation="horizontal")
        model_info_container.add_widget(model_info_image)
        model_info_container.add_widget(model_info_label)
        cooldown_info_image_container = BoxLayout(
            orientation="vertical", size_hint_x=0.2
        )
        speed_dial_image = Image(
            source="./asmcnc/apps/maintenance_app/img/speed_dial.png",
            allow_stretch=False,
        )
        countdown_image = Image(
            source="./asmcnc/apps/maintenance_app/img/countdown_small.png",
            allow_stretch=False,
        )
        cooldown_info_image_container.add_widget(speed_dial_image)
        cooldown_info_image_container.add_widget(countdown_image)
        cooldown_info_label = Label(
            text_size=(label_width, None),
            markup=True,
            halign="left",
            valign="middle",
            text=cooldown_info,
            color=[0, 0, 0, 1],
            font_size=default_font_size,
            background_color=[0.95, 0.95, 0.95, 1],
        )
        cooldown_info_container = BoxLayout(orientation="horizontal")
        cooldown_info_container.add_widget(cooldown_info_image_container)
        cooldown_info_container.add_widget(cooldown_info_label)

        stylus_info_image = Image(
            size_hint_x=0.2,
            source="./asmcnc/apps/maintenance_app/img/stylus_mini_logo.png",
            allow_stretch=False,
        )
        stylus_info_label = Label(
            text_size=(label_width, None),
            markup=True,
            halign="left",
            valign="middle",
            text=stylus_info,
            color=[0, 0, 0, 1],
            font_size=default_font_size,
            background_color=[0.95, 0.95, 0.95, 1],
        )
        stylus_info_container = BoxLayout(orientation="horizontal")
        stylus_info_container.add_widget(stylus_info_image)
        stylus_info_container.add_widget(stylus_info_label)
        get_data_info_image = Image(
            size_hint_x=0.2,
            source="./asmcnc/apps/maintenance_app/img/spindle_info.png",
            allow_stretch=False,
        )
        get_data_info_label = Label(
            text_size=(label_width, None),
            markup=True,
            halign="left",
            valign="middle",
            text=get_data_info,
            font_size=default_font_size,
            color=[0, 0, 0, 1],
            background_color=[0.95, 0.95, 0.95, 1],
        )
        get_data_info_container = BoxLayout(orientation="horizontal")
        get_data_info_container.add_widget(get_data_info_image)
        get_data_info_container.add_widget(get_data_info_label)

        first_page_layout = BoxLayout(orientation="vertical")
        first_page_layout.add_widget(model_info_container)
        first_page_layout.add_widget(cooldown_info_container)
        second_page_layout = BoxLayout(orientation="vertical")
        second_page_layout.add_widget(stylus_info_container)
        second_page_layout.add_widget(get_data_info_container)

        carousel = Carousel(direction="right")
        carousel.add_widget(first_page_layout)
        carousel.add_widget(second_page_layout)

        left_button = Button(
            background_color=[0, 0, 0, 0.2],
            border=(0, 0, 0, 0),
            background_normal="./asmcnc/skavaUI/img/lobby_scrollleft.png",
            background_down="./asmcnc/skavaUI/img/lobby_scrollleft.png",
            font_size=default_font_size,
        )
        left_button_container = BoxLayout(size_hint_x=0.06, padding=get_scaled_tuple((0, 90)))
        left_button_container.add_widget(left_button)
        right_button = Button(
            background_color=[0, 0, 0, 0.2],
            border=(0, 0, 0, 0),
            background_normal="./asmcnc/skavaUI/img/lobby_scrollright.png",
            background_down="./asmcnc/skavaUI/img/lobby_scrollright.png",
            font_size=default_font_size,
        )
        right_button_container = BoxLayout(size_hint_x=0.06, padding=get_scaled_tuple((0, 90)))
        right_button_container.add_widget(right_button)

        carousel_layout = BoxLayout(orientation="horizontal", spacing=get_scaled_tuple((15, 15)), size_hint_y=4)
        carousel_layout.add_widget(left_button_container)
        carousel_layout.add_widget(carousel)
        carousel_layout.add_widget(right_button_container)

        ok_button = Button(text=ok_string, markup=True, font_size=default_font_size)
        ok_button.background_normal = ""
        ok_button.background_color = [76 / 255.0, 175 / 255.0, 80 / 255.0, 1.0]

        btn_layout = BoxLayout(
            orientation="horizontal", spacing=15, padding=get_scaled_tuple((300, 10, 300, 0))
        )
        btn_layout.add_widget(ok_button)

        layout_plan = BoxLayout(orientation="vertical")
        layout_plan.add_widget(img)
        layout_plan.add_widget(carousel_layout)
        layout_plan.add_widget(btn_layout)

        popup = Popup(
            title=title_string,
            title_color=[0, 0, 0, 1],
            title_size=get_scaled_sp("20sp"),
            content=layout_plan,
            size_hint=(None, None),
            size=(popup_width, get_scaled_height(440)),
            auto_dismiss=False,
        )

        popup.background = "./asmcnc/apps/shapeCutter_app/img/popup_background.png"
        popup.separator_color = [249 / 255.0, 206 / 255.0, 29 / 255.0, 1.0]
        popup.separator_height = str(get_scaled_height(4)) + "dp"

        # Binding to the carousel functions directly causes argument issues, so create "wrapper" functions
        def cycle_left(*args):
            carousel.load_previous()

        def cycle_right(*args):
            carousel.load_next()

        ok_button.bind(on_press=popup.dismiss)
        left_button.bind(on_press=cycle_left)
        right_button.bind(on_press=cycle_right)

        popup.open()


class PopupDatum(Widget):
    def __init__(self, screen_manager, machine, localization, xy, warning_message, **kwargs):
        super(PopupDatum, self).__init__(**kwargs)
        self.sm = screen_manager
        self.m = machine
        self.l = localization

        description = warning_message
        title_string = self.l.get_str('Warning!')
        yes_string = self.l.get_bold('Yes')
        no_string = self.l.get_bold('No')
        chk_message = self.l.get_str('Use laser crosshair?')

        def on_checkbox_active(checkbox, value):
            self.sm.get_screen('home').default_datum_choice = 'laser' if value else 'spindle'

        def set_datum(*args):
            if self.sm.get_screen('home').default_datum_choice == 'laser' and self.m.is_laser_enabled:
                if xy == 'X':
                    self.m.set_x_datum_with_laser()  # testing!!
                elif xy == 'Y':
                    self.m.set_y_datum_with_laser()
                elif xy == 'XY':
                    self.m.set_workzone_to_pos_xy_with_laser()
            else:
                if xy == 'X':
                    self.m.set_x_datum()
                elif xy == 'Y':
                    self.m.set_y_datum()
                elif xy == 'XY':
                    self.m.set_workzone_to_pos_xy()

        def set_checkbox_default():
            return self.sm.get_screen('home').default_datum_choice == 'laser'

        img = Image(source="./asmcnc/apps/shapeCutter_app/img/error_icon.png", allow_stretch=False)
        label = Label(size_hint_y=1, text_size=get_scaled_tuple((360, None)), halign='center', valign='middle',
                      text=description, color=[0, 0, 0, 1], padding=get_scaled_tuple((40, 20)), markup=True)

        ok_button = Button(text=yes_string, markup=True, font_size=get_scaled_sp('15sp'))
        ok_button.background_normal = ''
        ok_button.background_color = [76 / 255., 175 / 255., 80 / 255., 1.]
        back_button = Button(text=no_string, markup=True, font_size=get_scaled_sp('15sp'))
        back_button.background_normal = ''
        back_button.background_color = [230 / 255., 74 / 255., 25 / 255., 1.]

        btn_layout = BoxLayout(orientation='horizontal', spacing=get_scaled_tuple((10, 10)), padding=[0, 0, 0, 0])
        btn_layout.add_widget(back_button)
        btn_layout.add_widget(ok_button)

        layout_plan = BoxLayout(orientation='vertical', spacing=get_scaled_tuple((10, 10)),
                                padding=get_scaled_tuple((20, 20, 20, 20)))
        layout_plan.add_widget(img)
        layout_plan.add_widget(label)

        if self.m.is_laser_enabled:
            chk_label = Label(size_hint_y=1, size_hint_x=0.8, halign='center', valign='middle', text=chk_message,
                              text_size=get_scaled_tuple((200, 100)), color=[0, 0, 0, 1], font_size=get_scaled_sp('15sp'),
                              padding=get_scaled_tuple((0, 20)), markup=True)
            checkbox = CheckBox(size_hint_x=0.2,
                                background_checkbox_normal="./asmcnc/skavaUI/img/checkbox_inactive.png",
                                active=set_checkbox_default())
            checkbox.bind(active=on_checkbox_active)

            chk_layout = BoxLayout(orientation='horizontal', spacing=0, padding=get_scaled_tuple((5, 0, 5, 0)))
            chk_layout.add_widget(chk_label)
            chk_layout.add_widget(checkbox)
            layout_plan.add_widget(chk_layout)

        layout_plan.add_widget(btn_layout)

        popup = Popup(title=title_string,
                      title_color=[0, 0, 0, 1],
                      title_size=get_scaled_sp('20sp'),
                      content=layout_plan,
                      size_hint=(None, None),
                      size=get_scaled_tuple((300, 350)),
                      auto_dismiss=False,
                      separator_color=[230 / 255., 74 / 255., 25 / 255., 1.],
                      separator_height='4dp',
                      background="./asmcnc/apps/shapeCutter_app/img/popup_background.png")

        ok_button.bind(on_press=popup.dismiss)
        ok_button.bind(on_press=set_datum)
        back_button.bind(on_press=popup.dismiss)

        popup.open()
