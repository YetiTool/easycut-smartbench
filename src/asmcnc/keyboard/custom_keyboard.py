# -*- coding: utf-8 -*-
import sys
from kivy.core.window import Window
from kivy.uix.vkeyboard import VKeyboard

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

    def setup_text_inputs(self, text_inputs):
        for text_input in text_inputs:
            try:
                text_input.keyboard_mode = 'managed'
                text_input.bind(focus=self.on_focus)
            except:
                print("setup failed")

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

    def on_focus(self,instance,value):
        if value:
            try:
                instance.get_focus_previous().focus = False
            except:
                pass
            instance.focus = True
            self.text_instance = instance
            try:
                for child in Window.children:
                    if isinstance(child,Keyboard):
                        print("Keyboard instance")
                        return
                else:
                    Window.add_widget(self)

            except:
                pass
        else:
            try:
                for child in Window.children:
                    if isinstance(child, Keyboard):
                        Window.remove_widget(child)
            except:
                pass