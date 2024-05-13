"""
@author: Archie

Popup system for easycut-smartbench
"""
from enum import Enum
from kivy.metrics import dp
from kivy.properties import ObjectProperty, StringProperty, ListProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.rst import RstDocument
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock

from asmcnc.core_UI import scaling_utils as utils
from asmcnc.core_UI.components.buttons.hold_button import WarningHoldButton
from asmcnc.comms.logging_system.logging_system import Logger
from asmcnc.core_UI.utils import color_provider

"""
Popup type enum

INFO: Info popup
ERROR: Error popup
QR: QR code popup (no image by default)
OTHER: Other popup (no image by default)

Each enum has a value which is the path to the image to be used in the popup, and a colour which is the colour of the
separator line at the top of the popup
"""


class PopupType(Enum):
    INFO = {
        "small_image": "./asmcnc/apps/shapeCutter_app/img/info_icon.png",
        "big_image": "./asmcnc/apps/shapeCutter_app/img/info_icon_scaled_up.png",
        "separator_color": color_provider.get_rgba("yellow"),
    }
    ERROR = {
        "small_image": "./asmcnc/apps/shapeCutter_app/img/error_icon.png",
        "big_image": "./asmcnc/apps/shapeCutter_app/img/error_icon_scaled_up.png",
        "separator_color": color_provider.get_rgba("red"),
    }
    QR = None
    OTHER = None


