# -*- coding: utf-8 -*-
import sys
from kivy.core.window import Window
from kivy.uix.vkeyboard import VKeyboard
import traceback
from kivy.clock import Clock

try:
    import hgtk
except:
    pass


class Keyboard(VKeyboard):
    def __init__(self, text_inputs, **kwargs):
        super(Keyboard, self).__init__(**kwargs)

        self.l = kwargs['localization']

        # For python 2 encoding issues
        reload(sys)
        sys.setdefaultencoding('utf-8')

        self.text_instance = None

        self.kr_layout = "./asmcnc/keyboard/layouts/kr.json"
        self.numeric_layout = "./asmcnc/keyboard/layouts/numeric.json"
        self.qwerty_layout = "data/keyboards/qwerty.json"
        self.qwertyKR_layout = "./asmcnc/keyboard/layouts/qwertyKR.json"

        try:
            if self.l.lang == "Korean (KO)":
                self.font = self.l.korean_font
                self.layout = self.kr_layout
            else:
                self.font_name = "data/fonts/DejaVuSans.ttf"
                self.layout = self.qwerty_layout
        except:
            pass

        self.do_translation = False
        self.width = Window.width
        self.height = int(Window.height / 2.1)
        self.pos = (Window.width - self.width, 0)
        self.on_key_up = self.key_up

        self.setup_text_inputs(text_inputs)


    # This is a wrapper function to make the "func" argument get called recursively, scheduled before the next frame. 
    # If the same callback is called more than 10 times before the next frame, kivy will issue a warning but won't freeze :). 
    def generic_for_loop_alternative(self, func, list_of_items, i=0, end_func=0):
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
                        self.text_instance.focus = False
                        self.text_instance.dispatch("on_text_validate")
                    else:
                        self.text_instance.text = self.text_instance.text + "\n"
                if keycode == "Han/Yeong":
                    #https://en.wikipedia.org/wiki/Language_input_keys#Keys_for_Korean_Keyboards
                    self.layout = self.qwertyKR_layout if self.layout == self.kr_layout else self.kr_layout
                if keycode == "escape":
                    self.text_instance.focus = False
                if keycode == "backspace":
                    self.text_instance.text = self.text_instance.text[:-1]
                return

            self.text_instance.text = self.text_instance.text + internal

    # On focus behaviour is bound to all text inputs
    def on_focus_raise_keyboard(self,instance,value):
        if value:
            try:
                instance.get_focus_previous().focus = False
            except:
                pass
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
