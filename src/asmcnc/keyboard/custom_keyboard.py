# -*- coding: utf-8 -*-
import sys
from kivy.core.window import Window
from kivy.uix.vkeyboard import VKeyboard
import traceback
from kivy.clock import Clock
from asmcnc.core_UI import scaling_utils

try:
    import hgtk
except:
    pass


class Keyboard(VKeyboard):
    def __init__(self, **kwargs):
        super(Keyboard, self).__init__(**kwargs)

        self.l = kwargs['localization']

        # For python 2 encoding issues
        reload(sys)
        sys.setdefaultencoding('utf-8')

        self.bind(layout=self.set_keyboard_background)
        self.bind(do_translation=self.set_keyboard_background)

        self.text_instance = None

        self.kr_layout = "./asmcnc/keyboard/layouts/kr.json"
        self.numeric_layout = "./asmcnc/keyboard/layouts/numeric.json"
        self.qwerty_layout = "data/keyboards/qwerty.json"
        self.qwertyKR_layout = "./asmcnc/keyboard/layouts/qwertyKR.json"
        self.font_size = scaling_utils.get_scaled_width(20)

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
        self.width = Window.width
        self.height = int(Window.height / 2.1)
        self.pos = (Window.width - self.width, 0)
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
                            self.text_instance.focus = False
                    else:
                        self.text_instance.insert_text(u'\n')
                if keycode == "Han/Yeong":
                    #https://en.wikipedia.org/wiki/Language_input_keys#Keys_for_Korean_Keyboards
                    self.layout = self.qwertyKR_layout if self.layout == self.kr_layout else self.kr_layout
                    self.previous_layout = self.layout
                if keycode == "escape":
                    self.text_instance.focus = False
                if keycode == "backspace":
                    self.text_instance.do_backspace()

                if keycode == "layout":
                    self.layout = self.numeric_layout if self.layout == self.previous_layout else self.previous_layout
                return
            self.text_instance.insert_text(internal)

    def set_keyboard_background(self, *args):
        if self.do_translation == (True,True) and sys.platform != 'darwin':
            self.margin_hint = [.15, .05, .06, .05]  # Set the margin between the keyboard background and the keys
            if self.layout == self.numeric_layout:
                self.background = "./asmcnc/keyboard/images/numeric_background_" + str(Window.width) + ".png"
            else:
                self.background = "./asmcnc/keyboard/images/background_" + str(Window.width) + ".png"
        else:
            self.margin_hint = [.05, .06, .05, .06]  # Default margin
            self.background = "atlas://data/images/defaulttheme/vkeyboard_background"

        if self.layout == self.numeric_layout:
            self.width = Window.width / 3
        else:
            self.width = Window.width

        # Make sure keyboard never goes off-screen and becomes unusable/unreachable
        if self.pos[0] + self.width > Window.width:
            self.pos = (Window.width - self.width, self.pos[1])
        if self.pos[1] < 0:
            self.pos = (self.pos[0], 0)
        if self.pos[0] < 0:
            self.pos = (0, self.pos[1])
        if self.pos[1] + self.height > Window.height:
            self.pos = (self.pos[0], Window.height - self.height)

    # On focus behaviour is bound to all text inputs
    def on_focus_raise_keyboard(self,instance,value):
        if value:
            try:
                instance.get_focus_previous().focus = False
            except:
                pass
            # input_filter can be either None, ‘int’ (string), or ‘float’ (string), or a callable.
            if instance.input_filter:
                self.layout = self.numeric_layout
            else:
                self.layout = self.previous_layout
            instance.focus = True
            self.text_instance = instance
            self.raise_keyboard_if_none_exists()
        else:
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
            print(traceback.format_exc())

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