class BasicPopup(Popup):
    # Fetched by kivy from the kwargs
    sm = ObjectProperty(None)
    m = ObjectProperty(None)
    l = ObjectProperty(None)

    # Widgets of BasicPopup class (if you need the others, navigate to them through these widgets)
    main_layout = None
    button_layout = None
    image = None
    main_label = None

    # Default properties
    # You can override these properties in the constructor, pass them as kwargs
    separator_color = ListProperty(color_provider.get_rgba("yellow"))
    separator_height = dp(utils.get_scaled_height(4))
    background = StringProperty(
        "./asmcnc/apps/shapeCutter_app/img/popup_background.png"
    )
    auto_dismiss = ObjectProperty(False)
    title_color = ObjectProperty([0, 0, 0, 1])
    title_size = ObjectProperty(str(utils.get_scaled_width(20)) + "sp")
    button_one_background_normal = StringProperty(
        "atlas://data/images/defaulttheme/button"
    )
    button_two_background_normal = StringProperty(
        "atlas://data/images/defaulttheme/button"
    )
    """
    title: string to be used as the title
    main_string: string to be used as main text
    popup_type: type of popup (enum) see PopupType class above
    main_label_padding: padding of main label
    main_layout_padding: padding of main layout
    main_layout_spacing: spacing of main layout
    main_label_size_delta: how much to reduce the width of the main label by compared to the popup width
    main_label_h_align: horizontal alignment of main label
    button_layout_padding: padding of button layout
    button_layout_spacing: spacing of button layout
    popup_width: width of popup, default 300
    popup_height: height of popup, default 350
    popup_image: image to be used in popup, default None (uses popup_type's image)
    popup_image_size_hint: size hint of popup image, default None
    button_one_text: text to be used in button one, default "Ok"
    button_one_callback: callback to be used when button one is pressed, default None
    button_one_background_color: background color to be used for button one, default None
    button_two_text: text to be used in button two, default None
    button_two_callback: callback to be used when button two is pressed, default None
    button_two_background_color: background color to be used for button two, default None
    
    Usage:
    popup = PopupSystem(sm=self.sm, m=self.m, l=self.l,
                        title_string="Title", main_string="Main text", popup_type=PopupType.INFO,
                        popup_width=300, popup_height=350)
                        
    popup.open()
    
    This will create a popup with title "Title", main text "Main text", type INFO, width 300, height 350. 
    The popup will have a singular button with text "Ok" and will close when pressed.
    
    You can also pass a callback to the button:
    popup = PopupSystem(sm=self.sm, m=self.m, l=self.l,
                        title_string="Title", main_string="Main text", popup_type=PopupType.INFO,
                        popup_width=300, popup_height=350, button_one_callback=self.callback)
        
    This will dismiss the popup and call the callback function when the button is pressed.
    
    Example of the Welcome popup:
    welcome_popup = popup.BasicPopup(sm=self.sm, m=self.m, l=self.l,
                                         title=self.l.get_str('Welcome to SmartBench'),
                                         main_string=self.welcome_popup_description,
                                         popup_type=popup.PopupType.INFO,
                                         popup_width=500, popup_height=440, main_label_size_delta=80,
                                         main_label_padding=(0, 0), main_layout_padding=(10, 10, 10, 10),
                                         main_layout_spacing=10, button_layout_padding=(20, 10, 20, 0),
                                         button_layout_spacing=15,
                                         button_two_background_color=(76 / 255., 175 / 255., 80 / 255., 1.),
                                         button_one_background_color=(230 / 255., 74 / 255., 25 / 255., 1.),
                                         button_one_text="Remind me", button_two_text="Ok",
                                         button_one_callback=self.set_trigger_to_true,
                                         button_two_callback=self.set_trigger_to_false)
    welcome_popup.open()
    
    Example of a QR popup:
    qr_popup = BasicPopup(
            sm=self.sm, m=self.m, l=self.l,
            title='Information',
            main_string=info,
            popup_type=PopupType.QR,
            popup_image=self.qr_source,
            popup_image_size_hint=(1, 1),
            popup_width=500,
            popup_height=440,
            main_label_size_delta=40,
            main_label_h_align='left',
            main_label_padding=(10, 10),
            main_layout_spacing=10,
            main_layout_padding=10,
            button_layout_padding=(150, 20, 150, 0),
            button_layout_spacing=15,
            button_one_text='Ok',
            button_one_background_color=(76 / 255., 175 / 255., 80 / 255., 1.)
        )
    qr_popup.open()
    """

    def __init__(
        self,
        main_string,
        popup_type,
        main_label_padding,
        main_layout_padding,
        main_layout_spacing,
        main_label_size_delta,
        button_layout_padding,
        button_layout_spacing,
        popup_width,
        popup_height,
        popup_image=None,
        popup_image_size_hint=None,
        button_one_text="Ok",
        button_one_callback=None,
        button_one_background_color=None,
        button_two_text=None,
        button_two_callback=None,
        button_two_background_color=None,
        main_label_h_align="center",
        main_label_size_hint_y=2,
        button_layout_size_hint_y=1,
        **kwargs
    ):
        super(BasicPopup, self).__init__(**kwargs)

        if button_one_callback is None:
            button_one_callback = self.dismiss
        if button_one_background_color is not None:
            self.button_one_background_normal = ""
        if button_two_background_color is not None:
            self.button_two_background_normal = ""

        self.title = self.l.get_str(kwargs["title"])
        self.size_hint = (None, None)
        self.width = dp(utils.get_scaled_width(popup_width))
        self.height = dp(utils.get_scaled_height(popup_height))
        self.popup_width = popup_width
        self.popup_height = popup_height
        self.main_string = self.l.get_str(main_string)
        self.main_label_padding = main_label_padding
        self.main_layout_padding = main_layout_padding
        self.main_label_size_delta = main_label_size_delta
        self.main_label_h_align = main_label_h_align
        self.main_label_size_hint_y = main_label_size_hint_y
        self.button_layout_padding = button_layout_padding
        self.button_layout_spacing = button_layout_spacing
        self.button_layout_size_hint_y = button_layout_size_hint_y
        self.main_layout_spacing = main_layout_spacing
        self.popup_type = popup_type
        self.popup_image = popup_image
        self.popup_image_size_hint = popup_image_size_hint
        self.button_one_text = (
            self.l.get_str(button_one_text) if button_one_text is not None else None
        )
        self.button_one_callback = button_one_callback
        self.button_two_text = (
            self.l.get_str(button_two_text) if button_two_text is not None else None
        )
        self.button_two_callback = button_two_callback
        self.button_one_background_color = button_one_background_color
        self.button_two_background_color = button_two_background_color
        self.button_one_background_normal = (
            self.button_one_background_normal
            if button_one_background_color is None
            else ""
        )
        self.button_two_background_normal = (
            self.button_two_background_normal
            if button_two_background_color is None
            else ""
        )
        if self.popup_type is not None:
            if self.popup_type.value is not None:
                self.separator_color = self.popup_type.value["separator_color"]

        self.popup_img_string = "big_image" if utils.is_screen_big() else "small_image"

        self.build()

    def build(self):
        text_size_x = dp(
            utils.get_scaled_width(self.popup_width - self.main_label_size_delta)
        )

        self.main_label = Label(
            size_hint_y=self.main_label_size_hint_y,
            text_size=(text_size_x, None),
            halign=self.main_label_h_align,
            valign="middle",
            text=self.l.get_str(self.main_string),
            color=color_provider.get_rgba("black"),
            padding=utils.get_scaled_tuple(self.main_label_padding),
            markup=True,
            font_size=str(utils.get_scaled_width(15)) + "sp",
        )

        self.main_layout = BoxLayout(
            orientation="vertical",
            spacing=utils.get_scaled_tuple(
                self.main_layout_spacing, orientation="vertical"
            ),
            padding=utils.get_scaled_tuple(self.main_layout_padding),
        )

        image = self.get_image()
        if image is not None:
            self.main_layout.add_widget(image)

        self.main_layout.add_widget(self.main_label)

        if self.button_one_text:
            self.button_layout = self.build_button_layout()
            self.main_layout.add_widget(self.button_layout)

        self.content = self.main_layout
        self.update_font_sizes()

    def update_font_sizes(self):
        if len(self.main_label.text) > 200 and utils.is_screen_big():
            self.main_label.font_size = str(utils.get_scaled_width(13)) + "sp"

    def build_button_layout(self):
        button_layout = BoxLayout(
            orientation="horizontal",
            spacing=utils.get_scaled_tuple(
                self.button_layout_spacing, orientation="horizontal"
            ),
            padding=utils.get_scaled_tuple(self.button_layout_padding),
        )

        for button in self.build_buttons():
            button_layout.add_widget(button)
        return button_layout

    def on_button_pressed(self, callback):
        if callback:
            callback()
        self.dismiss()

    def get_image(self):
        if self.popup_type.value is None:
            if self.popup_image is None:
                return None
            return Image(
                source=self.popup_image,
                allow_stretch=False,
                size_hint=self.popup_image_size_hint,
            )
        return Image(
            source=self.popup_type.value[self.popup_img_string], allow_stretch=False
        )

    def build_buttons(self):
        if self.button_one_text is None:
            return []

        buttons = [
            Button(
                text=self.l.get_bold(self.button_one_text),
                on_release=lambda x: self.on_button_pressed(self.button_one_callback),
                font_size=str(utils.get_scaled_width(15)) + "sp",
                background_normal=self.button_one_background_normal,
                background_color=self.button_one_background_color,
                markup=True,
            )
        ]
        if self.button_two_text is not None:
            buttons.append(
                Button(
                    text=self.l.get_bold(self.button_two_text),
                    on_release=lambda x: self.on_button_pressed(
                        self.button_two_callback
                    ),
                    font_size=str(utils.get_scaled_width(15)) + "sp",
                    background_normal=self.button_two_background_normal,
                    background_color=self.button_two_background_color,
                    markup=True,
                )
            )
        return buttons


