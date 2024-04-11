# -*- coding: utf-8 -*-
import sys, os

from asmcnc.comms.localization import Localization
from asmcnc.comms.logging_system.logging_system import Logger
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.vkeyboard import VKeyboard
import traceback
from kivy.clock import Clock
from asmcnc.core_UI import scaling_utils
from kivy.resources import resource_find
from kivy.core.image import Image
from kivy.graphics import Color, BorderImage
from kivy.utils import rgba

try:
    import hgtk
except:
    pass


class Keyboard(VKeyboard):
    font_color = [0, 0, 0, 1]

    def __init__(self, **kwargs):
        super(Keyboard, self).__init__(**kwargs)

        self.l = Localization()

        # For python 2 encoding issues
        reload(sys)
        sys.setdefaultencoding('utf-8')

        self.bind(layout=self.set_keyboard_background)
        self.bind(do_translation=self.set_keyboard_background)

        self.text_instance = None
        self.custom_numeric_pos = None
        self.custom_qwerty_pos = None

        dirname = os.path.dirname(__file__)

        self.kr_layout = os.path.join(dirname, "layouts", "kr.json")
        self.numeric_layout = os.path.join(dirname, "layouts", "numeric.json")
        self.qwerty_layout = "data/keyboards/qwerty.json"
        self.qwertyKR_layout = os.path.join(dirname, "layouts", "qwertyKR.json")
        self.font_size = scaling_utils.get_scaled_width(20)

        self.background_color = [0, 0, 0, 1]

        try:
            if self.l.lang == self.l.ko:
                self.font = self.l.korean_font
                self.layout = self.kr_layout
            else:
                self.font_name = "data/fonts/DejaVuSans.ttf"
                self.layout = self.qwerty_layout
        except:
            pass

        self.previous_layout = self.layout

        self.do_translation = True
        self.width = scaling_utils.Width
        self.height = int(scaling_utils.Height / 2.1)
        self.default_pos = (scaling_utils.Width - self.width, 0)
        self.pos = self.default_pos
        self.on_key_up = self.key_up

    def generic_for_loop_alternative(self, func, list_of_items, i=0, end_func=0):

        '''
        This alternative to using for loops prevents the UI from locking up while the "loop" continues in the background.

        This is a wrapper function to make the "func" argument get called recursively, scheduled before the next frame. 
        If the same callback is called more than 10 times before the next frame, kivy will issue a warning but won't freeze :).
        This means it will scale even if there's a long list of things to get through. 

        func: function that you would call from within the loop; if this returns true the "loop" will break
        list_of_items and i: imagine you were using 'for x in list_of_items:', list_of_items[i] is x
        end_func: the function that would be called when the loop ended

        e.g.
            for x in list_of_items:
                if func(x): return 

            if end_func: end_func()

        '''

        try: 
            # if the given function returns True, exit the "loop" :)
            if func(list_of_items[i]): return

            # passing "-1" as the time argument schedules the call before the next frame if possible
            Clock.schedule_once(lambda dt: self.generic_for_loop_alternative(func, list_of_items, i+1, end_func), -1)

        except IndexError as e:
            # When we get to the end of the list of things, call a final function if it exists
            if end_func:
                end_func()

    # Set up text input fields to raise the custom keyboard
    def setup_text_inputs(self, text_inputs):
        self.generic_for_loop_alternative(self.setup_single_text_input, text_inputs)

    def setup_single_text_input(self, text_input):
        text_input.keyboard_mode = 'managed'
        text_input.bind(focus=self.on_focus_raise_keyboard)

    # Function overrides the original VKeyboard class
    def draw_keys(self):
        layout = self.available_layouts[self.layout]
        layout_rows = layout['rows']
        layout_geometry = self.layout_geometry
        layout_mode = self.layout_mode

        # draw background
        background = resource_find(self.background_disabled
                                   if self.disabled else
                                   self.background)
        texture = Image(background, mipmap=True).texture
        self.background_key_layer.clear()
        with self.background_key_layer:
            # Color(*self.background_color)
            BorderImage(texture=texture, size=self.size,
                        border=self.background_border)

        # XXX separate drawing the keys and the fonts to avoid
        # XXX reloading the texture each time

        # first draw keys without the font
        key_normal = resource_find(self.key_background_disabled_normal
                                   if self.disabled else
                                   self.key_background_normal)
        texture = Image(key_normal, mipmap=True).texture
        with self.background_key_layer:
            Color(1, 1, 1, 0.5)
            for line_nb in range(1, layout_rows + 1):
                for pos, size in layout_geometry['LINE_%d' % line_nb]:
                    BorderImage(texture=texture, pos=pos, size=size,
                                border=self.key_border)

        # then draw the text
        for line_nb in range(1, layout_rows + 1):
            key_nb = 0
            for pos, size in layout_geometry['LINE_%d' % line_nb]:
                # retrieve the relative text
                text = layout[layout_mode + '_' + str(line_nb)][key_nb][0]
                z = Label(text=text, font_size=self.font_size, pos=pos,
                          size=size, font_name=self.font_name, color=self.font_color)
                self.add_widget(z)
                if z.text == "✓":
                    z.color = rgba("#4CAF50")
                    z.font_size += scaling_utils.get_scaled_width(10)
                key_nb += 1

    # Function overrides the original VKeyboard class
    def refresh_active_keys_layer(self):
        self.active_keys_layer.clear()

        active_keys = self.active_keys
        layout_geometry = self.layout_geometry
        background = resource_find(self.key_background_down)
        texture = Image(background, mipmap=True).texture

        with self.active_keys_layer:
            Color(1, 1, 1)
            for line_nb, index in active_keys.values():
                pos, size = layout_geometry['LINE_%d' % line_nb][index]
                BorderImage(texture=texture, pos=pos, size=size,
                            border=self.key_border)

    # This function dictates what happens when a user presses a keyboard key
    def key_up(self, keycode, internal, modifiers):
        try:
            if "kr" in self.layout.lower():
                if keycode == "spacebar":
                    if hgtk.text.compose(self.text_instance.text + "ᴥ") != self.text_instance.text:
                        self.text_instance.text = hgtk.text.compose(self.text_instance.text + "ᴥ")
                        return
        except:
            pass

        if self.text_instance:
            if internal == None:
                if keycode == "enter":
                    if not self.text_instance.multiline:
                        self.text_instance.dispatch("on_text_validate")
                        if self.text_instance.text_validate_unfocus:
                            self.defocus_text_input(self.text_instance)
                    else:
                        self.text_instance.insert_text(u'\n')
                if keycode == "Han/Yeong":
                    # https://en.wikipedia.org/wiki/Language_input_keys#Keys_for_Korean_Keyboards
                    self.layout = self.qwertyKR_layout if self.layout == self.kr_layout else self.kr_layout
                    self.previous_layout = self.layout
                if keycode == "escape":
                    self.defocus_text_input(self.text_instance)
                if keycode == "backspace":
                    if self.text_instance.selection_text:
                        self.text_instance.delete_selection()
                    else:
                        self.text_instance.do_backspace()

                if keycode == "layout":
                    self.layout = self.numeric_layout if self.layout == self.previous_layout else self.previous_layout
                return
            if self.text_instance.selection_text:
                self.text_instance.delete_selection()
            self.text_instance.insert_text(internal)

    def set_keyboard_background(self, *args):
        if self.do_translation == (True, True) and sys.platform != 'darwin':
            self.margin_hint = [.15, .05, .06, .05]  # Set the margin between the keyboard background and the keys
            if self.layout == self.numeric_layout:
                self.background = "./asmcnc/keyboard/images/numeric_background_" + str(Window.width) + ".png"
            else:
                self.background = "./asmcnc/keyboard/images/background_" + str(Window.width) + ".png"
        else:
            self.margin_hint = [.05, .06, .05, .06]  # Default margin
            self.background = "atlas://data/images/defaulttheme/vkeyboard_background"

        self.setup_layout()

        # Make sure keyboard never goes off-screen and becomes unusable/unreachable
        if self.pos[0] + self.width > scaling_utils.Width:
            self.pos = (scaling_utils.Width - self.width, self.pos[1])
        if self.pos[1] < 0:
            self.pos = (self.pos[0], 0)
        if self.pos[0] < 0:
            self.pos = (0, self.pos[1])
        if self.pos[1] + self.height > scaling_utils.Height:
            self.pos = (self.pos[0], scaling_utils.Height - self.height)

    def setup_layout(self):
        if self.layout == self.numeric_layout:
            self.width = scaling_utils.Width / 3.5
            if self.custom_numeric_pos:
                self.pos = self.custom_numeric_pos
                if self.text_instance:
                    if self.text_instance and self.collide_widget(self.text_instance):
                        self.pos = (scaling_utils.Width - self.custom_numeric_pos[0] - self.width, self.custom_numeric_pos[1])
            else:
                self.pos = self.default_pos
                if self.text_instance and self.collide_widget(self.text_instance):
                    self.pos = (scaling_utils.Width - self.default_pos[0] - self.width, self.default_pos[1])
        else:
            self.width = scaling_utils.Width
            if self.custom_qwerty_pos:
                self.pos = self.custom_qwerty_pos
                if self.text_instance and self.collide_widget(self.text_instance):
                    self.pos = (self.custom_qwerty_pos[0], scaling_utils.Height - self.custom_qwerty_pos[1] - self.height)
            else:
                self.pos = self.default_pos
                if self.text_instance and self.collide_widget(self.text_instance):
                    self.pos = (self.default_pos[0], scaling_utils.Height - self.default_pos[1] - self.height)

    # Set custom positions for the keyboard
    def set_numeric_pos(self, pos):
        self.custom_numeric_pos = pos

    def set_qwerty_pos(self, pos):
        self.custom_qwerty_pos = pos

    # On focus behaviour is bound to all text inputs
    def on_focus_raise_keyboard(self,instance,value):
        if value:
            if self.text_instance and self.text_instance.focus:
                self.defocus_text_input(self.text_instance)
            # input_filter can be either None, ‘int’ (string), or ‘float’ (string), or a callable.
            if instance.input_filter:
                self.layout = self.numeric_layout
            else:
                self.layout = self.previous_layout
            instance.focus = True
            self.text_instance = instance
            self.setup_layout()
            self.raise_keyboard_if_none_exists()
        else:
            self.defocus_text_input(instance)
            self.lower_keyboard_if_not_focused()

    # Functions to raise keyboard
    def raise_keyboard_if_none_exists(self):
        self.generic_for_loop_alternative(self.return_if_keyboard_exists, Window.children, i=0, end_func=self.add_keyboard_instance)

    def return_if_keyboard_exists(self, child):
        if isinstance(child, Keyboard):
            return True

    def add_keyboard_instance(self):
        try: 
            Window.add_widget(self)
        except:
            Logger.info(traceback.format_exc())

    # Functions to lower keyboard
    def lower_keyboard_if_not_focused(self):
        self.generic_for_loop_alternative(self.remove_children, Window.children)

    def remove_children(self, child):
        if isinstance(child, Keyboard):
            Window.remove_widget(child)

    def defocus_all_text_inputs(self, text_inputs):
        self.generic_for_loop_alternative(self.defocus_text_input, text_inputs)

    def defocus_text_input(self, text_input):
        text_input.focus = False
        if self.text_instance == text_input:
            self.text_instance = None
