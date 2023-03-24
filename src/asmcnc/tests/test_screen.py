from kivy.uix.screenmanager import Screen
from kivy.lang import Builder

Builder.load_string("""
<TestScreen>:
    main_label: main_label
    close_button: close_button

    Label:
        id: main_label
        text: 'Test Screen'
        
    Button:
        id: close_button
        text: 'Close'
        on_press: root.sm.current = root.return_screen

""")


class TestScreen(Screen):
    return_screen = ''

    def __init__(self, **kwargs):
        super(TestScreen, self).__init__(**kwargs)
        self.sm = kwargs['sm']

    def set_text(self, text):
        self.main_label.text = text

    def set_return(self, return_screen):
        self.return_screen = return_screen