class InfoPopup(BasicPopup):
    def __init__(
        self,
        main_string,
        popup_width,
        popup_height,
        button_one_text="Ok",
        button_one_callback=None,
        button_one_background_color=(76 / 255.0, 175 / 255.0, 80 / 255.0, 1.0),
        button_two_text=None,
        button_two_callback=None,
        button_two_background_color=None,
        title="Information",
        main_label_padding=(10, 10),
        main_layout_padding=(10, 10, 10, 10),
        main_layout_spacing=10,
        main_label_size_delta=40,
        button_layout_padding=(150, 20, 150, 0),
        button_layout_spacing=15,
        main_label_h_align="left",
        main_label_size_hint_y=2,
        **kwargs
    ):
        super(InfoPopup, self).__init__(
            main_string=main_string,
            popup_type=PopupType.INFO,
            main_label_padding=main_label_padding,
            main_layout_padding=main_layout_padding,
            main_layout_spacing=main_layout_spacing,
            main_label_size_delta=main_label_size_delta,
            button_layout_padding=button_layout_padding,
            button_layout_spacing=button_layout_spacing,
            main_label_h_align=main_label_h_align,
            popup_width=popup_width,
            popup_height=popup_height,
            button_one_text=button_one_text,
            button_one_callback=button_one_callback,
            button_one_background_color=button_one_background_color,
            button_two_text=button_two_text,
            button_two_callback=button_two_callback,
            button_two_background_color=button_two_background_color,
            title=title,
            main_label_size_hint_y=main_label_size_hint_y,
            **kwargs
        )


