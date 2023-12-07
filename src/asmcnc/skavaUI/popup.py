"""
@author: Archie

Popup system for easycut-smartbench
"""
from enum import Enum
from kivy.metrics import dp
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.popup import Popup

from asmcnc.skavaUI import utils


class PopupType(Enum):
    INFO = "./asmcnc/apps/shapeCutter_app/img/info_icon.png"
    ERROR = "./asmcnc/apps/shapeCutter_app/img/error_icon.png"
    QR = "./asmcnc/apps/shapeCutter_app/img/qr_icon.png"  # TODO: Implement QR CODE
    OTHER = ""


class PopupSystem(Popup):
    # Fetched by kivy from the kwargs
    sm = ObjectProperty(None)
    m = ObjectProperty(None)
    l = ObjectProperty(None)

    # Default properties
    separator_color = [230 / 255., 74 / 255., 25 / 255., 1.]
    separator_height = dp(4)

    # You can override these properties in the constructor, pass them as kwargs
    background = StringProperty('./asmcnc/apps/shapeCutter_app/img/popup_background.png')
    auto_dismiss = ObjectProperty(False)
    title_color = ObjectProperty([0, 0, 0, 1])
    title_size = ObjectProperty(str(utils.get_scaled_width(20)) + "sp")

    button_one_background_normal = 'atlas://data/images/defaulttheme/button'
    button_two_background_down = 'atlas://data/images/defaulttheme/button'

    """
    title: string to be used as the title
    main_string: string to be used as main text
    popup_type: type of popup (enum) see PopupType class above
    popup_width: width of popup, default 300
    popup_height: height of popup, default 350
    popup_image: image to be used in popup, default None (uses popup_type's image)
    button_one_text: text to be used in button one, default "Ok"
    button_one_callback: callback to be used when button one is pressed, default None
    button_two_text: text to be used in button two, default None
    button_two_callback: callback to be used when button two is pressed, default None
    
    Usage:
    popup = PopupSystem(title_string="Title", main_string="Main text", popup_type=PopupType.INFO,
                        popup_width=300, popup_height=350)
                        
    popup.open()
    
    This will create a popup with title "Title", main text "Main text", type INFO, width 300, height 350. 
    The popup will have a singular button with text "Ok" and will close when pressed.
    
    You can also pass a callback to the button:
    popup = PopupSystem(title_string="Title", main_string="Main text", popup_type=PopupType.INFO,
                        popup_width=300, popup_height=350, button_one_callback=self.callback)
        
    This will dismiss the popup and call the callback function when the button is pressed.
    """

    ## custom spacing
    def __init__(self, main_string, popup_type, main_label_padding=(None, None), main_layout_padding=(None, None),
                 main_layout_spacing=(None, None),
                 main_label_size_delta=0, button_layout_padding=(None, None), button_layout_spacing=(None, None),
                 popup_width=300, popup_height=350, popup_image=None,
                 button_one_text="Ok", button_one_callback=None, button_one_background_color=None,
                 button_two_text=None, button_two_callback=None, button_two_background_color=None,
                 **kwargs):
        super(PopupSystem, self).__init__(**kwargs)

        if button_one_callback is None:
            button_one_callback = self.dismiss
        if button_one_background_color is not None:
            self.button_one_background_normal = ""
        if button_two_background_color is not None:
            self.button_two_background_down = ""

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
        self.button_layout_padding = button_layout_padding
        self.button_layout_spacing = button_layout_spacing
        self.main_layout_spacing = main_layout_spacing
        self.popup_type = popup_type
        self.popup_image = popup_image
        self.button_one_text = self.l.get_str(button_one_text)
        self.button_one_callback = button_one_callback
        self.button_two_text = self.l.get_str(button_two_text) if button_two_text is not None else None
        self.button_two_callback = button_two_callback

        self.build()

    def build(self):
        image = Image(source=self.popup_type.value or self.popup_image)
        main_label = Label(size_hint_y=1,
                           text_size=(dp(utils.get_scaled_width(
                               self.popup_width - utils.get_scaled_width(self.main_label_size_delta))), None),
                           halign="center", valign="middle", text=self.main_string, color=(0, 0, 0, 1),
                           padding=(utils.get_scaled_width(self.main_label_padding[0]),
                                    utils.get_scaled_height(self.main_label_padding[1])),
                           markup=True, font_size=str(utils.get_scaled_width(14)) + "sp")

        button_layout = self.build_button_layout()

        main_layout = BoxLayout(orientation="vertical",
                                spacing=(utils.get_scaled_width(self.main_layout_spacing[0]),
                                         utils.get_scaled_height(self.main_layout_spacing[1])),
                                padding=(utils.get_scaled_width(self.main_layout_padding[0]),
                                         utils.get_scaled_height(self.main_layout_padding[1])))

        main_layout.add_widget(image)
        main_layout.add_widget(main_label)
        main_layout.add_widget(button_layout)

        self.content = main_layout

    def build_button_layout(self):
        button_layout = BoxLayout(orientation="horizontal",
                                  spacing=(utils.get_scaled_width(self.button_layout_spacing[0]),
                                           utils.get_scaled_height(self.button_layout_spacing[1])),
                                  padding=(utils.get_scaled_width(self.button_layout_padding[0]),
                                           utils.get_scaled_height(self.button_layout_padding[1])))

        for button in self.build_buttons():
            button_layout.add_widget(button)
        return button_layout

    def on_button_pressed(self, callback):
        self.dismiss()
        callback()

    def build_buttons(self):
        buttons = [Button(text=self.button_one_text,
                          on_release=lambda x: self.on_button_pressed(self.button_one_callback),
                          font_size=str(utils.get_scaled_width(14)) + "sp")]
        if self.button_two_text is not None:
            buttons.append(Button(text=self.button_two_text,
                                  on_release=lambda x: self.on_button_pressed(self.button_two_callback),
                                  font_size=str(utils.get_scaled_width(14)) + "sp"))
        return buttons
