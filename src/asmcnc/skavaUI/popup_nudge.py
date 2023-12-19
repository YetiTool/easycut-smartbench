import textwrap
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image


class PopupNudgeDatum(Widget):
    def __init__(self, screen_manager, machine, localization):
        self.sm = screen_manager
        self.m = machine
        self.l = localization

        description_text = (
            self.l.get_str("Is this where you want to set your X-Y datum?").replace(
                "X-Y", "[b]X-Y[/b]"
            )
        ).replace(self.l.get_str("datum"), self.l.get_bold("datum"))
        description = textwrap.fill(description_text, width=35, break_long_words=False)
        title_string = self.l.get_str("Warning!")
        yes_string = self.l.get_bold("Yes")
        no_string = self.l.get_bold("No")

        def set_datum(*args):
            self.sm.get_screen("nudge").set_datum()

        img = Image(
            source="./asmcnc/apps/shapeCutter_app/img/error_icon.png",
            allow_stretch=False,
        )
        label = Label(
            size_hint_y=1,
            text_size=(360, None),
            halign="center",
            valign="middle",
            text=description,
            color=[0, 0, 0, 1],
            padding=[40, 20],
            markup=True,
        )

        ok_button = Button(text=yes_string, markup=True)
        ok_button.background_normal = ""
        ok_button.background_color = [76 / 255.0, 175 / 255.0, 80 / 255.0, 1.0]
        back_button = Button(text=no_string, markup=True)
        back_button.background_normal = ""
        back_button.background_color = [230 / 255.0, 74 / 255.0, 25 / 255.0, 1.0]

        btn_layout = BoxLayout(
            orientation="horizontal", spacing=10, padding=[0, 0, 0, 0]
        )
        btn_layout.add_widget(back_button)
        btn_layout.add_widget(ok_button)

        layout_plan = BoxLayout(
            orientation="vertical", spacing=10, padding=[20, 20, 20, 20]
        )
        layout_plan.add_widget(img)
        layout_plan.add_widget(label)
        layout_plan.add_widget(btn_layout)

        popup = Popup(
            title=title_string,
            title_color=[0, 0, 0, 1],
            title_size="20sp",
            content=layout_plan,
            size_hint=(None, None),
            size=(300, 350),
            auto_dismiss=False,
        )

        popup.separator_color = [230 / 255.0, 74 / 255.0, 25 / 255.0, 1.0]
        popup.separator_height = "4dp"
        popup.background = "./asmcnc/apps/shapeCutter_app/img/popup_background.png"

        ok_button.bind(on_press=popup.dismiss)
        ok_button.bind(on_press=set_datum)
        back_button.bind(on_press=popup.dismiss)

        popup.open()


class PopupNudgeWarning(Widget):
    def __init__(self, screen_manager, machine, localization, nudge_distance):
        self.sm = screen_manager
        self.m = machine
        self.l = localization

        description = (
            self.l.get_str(
                "You have nudged the machine Xmm, this will adjust your datum by this value."
            )
            .replace("Xmm", nudge_distance + "mm")
            .replace("xMM", nudge_distance + "MM")
            + "\n\n"
            + self.l.get_str("Are you sure you want to continue?")
            + "\n\n"
            + self.l.get_str("You will not be able to undo this.")
        )
        title_string = self.l.get_str("Warning!")
        yes_string = self.l.get_bold("Yes")
        no_string = self.l.get_bold("No")

        def show_set_datum_popup(*args):
            PopupNudgeDatum(screen_manager=self.sm, machine=self.m, localization=self.l)

        img = Image(
            source="./asmcnc/apps/shapeCutter_app/img/error_icon.png",
            allow_stretch=False,
        )
        label = Label(
            size_hint_y=2,
            text_size=(400, None),
            halign="center",
            valign="middle",
            text=description,
            color=[0, 0, 0, 1],
            padding=[20, 20],
            markup=True,
        )

        ok_button = Button(text=yes_string, markup=True)
        ok_button.background_normal = ""
        ok_button.background_color = [76 / 255.0, 175 / 255.0, 80 / 255.0, 1.0]
        back_button = Button(text=no_string, markup=True)
        back_button.background_normal = ""
        back_button.background_color = [230 / 255.0, 74 / 255.0, 25 / 255.0, 1.0]

        btn_layout = BoxLayout(
            orientation="horizontal", spacing=10, padding=[0, 0, 0, 0]
        )
        btn_layout.add_widget(back_button)
        btn_layout.add_widget(ok_button)

        layout_plan = BoxLayout(
            orientation="vertical", spacing=10, padding=[20, 20, 20, 10]
        )
        layout_plan.add_widget(img)
        layout_plan.add_widget(label)
        layout_plan.add_widget(btn_layout)

        popup = Popup(
            title=title_string,
            title_color=[0, 0, 0, 1],
            title_size="20sp",
            content=layout_plan,
            size_hint=(None, None),
            size=(400, 350),
            auto_dismiss=False,
        )

        popup.separator_color = [230 / 255.0, 74 / 255.0, 25 / 255.0, 1.0]
        popup.separator_height = "4dp"
        popup.background = "./asmcnc/apps/shapeCutter_app/img/popup_background.png"

        ok_button.bind(on_press=popup.dismiss)
        ok_button.bind(on_press=show_set_datum_popup)
        back_button.bind(on_press=popup.dismiss)

        popup.open()