class ErrorPopup(BasicPopup):
    def __init__(
        self,
        main_string,
        popup_width=500,
        popup_height=400,
        button_one_text="Ok",
        button_one_callback=None,
        button_one_background_color = color_provider.get_rgba("red"),
        button_two_text=None,
        button_two_callback=None,
        button_two_background_color=None,
        main_label_padding=(0, 10),
        main_layout_padding=(40, 20, 40, 20),
        main_layout_spacing=10,
        main_label_size_delta=40,
        main_label_h_align="center",
        title="Error!",
        button_layout_padding=(0, 20, 0, 0),
        button_layout_spacing=10,
        main_label_size_hint_y=1,
        **kwargs
    ):
        super(ErrorPopup, self).__init__(
            main_string=main_string,
            popup_type=PopupType.ERROR,
            main_label_padding=main_label_padding,
            main_layout_padding=main_layout_padding,
            main_layout_spacing=main_layout_spacing,
            main_label_size_delta=main_label_size_delta,
            button_layout_padding=button_layout_padding,
            button_layout_spacing=button_layout_spacing,
            main_label_h_align=main_label_h_align,
            popup_width=popup_width,
            popup_height=popup_height,
            button_one_text=button_one_text,
            button_one_callback=button_one_callback,
            button_one_background_color=button_one_background_color,
            button_two_text=button_two_text,
            button_two_callback=button_two_callback,
            button_two_background_color=button_two_background_color,
            title=title,
            main_label_size_hint_y=main_label_size_hint_y,
            **kwargs
        )


class QRPopup(BasicPopup):
    def __init__(
        self,
        main_string,
        popup_width,
        popup_height,
        popup_image,
        popup_image_size_hint,
        button_one_text="Ok",
        button_one_callback=None,
        button_one_background_color=None,
        button_two_text=None,
        button_two_callback=None,
        button_two_background_color=None,
        **kwargs
    ):
        super(QRPopup, self).__init__(
            main_string=main_string,
            popup_type=PopupType.QR,
            main_label_padding=(10, 10),
            main_layout_padding=10,
            main_layout_spacing=10,
            main_label_size_delta=40,
            button_layout_padding=(150, 20, 150, 0),
            button_layout_spacing=15,
            popup_width=popup_width,
            popup_height=popup_height,
            popup_image=popup_image,
            popup_image_size_hint=popup_image_size_hint,
            button_one_text=button_one_text,
            button_one_callback=button_one_callback,
            button_one_background_color=button_one_background_color,
            button_two_text=button_two_text,
            button_two_callback=button_two_callback,
            button_two_background_color=button_two_background_color,
            **kwargs
        )


class MiniInfoPopup(BasicPopup):
    def __init__(
        self,
        main_string,
        popup_width=300,
        popup_height=300,
        button_one_text="Ok",
        button_one_callback=None,
        button_one_background_color=(76 / 255.0, 175 / 255.0, 80 / 255.0, 1.0),
        button_two_text=None,
        button_two_callback=None,
        button_two_background_color=None,
        title="Information",
        **kwargs
    ):
        super(MiniInfoPopup, self).__init__(
            main_string=main_string,
            popup_type=PopupType.INFO,
            main_label_padding=(40, 20),
            title=title,
            main_layout_padding=(40, 20),
            main_layout_spacing=10,
            main_label_size_delta=-60,
            button_layout_padding=(0, 0),
            button_layout_spacing=10,
            popup_width=popup_width,
            popup_height=popup_height,
            button_one_text=button_one_text,
            button_one_callback=button_one_callback,
            button_one_background_color=button_one_background_color,
            button_two_text=button_two_text,
            button_two_callback=button_two_callback,
            button_two_background_color=button_two_background_color,
            main_label_h_align="center",
            main_label_size_hint_y=1,
            **kwargs
        )


