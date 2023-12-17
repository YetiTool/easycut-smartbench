"""
Popups that aren't covered by the default popup system.
"""
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
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
        )

        img_full_brush = Image(
            source="./asmcnc/apps/maintenance_app/img/brush_long_img.png",
            allow_stretch=False,
            size=(get_scaled_width(68), get_scaled_height(99)),
        )
        label_full_brush_top = Label(
            text=self.l.get_bold("NEW"),
            text_size=(get_scaled_width(760), self.height),
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

        ok_button = Button(text="[b]Ok[/b]", markup=True)
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


class PopupDisplaySpindleData(Widget):  # TODO: SCALE AND MOVE TO A UNIQUE POPUPS FILE
    def __init__(self, screen_manager, localization, serial, **kwargs):
        super(PopupDisplaySpindleData, self).__init__(**kwargs)
        self.sm = screen_manager
        self.l = localization
        self.s = serial

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
            padding=0,
            markup=True,
            bold=True,
        )
        value_label = Label(
            text_size=get_scaled_tuple((250, None)),
            halign="right",
            valign="middle",
            text=value_string,
            color=(0, 0, 0, 1),
            padding=0,
            markup=True,
        )

        label_layout = BoxLayout(
            orientation="horizontal", size_hint_y=2, padding=get_scaled_tuple((75, 0))
        )
        label_layout.add_widget(category_label)
        label_layout.add_widget(value_label)

        ok_button = Button(text=ok_string, markup=True)
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
