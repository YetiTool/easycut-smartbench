"""
@author: Archie

Popup system for easycut-smartbench
"""
from enum import Enum
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.properties import ObjectProperty, StringProperty, partial
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.popup import Popup

from asmcnc.skavaUI import utils


class PopupType(Enum):
    INFO = "./asmcnc/apps/shapeCutter_app/img/info_icon.png"
    ERROR = "./asmcnc/apps/shapeCutter_app/img/error_icon.png"
    OTHER = ""


class PopupSystem(Popup):
    # Fetched by kivy from the kwargs
    sm = ObjectProperty(None)
    m = ObjectProperty(None)
    l = ObjectProperty(None)

    # Default properties
    separator_color = [230 / 255., 74 / 255., 25 / 255., 1.]
    separator_height = 4

    # You can override these properties in the constructor, pass them as kwargs
    background = StringProperty('./asmcnc/apps/shapeCutter_app/img/popup_background.png')
    auto_dismiss = ObjectProperty(False)
    title_color = ObjectProperty([0, 0, 0, 1])
    title_size = ObjectProperty(str(utils.get_scaled_width(20)) + "sp")

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

    def __init__(self, main_string, popup_type,
                 popup_width=300, popup_height=350, popup_image=None,
                 button_one_text="Ok", button_one_callback=None,
                 button_two_text=None, button_two_callback=None,
                 **kwargs):
        super(PopupSystem, self).__init__(**kwargs)

        if button_one_callback is None:
            button_one_callback = self.dismiss

        self.title = self.l.get_str(kwargs["title"])
        self.size_hint = (None, None)
        self.width = dp(float(popup_width)/800.0)*Window.width
        self.height = dp(float(popup_height)/480.0)*Window.height

        self.main_string = self.l.get_str(main_string)
        self.popup_type = popup_type
        self.popup_image = popup_image
        self.button_one_text = self.l.get_str(button_one_text)
        self.button_one_callback = button_one_callback
        self.button_two_text = self.l.get_str(button_two_text) if button_two_text is not None else None
        self.button_two_callback = button_two_callback

        self.build()

    def build(self):
        image = Image(source=self.popup_type.value or self.popup_image)
        main_label = Label(size_hint_y=1, text_size=(utils.get_scaled_width(360), None), halign="center",
                           valign="middle", text=self.main_string, color=(0, 0, 0, 1), padding=(40, 20), markup=True,
                           font_size=str(utils.get_scaled_width(14)) + "sp")

        button_layout = self.build_button_layout()

        main_layout = BoxLayout(orientation="vertical", spacing=10, padding=(40, 20))

        main_layout.add_widget(image)
        main_layout.add_widget(main_label)
        main_layout.add_widget(button_layout)

        self.content = main_layout

    def build_button_layout(self):
        button_layout = BoxLayout(orientation="horizontal", spacing=10, padding=0)
        for button in self.build_buttons():
            button_layout.add_widget(button)
        return button_layout

    def dismiss(self, callback, *largs, **kwargs):
        super(PopupSystem, self).dismiss(*largs, **kwargs)
        callback()

    def build_buttons(self):
        buttons = [Button(text=self.button_one_text, callback=partial(self.dismiss, self.button_one_callback),
                          font_size=str(utils.get_scaled_width(14)) + "sp")]
        if self.button_two_text is not None:
            buttons.append(Button(text=self.button_two_text, callback=partial(self.dismiss, self.button_two_callback),
                                  font_size=str(utils.get_scaled_width(14)) + "sp"))
        return buttons