class StopPopup(BasicPopup):
    def __init__(
        self,
        main_string="Is everything OK? You can resume the job, or cancel it completely.",
        popup_width=400,
        popup_height=300,
        button_one_text="Cancel",
        button_one_background_color=(230 / 255., 74 / 255., 25 / 255., 1.),
        button_two_text="Resume",
        button_two_background_color=(76 / 255., 175 / 255., 80 / 255., 1.),
        main_label_padding=(0, 0),
        main_layout_padding=(30, 20, 30, 0),
        main_layout_spacing=5,
        main_label_size_delta=40,
        main_label_h_align="center",
        title="Warning!",
        button_layout_padding=(0, 5, 0, 0),
        button_layout_spacing=15,
        main_label_size_hint_y=2,
        button_layout_size_hint_y=2,
        **kwargs
    ):
        self.m = kwargs['m']

        button_one_callback = self.m.resume_from_a_soft_door
        button_two_callback = self.m.stop_from_soft_stop_cancel

        super(StopPopup, self).__init__(
            main_string=main_string,
            popup_type=PopupType.ERROR,
            main_label_padding=main_label_padding,
            main_layout_padding=main_layout_padding,
            main_layout_spacing=main_layout_spacing,
            main_label_size_delta=main_label_size_delta,
            button_layout_padding=button_layout_padding,
            button_layout_spacing=button_layout_spacing,
            main_label_h_align=main_label_h_align,
            popup_width=popup_width,
            popup_height=popup_height,
            button_one_text=button_one_text,
            button_one_callback=button_one_callback,
            button_one_background_color=button_one_background_color,
            button_two_text=button_two_text,
            button_two_callback=button_two_callback,
            button_two_background_color=button_two_background_color,
            title=title,
            main_label_size_hint_y=main_label_size_hint_y,
            button_layout_size_hint_y=button_layout_size_hint_y,
            **kwargs
        )


class ParkPopup(BasicPopup):
    def __init__(
        self,
        main_string,
        popup_width=300,
        popup_height=350,
        button_one_text="No",
        button_one_background_color=(230 / 255., 74 / 255., 25 / 255., 1.),
        button_two_text="Yes",
        button_two_background_color=(76 / 255., 175 / 255., 80 / 255., 1.),
        main_label_padding=(40, 20),
        main_layout_padding=(40, 20, 40, 20),
        main_layout_spacing=10,
        main_label_size_delta=-60,
        main_label_h_align="center",
        title="Warning!",
        button_layout_padding=(0, 0, 0, 0),
        button_layout_spacing=10,
        main_label_size_hint_y=1,
        **kwargs
    ):
        self.m = kwargs['m']
        def set_park(*args):
            self.m.set_standby_to_pos()
            self.m.get_grbl_status()

        button_two_callback = set_park

        super(ParkPopup, self).__init__(
            main_string=main_string,
            popup_type=PopupType.ERROR,
            main_label_padding=main_label_padding,
            main_layout_padding=main_layout_padding,
            main_layout_spacing=main_layout_spacing,
            main_label_size_delta=main_label_size_delta,
            button_layout_padding=button_layout_padding,
            button_layout_spacing=button_layout_spacing,
            main_label_h_align=main_label_h_align,
            popup_width=popup_width,
            popup_height=popup_height,
            button_one_text=button_one_text,
            button_one_callback=None,
            button_one_background_color=button_one_background_color,
            button_two_text=button_two_text,
            button_two_callback=button_two_callback,
            button_two_background_color=button_two_background_color,
            title=title,
            main_label_size_hint_y=main_label_size_hint_y,
            **kwargs
        )


class SoftwareUpdateSuccessPopup(BasicPopup):
    def __init__(
        self,
        main_string,
        popup_width=700,
        popup_height=400,
        button_one_text="Ok",
        button_one_background_color=(76 / 255., 175 / 255., 80 / 255., 1.),
        button_two_text=None,
        button_two_background_color=None,
        main_label_padding=(40, 10),
        main_layout_padding=(40, 20, 40, 20),
        main_layout_spacing=10,
        main_label_size_delta=40,
        main_label_h_align="center",
        title="Update Successful!",
        button_layout_padding=(0, 0, 0, 0),
        button_layout_spacing=10,
        main_label_size_hint_y=1.2,
        **kwargs
    ):

        super(SoftwareUpdateSuccessPopup, self).__init__(
            main_string=main_string,
            popup_type=PopupType.INFO,
            main_label_padding=main_label_padding,
            main_layout_padding=main_layout_padding,
            main_layout_spacing=main_layout_spacing,
            main_label_size_delta=main_label_size_delta,
            button_layout_padding=button_layout_padding,
            button_layout_spacing=button_layout_spacing,
            main_label_h_align=main_label_h_align,
            popup_width=popup_width,
            popup_height=popup_height,
            button_one_text=button_one_text,
            button_one_callback=None,
            button_one_background_color=button_one_background_color,
            button_two_text=button_two_text,
            button_two_callback=None,
            button_two_background_color=button_two_background_color,
            title=title,
            main_label_size_hint_y=main_label_size_hint_y,
            **kwargs
        )


class WarningPopup(BasicPopup):
    def __init__(
        self,
        main_string,
        popup_width=500,
        popup_height=400,
        button_one_text="Ok",
        button_one_callback=None,
        button_one_background_color = color_provider.get_rgba("red"),
        button_two_text=None,
        button_two_callback=None,
        button_two_background_color=None,
        main_label_padding=(0, 0),
        main_layout_padding=(40, 20, 40, 20),
        main_layout_spacing=10,
        main_label_size_delta=140,
        main_label_h_align="center",
        title="Warning!",
        button_layout_padding=(20, 10, 20, 0),
        button_layout_spacing=10,
        main_label_size_hint_y=1,
        **kwargs
    ):
        super(WarningPopup, self).__init__(
            main_string=main_string,
            popup_type=PopupType.ERROR,
            main_label_padding=main_label_padding,
            main_layout_padding=main_layout_padding,
            main_layout_spacing=main_layout_spacing,
            main_label_size_delta=main_label_size_delta,
            button_layout_padding=button_layout_padding,
            button_layout_spacing=button_layout_spacing,
            main_label_h_align=main_label_h_align,
            popup_width=popup_width,
            popup_height=popup_height,
            button_one_text=button_one_text,
            button_one_callback=button_one_callback,
            button_one_background_color=button_one_background_color,
            button_two_text=button_two_text,
            button_two_callback=button_two_callback,
            button_two_background_color=button_two_background_color,
            title=title,
            main_label_size_hint_y=main_label_size_hint_y,
            **kwargs
        )


class WaitPopup(BasicPopup):
    def __init__(
        self,
        main_string=None,
        popup_width=500,
        popup_height=200,
        button_one_text=None,
        button_one_callback=None,
        button_one_background_color=None,
        button_two_text=None,
        button_two_callback=None,
        button_two_background_color=None,
        main_label_padding=(40, 20),
        main_layout_padding=(40, 20, 40, 20),
        main_layout_spacing=10,
        main_label_size_delta=140,
        main_label_h_align="center",
        title="Please wait...",
        button_layout_padding=None,
        button_layout_spacing=None,
        main_label_size_hint_y=1,
        **kwargs
    ):
        if not main_string:
            main_string = "Please wait..."

        super(WaitPopup, self).__init__(
            main_string=main_string,
            popup_type=PopupType.INFO,
            main_label_padding=main_label_padding,
            main_layout_padding=main_layout_padding,
            main_layout_spacing=main_layout_spacing,
            main_label_size_delta=main_label_size_delta,
            button_layout_padding=button_layout_padding,
            button_layout_spacing=button_layout_spacing,
            main_label_h_align=main_label_h_align,
            popup_width=popup_width,
            popup_height=popup_height,
            button_one_text=button_one_text,
            button_one_callback=button_one_callback,
            button_one_background_color=button_one_background_color,
            button_two_text=button_two_text,
            button_two_callback=button_two_callback,
            button_two_background_color=button_two_background_color,
            title=title,
            main_label_size_hint_y=main_label_size_hint_y,
            **kwargs
        )


class UploadSettingsFromUsbPopup(BasicPopup):
    def __init__(
        self,
        main_string,
        popup_width=600,
        popup_height=450,
        button_one_text="Ok",
        button_one_background_color=(76 / 255., 175 / 255., 80 / 255., 1.),
        main_label_padding=(40, 20),
        main_layout_padding=(40, 20, 40, 20),
        main_layout_spacing=10,
        main_label_size_delta=-60,
        main_label_h_align="left",
        title="Information",
        button_layout_padding=(150, 40, 150, 0),
        button_layout_spacing=10,
        main_label_size_hint_y=1,
        **kwargs
    ):
        self.sm = kwargs['sm']

        def button_one_callback(*args):
            self.sm.upload_settings_from_usb(*args)

        super(UploadSettingsFromUsbPopup, self).__init__(
            main_string=main_string,
            popup_type=PopupType.INFO,
            main_label_padding=main_label_padding,
            main_layout_padding=main_layout_padding,
            main_layout_spacing=main_layout_spacing,
            main_label_size_delta=main_label_size_delta,
            button_layout_padding=button_layout_padding,
            button_layout_spacing=button_layout_spacing,
            main_label_h_align=main_label_h_align,
            popup_width=popup_width,
            popup_height=popup_height,
            button_one_text=button_one_text,
            button_one_callback=button_one_callback,
            button_one_background_color=button_one_background_color,
            title=title,
            main_label_size_hint_y=main_label_size_hint_y,
            button_layout_size_hint_y= 1,
            **kwargs
        )


class DownloadSettingsToUsbPopup(BasicPopup):
    def __init__(
        self,
        main_string,
        popup_width=600,
        popup_height=450,
        button_one_text="Ok",
        button_one_background_color=(76 / 255., 175 / 255., 80 / 255., 1.),
        main_label_padding=(40, 20),
        main_layout_padding=(40, 20, 40, 20),
        main_layout_spacing=10,
        main_label_size_delta=-60,
        main_label_h_align="left",
        title="Information",
        button_layout_padding=(150, 40, 150, 0),
        button_layout_spacing=10,
        main_label_size_hint_y=1,
        **kwargs
    ):
        self.sm = kwargs['sm']

        def button_one_callback(*args):
            self.sm.download_settings_to_usb(*args)

        super(DownloadSettingsToUsbPopup, self).__init__(
            main_string=main_string,
            popup_type=PopupType.INFO,
            main_label_padding=main_label_padding,
            main_layout_padding=main_layout_padding,
            main_layout_spacing=main_layout_spacing,
            main_label_size_delta=main_label_size_delta,
            button_layout_padding=button_layout_padding,
            button_layout_spacing=button_layout_spacing,
            main_label_h_align=main_label_h_align,
            popup_width=popup_width,
            popup_height=popup_height,
            button_one_text=button_one_text,
            button_one_callback=button_one_callback,
            button_one_background_color=button_one_background_color,
            title=title,
            main_label_size_hint_y=main_label_size_hint_y,
            button_layout_size_hint_y= 1,
            **kwargs
        )


class SpindleSafetyPopup(BasicPopup):
    def __init__(
        self,
        popup_width=600,
        popup_height=450,
        button_one_text="Cancel",
        button_one_callback=None,
        button_one_background_color=(230 / 255., 74 / 255., 25 / 255., 1.),
        button_two_text=None,
        button_two_callback=None,
        button_two_background_color=None,
        title="Information",
        main_label_padding=(0, 10),
        main_layout_padding=(10, 10, 10, 10),
        main_layout_spacing=10,
        main_label_size_delta=10,
        button_layout_padding=(0, 5, 0, 5),
        button_layout_spacing=15,
        main_label_h_align="center",
        main_label_size_hint_y=2,
        **kwargs
    ):
        self.l = kwargs["l"]

        main_string = self.l.get_str("This will start the spindle at 12,000 rpm! Please make sure:")
        main_string += "\n\n"
        main_string += " - " + self.l.get_str("The spindle is clamped properly") + "\n\n"
        main_string += " - " + self.l.get_str("The spindle is plugged in") + "\n\n"
        main_string += " - " + self.l.get_str("The dust shoe plug is inserted") + "\n\n"
        main_string += " - " + self.l.get_str("The cutter is free to move")

        super(SpindleSafetyPopup, self).__init__(
            main_string=main_string,
            popup_type=PopupType.INFO,
            main_label_padding=main_label_padding,
            main_layout_padding=main_layout_padding,
            main_layout_spacing=main_layout_spacing,
            main_label_size_delta=main_label_size_delta,
            button_layout_padding=button_layout_padding,
            button_layout_spacing=button_layout_spacing,
            main_label_h_align=main_label_h_align,
            popup_width=popup_width,
            popup_height=popup_height,
            button_one_text=button_one_text,
            button_one_callback=button_one_callback,
            button_one_background_color=button_one_background_color,
            button_two_text=button_two_text,
            button_two_callback=button_two_callback,
            button_two_background_color=button_two_background_color,
            title=title,
            main_label_size_hint_y=main_label_size_hint_y,
            button_layout_size_hint_y=1,
            **kwargs
        )

    def build_buttons(self):
        return [
            Button(
                text=self.l.get_str(self.button_one_text),
                on_release=lambda x: self.on_button_pressed(self.button_one_callback),
                font_size=utils.get_scaled_sp("15sp"),
                background_normal=self.button_one_background_normal,
                background_color=self.button_one_background_color,
                markup=True,
            ),
            WarningHoldButton(
                text=self.l.get_str("Press for 1s to start spindle"),
                hold_time=1,
                callback=lambda: self.on_button_pressed(self.button_two_callback),
                font_size=utils.get_scaled_sp("15sp"),
                color=color_provider.get_rgba("black"),
                markup=True
            )
        ]


class JobValidationPopup(BasicPopup):
    def __init__(
        self,
        main_string,
        popup_width=740,
        popup_height=450,
        button_one_text="Ok",
        button_one_callback=None,
        button_one_background_color=(230 / 255., 74 / 255., 25 / 255., 1.),
        button_two_text=None,
        button_two_callback=None,
        button_two_background_color=None,
        title="Error",
        main_label_padding=(0, 10),
        main_layout_padding=(10, 10, 10, 10),
        main_layout_spacing=10,
        main_label_size_delta=30,
        button_layout_padding=(0, 5, 0, 5),
        button_layout_spacing=15,
        main_label_h_align="center",
        main_label_size_hint_y=2,
        **kwargs
    ):
        super(JobValidationPopup, self).__init__(
            main_string=main_string,
            popup_type=PopupType.ERROR,
            main_label_padding=main_label_padding,
            main_layout_padding=main_layout_padding,
            main_layout_spacing=main_layout_spacing,
            main_label_size_delta=main_label_size_delta,
            button_layout_padding=button_layout_padding,
            button_layout_spacing=button_layout_spacing,
            main_label_h_align=main_label_h_align,
            popup_width=popup_width,
            popup_height=popup_height,
            button_one_text=button_one_text,
            button_one_callback=button_one_callback,
            button_one_background_color=button_one_background_color,
            button_two_text=button_two_text,
            button_two_callback=button_two_callback,
            button_two_background_color=button_two_background_color,
            title=title,
            main_label_size_hint_y=main_label_size_hint_y,
            button_layout_size_hint_y=1,
            **kwargs
        )

    def build(self):
        text_size_x = dp(
            utils.get_scaled_width(self.popup_width - self.main_label_size_delta)
        )

        self.scroll_view = ScrollView(
            padding=utils.get_scaled_tuple((10, 10)),
        )

        self.main_label = RstDocument(
            text_size=(text_size_x, None),
            text=self.l.get_str(self.main_string),
            color=color_provider.get_rgba("black"),
            background_color=color_provider.get_rgba("white"),
            markup=True,
            font_size=str(utils.get_scaled_width(15)) + "sp",
        )
        self.scroll_view.add_widget(self.main_label)

        self.main_layout = BoxLayout(
            orientation="vertical",
            spacing=utils.get_scaled_tuple(
                self.main_layout_spacing, orientation="vertical"
            ),
            padding=utils.get_scaled_tuple(self.main_layout_padding),
        )

        image = self.get_image()
        if image is not None:
            self.main_layout.add_widget(image)

        self.main_layout.add_widget(self.scroll_view)

        if self.button_one_text:
            self.button_layout = self.build_button_layout()
            self.main_layout.add_widget(self.button_layout)

        self.content = self.main_layout
        self.update_font_sizes()


class SimulatingJobPopup(ErrorPopup):
    def __init__(
        self,
        main_string,
        popup_width=500,
        popup_height=400,
        button_one_text="Stop",
        button_one_background_color = color_provider.get_rgba("red"),
        button_two_text=None,
        button_two_callback=None,
        button_two_background_color=None,
        main_label_padding=(0, 10),
        main_layout_padding=(40, 20, 40, 20),
        main_layout_spacing=10,
        main_label_size_delta=40,
        main_label_h_align="center",
        title="Simulating Job",
        button_layout_padding=(0, 20, 0, 0),
        button_layout_spacing=10,
        main_label_size_hint_y=1,
        **kwargs
    ):
        
        self.m = kwargs['m']

        def stop(*args):
            Logger.info("User stopped simulation.")
            self.m.s.suppress_error_screens = True
            self.m._grbl_feed_hold()
            self.m.s.cancel_stream()
            Clock.schedule_once(lambda dt: reset(), 1)

        def reset(*args):
            self.m._grbl_soft_reset()
            self.m.s.suppress_error_screens = False

        super(SimulatingJobPopup, self).__init__(
            main_string=main_string,
            popup_width=popup_width,
            popup_height=popup_height,
            button_one_text=button_one_text,
            button_one_callback=stop,
            button_one_background_color=button_one_background_color,
            button_two_text=button_two_text,
            button_two_callback=button_two_callback,
            button_two_background_color=button_two_background_color,
            main_label_padding=main_label_padding,
            main_layout_padding=main_layout_padding,
            main_layout_spacing=main_layout_spacing,
            main_label_size_delta=main_label_size_delta,
            main_label_h_align=main_label_h_align,
            title=title,
            button_layout_padding=button_layout_padding,
            button_layout_spacing=button_layout_spacing,
            main_label_size_hint_y=main_label_size_hint_y,
            **kwargs
        )